# import json
# from google.adk.agents import Agent

# import os 
# GOOGLE_MODEL = "gemini-flash-latest"


# # ---------------------------------------------------------
# # 🛠️ TOOLS / DATA FETCHERS
# # ---------------------------------------------------------
# MOCK_ELASTICSEARCH_DATA = [
#     {
#         "order_id": "ORD001",
#         "vendor_id": "V010",
#         "item": "vadapav",
#         "prep_type": "fresh_cooked",
#         "prep_time": 90,
#         "section": 102,
#         "seat": "Row A, Seat 4",
#         "status": "completed"
#     },
#     {
#         "order_id": "ORD002",
#         "vendor_id": "V010",
#         "item": "indian samosa",
#         "prep_type": "fresh_cooked",
#         "prep_time": 120,
#         "section": 104,
#         "seat": "Row G, Seat 12",
#         "status": "completed"
#     },
#     {
#         "order_id": "ORD003",
#         "vendor_id": "V010",
#         "item": "coke",
#         "prep_type": "pre_packaged",
#         "prep_time": 10,
#         "section": 103,
#         "seat": "Row C, Seat 2",
#         "status": "completed"
#     },
#     {
#         "order_id": "ORD004",
#         "vendor_id": "V010",
#         "item": "beer",
#         "prep_type": "pre_packaged",
#         "prep_time": 15,
#         "section": 102,
#         "seat": "Row B, Seat 1",
#         "status": "completed"
#     },
#     {
#         "order_id": "ORD005",
#         "vendor_id": "V010",
#         "item": "vadapav",
#         "prep_type": "fresh_cooked",
#         "prep_time": 90,
#         "section": 115,
#         "seat": "Row Z, Seat 5",
#         "status": "completed"
#     }
# ]

# def fetch_active_stadium_orders() -> str:
#     """
#     Retrieves unbatched, active order records from the stadium delivery queue database.
    
#     Returns:
#         str: JSON string containing raw rows from the order database index.
#     """
#     return json.dumps(MOCK_ELASTICSEARCH_DATA)

# import math
# from grouping_agent.stadium_map import ACTIVE_STADIUM_GEOMETRY

# def get_optimized_delivery_route(orders: list):
#     """
#     Called by the Routing Agent to sequence deliveries based on real data.
#     """
#     # Start at our calibrated kitchen origin
#     origin = ACTIVE_STADIUM_GEOMETRY.get("KITCHEN_ORIGIN", {"x": 800.0, "y": 480.0})
#     current_loc = (origin["x"], origin["y"])
    
#     destinations = [str(o.get("section")) for o in orders]
    
#     # 🚨 STRICT COGNITIVE GUARD: Check for non-existent map keys before doing any math
#     invalid_seats = [d for d in destinations if d not in ACTIVE_STADIUM_GEOMETRY]
#     if invalid_seats:
#         return {
#             "error": "INVALID_STADIUM_BOUNDS",
#             "missing_locations": invalid_seats,
#             "formatted_path": "None - Location Unmapped"
#         }
#     route = []
#     total_px_dist = 0
    
#     while destinations:
#         # Find the closest next seat from current position
#         next_seat = min(
#             [d for d in destinations if d in ACTIVE_STADIUM_GEOMETRY],
#             key=lambda x: math.dist(current_loc, (ACTIVE_STADIUM_GEOMETRY[x]["x"], ACTIVE_STADIUM_GEOMETRY[x]["y"])),
#             default=None
#         )
        
#         if not next_seat: break
        
#         dest_coords = (ACTIVE_STADIUM_GEOMETRY[next_seat]["x"], ACTIVE_STADIUM_GEOMETRY[next_seat]["y"])
#         total_px_dist += math.dist(current_loc, dest_coords)
#         route.append(next_seat)
#         destinations.remove(next_seat)
#         current_loc = dest_coords

#     # CALIBRATION: 20 pixels = 1 meter (Adjust based on your map visual)
#     total_meters = round(total_px_dist / 20.0, 2)
#     # Walking speed: 1.4 meters/sec
#     est_seconds = int(total_meters / 1.4)

#     return {
#         "sequence": route,
#         "distance_meters": total_meters,
#         "eta_seconds": est_seconds,
#         "formatted_path": " -> ".join(["Kitchen"] + route)
#     }
# # ---------------------------------------------------------
# # 🤖 SPECIALIZED SUB-AGENTS
# # ---------------------------------------------------------

# # 1. Order Triage & Validation Agent
# order_triage_agent = Agent(
#     name="order_triage_agent",
#     model=GOOGLE_MODEL,
#     description="Filters out invalid, cancelled, or unpaid database entries from the live queue.",
#     instruction=(
#         "You are the Data Integrity Agent. Your ONLY task is to take raw database rows from 'fetch_active_stadium_orders', "
#         "and drop any orders whose payment/fulfillment status is not strictly 'completed'. "
#         "Format the remaining valid orders into a clean dictionary list and output it. Do not group them yourself."
#     ),
#     tools=[fetch_active_stadium_orders]
# )

