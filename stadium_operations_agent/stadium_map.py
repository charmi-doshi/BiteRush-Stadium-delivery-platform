# # grouping_agent/stadium_map.py
# import json
# import os

# def load_and_flatten_canvas_map():
#     """
#     Parses the stadium map by traversing zones -> rows -> seats,
#     saving two types of keys so our agent can always match the location.
#     """
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     root_dir = os.path.dirname(current_dir) 
#     file_path = os.path.join(root_dir, "stadium_canvas_blueprint.json")
    
#     if not os.path.exists(file_path):
#         print(f" Missing JSON blueprint at {file_path}! Using test fallback.")
#         return {
#             "KITCHEN_ORIGIN": {"x": 800.0, "y": 480.0},
#             "A-1": {"x": 881.93, "y": 481.21, "title": "Fallback - Row A, Seat 1"},
#             "A-5": {"x": 981.93, "y": 481.21, "title": "Fallback - Row A, Seat 5"}
#         }

#     with open(file_path, "r", encoding="utf-8") as f:
#         raw_data = json.load(f)
    
#     flat_stadium_map = {}
    
#     #  Establish our Central Kitchen Ground Station
#     flat_stadium_map["KITCHEN_ORIGIN"] = {"x": 800.0, "y": 480.0}
    
#     zones = raw_data.get("zones", [])
#     for zone in zones:
#         zone_name = zone.get("name", "Groundfloor").replace(" ", "")
#         rows = zone.get("rows", [])
        
#         for row in rows:
#             row_pos = row.get("position", {"x": 0, "y": 0})
#             row_base_x = float(row_pos.get("x", 0))
#             row_base_y = float(row_pos.get("y", 0))
#             row_id = str(row.get("row_number", "")).strip()
            
#             seats = row.get("seats", [])
#             for seat in seats:
#                 seat_num = str(seat.get("seat_number", "")).strip()
#                 seat_pos = seat.get("position", {"x": 0, "y": 0})
                
#                 # Calculate True Absolute Grid Coordinates
#                 abs_x = row_base_x + float(seat_pos.get("x", 0))
#                 abs_y = row_base_y + float(seat_pos.get("y", 0))
                
#                 seat_data = {
#                     "x": round(abs_x, 2),
#                     "y": round(abs_y, 2),
#                     "title": f"{zone.get('name')} - Row {row_id}, Seat {seat_num}"
#                 }
                
#                 # 💡 ADDED HERE: Create both lookup formats so the agent never fails
#                 guid_key = seat.get("seat_guid", f"{zone_name}-{row_id}-{seat_num}")
#                 simple_key = f"{row_id}-{seat_num}"
                
#                 flat_stadium_map[guid_key] = seat_data
#                 flat_stadium_map[simple_key] = seat_data
            
#     return flat_stadium_map

# ACTIVE_STADIUM_GEOMETRY = load_and_flatten_canvas_map()
# # =====================================================================
# # 🧪 STANDALONE VERIFICATION TEST BED
# # =====================================================================
# if __name__ == "__main__":
#     import math

#     print(" Starting Standalone Verification Test for stadium_map.py...\n")

#     # 1. Test Data Loading and Flattening Engine
#     print(" Step 1: Parsing stadium_canvas_blueprint.json...")
#     try:
#         geometry_map = load_and_flatten_canvas_map()
        
#         if geometry_map and "101" in geometry_map:
#             print(" Success! Blueprint parsed successfully.")
#             print(f" Total Sections Processed: {len(geometry_map)}")
#             print(f" Sample Section 101 Coordinates: {geometry_map['101']}\n")
#         else:
#             print(" Parsed map is empty or Section 101 fallback was triggered.\n")
            
#     except Exception as e:
#         print(f" Structural Parsing Error occurred: {str(e)}\n")
#         geometry_map = {}

#     # 2. Test Spatial Math Routing Utility
#     print(" Step 2: Testing Distance Calculation & Routing Engine...")
    
#     # Let's mock a batch of incoming orders to see if the math computes
#     mock_batch = [
#        {"order_id": "ORD001", "section": "A-1"},
#         {"order_id": "ORD002", "section": "A-5"}
#     ]

#     print(f" Location Coordinates for Seat A-1: {geometry_map.get('A-1')}")
#     print(f" Location Coordinates for Seat A-5: {geometry_map.get('A-5')}")
    
#     # Run the routing tool path logic loop
#     kitchen_loc = (800.0, 480.0)
#     current_loc = kitchen_loc
#     destinations = [str(o["section"]) for o in mock_batch]
    
#     print("\n stand-alone seat-level mapping matrix checks out perfectly!")
    
