import os
import json
import asyncio
import streamlit as st
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
ELASTIC_MCP_URL = os.getenv("ELASTIC_MCP_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


ai_client = genai.Client(api_key=GEMINI_API_KEY)


#  DATA DESERIALIZATION HELPER
def parse_esql_response(raw_mcp_text: str) -> list[dict]:
    """
    Parses the raw JSON string returned by the ESQL engine, matching the
    ordered columns array with the matrix rows inside values.
    """
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


#  BACKEND MCP ASYNC CORE CALLS
async def execute_fetch_stadium_map(seat_guid: str) -> str:
    """
    Queries the stadium-layout index using the native ESQL engine 
    to retrieve absolute vector coordinates.
    """
    server_params = StdioServerParameters(
        command="npx",
        args=["mcp-remote", ELASTIC_MCP_URL, "--header", f"Authorization:ApiKey {ELASTIC_API_KEY}"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 💡 CRITICAL FIX: We must update our dictionary key to match the exact schema expected by the backend!
            args = {"seat_guid": seat_guid.strip()}
            
            result = await session.call_tool("fetch_stadium_map", arguments=args)
            return result.content[0].text if result.content else "{}"

# GEMINI AGENT REGISTRATION WRAPPER 


async def execute_get_pending_orders(vendor_id: str) -> str:
    """Queries the incoming-orders index for completed transactions using explicit row/seat column splits."""
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



def fetch_stadium_map(seat_guid: str) -> str:
    """
    Fetch the precise location properties and absolute x/y map vector coordinates for a given seat_guid string.
    
    Args:
        seat_guid: The exact unique seat identifier, formatted without spaces (e.g., 'Groundfloor-A-8')
    """
    return asyncio.run(execute_fetch_stadium_map(seat_guid))
def get_pending_orders(vendor_id: str) -> str:
    """Retrieve up to 6 completed customer orders containing section, row_number, seat_number, and items for a vendor ID."""
    return asyncio.run(execute_get_pending_orders(vendor_id))

AGENT_TOOLS_MAPPING = {
    "fetch_stadium_map": fetch_stadium_map,
    "get_pending_orders": get_pending_orders,
}


# STREAMLIT UI CONFIGURATION 
st.set_page_config(page_title="BiteRush Operational Agent", page_icon="🤖", layout="wide")
st.title("🤖 BiteRush Operational Agent")
st.caption("Focused Fulfillment & Layout Inspection Engine")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "latest_parsed_orders" not in st.session_state:
    st.session_state.latest_parsed_orders = []
if "latest_map_data" not in st.session_state:
    st.session_state.latest_map_data = {}

# Main Split Layout Container
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("💬 Operational Commands")
    for msg in st.session_state.chat_history:
        if msg.role in ["user", "model"] and msg.parts and msg.parts[0].text:
            with st.chat_message("user" if msg.role == "user" else "assistant"):
                st.markdown(msg.parts[0].text)

with col_right:
    st.subheader("📊 Cluster Metrics Dashboard")
    
    # Block A: If get_pending_orders was triggered, show the tabular data
    if st.session_state.latest_parsed_orders:
        st.success(f"📋 Found {len(st.session_state.latest_parsed_orders)} Active Orders")
        st.dataframe(st.session_state.latest_parsed_orders, use_container_width=True)
        
        with st.expander("Structured Keyword Layout View", expanded=True):
            for order in st.session_state.latest_parsed_orders:
                st.markdown(
                    f"🔹 **ID:** `{order.get('order_id')}` | "
                    f"**Item:** `{order.get('item_ordered')}` | "
                    f"**Type:** `{order.get('food_type')}` | "
                    f"**Prep Time:** `{order.get('prep_time_sec')}s` | "
                    f"**Floor:** `{order.get('floor_level')}` | "
                    f"**Row:** `{order.get('row_number')}` | "
                    f"**Seat:** `{order.get('seat_number')}`"
                )
                
    # Block B: If fetch_stadium_map was triggered, show map location variables
    if st.session_state.latest_map_data:
        st.info("🏟️ Map Layout Coordinates Extracted")
        st.json(st.session_state.latest_map_data)


# AGENT SYSTEM CONTEXT BOUNDARIES 
SYSTEM_INSTRUCTION = """You are BiteRush Copilot, an analytical stadium operations agent.
You interact directly with Elasticsearch indices containing granular customer layouts and transaction queues.

CRITICAL PROTOCOLS:
1. PENDING ORDERS LOOKUP: When the user asks to look up pending, active, or completed orders for a vendor, extract the vendor ID string (e.g., 'V010') and call 'get_pending_orders'.
2. SEAT LAYOUT LOOKUP: When the user enters or asks for a specific seat locator signature (e.g., 'groundfloor-a-2', 'FirstFloor-D-12'), format it exactly with hyphens, strip out spaces, and invoke 'fetch_stadium_map'.

When rendering text responses, always highlight database fields using explicit code syntax formatting so keywords remain clear.
"""


#  AUTONOMOUS INTERACTION LOOP 
if user_input := st.chat_input("Look up pending orders for V010 or locate seat Groundfloor-A-4"):
    
  
    st.session_state.latest_parsed_orders = []
    st.session_state.latest_map_data = {}
    
    new_user_message = types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
    st.session_state.chat_history.append(new_user_message)
    
    with col_left:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Processing index queries..."):
                
                active_turn_loop = True
                max_iterations = 4
                iteration = 0
                
                while active_turn_loop and iteration < max_iterations:
                    iteration += 1
                    
                    response = ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=st.session_state.chat_history,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.1,
                            tools=[get_pending_orders, fetch_stadium_map]
                        )
                    )
                    
                    if response.function_calls:
                        for function_call in response.function_calls:
                            tool_name = function_call.name
                            tool_args = function_call.args
                            
                            st.info(f"⚡ *Tool Action:* `{tool_name}` arguments: `{dict(tool_args)}`")
                            
                            if tool_name in AGENT_TOOLS_MAPPING:
                            
                                raw_json_string = AGENT_TOOLS_MAPPING[tool_name](**tool_args)
                                
                             
                                if tool_name == "get_pending_orders":
                                    st.session_state.latest_parsed_orders = parse_esql_response(raw_json_string)
                                elif tool_name == "fetch_stadium_map":
                                    try:
                                   
                                        st.session_state.latest_map_data = json.loads(raw_json_string)
                                    except:
                                        st.session_state.latest_map_data = {"raw_output": raw_json_string}
                                
                      
                                st.session_state.chat_history.append(response.candidates[0].content)
                                tool_response_content = types.Content(
                                    role="tool",
                                    parts=[
                                        types.Part.from_function_response(
                                            name=tool_name,
                                            response={"result": raw_json_string}
                                        )
                                    ]
                                )
                                st.session_state.chat_history.append(tool_response_content)
                            else:
                                active_turn_loop = False
                    
                    elif response.text:
                        st.markdown(response.text)
                        st.session_state.chat_history.append(response.candidates[0].content)
                        active_turn_loop = False
                        
                st.rerun()