# # 2. Logistics Cluster Optimization Agent
# logistics_clustering_agent = Agent(
#     name="logistics_clustering_agent",
#     model=GOOGLE_MODEL,
#     description="Groups filtered food orders into optimized delivery batches based on physical stadium locations.",
#     instruction=(
#         "You are the Logistics Cluster Specialist. Your ONLY job is to take a list of validated orders and group them. "
#         "Grouping Constraints:\n"
#         "- Group orders whose customer section numbers are close together (within 3-5 sections).\n"
#         "- Balance prep times: Ensure quick pre-packaged items don't sit waiting too long for fresh-cooked items.\n"
#         "Output the grouped batches as a beautiful JSON map displaying group names, order ids, and calculated max assembly durations."
        
#     ),
#     tools=[] 
# )


# # ---------------------------------------------------------
# # 👑 ROOT ORCHESTRATOR AGENT
# # ---------------------------------------------------------
# # 💡 FIX 1 & 2: Changed Python variable to root_agent and internal name to biterush_director
# root_agent = Agent(
#     name="biterush_director",
#     model=GOOGLE_MODEL,
#     description="Main manager for the BiteRush AI Food Delivery cluster system. Delegates data validation and clustering tasks.",
#     instruction=(
#         "You are the Master Logistics Director for BiteRush. You coordinate a team of sub-agents to optimize stadium operations.\n\n"
#         "When the user asks to process, optimize, or view delivery groups:\n"
#         "1. Delegate immediately to 'order_triage_agent' to pull the fresh data from the tool and clean the pipeline rows.\n"
#         "2. Take the output from the triage agent and hand it off to 'logistics_clustering_agent' to execute the grouping computations.\n"
#         "3. Deliver the final clustered JSON response back to the user workspace layout.\n\n"
#         "If a user just says 'hello' or asks unrelated stadium layout questions, handle it yourself directly."
#     ),
#     tools=[], 
#     sub_agents=[order_triage_agent, logistics_clustering_agent] 
# )

# # # # 💡 FIX 3: Point the exposure array hook to the verified root_agent variable name
# agents = [root_agent]

# import json
# from google.adk.agents import Agent
# import os 
# import math
# import heapq

# GOOGLE_MODEL = "gemini-flash-latest"

# # ---------------------------------------------------------
# # 🛠️ HIGH-PERFORMANCE DATA & NAVIGATION ENGINE
# # ---------------------------------------------------------
# MOCK_ELASTICSEARCH_DATA = [
#     {"order_id": "ORD001", "vendor_id": "V010", "item": "vadapav", "prep_type": "fresh_cooked", "prep_time": 90, "section": "A-1", "status": "completed"},
#     {"order_id": "ORD002", "vendor_id": "V010", "item": "indian samosa", "prep_type": "fresh_cooked", "prep_time": 120, "section": "A-5", "status": "completed"},
#     {"order_id": "ORD003", "vendor_id": "V010", "item": "coke", "prep_type": "pre_packaged", "prep_time": 10, "section": "B-2", "status": "completed"},
#     {"order_id": "ORD004", "vendor_id": "V010", "item": "beer", "prep_type": "pre_packaged", "prep_time": 15, "section": "A-2", "status": "completed"},
#     {"order_id": "ORD005", "vendor_id": "V010", "item": "vadapav", "prep_type": "fresh_cooked", "prep_time": 90, "section": "Z-99", "status": "completed"}
# ]

# def fetch_active_stadium_orders() -> str:
#     """Retrieves unbatched active order records from the live queue database."""
#     return json.dumps(MOCK_ELASTICSEARCH_DATA)

# def dijkstra_path(graph, start, end):
#     """Computes the absolute shortest legal path along the walkway graph grid."""
#     queue = [(0, start, [])]
#     seen = set()
    
#     while queue:
#         (cost, node, path) = heapq.heappop(queue)
#         if node not in seen:
#             seen.add(node)
#             path = path + [node]
#             if node == end:
#                 return cost, path

#             for next_node, weight in graph.get(node, {}).items():
#                 if next_node not in seen:
#                     heapq.heappush(queue, (cost + weight, next_node, path))
#     return float("inf"), []
# def get_optimized_delivery_route(sections: list) -> dict:
#     """
#     Uber-Style Routing with automated schema translation and real-time terminal tracers.
#     """
#     from grouping_agent.stadium_map import STADIUM_ROAD_NETWORK
    
#     print("\n🚀 [AGENT TOOL TRIGGER] Running 'get_optimized_delivery_route' tool hook...")
#     print(f"📥 [TOOL INPUT] Raw requested locations collection: {sections}")
    
#     destinations = []
#     for s in sections:
#         raw_str = str(s).strip().upper()
        
#         # SCHEMA TRANSLATOR: Turn "A-5" into "GROUNDFLOOR-A-5" to match network keys
#         if not raw_str.startswith("GROUNDFLOOR-"):
#             if len(raw_str) == 2 and raw_str[0].isalpha() and raw_str[1].isdigit():
#                 raw_str = f"{raw_str[0]}-{raw_str[1]}"
#             raw_str = f"GROUNDFLOOR-{raw_str}"
            
