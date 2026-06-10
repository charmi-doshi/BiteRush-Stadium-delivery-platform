# import streamlit as st
# import requests

# # 1. Configuration
# ADK_BASE_URL = "http://localhost:8000"
# APP_NAME = "stadium_operations_agent"
# USER_ID = "hackathon_judge"
# SESSION_ID = "biterush_stadium_session"

# st.set_page_config(page_title="BiteRush Fulfillment Copilot", page_icon="🏟️", layout="wide")
# st.title("🏟️ BiteRush: Stadium Fulfillment Copilot")

# def ensure_session():
#     url = f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions"
#     try:
#         requests.post(url, json={"sessionId": SESSION_ID})
#     except Exception as e:
#         st.error(f"Failed to initialize session: {e}")

# if "session_initialized" not in st.session_state:
#     ensure_session()
#     st.session_state.session_initialized = True

# if "chat_history_logs" not in st.session_state:
#     st.session_state.chat_history_logs = []


# for message in st.session_state.chat_history_logs:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# if prompt := st.chat_input("Enter command..."):
#     st.session_state.chat_history_logs.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
        
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         with st.spinner("Processing..."):
#             payload = {
#                 "appName": APP_NAME,
#                 "userId": USER_ID,
#                 "sessionId": SESSION_ID,
#                 "newMessage": {"role": "user", "parts": [{"text": prompt}]}
#             }
            
#             try:
#                 response = requests.post(f"{ADK_BASE_URL}/run", json=payload, timeout=60)
                
#                 if response.status_code == 200:
#                     data = response.json()
                    
#                     # DEBUG: See what is actually coming back
#                     print(f"DEBUG DATA TYPE: {type(data)}")
#                     print(f"DEBUG DATA CONTENT: {data}")
#                     if isinstance(data, list):
#                         target = data[0]
#                     else:
#                         target = data
                    
#                     # Navigate the hierarchy: content -> parts -> [0] -> text
#                     try:
#                         content_parts = target.get("content", {}).get("parts", [])
#                         assistant_text = content_parts[0].get("text", "No text found.")
                        
#                         message_placeholder.markdown(assistant_text)
#                         st.session_state.chat_history_logs.append({"role": "assistant", "content": assistant_text})
#                     except (IndexError, KeyError, AttributeError):
#                         message_placeholder.error("Could not parse agent response structure.")
#             except Exception as e:
#                 message_placeholder.error(f"Connection failed: {str(e)}")


import streamlit as st
import requests
import pandas as pd

# 1. Configuration
ADK_BASE_URL = "http://localhost:8000"
APP_NAME = "stadium_operations_agent"
USER_ID = "hackathon_judge"
SESSION_ID = "biterush_stadium_session"

st.set_page_config(page_title="BiteRush Fulfillment Copilot", page_icon="🏟️", layout="wide")

# --- SIDEBAR: DASHBOARD UI ---
st.sidebar.title("⚙️ Operations Dashboard")
st.sidebar.subheader("Live Agent Steps")
agent_steps = st.sidebar.empty() # This will display the agent's progress
st.sidebar.divider()
st.sidebar.metric("System Status", "Live", "Stable")

st.title("🏟️ BiteRush: Stadium Fulfillment Copilot")

def ensure_session():
    url = f"{ADK_BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions"
    try:
        requests.post(url, json={"sessionId": SESSION_ID})
    except Exception as e:
        st.error(f"Failed to initialize session: {e}")

if "session_initialized" not in st.session_state:
    ensure_session()
    st.session_state.session_initialized = True

if "chat_history_logs" not in st.session_state:
    st.session_state.chat_history_logs = []

for message in st.session_state.chat_history_logs:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter command..."):
    st.session_state.chat_history_logs.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # --- AGENT LOGIC FLOW ---
        agent_steps.markdown("1. 🔍 Analyzing request...\n2. 🛰️ Fetching spatial data...\n3. 🧠 Optimizing routes...")
        
        with st.spinner("Processing..."):
            payload = {
                "appName": APP_NAME,
                "userId": USER_ID,
                "sessionId": SESSION_ID,
                "newMessage": {"role": "user", "parts": [{"text": prompt}]}
            }
            
            try:
                response = requests.post(f"{ADK_BASE_URL}/run", json=payload, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    target = data[0] if isinstance(data, list) else data
                    
                    content_parts = target.get("content", {}).get("parts", [])
                    assistant_text = content_parts[0].get("text", "No text found.")
                    
                    message_placeholder.markdown(assistant_text)
                    st.session_state.chat_history_logs.append({"role": "assistant", "content": assistant_text})
                    
                    # --- INTERACTIVE CHART LOGIC ---
                    # Only show if the agent is talking about batches/orders
                    if "Batch" in assistant_text:
                        agent_steps.markdown("✅ Dispatch Plan Generated.")
                        # Demo Mock Data based on typical stadium coordinates
                        chart_data = pd.DataFrame(
                            {"x": [100, 150, 80, 400], "y": [200, 250, 180, 400], "order": ["A-4", "C-2", "A-1", "G-12"]}
                        )
                        st.subheader("📍 Order Fulfillment Map")
                        st.scatter_chart(chart_data, x='x', y='y', size=200)
                    else:
                        agent_steps.markdown("✅ Task complete.")

                else:
                    message_placeholder.error(f"Error {response.status_code}")
            except Exception as e:
                message_placeholder.error(f"Connection failed: {str(e)}")