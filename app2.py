# # import streamlit as st

# # ADK_BASE_URL = "http://localhost:8000"
# # APP_NAME = "stadium_operations_agent"
# # USER_ID = "hackathon_judge"
# # SESSION_ID = "biterush_stadium_session"

# # import requests
# # import streamlit as st

# # # --- API HELPERS ---
# # def fetch_batches():
# #     """Fetches batch updates from your agent API."""
# #     url = f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}/state"
# #     try:
# #         response = requests.get(url)
# #         if response.status_code == 200:
# #             # Assuming your agent returns the list of batches in the state
# #             return response.json().get("batches", [])
# #     except Exception as e:
# #         st.sidebar.error(f"Sync error: {e}")
# #     return []



# # def parse_agent_batch(text):
# #     """
# #     Extracts structured data from the agent's string format.
# #     """
# #     lines = text.split("\n")
# #     batch_title = lines[0].replace("### ", "").strip()
    
# #     # Extract data using string parsing
# #     route = ""
# #     items = []
# #     prep_time = "N/A"
# #     seats = "N/A"

# #     for line in lines:
# #         if "**Runner Route:**" in line:
# #             route = line.split("**Runner Route:**")[1].strip()
# #         elif "- **Items Included:**" in line:
# #             items.append(line.replace("- **Items Included:**", "").strip())
# #         elif "Prep:" in line:
# #             # Attempt to grab prep time from the end of the item line
# #             prep_time = line.split("Prep:")[1].strip()
# #         elif "Seats" in line:
# #             seats = line.split("Seats")[1].strip()

# #     return {
# #         "title": batch_title,
# #         "route": route,
# #         "items": items,
# #         "prep": prep_time,
# #         "seats": seats
# #     }
# # # 1. Page Configuration
# # st.set_page_config(page_title="BiteRush Logistics OS", layout="wide", page_icon="🏟️")

# # # 2. Enhanced CSS with Vibrant Colors
# # st.markdown("""
# #     <style>
# #         [data-testid="stSidebar"] { 
# #             background-color: #1e293b; 
# #             color: white; 
# #         }
# #         [data-testid="stSidebar"] * { color: white !important; }
        
# #         .logistics-card {
# #             background-color: white;
# #             border-radius: 16px;
# #             padding: 24px;
# #             box-shadow: 0 10px 20px rgba(0,0,0,0.08);
# #             border-left: 6px solid #3b82f6; /* Blue Accent */
# #             margin-bottom: 20px;
# #             transition: all 0.3s ease;
# #         }
# #         .logistics-card:hover { transform: scale(1.02); box-shadow: 0 15px 30px rgba(0,0,0,0.12); }
        
# #         .card-title { font-weight: 800; font-size: 1.3rem; color: #1e293b; }
# #         .card-details { font-size: 0.95rem; color: #64748b; margin: 10px 0; }
        
# #         .status-badge {
# #             background-color: #dcfce7; color: #166534;
# #             padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.8rem;
# #         }
# #     </style>
# # """, unsafe_allow_html=True)

# # # 3. State Initialization
# # if "dispatched_batches" not in st.session_state:
# #     st.session_state.dispatched_batches = [
# #         "### 📦 Delivery Batch 1 (Floor: Level 2 | Type: Hot)\n"
# #         "- **Runner Route:** Zone A -> Row 12, Seats A-4 to A-6\n"
# #         "- **Items Included:** `ORD-992` (2x Vadapav) | Prep: 4m\n"
# #         "- **Items Included:** `ORD-881` (1x Cold Coffee) | Prep: 2m",
        
# #         "### 📦 Delivery Batch 2 (Floor: Level 1 | Type: Cold)\n"
# #         "- **Runner Route:** Zone B -> Row 4, Seats G-12 to G-14\n"
# #         "- **Items Included:** `ORD-772` (2x Burger) | Prep: 6m\n"
# #         "- **Items Included:** `ORD-110` (1x Soda) | Prep: 1m",
        
# #         "### 📦 Delivery Batch 3 (Floor: Level 3 | Type: Snacks)\n"
# #         "- **Runner Route:** Zone C -> Row 1, Seats VIP-1 to VIP-2\n"
# #         "- **Items Included:** `ORD-445` (1x Fries) | Prep: 3m"
# #     ]