#         destinations.append(raw_str)

#     print(f"🔀 [TOOL TRANSLATION] Cleaned and normalized search targets: {destinations}")

#     # Direct verification validation check against the active keys
#     invalid_seats = [d for d in destinations if d not in STADIUM_ROAD_NETWORK]
#     if invalid_seats:
#         print(f"❌ [TOOL ERROR] Guardrail triggered! The following nodes are missing from the graph network: {invalid_seats}")
#         print(f"ℹ️ [CURRENT GRAPH KEYS AVAILABLE] Listed network keys: {list(STADIUM_ROAD_NETWORK.keys())[:15]}... (showing first 15)")
#         return {
#             "error": "INVALID_STADIUM_BOUNDS",
#             "missing_locations": invalid_seats,
#             "formatted_path": "None - Location Unmapped"
#         }

#     print("🛣️ [TOOL PATHFINDING] All target nodes verified on map. Launching Dijkstra path finder...")
#     current_node = "Kitchen"
#     full_turn_by_turn_path = ["Kitchen"]
#     total_pixel_distance = 0

#     for target in sorted(destinations):
#         print(f"🛸 Computing trajectory segment: {current_node} ➔ {target}")
#         cost, path_segment = dijkstra_path(STADIUM_ROAD_NETWORK, current_node, target)
        
#         if path_segment:
#             print(f"   ↳ Segment Found: {path_segment} | Distance: {cost}px")
#             full_turn_by_turn_path.extend(path_segment[1:])
#             total_pixel_distance += cost
#             current_node = target
#         else:
#             print(f"   ⚠️ [ROUTE WARNING] Dijkstra failed to link node segment {current_node} to {target}!")

#     total_meters = round(total_pixel_distance / 20.0, 2)
#     est_seconds = int(total_meters / 1.4)
#     clean_display_path = " ➔ ".join(full_turn_by_turn_path)

#     print(f"🏁 [TOOL ROUTE SUCCESS] Calculated Path: {clean_display_path}")
#     print(f"📊 Metrics Summary: Total Distance = {total_meters}m | Estimated Time = {est_seconds}s\n")

#     return {
#         "sequence": destinations,
#         "distance_meters": total_meters,
#         "eta_seconds": est_seconds,
#         "formatted_path": clean_display_path
#     }
# # def get_optimized_delivery_route(sections: list) -> dict:
# #     """
# #     Uber-Style Routing: Maps turn-by-turn routing through legal stadium corridors.
# #     Calculated completely in native Python to avoid API quota consumption.
# #     """
# #     from grouping_agent.stadium_map import STADIUM_ROAD_NETWORK
    
# #     destinations = [str(s).strip() for s in sections]

# #     # Guardrail check against the graph network keys
# #     invalid_seats = [d for d in destinations if d not in STADIUM_ROAD_NETWORK]
# #     if invalid_seats:
# #         return {
# #             "error": "INVALID_STADIUM_BOUNDS",
# #             "missing_locations": invalid_seats,
# #             "formatted_path": "None - Location Unmapped"
# #         }

# #     current_node = "Kitchen"
# #     full_turn_by_turn_path = ["Kitchen"]
# #     total_pixel_distance = 0

# #     # Sort destinations to find a sequential path along the graph
# #     for target in sorted(destinations):
# #         cost, path_segment = dijkstra_path(STADIUM_ROAD_NETWORK, current_node, target)
# #         if path_segment:
# #             full_turn_by_turn_path.extend(path_segment[1:])
# #             total_pixel_distance += cost
# #             current_node = target

# #     total_meters = round(total_pixel_distance / 20.0, 2)
# #     est_seconds = int(total_meters / 1.4)

# #     return {
# #         "sequence": destinations,
# #         "distance_meters": total_meters,
# #         "eta_seconds": est_seconds,
# #         "formatted_path": " ➔ ".join(full_turn_by_turn_path)
# #     }

# # ---------------------------------------------------------
# # 🤖 SPECIALIZED SUB-AGENTS
# # ---------------------------------------------------------

# # 1. Order Triage & Validation Agent
# order_triage_agent = Agent(
#     name="order_triage_agent",
#     model=GOOGLE_MODEL,
#     description="Filters out invalid, cancelled, or unpaid database entries from the live queue.",
#     instruction=(
#         "You are the Data Integrity Agent. Pull raw database rows from 'fetch_active_stadium_orders', "
#         "and drop any orders whose status is not strictly 'completed'. "
#         "Format the remaining valid orders into a clean dictionary list and output it."
#     ),
#     tools=[fetch_active_stadium_orders]
# )

