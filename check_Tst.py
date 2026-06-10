# Save as check_agent.py
from stadium_operations_agent import agents 

if agents:
    print(f"SUCCESS: Agent '{agents[0].name}' is registered.")
else:
    print("ERROR: Agent list is empty. The server cannot build the /run endpoint.")