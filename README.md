# 🏟️ BiteRush - Agentic AI Stadium Delivery Platform

**An autonomous agent that replaces manual stadium dispatch with real-time, reasoning-driven order clustering and routing.**

Built for large-venue events: World Cup matches, concerts  where thousands of seat-side food orders need to be coordinated across floors and sections faster than any human dispatcher can manage.

---

## The Problem

During large sporting events and concerts, customers often order food and beverages from their seats. Stadium staff typically rely on manual assignment and communication to fulfill these orders, leading to inefficient delivery routes, longer wait times, and inconsistent customer experiences. As attendance increases, coordinating thousands of deliveries across multiple seating sections becomes increasingly challenging.
## The Approach

<img width="1140" height="935" alt="diagram-export-7-16-2026-5_14_52-PM" src="https://github.com/user-attachments/assets/289bf106-012b-438e-b9a5-715cc4ed5db4" />


## Why these technology choices

**Why an AI agent, not a fixed algorithm** - Clustering depends on multiple real-time variables that interact with each other (prep time × floor × seating proximity × order volume). A hardcoded heuristic would need constant tuning as conditions change; an agent reasons over live state directly against a strict operational protocol instead.

**Why Elasticsearch, not a conventional database** - The system's decisions are only as good as how current its data is. A conventional database can persist order data, but resolving a query like *"which pending orders are near this seat and within an acceptable wait window"* fast enough to matter requires real-time structured querying. That's what ES|QL is built for! Elasticsearch here is a live operational store the agent actively queries, not just a place data gets written to.

**Why MCP** - The agent never talks to Elasticsearch directly. MCP (authenticated via API key) exposes exactly two custom coded tools keeping the raw index schema and query surface out of the LLM's context entirely. The agent can only do what the tool contract allows.

---

## Agent Design

`stadium_operations_agent` runs on Google ADK with `gemini-flash-latest` as the reasoning model, registered with two tools:

| Tool
|---|
| `get_pending_orders(vendor_id)` 
| `fetch_stadium_map(seat)` 

The agent operates under a strict system protocol, not open-ended generation:

- **Capacity constraint** 
- **Spatial cohesion (priority 1)** 
- **Thermal/prep compatibility (priority 2)** 
- **Max ETA** 

---

## Challenges and Design Choices

The first version of BiteRush split responsibilities across **four specialized agents** : assignment, routing, staffing, analysis communicating with each other. It worked, but cost:

- Up to **24 network calls per order**
- **~2 minutes** of end-to-end latency

Unusable for live stadium conditions during peak demand.

**Redesigned into a single orchestrator agent with direct tool execution** one agent, calling its own tools instead of delegating to other agents:

| | Before (multi-agent) | After (single orchestrator) |
|---|---|---|
| Network calls / order | up to 24 | **1** |
| Latency | ~2 min | **10 - 20 sec** |

**Takeaway:** more agents isn't more intelligence as the bottleneck was coordination overhead, not reasoning quality.

---

## Human-in-the-Loop

The agent proposes clusters; a vendor reviews and dispatches each batch from the live dashboard. Staff keep final control over dispatch while the agent absorbs the coordination work that doesn't scale manually — which is precisely what breaks down first during high-traffic windows.

---

## Tech Stack

| | |
|---|---|
| **Agent orchestration** | Google Agent Development Kit (ADK) |
| **Reasoning model** | Gemini (`gemini-flash-latest`) |
| **Data layer** | Elasticsearch :MCP tools and storage indexes |
| **Connectivity** | MCP server (`mcp-remote`), API-key authenticated |
| **Frontend** | Streamlit : customer ordering app + vendor logistics dashboard |
| **Backend** | Python |
| **Deployment** | Railway |

---
**Live demo:** 
Vendor DashBoard:- [https://biterush-stadium-ecommerce-platform-production.up.railway.app](https://biterush-stadium-ecommerce-platform-production.up.railway.app/)


Customer Module:-  [biterush-customer-module-production.up.railway.app](https://biterush-customer-module-production.up.railway.app/)

**Video demo:** 
https://youtu.be/h9sDZzl3SCw

---
## Running Locally

```bash
pip install -r requirements.txt
```

```bash
# .env
ELASTIC_API_KEY=your_key
ADK_BASE_URL=http://127.0.0.1:8000
```

```bash
adk web stadium_operations_agent      # start the agent
streamlit run customer_app.py         # customer ordering app
streamlit run app.py                  # vendor dashboard
```


---

## What's Next

- Spatial-aware navigation layer with live map-based delivery guidance for runners
- Camera/sensor integration for crowd-density-aware routing
- Multi-vendor marketplace support (currently single-vendor)

---

## CopyRight

Built solo by **Charmi Doshi** for the Google Agent Hackathon - Building Agents for Real-World Challenges.

## License

MIT - see [`LICENSE`](./LICENSE)