# # # 2. Sidebar Tabs (Custom UI)
# # with st.sidebar:
# #     # 1. Cleaner Header: Using st.markdown for a modern, text-based look
# #     st.markdown("## ⚡ BiteRush OS")
# #     st.markdown("---")
    
# #     # 2. Tab Navigation
# #     menu_selection = st.radio(
# #         "NAVIGATION", 
# #         ["Dashboard", "Analytics", "Profile", "Settings"],
# #         label_visibility="collapsed"
# #     )
    
# #     st.markdown("---")
# #     st.subheader("🤖 AI Command Console")
# #     st.chat_input("Dispatch command...")

# # # --- MAIN CONTENT DYNAMICS ---
# # if menu_selection == "Dashboard":
# #     st.title("🏟️ Logistics Dashboard")
# #     col1, col2, col3 = st.columns(3)
# #     col1.metric("Active Runners", "12", "↑ 2")
# #     col2.metric("Pending Batches", len(st.session_state.get("dispatched_batches", [])))
# #     col3.metric("System Health", "98%")

# # elif menu_selection == "Profile":
# #     st.title("👤 Vendor Profile")
# #     # Professional Profile Card Look
# #     with st.container(border=True):
# #         st.subheader("Franky Vadapav HQ")
# #         st.write("**Vendor ID:** #BR-9921")
# #         st.write("**Location:** North Stadium Gate")
# #         st.write("**Account Status:** Verified")
# #         st.button("Edit Profile")

# # elif menu_selection == "Analytics":
# #     st.title("📊 Operational Insights")
# #     col1, col2 = st.columns(2)
# #     col1.metric("Avg Delivery Time", "12m", "-2m")
# #     col2.metric("Efficiency", "94%")

# # elif menu_selection == "Settings":
# #     st.title("⚙️ System Settings")
# #     st.toggle("Enable Auto-Dispatch")
# #     st.toggle("Dark Mode", value=True)
# #     st.markdown("---")
# #     # Signout Section
# #     if st.button("🚪 Sign Out", type="primary"):
# #         st.warning("You have been signed out.")
# #         # Logic to clear session state or redirect
# #         st.stop()
# # # 6. Grid-based Layout
# # # cols = st.columns(3)
# # # for i, raw_text in enumerate(st.session_state.dispatched_batches):
# # #         data = parse_agent_batch(raw_text)
        
# # #         with cols[i % 3]:
# # #             st.markdown(f"""
# # #                 <div class="logistics-card">
# # #                     <div class="card-title">{data['title']}</div></br>
# # #                     <div style="color: #ef4444; font-weight: 700;">⏱️ Prep: {data['prep']}</div>
# # #                     <div style="font-size: 0.9rem; margin-top: 5px;">💺 Seats: {data['seats']}</div>
# # #                     <hr style="margin: 10px 0;">
# # #                     <div style="font-size: 0.85rem;"><strong>Items:</strong> {", ".join(data['items'])}</div>
# # #                     <div style="margin-top: 10px; padding: 8px; background: #f3f4f6; border-radius: 6px; font-size: 0.8rem;">
# # #                         <strong>Route:</strong> {data['route']}
# # #                     </div>
# # #                 </div>
# # #             """, unsafe_allow_html=True)
            
# # #             if st.button("Mark Completed", key=f"btn_{i}"):
# # #                 st.session_state.dispatched_batches.pop(i)
# # #                 st.rerun()

# # # --- MAIN DASHBOARD LOGIC ---
# # st.subheader("📋 Active Dispatch Board")

# # # Fetch fresh data from Agent
# # batches = fetch_batches()

# # if not batches:
# #     # --- SHOW THIS WHEN NO ORDERS ARE LEFT ---
# #     st.container(border=True).info("🚀 All systems clear. No pending delivery batches.")
# # else:
# #     # --- RENDER DYNAMIC CARDS ---
# #     cols = st.columns(3)
# #     for i, raw_text in enumerate(batches):
# #         data = parse_agent_batch(raw_text) # Your custom parsing function
        