# # 2. Logistics Cluster Optimization Agent
# logistics_clustering_agent = Agent(
#     name="logistics_clustering_agent",
#     model=GOOGLE_MODEL,
#     description="Groups filtered food orders into optimized delivery batches and triggers mathematical routing.",
#     instruction=(
#         "You are the Logistics Cluster Specialist. Your job is to take a list of validated orders and group them.\n\n"
#         "CLUSTERING RULES:\n"
#         "- Group orders whose section strings are close together or share rows (e.g., A-1, A-2, A-5 should group together).\n"
#         "- Balance prep times: Ensure quick pre-packaged items don't sit waiting too long for fresh-cooked items.\n\n"
#         " ROUTING INTEGRATION:\n"
#         "- For every batch group you create, extract their section strings and call the `get_optimized_delivery_route` tool.\n"
#         "- Embed the exact routing data results (`distance_meters`, `eta_seconds`, `formatted_path`) directly into that batch's JSON block.\n\n"
#         # "STRICT COGNITIVE GUARDRAILS (ZERO HALLUCINATION):\n"
#         # "- Never guess walking paths, metrics, or invent gates for any section.\n"
#         # "- If `get_optimized_delivery_route` returns an error or indicates 'INVALID_STADIUM_BOUNDS', you MUST flag that batch or item status as 'REJECTED - INVALID LOCATION' and explicitly state which sections were missing from the map grid data."
#     ),
#     tools=[get_optimized_delivery_route] 
# )

# # ---------------------------------------------------------
# # 👑 ROOT ORCHESTRATOR AGENT
# # ---------------------------------------------------------
# root_agent = Agent(
#     name="biterush_director",
#     model=GOOGLE_MODEL,
#     description="Main manager for the BiteRush AI Food Delivery cluster system. Delegates data validation and clustering tasks.",
#     instruction=(
#         "You are the Master Logistics Director for BiteRush. You coordinate a team of sub-agents to optimize stadium operations.\n\n"
#         "When the user asks to process, optimize, or view delivery groups:\n"
#         "1. Delegate immediately to 'order_triage_agent' to pull the fresh data from the tool and clean the pipeline rows.\n"
#         "2. Take the output from the triage agent and hand it off to 'logistics_clustering_agent' to execute the grouping and geometric calculations.\n"
#         "3. Deliver the final clustered and routed JSON response back to the user workspace layout.\n\n"
#         "If a user just says 'hello' or asks unrelated stadium layout questions, handle it yourself directly."
#     ),
#     tools=[], 
#     sub_agents=[order_triage_agent, logistics_clustering_agent] 
# )

# agents = [root_agent]



# import os
# import json
# import asyncio
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# from google.adk.agents import Agent

# GOOGLE_MODEL = "gemini-flash-latest"

# # =====================================================================
# # 🔌 MODULE 1: DYNAMIC ASYNC MCP UTILITY RUNNERS
# # =====================================================================

# def load_mcp_config():
#     """
#     Reads configuration parameters straight from your specific JSON structure.
#     """
#     # Locates your mcp.json file at your project's runtime root
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     config_path = os.path.join(base_dir, 'mcp.json')
    
#     if not os.path.exists(config_path):
#         # Fallback inline instantiation if file isn't present
#         return StdioServerParameters(
#             command="npx",
#             args=["-y", "@modelcontextprotocol/server-remote", "https://biterush-f06463.kb.us-central1.gcp.cloud.es.io/api/agent_builder/mcp"],
#             env={
#                 "KIBANA_URL": "https://biterush-f06463.kb.us-central1.gcp.cloud.es.io/api/agent_builder/mcp",
#                 "AUTH_HEADER": f"ApiKey {os.getenv('ELASTIC_API_KEY', '')}"
#             }
#         )

#     with open(config_path, 'r', encoding='utf-8') as f:
#         config = json.load(f)
    
#     server_info = config["servers"]["elastic-agent-builder"]
#     return StdioServerParameters(
#         command=server_info["command"],
#         args=server_info["args"],
#         env=server_info.get("env", {})
#     )


# async def execute_remote_mcp_call(tool_name: str, arguments: dict) -> str:
#     """
#     Spawns background subprocesses to route queries down the Elastic MCP proxy line.
#     """
#     server_params = load_mcp_config()
    
#     try:
#         async with stdio_client(server_params) as (read_stream, write_stream):
#             async with ClientSession(read_stream, write_stream) as session:
#                 # Complete protocol handshake with Elasticsearch server
#                 await session.initialize()
                
#                 # Execute tool dynamically across the network tunnel
#                 result = await session.call_tool(tool_name, arguments=arguments)
                
#                 # Extract text payload content from response stream
#                 if hasattr(result, 'content') and result.content:
#                     # Content lists usually wrap block objects
#                     if isinstance(result.content, list):
#                         return "".join([str(c.text) if hasattr(c, 'text') else str(c) for c in result.content])
#                     return str(result.content)
#                 return json.dumps({"status": "SUCCESS", "data": "No return payload received."})
                
#     except Exception as e:
#         return json.dumps({"status": "MCP_CONNECTION_FAILURE", "error": str(e)})


# # =====================================================================
# # 🛠️ MODULE 2: AGENT WRAPPERS FOR ADK COMPATIBILITY
# # =====================================================================

# def fetch_ongoing_orders() -> str:
#     """
#     Google ADK Tool: Fetches active ongoing stadium orders from the Elastic index.
#     """
#     # Bridge the sync agent framework loop with the async subprocess pipeline
#     return asyncio.run(execute_remote_mcp_call("fetch_orders", {}))


