import streamlit as st
import json
import uuid
import requests
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()
ES_BASE_URL = os.getenv("ELASTIC_BASE_URL")
ES_API_KEY  = os.getenv("ELASTIC_API_KEY")


st.set_page_config(page_title="Franky Vadapav", layout="centered")

"""
Copyright (c) 2026 [Charmi Doshi]
All Rights Reserved. This code is shared publicly for portfolio 
purposes only. Unauthorized copying or reuse is prohibited.
"""

st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .brand { padding: 1.2rem 0 0.5rem 0; border-bottom: 2px solid #E24B4A; margin-bottom: 1.5rem; }
    .brand h1 { font-size: 1.8rem; font-weight: 700; color: #E24B4A; margin: 0; letter-spacing: -0.5px; }
    .brand p { font-size: 0.82rem; color: #888; margin: 2px 0 0 0; }
    .sec-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #aaa; margin-bottom: 6px; }
    .menu-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; border: 1px solid #e8e8e8; border-radius: 8px; margin-bottom: 6px; background: #fff; }
    .menu-row.active { border-color: #E24B4A; border-width: 2px; background: #fff8f8; }
    .menu-name { font-size: 0.93rem; font-weight: 600; color: #111; }
    .menu-price { font-size: 0.82rem; color: #888; margin-top: 1px; }
    .tag-v { display: inline-block; font-size: 9px; font-weight: 700; background: #EAF3DE; color: #3B6D11; border-radius: 3px; padding: 1px 5px; margin-left: 5px; vertical-align: middle; }
    .tag-a { display: inline-block; font-size: 9px; font-weight: 700; background: #FAEEDA; color: #854F0B; border-radius: 3px; padding: 1px 5px; margin-left: 5px; vertical-align: middle; }
    .summary-box { background: #f9f9f9; border-radius: 8px; padding: 12px 16px; margin: 8px 0 4px 0; }
    .s-row { display: flex; justify-content: space-between; font-size: 0.88rem; color: #555; padding: 3px 0; }
    .s-total { display: flex; justify-content: space-between; font-size: 1rem; font-weight: 700; color: #111; border-top: 1px solid #e0e0e0; margin-top: 6px; padding-top: 6px; }
    .s-seat { font-size: 0.78rem; color: #999; margin-top: 6px; }
    .s-seat strong { color: #333; }
    .success-wrap { text-align: center; padding: 2.5rem 1rem; }
    .checkmark { display: inline-block; width: 72px; height: 72px; border-radius: 50%; background: #E24B4A; line-height: 72px; font-size: 2rem; color: white; animation: popIn 0.4s cubic-bezier(0.34,1.56,0.64,1) both; margin-bottom: 1rem; }
    @keyframes popIn { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .oid { font-size: 1.3rem; font-weight: 700; color: #E24B4A; letter-spacing: 0.04em; margin: 4px 0; }
    .success-wrap h2 { margin: 0 0 4px 0; color: #111; }
    .success-wrap p  { color: #777; font-size: 0.88rem; margin: 4px 0; }
</style>
""", unsafe_allow_html=True)

VENDOR_ID = "V010"
ES_INDEX  = "incoming-orders"

MENU_ITEMS = [
    {"id": "vadapav", "name": "Vada pav",      "icon": "🥙", "price": 20,  "tag": "veg", "food_type": "fresh_cooked", "prep_time_sec": 90},
    {"id": "samosa",  "name": "Indian samosa", "icon": "🥟", "price": 35,  "tag": "veg", "food_type": "fresh_cooked", "prep_time_sec": 75},
    {"id": "fries",   "name": "French fries",  "icon": "🍟", "price": 5,  "tag": "veg", "food_type": "fresh_cooked", "prep_time_sec": 60},
    {"id": "hotdog",  "name": "Hot dog",        "icon": "🌭", "price": 7,  "tag": "",    "food_type": "fresh_cooked", "prep_time_sec": 70},
    {"id": "tacos",   "name": "Tacos",          "icon": "🌮", "price": 4,  "tag": "",    "food_type": "fresh_cooked", "prep_time_sec": 80},
    {"id": "coke",    "name": "Coke",           "icon": "🥤", "price": 3,  "tag": "",    "food_type": "packaged",     "prep_time_sec": 0},
    {"id": "beer",    "name": "Beer",           "icon": "🍺", "price": 10, "tag": "alc", "food_type": "packaged",     "prep_time_sec": 0},
]
MENU_BY_ID = {m["id"]: m for m in MENU_ITEMS}
FLOORS = ["Ground floor", "First floor"]
ROWS   = list("ABCDEF")
SEATS  = list(range(1, 14))

for k, v in {"cart": {}, "order_placed": False, "last_order": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def build_es_doc(floor, row, seat, cart: dict, payment) -> dict:
    """
    One document per order. item_ordered is an array of item ids,
    e.g. ["fries", "beer"]. All other fields match the original schema.
    food_type and prep_time_sec reflect the dominant (max prep) item.
    """
    oid = "ORD" + uuid.uuid4().hex[:6].upper()

    
    item_ordered = list(cart.keys())  

  
    dominant = max(cart.keys(), key=lambda iid: MENU_BY_ID[iid]["prep_time_sec"])

    source = {
        "order_id":       oid,
        "vendor_id":      VENDOR_ID,
        "item_ordered":   item_ordered,                          # ← array
        "food_type":      MENU_BY_ID[dominant]["food_type"],
        "prep_time_sec":  MENU_BY_ID[dominant]["prep_time_sec"],
        "row_number":     row,
        "seat_number":    int(seat),
        "payment_status": "completed" if payment in ("Card", "UPI") else "pending",
        "floor_level":    floor,
        "timestamp":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return {"_index": ES_INDEX, "_id": oid, "_score": 1, "_source": source}


def print_order(doc: dict):
    print("\n" + "="*52)
    print("  FRANKY VADAPAV — NEW ORDER")
    print("="*52)
    print(json.dumps(doc, indent=2))
    print("="*52 + "\n")


def push_to_es(doc: dict) -> tuple[bool, str]:
    url = f"{ES_BASE_URL.rstrip('/')}/{doc['_index']}/_doc/{doc['_id']}"
    headers = {"Content-Type": "application/json", "Authorization": f"ApiKey {ES_API_KEY}"}
    try:
        resp = requests.put(url, headers=headers, data=json.dumps(doc["_source"]), timeout=8)
        if resp.status_code in (200, 201):
            return True, resp.json().get("result", "ok")
        return False, f"HTTP {resp.status_code} — {resp.text[:200]}"
    except requests.exceptions.ConnectionError:
        return False, f"Cannot reach Elasticsearch at {ES_BASE_URL}"
    except requests.exceptions.Timeout:
        return False, "Request timed out (8 s)"
    except Exception as exc:
        return False, str(exc)

st.markdown("""
<div class="brand">
  <h1>🍔 Franky Vadapav</h1>
  <p>Order fresh food to your seat</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.order_placed and st.session_state.last_order:
    doc = st.session_state.last_order
    src = doc["_source"]
    seat_str = f"{src['floor_level']} · Row {src['row_number']} · Seat {src['seat_number']}"
    
    st.markdown(f"""
    <div class="success-wrap">
      <div class="checkmark">✓</div>
      <h2>Order placed!</h2>
      <p>Delivering to <strong>{seat_str}</strong></p>
      <div class="oid">{doc['_id']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Place another order", use_container_width=True):
        st.session_state.order_placed = False
        st.session_state.last_order   = None
        st.session_state.cart         = {}
        st.rerun()
    st.stop()

st.markdown('<div class="sec-label">Your seat</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    floor = st.selectbox("Floor", [""] + FLOORS,
                         format_func=lambda x: "Floor" if x == "" else x,
                         label_visibility="collapsed")
with c2:
    row = st.selectbox("Row", [""] + ROWS,
                       format_func=lambda x: "Row" if x == "" else f"Row {x}",
                       label_visibility="collapsed")
with c3:
    seat = st.selectbox("Seat", [""] + SEATS,
                        format_func=lambda x: "Seat" if x == "" else str(x),
                        label_visibility="collapsed")

st.divider()

st.markdown('<div class="sec-label">Menu</div>', unsafe_allow_html=True)

for item in MENU_ITEMS:
    in_cart  = item["id"] in st.session_state.cart
    card_cls = "menu-row active" if in_cart else "menu-row"

    tag_html = ""
    if item["tag"] == "veg":
        tag_html = '<span class="tag-v">VEG</span>'
    elif item["tag"] == "alc":
        tag_html = '<span class="tag-a">21+</span>'

    col_info, col_btn = st.columns([4, 1])
    with col_info:
        st.markdown(f"""
        <div class="{card_cls}">
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:1.5rem; line-height:1;">{item['icon']}</span>
            <div>
              <span class="menu-name">{item['name']}</span>{tag_html}
              <div class="menu-price">$ {item['price']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        label = "Remove" if in_cart else "Add"
        if st.button(label, key=f"b_{item['id']}", use_container_width=True):
            if in_cart:
                del st.session_state.cart[item["id"]]
            else:
                st.session_state.cart[item["id"]] = 1
            st.rerun()

    if in_cart:
        qty     = st.session_state.cart[item["id"]]
        new_qty = st.number_input("Quantity", min_value=1, max_value=20, value=qty,
                                  key=f"q_{item['id']}", label_visibility="visible")
        if new_qty != qty:
            st.session_state.cart[item["id"]] = new_qty
            st.rerun()

st.divider()
st.markdown('<div class="sec-label">Payment</div>', unsafe_allow_html=True)
payment = st.radio("Payment method", ["Card", "UPI", "Cash"],
                   horizontal=True, label_visibility="collapsed")

st.divider()

if st.session_state.cart:
    st.markdown('<div class="sec-label">Order summary</div>', unsafe_allow_html=True)
    total, rows_html = 0, ""
    for iid, qty in st.session_state.cart.items():
        m   = MENU_BY_ID[iid]
        sub = m["price"] * qty
        total += sub
        rows_html += f'<div class="s-row"><span>{m["name"]} x{qty}</span><span>$. {sub}</span></div>'

    seat_str = f"{floor} / Row {row} / Seat {seat}" if (floor and row and seat) else "—"
    st.markdown(f"""
    <div class="summary-box">
      {rows_html}
      <div class="s-total"><span>Total</span><span>$. {total}</span></div>
      <div class="s-seat">Delivering to: <strong>{seat_str}</strong></div>
    </div>
    """, unsafe_allow_html=True)


can_order = bool(floor and row and seat and st.session_state.cart)

if st.button("Place order", use_container_width=True, type="primary", disabled=not can_order):
    if not (floor and row and seat):
        st.error("Select your floor, row, and seat.")
    elif not st.session_state.cart:
        st.error("Add at least one item.")
    else:
        doc = build_es_doc(floor, row, seat, st.session_state.cart, payment)
        print_order(doc)

        with st.spinner("Sending to kitchen…"):
            ok, msg = push_to_es(doc)
            if ok:
                print(f"  ES indexed {doc['_id']} ({msg})")
            else:
                print(f"  ES error  {doc['_id']}: {msg}")
                st.error(f"Elasticsearch indexing failed:\n{doc['_id']}: {msg}")

        st.session_state.last_order   = doc
        st.session_state.order_placed = True
        st.session_state.cart         = {}
        st.rerun()