# #         with cols[i % 3]:
# #             st.markdown(f"""
# #                 <div class="logistics-card">
# #                     <div class="card-title">{data['title']}</div>
# #                     <div style="color: #ef4444; font-weight: 700;">⏱️ Prep: {data['prep']}</div>
# #                     <div style="font-size: 0.9rem; margin-top: 5px;">💺 Seats: {data['seats']}</div>
# #                     <hr style="margin: 10px 0;">
# #                     <div style="font-size: 0.85rem;"><strong>Items:</strong> {", ".join(data['items'])}</div>
# #                     <div style="margin-top: 10px; padding: 8px; background: #f3f4f6; border-radius: 6px; font-size: 0.8rem;">
# #                         <strong>Route:</strong> {data['route']}
# #                     </div>
# #                 </div>
# #             """, unsafe_allow_html=True)
            
# #             if st.button("Mark Completed", key=f"btn_{i}"):
# #                 # OPTIONAL: Add API call here to tell the agent the task is done
# #                 st.rerun()


# import requests
# import streamlit as st

# # 1. Configuration
# ADK_BASE_URL = "http://localhost:8000"
# APP_NAME = "stadium_operations_agent"
# USER_ID = "hackathon_judge"
# SESSION_ID = "biterush_stadium_session"

# # Initialize Session State
# if "batches" not in st.session_state:
#     st.session_state.batches = []
# def trigger_batching_agent():
#     # Use the /run endpoint to execute the agent
#     url = f"{ADK_BASE_URL}/run"
#     payload = {
#         "appName": APP_NAME,
#         "userId": USER_ID,
#         "sessionId": SESSION_ID,
#         "newMessage": {
#             "role": "user", 
#             "parts": [{"text": "group pending order for V010"}]
#         }
#     }
    
#     try:
#         response = requests.post(url, json=payload, timeout=60)
#         if response.status_code == 200:
#             st.success("Agent processed batching logic.")
#             return True
#         else:
#             st.error(f"Failed to trigger agent: {response.status_code}")
#             return False
#     except Exception as e:
#         st.error(f"Connection Error: {e}")
#         return False
# def fetch_batches():
#     url = f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             # ADD THIS LINE TO DEBUG
#             st.write("DEBUG - API Response:", data) 
#             return data.get("batches", [])
#         return []
#     except Exception as e:
#         return []

# def parse_agent_batch(text):
#     if not isinstance(text, str): return {"title": "Error", "route": "", "items": [], "prep": "N/A", "seats": "N/A"}
#     lines = text.split("\n")
#     batch_title = lines[0].replace("### ", "").strip()
#     route, items, prep_time, seats = "", [], "N/A", "N/A"
#     for line in lines:
#         if "**Runner Route:**" in line: route = line.split("**Runner Route:**")[1].strip()
#         elif "- **Items Included:**" in line: items.append(line.replace("- **Items Included:**", "").strip())
#         elif "Prep:" in line: prep_time = line.split("Prep:")[1].strip()
#         elif "Seats" in line: seats = line.split("Seats")[1].strip()
#     return {"title": batch_title, "route": route, "items": items, "prep": prep_time, "seats": seats}

# # 2. UI Setup
# st.set_page_config(page_title="BiteRush Logistics OS", layout="wide", page_icon="🏟️")
# st.markdown("""
#     <style>
#         [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
#         [data-testid="stSidebar"] * { color: white !important; }
#         .logistics-card { background-color: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 20px rgba(0,0,0,0.08); border-left: 6px solid #3b82f6; margin-bottom: 20px; }
#         .card-title { font-weight: 800; font-size: 1.3rem; color: #1e293b; }
#     </style>
# """, unsafe_allow_html=True)

# # 3. Sidebar
# with st.sidebar:
#     st.markdown("## ⚡ BiteRush OS")
#     menu_selection = st.radio("NAVIGATION", ["Dashboard", "Analytics", "Profile", "Settings"], label_visibility="collapsed")
#     st.markdown("---")
#     st.subheader("🤖 AI Command Console")
#     st.chat_input("Dispatch command...")

# # 4. Main Content
# if menu_selection == "Dashboard":
#     st.title("🏟️ Logistics Dashboard")
    
#     # Single load for the session
#     # 1. Initialize the flag in session state
#     if "agent_run_complete" not in st.session_state:
#         st.session_state.agent_run_complete = False