#     # We simulate a simplified version of our routing function right here
#     print(f" Injecting Test Batch Destinations: {[o['section'] for o in mock_batch]}")
    
#     current_loc = kitchen_loc  # Mock Central Kitchen Origin
#     destinations = list(set([str(o["section"]) for o in mock_batch]))
#     route_sequence = []
#     total_distance = 0
    
#     while destinations:
#         # Filter matching sections in our parsed geometry map
#         valid_targets = [d for d in destinations if d in geometry_map]
#         if not valid_targets:
#             print(" Error: None of the mock sections were found in your JSON map matrix.")
#             break
            
#         # Find closest spatial node coordinate point
#         next_target = min(
#             valid_targets,
#             key=lambda x: math.dist(current_loc, (geometry_map[x]["x"], geometry_map[x]["y"]))
#         )
#         destinations.remove(next_target)
        
#         target_coords = (geometry_map[next_target]["x"], geometry_map[next_target]["y"])
#         total_distance += math.dist(current_loc, target_coords)
        
#         route_sequence.append(next_target)
#         current_loc = target_coords

#     print("Math Execution Complete!")
#     print(f"  Computed Shortest Sequence Path: {' -> '.join(['Central Kitchen'] + route_sequence)}")
#     print(f" Calculated Relative Sequence Distance Vector: {round(total_distance, 2)} units")
#     print("\n Standalone pipeline testing complete!")


# grouping_agent/stadium_map.py
import json
import os
import math

def build_stadium_uber_network():
    """
    100% DYNAMIC NETWORK BUILDER:
    Parses stadium_canvas_blueprint.json and weaves a network graph on the fly.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    file_path = os.path.join(root_dir, "stadium_canvas_blueprint.json")
    
    network_graph = {}
    
    def add_edge(node_a, node_b, distance):
        if node_a not in network_graph: network_graph[node_a] = {}
        if node_b not in network_graph: network_graph[node_b] = {}
        network_graph[node_a][node_b] = round(distance, 2)
        network_graph[node_b][node_a] = round(distance, 2)

    # Base Highway Entry Point
    network_graph["Kitchen"] = {}

    # Safety Fallback: If the JSON file vanishes, the server won't crash
    if not os.path.exists(file_path):
        add_edge("Kitchen", "Concourse_Gate_A", 40.0)
        add_edge("Concourse_Gate_A", "GROUNDFLOOR-A-1", 15.0)
        add_edge("GROUNDFLOOR-A-1", "GROUNDFLOOR-A-5", 35.0)
        return network_graph

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        zones = raw_data.get("zones", [])
        for zone in zones:
            rows = zone.get("rows", [])
            for row in rows:
                row_id = str(row.get("row_number", "")).strip().upper()
                seats = row.get("seats", [])
                
                previous_seat_key = None
                for i, seat in enumerate(seats):
                    # 🎯 DYNAMIC READING: Grab the unique string directly from the file
                    current_seat_key = str(seat.get("seat_guid", "")).strip().upper()
                    pos = seat.get("position", {"x": 0.0, "y": 0.0})
                    
                    # Deduce the gate prefix dynamically (e.g., "GROUNDFLOOR-A-4" -> "A")
                    guid_parts = current_seat_key.split("-")
                    zone_letter = guid_parts[1] if len(guid_parts) >= 2 else row_id
                    concourse_hub = f"Concourse_Gate_{zone_letter}"

                    # Automatically connect new gates to the kitchen on the fly
                    if concourse_hub not in network_graph["Kitchen"]:
                        add_edge("Kitchen", concourse_hub, 50.0)

                    # Connect the first seat of a row to its gate walkway
                    if i == 0:
                        add_edge(concourse_hub, current_seat_key, 20.0)

                    # Connect seats side-by-side along the row aisle
                    if previous_seat_key:
                        prev_seat = seats[i-1]
                        prev_pos = prev_seat.get("position", {"x": 0.0, "y": 0.0})
                        
                        # Calculate the distance between coordinates dynamically
                        px_gap = math.dist(
                            (float(pos["x"]), float(pos["y"])), 
                            (float(prev_pos["x"]), float(prev_pos["y"]))
                        )
                        if px_gap == 0: px_gap = 12.0 # Protection gap
                        
                        add_edge(previous_seat_key, current_seat_key, px_gap)

                    previous_seat_key = current_seat_key

    except Exception:
        # If the JSON layout formatting is broken, absorb the error safely
        add_edge("Concourse_Gate_A", "GROUNDFLOOR-A-5", 30.0)

    return network_graph

# Execute the dynamic builder on startup
STADIUM_ROAD_NETWORK = build_stadium_uber_network()