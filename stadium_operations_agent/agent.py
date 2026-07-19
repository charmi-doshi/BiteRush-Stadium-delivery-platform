import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
ELASTIC_MCP_URL = os.getenv("ELASTIC_MCP_URL")

print(ELASTIC_API_KEY, ELASTIC_MCP_URL)

"""
Copyright (c) 2026 [Charmi Doshi]
All Rights Reserved. This code is shared publicly for portfolio 
purposes only. Unauthorized copying or reuse is prohibited.
"""

import re
import json
from datetime import datetime

def parse_agent_batches_to_es(agent_output: str, vendor_id: str = "V010") -> dict:
    """
    Parses strict-formatted text from BiteRush Copilot into an Elasticsearch 'hits' JSON array.
    """
    batch_pattern = re.compile(r'---BATCH_START---\n(.*?)\n---BATCH_END---', re.DOTALL)
    raw_batches = batch_pattern.findall(agent_output)
    
    hits = []
    
    for i, batch_text in enumerate(raw_batches, start=1):

        def extract_list(field_name):
            match = re.search(fr"{field_name}:\s*\[?(.*?)\]?$", batch_text, re.MULTILINE)
            if match and match.group(1).strip():
                return [item.strip() for item in match.group(1).split(',')]
            return []
            
        def extract_string(field_name):
            match = re.search(fr"{field_name}:\s*(.*)", batch_text)
            return match.group(1).strip() if match else ""
            
        cluster_id = f"CLU-{str(i).zfill(3)}"
        
        order_ids = extract_list("Orders")
        items = extract_list("Food")
        route_steps = extract_string("Route")
        
        max_wait_str = extract_string("Max_Wait")
        eta_match = re.search(r'\d+', max_wait_str)
        total_eta_min = int(eta_match.group()) if eta_match else 0
        
        hit_doc = {
            "_index": "logistics-clusters",
            "_id": cluster_id,
            "_score": 1,
            "_source": {
                "cluster_id": cluster_id,
                "order_ids": order_ids,
                "items": items,
                "vendor_id": vendor_id,
                "route_steps": route_steps,
                "total_eta_min": total_eta_min,
                "status": "PENDING",
                "created_at": datetime.utcnow().isoformat()
            }
        }
        hits.append(hit_doc)
        
    return {"hits": hits}
async def post_cluster_to_es(batch_string: str) -> str:
    """Parses the final formatted batch string and prepares it for Elasticsearch indexing.

    Args:
        batch_string (str): The strict-formatted batch text output starting with ---BATCH_START---.

    Returns:
        str: A confirmation message indicating success or failure.
    """
    try:
  
        es_payload = parse_agent_batches_to_es(batch_string, vendor_id="V010")
        
        hit_count = len(es_payload.get("hits", []))
        return f"SUCCESS: Parsed and staged {hit_count} clusters for Elasticsearch."
        
    except Exception as e:
        return f"ERROR: Failed to parse batches. Check your string formatting. Details: {str(e)}"
    
#parser
def parse_esql_response(raw_mcp_text: str) -> list[dict]:
    """Parses raw ESQL JSON matrix formats back into explicit Python dict arrays."""
    try:
        data = json.loads(raw_mcp_text)
        for result in data.get("results", []):
            if result.get("type") == "esql_results":
                esql_data = result["data"]
                columns = [col["name"] for col in esql_data["columns"]]
                return [dict(zip(columns, row)) for row in esql_data["values"]]
    except Exception as e:
        print(f"[PARSER ERROR] Failed to deserialize ESQL layout matrix: {e}")
    return []