#     # 2. Page Load Logic: Trigger ONLY IF not already done
#     if not st.session_state.agent_run_complete:
#         with st.spinner("Initializing logistics dispatcher..."):
#             success = trigger_batching_agent() # Your POST request
#             if success:
#                 st.session_state.agent_run_complete = True
#                 st.session_state.batches = fetch_batches() # Your GET request
#                 st.rerun() # Refresh to update the UI with data
#             else:
#                 st.error("Failed to connect to Dispatcher.")
#                 st.stop()
    
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Active Runners", "12")
#     col2.metric("Pending Batches", len(st.session_state.batches))
#     col3.metric("System Health", "98%")
#     st.markdown("---")
    
#     if not st.session_state.batches:
#         st.info("🚀 All systems clear. No pending delivery batches.")
#     else:
#         cols = st.columns(3)
#         for i, raw_text in enumerate(st.session_state.batches):
#             data = parse_agent_batch(raw_text)
#             with cols[i % 3]:
#                 st.markdown(f"""
#                     <div class="logistics-card">
#                         <div class="card-title">{data['title']}</div>
#                         <div style="color: #ef4444; font-weight: 700;">⏱️ Prep: {data['prep']}</div>
#                         <div style="font-size: 0.9rem; margin-top: 5px;">💺 Seats: {data['seats']}</div>
#                         <hr style="margin: 10px 0;">
#                         <div style="font-size: 0.85rem;"><strong>Items:</strong> {", ".join(data['items'])}</div>
#                         <div style="margin-top: 10px; padding: 8px; background: #f3f4f6; border-radius: 6px; font-size: 0.8rem;">
#                             <strong>Route:</strong> {data['route']}
#                         </div>
#                     </div>
#                 """, unsafe_allow_html=True)
#                 if st.button("Mark Completed", key=f"btn_{i}"):
#                     st.session_state.batches.pop(i)
#                     st.rerun()

# elif menu_selection == "Profile":
#     st.title("👤 Vendor Profile")
#     st.write("**Vendor ID:** #BR-9921")

# elif menu_selection == "Settings":
#     st.title("⚙️ System Settings")
#     if st.button("🚪 Sign Out"): st.stop()


# import requests
# ADK_BASE_URL = "http://localhost:8000"
# APP_NAME = "stadium_operations_agent"
# USER_ID = "hackathon_judge"
# SESSION_ID = "biterush_stadium_session"
# response = requests.get(f"{ADK_BASE_URL}/apps/{APP_NAME}")
# st.write(response.json())

# import streamlit as st
# import requests

# # --- CONFIGURATION (Missing Elements) ---
# ADK_BASE_URL = "http://localhost:8000"
# APP_NAME = "stadium_operations_agent"
# USER_ID = "hackathon_judge"
# SESSION_ID = "biterush_stadium_session"

# # --- STATE MANAGEMENT ---
# if "data_loaded" not in st.session_state:
#     st.session_state.data_loaded = False
# if "agent_output" not in st.session_state:
#     st.session_state.agent_output = None

# def get_agent_data():
#     # Only run if we haven't already succeeded
#     if st.session_state.data_loaded:
#         return

#     # --- MISSING PAYLOAD AND URL ---
#     url = f"{ADK_BASE_URL}/run"
#     payload = {
#         "appName": APP_NAME,
#         "userId": USER_ID,
#         "sessionId": SESSION_ID,
#         "newMessage": {"role": "user", "parts": [{"text": "pending orders for vendor V010"}]}
#     }
    
#     try:
#         # --- MISSING REQUEST EXECUTION ---
#         with st.spinner("Agent is optimizing routes..."):
#             response = requests.post(url, json=payload, timeout=60)
            
#             if response.status_code == 200:
#                 data = response.json()
#                 # Extract text from the agent's nested response structure
#                 target = data[0] if isinstance(data, list) else data
#                 assistant_text = target.get("content", {}).get("parts", [{}])[0].get("text", "No response content.")
                
#                 st.session_state.agent_output = assistant_text
#                 st.session_state.data_loaded = True # THE LOCK
#             else:
#                 st.error(f"API failed with status code: {response.status_code}")
#     except Exception as e:
#         st.error(f"API call failed: {e}")

# # --- UI ACTION ---
# if st.button("🚀 Generate Dispatch Plan"):
#     if not st.session_state.data_loaded:
#         get_agent_data()
#     else:
#         st.info("Plan already generated for this session.")