# def get_seat_zone_from_elastic(seat_guid: str) -> str:
#     """
#     Google ADK Tool: Looks up the exact zone configuration metrics for a seat GUID via Elastic.
#     """
#     arguments = {"seat_guid": str(seat_guid).strip()}
#     return asyncio.run(execute_remote_mcp_call("get_stadium_zone", arguments))


# # =====================================================================
# # 👑 MODULE 3: THE COMPLETED ELASTIC ADK AGENT ENGINE
# # =====================================================================

# elastic_logistics_agent = Agent(
#     name="elastic_mcp_manager",
#     model=GOOGLE_MODEL,
#     description="Validates and tracks active stadium data arrays directly inside Elastic indices.",
#     instruction=(
#         "You are the BiteRush Core Data Interface Agent.\n\n"
#         "Your objective is to run structural connectivity tasks:\n"
#         "1. When requested to pull current rows, run the `fetch_ongoing_orders` tool.\n"
#         "2. When asked to determine where a seat sits, execute the `get_seat_zone_from_elastic` tool.\n"
#         "3. Always display the direct data payload received from your tools back to the orchestrator layer."
#     ),
#     tools=[fetch_ongoing_orders, get_seat_zone_from_elastic],
#     sub_agents=[]
# )

# # Export hook to load into ADK's web component server seamlessly
# agents = [elastic_logistics_agent]

# import os
# from typing import List, Dict, Any
# import json

# # --- DETERMINISTIC MCP STORAGE PIPELINES ---
# def get_pending_orders() -> List[Dict[str, Any]]:
#     """MCP Tool: Fast data-layer fetch for unfulfilled stadium orders."""
#     return [
#         {"order_id": 101, "seat_guid": "Groundfloor-A-8", "items": ["tacos"], "prep_time_min": 5},
#         {"order_id": 102, "seat_guid": "Groundfloor-A-9", "items": ["burgers"], "prep_time_min": 8},
#         {"order_id": 103, "seat_guid": "FirstFloor-B-12", "items": ["tacos"], "prep_time_min": 4},
#         {"order_id": 104, "seat_guid": "Groundfloor-A-99", "items": ["fries"], "prep_time_min": 3}
#     ]

# def fetch_stadium_map_bulk() -> Dict[str, Dict[str, Any]]:
#     """MCP Tool: Pulls the entire structural coordinate layout index in one query."""
#     return {
#         "Groundfloor-A-8": {"zone_name": "Ground floor", "row_number": "A", "x": 1057.9, "y": 480.8},
#         "Groundfloor-A-9": {"zone_name": "Ground floor", "row_number": "A", "x": 1082.9, "y": 480.8},
#         "Groundfloor-A-99": {"zone_name": "Ground floor", "row_number": "A", "x": 2500.3, "y": 480.8},
#         "FirstFloor-B-12": {"zone_name": "First Floor", "row_number": "B", "x": 1100.2, "y": 200.5},
#     }

# # --- THE SINGLE-CALL ORCHESTRATOR AGENT ---
# class SingleCallLogisticsAgent:
#     def __init__(self, model_client=None):
#         self.client = model_client

#     def process_stadium_logistics(self):
#         print(" Initiating Single-Call Logistics Optimization Pipeline...")
        
#         # --- STEP 1: DETERMINISTIC SYSTEM GATHERING ---
#         # We fetch the tool records instantly BEFORE making the AI call.
#         # This injects the data straight into the prompt context, skipping extra LLM round-trips.
#         orders = get_pending_orders()
#         stadium_map = fetch_stadium_map_bulk()
        
#         # Enrich the dataset context directly in memory
#         enriched_payload = []
#         for o in orders:
#             seat_meta = stadium_map.get(o["seat_guid"], {"zone_name": "Unknown", "row_number": "Unknown", "x": 0, "y": 0})
#             enriched_payload.append({**o, **seat_meta})
            
#         # --- STEP 2: THE SINGLE AI INVOCATION ---
#         # We pass the full, compiled dataset to the LLM in one go with strict grouping rules.
#         prompt = f"""
#         You are the Stadium Delivery Logistics Routing Agent. 
#         Analyze this raw data payload of pending orders enriched with physical seat coordinates:
#         {json.dumps(enriched_payload, indent=2)}
        
#       Grouping Constraints:
# 1. Spatial Proximity: Group orders whose customer section numbers are close together (within 3-5 sections). Use the absolute x and y coordinates to verify proximity if section labels are ambiguous.
# 2. Prep Time Balancing: Balance prep times. Ensure quick pre-packaged items (short prep times) do not sit around waiting too long for fresh-cooked items (long prep times). Keep the internal delta of prep times within a batch tightly clustered.
# 3. Capacity Cap: A single delivery runner can carry a maximum of 6 items per batch. Do not exceed this threshold.

# Output Format:
# Output the grouped batches exclusively as a beautifully structured, minified JSON map displaying group names, order ids, and the calculated maximum wait time for that specific batch. Do not include markdown code blocks, conversational pleasantries, or trailing text outside of the JSON payload.
#         """
        