# BACKEND CONNECTION 
async def execute_fetch_stadium_map(seat_identifier: str) -> str:
    server_params = StdioServerParameters(
        command="npx",
        args=["mcp-remote", ELASTIC_MCP_URL, "--header", f"Authorization:ApiKey {ELASTIC_API_KEY}"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            args = {"seat": seat_identifier.strip()} 
            result = await session.call_tool("fetch_stadium_map", arguments=args)
            return result.content[0].text if result.content else "{}"

async def execute_get_pending_orders(vendor_id: str) -> str:
    server_params = StdioServerParameters(
        command="npx",
        args=["mcp-remote", ELASTIC_MCP_URL, "--header", f"Authorization:ApiKey {ELASTIC_API_KEY}"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            args = {"vendor_id": vendor_id.strip()}
            result = await session.call_tool("get_pending_orders", arguments=args)
            return result.content[0].text if result.content else "[]"


# TOOLS FOR ADK AGENT
async def fetch_stadium_map(seat: str) -> dict:
    """Fetch the precise location properties and absolute x/y map vector coordinates for a given seat locator.

    Args:
        seat (str): The unique seat identifier string, formatted precisely without spaces (e.g., 'Groundfloor-A-8').

    Returns:
        dict: The parsed spatial coordinates and layout details from the database.
    """
    raw_json = await execute_fetch_stadium_map(seat)
    try:
        return json.loads(raw_json)
    except Exception:
        return {"raw_data": raw_json}

async def get_pending_orders(vendor_id: str) -> list[dict]:
    """Retrieve up to 6 completed customer orders containing section, row_number, seat_number, and items for a vendor ID.

    Args:
        vendor_id (str): The unique string token identification for the kitchen vendor (e.g., 'V010').

    Returns:
        list[dict]: A structured collection of open order queue items.
    """
    raw_json = await execute_get_pending_orders(vendor_id)
    return parse_esql_response(raw_json)


#  LOGISTICS CLUSTERING INSTRUCTIONS
root_agent = Agent(
    name="stadium_operations_agent",
    model="gemini-flash-latest",
    description="Agent to handle stadium order routing audits and seat coordinate lookups with batch optimization algorithms.",
    instruction=(
        "You are BiteRush Copilot, an expert stadium fulfillment coordination engine. "
        "Your core responsibility is sorting and packing raw pending order for vendorid = V010 into optimized, logical runner delivery batches.\n\n"
        
        "── BATCHING & LOGISTICS PROTOCOLS ──\n"
        "When an operator pulls pending orders, you must analyze the list and display them grouped into discrete 'Delivery Batches' according to these strict operational constraints:\n\n"
        
        "1. CAPACITY CONSTRAINT:\n"
        "   - Maximum of 6 orders per delivery runner batch. Never exceed this limit.\n\n"
        
        "2. SPATIAL GEOMETRY COHESION (PRIORITY 1):\n"
        "   - Group orders by `floor_level` and `zone_name` first. A runner should never change floors or cross distant structural stadium configurations during a single batch run.\n"
        "   - Cluster nearby rows and seats together to minimize runner transit steps.\n\n"
        
        "3. THERMAL & PREP COMPATIBILITY (PRIORITY 2):\n"
        "   - Isolate item profiles based on `food_type` properties:\n"
        "   - Align batch sequences by `prep_time_sec` so items finishing around the same time leave together, preventing hot items from sitting under heat lamps.\n\n"
        
        """MAX ETA: Any batch you create MUST have a total ETA of 10 minutes or less. If a cluster's combined route distance and prep time results in an ETA > 10 minutes, you must split that cluster or drop orders until it is 10 minutes or less."""
       
       
       "── EXECUTION PIPELINE ──\n"
        "1. CALL 'get_pending_orders' to retrieve raw queue data.\n"
        "2. CALL 'fetch_stadium_map' to verify seat coordinates (Input format: 'Floorlevel-Row-Seat').\n"
       "3. CLUSTER & CALCULATE: Perform routing from the KITCHEN_ORIGIN to each seat.\n"
        "   - Sequence seats logically to minimize walking distance.\n"
        "   - OUTPUT FORMAT for Route: 'KITCHEN, Zone, Row, Seat, Seat, Seat'.\n\n"
       
        
"── OUTPUT FORMAT (STRICT) ──\n"
        "Immediately output your results using the delimited format below. Do not use JSON. "
        "Do not include any conversational filler. Start with ---BATCH_START---.\n\n"
        
        "---BATCH_START---\n"
        "Group: [Name]\n"
        "Orders: [ID1, ID2]\n"
        "Seats: [A-1, A-2]\n"
        "Food: [Item1, Item2]\n"
        "Max_Wait: [Time]\n"
        "Route: [KITCHEN, Zone, Row, Seat1, Seat2]\n"
        "---BATCH_END---"

        
    ),
    tools=[get_pending_orders, fetch_stadium_map],
)