# # --- DATA DISPLAY ---
# if st.session_state.agent_output:
#     st.subheader("📋 Dispatch Plan Results")
#     st.markdown(st.session_state.agent_output)
    
#     if st.button("Reset Session"):
#         st.session_state.data_loaded = False
#         st.session_state.agent_output = None
        

import streamlit as st
import requests

# --- CONFIGURATION ---
ADK_BASE_URL = "http://localhost:8000"
APP_NAME = "stadium_operations_agent"
USER_ID = "hackathon_judge"
SESSION_ID = "biterush_stadium_session"


def create_session():
    """Must exist before /run is called."""
    try:
        response = requests.post(
            f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}",
            json={},
            timeout=10
        )
        # 200 = created, 409 = already exists — both OK
        return response.status_code in (200, 409)
    except Exception as e:
        st.error(f"Session error: {e}")
        return False


def trigger_batching_agent():
    try:
        # ✅ Step 1: Guarantee session exists
        if not create_session():
            return False

        # ✅ Step 2: camelCase confirmed correct from your schema
        response = requests.post(
            f"{ADK_BASE_URL}/run",
            json={
                "appName": APP_NAME,
                "userId": USER_ID,
                "sessionId": SESSION_ID,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": "group pending order for V010"}]
                },
                "streaming": False
            },
            timeout=60
        )

        if response.status_code != 200:
            st.error(f"Agent error {response.status_code}: {response.text}")
            return False
        return True

    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

def fetch_batches():
    try:
        response = requests.get(
            f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
        )
        if response.status_code == 200:
            events = response.json().get("events", [])
            # Walk events newest-first, find the last agent text response
            for event in reversed(events):
                if event.get("author") == "stadium_operations_agent":
                    parts = event.get("content", {}).get("parts", [{}])
                    raw_text = parts[0].get("text", "") if parts else ""
                    if raw_text:
                        return parse_agent_response(raw_text)
        return []
    except Exception as e:
        st.error(f"Fetch error: {e}")
        return []


# def parse_agent_response(text: str) -> list[dict]:
#     """
#     Parses the agent's ---BATCH_START--- / ---BATCH_END--- delimited output
#     into a list of dicts with keys: batch_title, orders, items, prep_time.
#     """
#     batches = []
#     sections = text.split("---BATCH_START---")

#     for section in sections:
#         if "---BATCH_END---" not in section:
#             continue

#         content = section.split("---BATCH_END---")[0].strip()
#         batch = {
#             "batch_title": "Delivery Batch",
#             "orders": "",
#             "items": [],
#             "prep_time": "N/A",
#             "seats": "N/A",
#         }

#         for line in content.splitlines():
#             line = line.strip()
#             if not line:
#                 continue
#             if line.startswith("Group:"):
#                 batch["batch_title"] = line.replace("Group:", "").strip()
#             elif line.startswith("Orders:"):
#                 raw_orders = line.replace("Orders:", "").strip()
#                 batch["orders"] = raw_orders
#                 # Use order IDs as the items list for display
#                 batch["items"] = [o.strip() for o in raw_orders.split(",") if o.strip()]
#             elif line.startswith("Max_Wait:"):
#                 batch["prep_time"] = line.replace("Max_Wait:", "").strip()
#             elif line.startswith("Seats:"):
#                 batch["seats"] = line.replace("Seats:", "").strip()

#         batches.append(batch)

#     return batches

def parse_agent_response(text: str) -> list[dict]:
    """
    Parses ---BATCH_START--- / ---BATCH_END--- delimited agent output into dicts.
    
    Expected format:
        ---BATCH_START---
        Group: [Name]
        Orders: [ID1, ID2]
        Seats: [A-1, A-2]
        Food: [Item1, Item2]
        Max_Wait: [Time]
        ---BATCH_END---
    """
    batches = []
    sections = text.split("---BATCH_START---")

    for section in sections:
        if "---BATCH_END---" not in section:
            continue

        content = section.split("---BATCH_END---")[0].strip()

        batch = {
            "batch_title": "Delivery Batch",
            "orders": "",
            "items": [],       # Food items
            "order_ids": [],   # Order IDs
            "prep_time": "N/A",
            "seats": "N/A",
        }

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("Group:"):
                batch["batch_title"] = line.replace("Group:", "").strip()
            elif line.startswith("Orders:"):
                raw = line.replace("Orders:", "").strip().strip("[]")
                batch["orders"] = raw
                batch["order_ids"] = [o.strip() for o in raw.split(",") if o.strip()]
            elif line.startswith("Seats:"):
                batch["seats"] = line.replace("Seats:", "").strip().strip("[]")
            elif line.startswith("Food:"):
                raw = line.replace("Food:", "").strip().strip("[]")
                batch["items"] = [f.strip() for f in raw.split(",") if f.strip()]
            elif line.startswith("Max_Wait:"):
                batch["prep_time"] = line.replace("Max_Wait:", "").strip().strip("[]")

        batches.append(batch)

    return batches