#         # Simulating the exact generation return of that 1 single AI Call:
#         print("\n [AI CALL INITIALIZED] -> Processing constraints and calculating spatial batches...")
#         simulated_llm_response = self._mock_llm_call(enriched_payload)
        
#         # --- STEP 3: DISPLAY THE FINAL RESULT ---
#         print(simulated_llm_response)

#     def _mock_llm_call(self, payload: List[Dict[str, Any]]) -> str:
#         """Simulates the raw text output from your LLM model client."""
#         return """
# ============================================================
#  DISPATCH CONSOLE: SPATIALLY GROUPED DELIVERY BATCHES
# ============================================================

# 🟢 BATCH 1: Ground floor - Row A (East Side)
#    • Runner Load: 2 items
#    • Sequence: 
#      - Order #101 -> Seat Groundfloor-A-8 [Items: ['tacos'] | Prep: 5m]
#      - Order #102 -> Seat Groundfloor-A-9 [Items: ['burgers'] | Prep: 8m]
#    • Routing Note: High spatial proximity. Fulfill at Vendor together.

# 🔵 BATCH 2: Ground floor - Row A (West Side)
#    • Runner Load: 1 item
#    • Sequence:
#      - Order #104 -> Seat Groundfloor-A-99 [Items: ['fries'] | Prep: 3m]
#    • Routing Note: Isolated from East Side Row A due to X-Coordinate delta > 1000.

# 🟡 BATCH 3: First Floor - Row B
#    • Runner Load: 1 item
#    • Sequence:
#      - Order #103 -> Seat FirstFloor-B-12 [Items: ['tacos'] | Prep: 4m]
#    • Routing Note: Hard floor boundary separation active.

# ============================================================
# Execution Metrics: 1 AI Call | 0 Tool Round-trips | Latency: ~420ms
# ============================================================
# """

# if __name__ == "__main__":
#     agent = SingleCallLogisticsAgent()
#     agent.process_stadium_logistics()

# import os
# from google.adk.agents import LlmAgent
# from google.adk.tools.mcp_tool import McpToolset
# from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
# from mcp import StdioServerParameters

# # Define the single-turn clustering logic parameters
# SYSTEM_INSTRUCTION = """
# You are the Logistics Cluster Specialist. Your ONLY job is to take a list of validated orders and group them into optimal runner delivery batches.

# Use the following execution workflow to complete your job in one turn:
# 1. Call 'get_pending_orders' to retrieve all unfulfilled order items.
# 2. For each order, look up its spatial metadata using 'fetch_stadium_map'.
# 3. Once the full data is gathered, evaluate these strict grouping constraints:
#    - Spatial Proximity: Group orders whose row letters/zones are close together. Use the absolute x and y coordinates to verify proximity since section labels do not exist in the data.
#    - Prep Time Balancing: Ensure quick pre-packaged items (short prep times) do not sit around waiting too long for fresh-cooked items (long prep times). Keep the internal delta of prep times within a batch tightly clustered.
#    - Capacity Cap: A single delivery runner can carry a maximum of 6 items per batch. Do not exceed this threshold.

# Output Format:
# Output the grouped batches exclusively as a beautifully structured, minified JSON map displaying group names, order ids, and the calculated maximum wait time for that specific batch. Do not include markdown code blocks, conversational pleasantries, or trailing text outside of the JSON payload.
# """

# # Defining the root agent matching the official Google ADK design pattern
# root_agent = LlmAgent(
#     model='gemini-2.0-flash', # Upgraded from flash-latest to leverage native multi-tool parallel performance
#     name='logistics_specialist',
#     instruction=SYSTEM_INSTRUCTION,
#     tools=[
#         McpToolset(
#             connection_params=StdioConnectionParams(
#                 server_params=StdioServerParameters(
#                     command='npx',
#                     args=[
#                         "mcp-remote",
#                         "https://biterush-f06463.kb.us-central1.gcp.cloud.es.io/api/agent_builder/mcp",
#                         "--header",
#                         "Authorization:ApiKey MXNmQWJKNEJkeXBlNnFJeUR2d0w6RzE0bGY1RGJ2MGlqQXRDbTVvQ0o4QQ=="
#                     ],
#                     # Standard environment parameters mapping for the child process execution pipe
#                     env={
#                         "KIBANA_URL": "https://biterush-f06463.kb.us-central1.gcp.cloud.es.io/api/agent_builder/mcp",
#                         "AUTH_HEADER": "ApiKey MXNmQWJKNEJkeXBlNnFJeUR2d0w6RzE0bGY1RGJ2MGlqQXRDbTVvQ0o4QQ=="
#                     }
#                 )
#             )
#         )
#     ],
# )

# import asyncio
# import json
# import os
# from dotenv import load_dotenv

# # Import ADK's internal session tools to handle the server connections directly
# from google.adk.tools.mcp_tool import McpToolset
# from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
# from mcp import StdioServerParameters

# load_dotenv()

# async def run_raw_tool_fetch():
#     print(" Establishing direct pipe to Elastic MCP Server via mcp-remote...")
    
#     # Configure the exact same server connection parameters
#     connection_params = StdioConnectionParams(
#         server_params=StdioServerParameters(
#             command='npx',
#             args=[
#                 "mcp-remote",
#                 "https://biterush-f06463.kb.us-central1.gcp.cloud.es.io/api/agent_builder/mcp",
#                 "--header",
#                 "Authorization:ApiKey MXNmQWJKNEJkeXBlNnFJeUR2d0w6RzE0bGY1RGJ2MGlqQXRDbTVvQ0o4QQ=="
#             ],
#             env={
#                 "KIBANA_URL": "https://biterush-f06463.kb.us-central1.gcp.cloud.es.io/api/agent_builder/mcp",
#                 "AUTH_HEADER": "ApiKey MXNmQWJKNEJkeXBlNnFJeUR2d0w6RzE0bGY1RGJ2MGlqQXRDbTVvQ0o4QQ=="
#             }
#         )
#     )

#     # Initialize the Toolset object
#     toolset = McpToolset(connection_params=connection_params)
    
#     # We use ADK's session manager context to open the underlying client session pipe
#     async with toolset._mcp_session_manager.get_session(connection_params) as session:
#         print(" Session created successfully! Fetching tools metadata index...")
        
#         # 1. Discover what tools your Elastic Server has registered
#         available_tools = await session.list_tools()
#         print("\n=== Registered MCP Tools Found ===")
#         for tool in available_tools.tools:
#             print(f"  Tool Name: {tool.name} -> {tool.description[:60]}...")
#         print("===================================\n")

#         # 2. Call your pending orders tool explicitly, capping it at 6 items
#         print(" Invoking 'get_pending_orders' directly from the server...")
#         try:
#             # Replace 'get_pending_orders' if your tool name matches a different key
#             result = await session.call_tool(
#                 name="get_pending_orders", 
#                 arguments={"size": 6} 
#             )
            
#             print("\n [RAW TOOL RESPONSE RECEIVED] 🚨")
#             # Extract and display the clean payload text back out
#             for content_item in result.content:
#                 if hasattr(content_item, 'text'):
#                     print(content_item.text)
#                 else:
#                     print(content_item)
                    
#         except Exception as e:
#             print(f" Failed to execute tool: {str(e)}")

# if __name__ == "__main__":
#     # Run the direct connection pipeline script natively without adk web
#     asyncio.run(run_raw_tool_fetch())



###################################################################multitool


# import os
# import json
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# from google.adk.agents import Agent

# ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
# ELASTIC_MCP_URL = os.getenv("ELASTIC_MCP_URL")


# # ── I. DATA DESERIALIZATION PARSER ──────────────────────────────────────────
# def parse_esql_response(raw_mcp_text: str) -> list[dict]:
#     """Parses raw ESQL JSON matrix formats back into explicit Python dict arrays."""
#     try:
#         data = json.loads(raw_mcp_text)
#         for result in data.get("results", []):
#             if result.get("type") == "esql_results":
#                 esql_data = result["data"]
#                 columns = [col["name"] for col in esql_data["columns"]]
#                 return [dict(zip(columns, row)) for row in esql_data["values"]]
#     except Exception as e:
#         print(f"[PARSER ERROR] Failed to deserialize ESQL layout matrix: {e}")
#     return []


# # ── II. RAW BACKEND CONNECTION RUNTIMES ──────────────────────────────────────
# async def execute_fetch_stadium_map(seat_identifier: str) -> str:
#     server_params = StdioServerParameters(
#         command="npx",
#         args=["mcp-remote", ELASTIC_MCP_URL, "--header", f"Authorization:ApiKey {ELASTIC_API_KEY}"],
#     )
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
            
#             # ✅ CRITICAL FIX: The key name must be exactly what the server expects: "seat"
#             args = {"seat": seat_identifier.strip()} 
            
#             result = await session.call_tool("fetch_stadium_map", arguments=args)
#             return result.content[0].text if result.content else "{}"




# async def execute_get_pending_orders(vendor_id: str) -> str:
#     server_params = StdioServerParameters(
#         command="npx",
#         args=["mcp-remote", ELASTIC_MCP_URL, "--header", f"Authorization:ApiKey {ELASTIC_API_KEY}"],
#     )
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
#             args = {"vendor_id": vendor_id.strip()}
#             result = await session.call_tool("get_pending_orders", arguments=args)
#             return result.content[0].text if result.content else "[]"


# # ── 2. FIX THE ADK TOOL WRAPPER ──────────────────────────────────────────────
# # We change the function argument name to 'seat' so Gemini generates {"seat": "..."}
# async def fetch_stadium_map(seat: str) -> dict:
#     """Fetch the precise location properties and absolute x/y map vector coordinates for a given seat locator.

#     Args:
#         seat (str): The unique seat identifier string, formatted precisely without spaces (e.g., 'Groundfloor-A-8').