# --- UI SETUP ---
st.set_page_config(page_title="BiteRush Logistics OS", layout="wide", page_icon="🏟️")
st.markdown("""
    <style>
        [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
        [data-testid="stSidebar"] * { color: white !important; }
        .logistics-card {
            background-color: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.08);
            border-left: 6px solid #3b82f6;
            margin-bottom: 20px;
        }
        .card-title { font-weight: 800; font-size: 1.3rem; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION INITIALIZATION ---
if "agent_run_complete" not in st.session_state:
    st.session_state.agent_run_complete = False
if "batches" not in st.session_state:
    st.session_state.batches = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚡ BiteRush OS")
    menu_selection = st.radio(
        "NAVIGATION",
        ["Dashboard", "Analytics", "Profile", "Settings"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.subheader("🤖 AI Command Console")
    if st.button("🔄 Sync Logistics Data"):
        st.session_state.agent_run_complete = False
        st.session_state.batches = []
        st.rerun()

# --- MAIN LOGIC ---
if menu_selection == "Dashboard":
    st.title("🏟️ Logistics Dashboard")

    # Trigger agent only once per session (or after manual sync)
    if not st.session_state.agent_run_complete:
        with st.spinner("Optimizing routes..."):
            if trigger_batching_agent():
                st.session_state.batches = fetch_batches()
                st.session_state.agent_run_complete = True
                st.rerun()
            else:
                st.error("Dispatcher offline. Is `adk api_server` running on port 8000?")
                st.stop()

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Runners", "12")
    col2.metric("Pending Batches", len(st.session_state.batches))
    col3.metric("System Health", "98%")
    st.markdown("---")

    if not st.session_state.batches:
        st.info("🚀 All systems clear. No pending delivery batches.")
    else:
        cols = st.columns(3)
        # Iterate over a copy so pop() doesn't break the loop index
        for i, data in enumerate(list(st.session_state.batches)):
            with cols[i % 3]:
                # ✅ FIX: unsafe_allow_html (not unsafe_html)
                st.markdown(f"""
                    <div class="logistics-card">
                        <div class="card-title">📦 {data.get('batch_title', 'Batch')}</div>
                        <div style="color:#ef4444;font-weight:700;margin-top:8px;">
                            ⏱️ Max Wait: {data.get('prep_time', 'N/A')}
                        </div>
                        <div style="font-size:0.9rem;margin-top:5px;">
                            💺 Seats: {data.get('seats', 'N/A')}
                        </div>
                        <hr style="margin:10px 0;">
                        <div style="font-size:0.85rem;">
                            <strong>🍔 Food:</strong> {", ".join(data.get('items', []))}
                        </div>
                        <div style="font-size:0.85rem;margin-top:5px;">
                            <strong>📋 Orders:</strong> {", ".join(data.get('order_ids', []))}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("✅ Mark Completed", key=f"btn_{i}"):
                    st.session_state.batches.pop(i)
                    st.rerun()

elif menu_selection == "Analytics":
    st.title("📊 Operational Insights")
    col1, col2 = st.columns(2)
    col1.metric("Avg Delivery Time", "12m", "-2m")
    col2.metric("Efficiency", "94%")

elif menu_selection == "Profile":
    st.title("👤 Vendor Profile")
    with st.container(border=True):
        st.subheader("Franky Vadapav HQ")
        st.write("**Vendor ID:** #BR-9921")
        st.write("**Location:** North Stadium Gate")
        st.write("**Account Status:** Verified")
        st.button("Edit Profile")

elif menu_selection == "Settings":
    st.title("⚙️ System Settings")
    st.toggle("Enable Auto-Dispatch")
    st.toggle("Dark Mode", value=True)
    st.markdown("---")
    if st.button("🚪 Sign Out", type="primary"):
        st.warning("You have been signed out.")
        st.stop()
# import streamlit as st
# import requests

# # --- CONFIGURATION ---
# ADK_BASE_URL = "http://localhost:8000"
# APP_NAME = "stadium_operations_agent"
# USER_ID = "hackathon_judge"
# SESSION_ID = "biterush_stadium_session"



# # --- HELPER FUNCTIONS ---
# def trigger_batching_agent():
#     try:
#         response = requests.post(f"{ADK_BASE_URL}/run", json={
#             "appName": APP_NAME,
#             "userId": USER_ID,
#             "sessionId": SESSION_ID,
#             "newMessage": {"role": "user", "parts": [{"text": "group pending order for V010"}]}
#         }, timeout=60)
#         return response.status_code == 200
#     except:
#         return False

# def fetch_batches():
#     try:
#         response = requests.get(f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}")
#         if response.status_code == 200:
#             events = response.json().get("events", [])
#             for event in reversed(events):
#                 if event.get("author") == "stadium_operations_agent":
#                     raw_text = event.get("content", {}).get("parts", [{}])[0].get("text", "")
#                     # Return the parsed list directly
#                     return parse_agent_response(raw_text)
#         return []
#     except:
#         return []

# import json

# def parse_agent_response(text):
#     batches = []
#     # Split the agent output by your new delimiter
#     sections = text.split("---BATCH_START---")
#     for section in sections:
#         if "---BATCH_END---" in section:
#             # Extract content and map to dictionary
#             content = section.split("---BATCH_END---")[0].strip()
#             # ... process content lines ...
#             batches.append(content)
#     return batches

# # --- UI SETUP ---
# st.set_page_config(page_title="BiteRush Logistics OS", layout="wide", page_icon="🏟️")
# st.markdown("""
#     <style>
#         [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
#         [data-testid="stSidebar"] * { color: white !important; }
#         .logistics-card { background-color: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 20px rgba(0,0,0,0.08); border-left: 6px solid #3b82f6; margin-bottom: 20px; }
#         .card-title { font-weight: 800; font-size: 1.3rem; color: #1e293b; }
#     </style>
# """, unsafe_allow_html=True)

# # --- SESSION INITIALIZATION ---
# if "agent_run_complete" not in st.session_state:
#     st.session_state.agent_run_complete = False
#     st.session_state.batches = []

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("## ⚡ BiteRush OS")
#     menu_selection = st.radio("NAVIGATION", ["Dashboard", "Analytics", "Profile", "Settings"])
#     st.markdown("---")
#     st.subheader("🤖 AI Command Console")
#     # Using a button here instead of chat_input to control API usage
#     if st.button("🔄 Sync Logistics Data"):
#         st.session_state.agent_run_complete = False
#         st.rerun()

# # --- MAIN LOGIC ---
# if menu_selection == "Dashboard":
#     st.title("🏟️ Logistics Dashboard")
    
#     # Run API Only Once
#     if not st.session_state.agent_run_complete:
#         with st.spinner("Optimizing routes..."):
#             if trigger_batching_agent():
#                 st.session_state.batches = fetch_batches()
#                 st.session_state.agent_run_complete = True
#                 st.rerun()
#             else:
#                 st.error("Dispatcher offline.")
#                 st.stop()
    
#     # ... inside Dashboard logic ...
    
#     # st.session_state.batches is now a list of DICTIONARIES, not strings
#     cols = st.columns(3)
#     for i, data in enumerate(st.session_state.batches):
#         with cols[i % 3]:
#             st.markdown(f"""
#                 <div class="logistics-card">
#                     <div class="card-title">{data.get('batch_title', 'Batch')}</div>
#                     <div style="color: #ef4444; font-weight: 700;">⏱️ Prep: {data.get('prep_time')}</div>
#                     <div style="font-size: 0.9rem; margin-top: 5px;">💺 Seats: {data.get('seats')}</div>
#                     <hr>
#                     <div style="font-size: 0.85rem;"><strong>Items:</strong> {", ".join(data.get('items', []))}</div>
#                 </div>
#             """, unsafe_allow_html=True)
#             if st.button("Mark Completed", key=f"btn_{i}"):
#                 st.session_state.batches.pop(i)
            
              