#     Returns:
#         dict: The parsed spatial coordinates and layout details from the database.
#     """
#     # Pass it straight to the connector
#     raw_json = await execute_fetch_stadium_map(seat)
#     try:
#         return json.loads(raw_json)
#     except Exception:
#         return {"raw_data": raw_json}

# async def get_pending_orders(vendor_id: str) -> list[dict]:
#     """Retrieve up to 6 completed customer orders containing section, row_number, seat_number, and items for a vendor ID.

#     Args:
#         vendor_id (str): The unique string token identification for the kitchen vendor (e.g., 'V010').

#     Returns:
#         list[dict]: A structured collection of open order queue items.
#     """
#     raw_json = await execute_get_pending_orders(vendor_id)
#     return parse_esql_response(raw_json)


# # ── IV. THE ADK AGENT DEFINITION ─────────────────────────────────────────────
# root_agent = Agent(
#     name="stadium_operations_agent",
#     model="gemini-flash-latest",
#     description="Agent to handle stadium order routing audits and seat coordinate lookups.",
#     instruction=(
#         "You are BiteRush Copilot, an analytical stadium operations agent. You use your tools to query database targets.\n\n"
#         "CRITICAL PROTOCOLS:\n"
#         "1. PENDING ORDERS LOOKUP: When asked to look up pending/completed orders for a vendor, extract the vendor ID (e.g., 'V010') and invoke 'get_pending_orders'.\n"
#         "2. SEAT LAYOUT LOOKUP: When a seat lookup is requested, clean the parameter: capitalize the first letter of the floor, uppercase the row letter, strip spaces, join them with hyphens, and call 'fetch_stadium_map' passing the parameter as 'seat_guid' (e.g., 'Groundfloor-A-8').\n\n"
#         "Always present data back cleanly, explicitly referencing keyword attributes."
#     ),
#     tools=[get_pending_orders, fetch_stadium_map],
# )


########################################################################

# Copyright 2026 Google LLC
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google.adk.agents import Agent

ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
ELASTIC_MCP_URL = os.getenv("ELASTIC_MCP_URL")


# ── I. DATA DESERIALIZATION PARSER ──────────────────────────────────────────
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


# ── II. RAW BACKEND CONNECTION RUNTIMES ──────────────────────────────────────
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


# ── III. NATIVE ASYNC TOOLS FOR ADK AGENT ─────────────────────────────────────
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


# ── IV. THE ADK AGENT DEFINITION WITH LOGISTICS CLUSTERING INSTRUCTIONS ───────
root_agent = Agent(
    name="stadium_operations_agent",
    model="gemini-flash-latest",
    description="Agent to handle stadium order routing audits and seat coordinate lookups with batch optimization algorithms.",
    instruction=(
        "You are BiteRush Copilot, an expert stadium fulfillment coordination engine. "
        "Your core responsibility is sorting and packing raw pending order vectors into optimized, logical runner delivery batches.\n\n"
        
        "── BATCHING & LOGISTICS PROTOCOLS ──\n"
        "When an operator pulls pending orders, you must analyze the list and display them grouped into discrete 'Delivery Batches' according to these strict operational constraints:\n\n"
        
        "1. CAPACITY CONSTRAINT:\n"
        "   - Maximum of 6 orders per delivery runner batch. Never exceed this limit.\n\n"
        
        "2. SPATIAL GEOMETRY COHESION (PRIORITY 1):\n"
        "   - Group orders by `floor_level` and `zone_name` first. A runner should never change floors or cross distant structural stadium configurations during a single batch run.\n"
        "   - Cluster nearby rows and seats together to minimize runner transit steps.\n\n"
        
        "3. THERMAL & PREP COMPATIBILITY (PRIORITY 2):\n"
        "   - Isolate item profiles based on `food_type` properties:\n"
        "     * WARM FOOD (e.g., burgers, fries, fresh items) must stay grouped to prevent heat loss.\n"
        "     * COLD ITEMS / DRINKS (e.g., soda, beer, ice cream) should not be packed alongside high-temperature elements.\n"
        "     * PREPACKAGED ITEMS (e.g., chips, candy) are neutral and can act as batch fillers.\n"
        "   - Align batch sequences by `prep_time_sec` so items finishing around the same time leave together, preventing hot items from sitting under heat lamps.\n\n"
        
        "── TOOL EXECUTION PROTOCOLS ──\n"
        "1. PENDING ORDERS LOOKUP: Extract the vendor token (e.g., 'V010') and call 'get_pending_orders'. Afterwards, output your strategic batch configuration maps.\n"
        "2. SEAT LAYOUT LOOKUP: Clean the parameter format precisely to 'Floorlevel-Row-Seat' (e.g., 'Groundfloor-A-8') and invoke 'fetch_stadium_map' via the 'seat' parameter key.\n\n"
    
       
        """OUTPUT FORMAT:
Provide the batches clearly using these delimiters. Do not use JSON.
---BATCH_START---
Group: [Name]
Orders: [ID1, ID2]
Seats: [A-1, A-2]
Food: [Item1, Item2]
Max_Wait: [Time]
---BATCH_END---"""
    ),
    tools=[get_pending_orders, fetch_stadium_map],
)
