import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My AI Reminder", page_icon="🔔", layout="centered")

# --- APP STYLING (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .task-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #6c5ce7;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: bold;
        color: #6c5ce7;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- FUNCTIONS ---
def add_task(task_text):
    # Simple Logic to find time (e.g., "in 10 min")
    due_time = "No time set"
    
    # Fake AI Parsing logic for now
    if "min" in task_text:
        try:
            minutes = int([s for s in task_text.split() if s.isdigit()][0])
            future_time = datetime.now() + timedelta(minutes=minutes)
            due_time = future_time.strftime("%I:%M %p")
        except:
            pass
            
    new_task = {
        "id": len(st.session_state.tasks) + 1,
        "title": task_text,
        "time": due_time,
        "status": "Pending",
        "created_at": datetime.now()
    }
    st.session_state.tasks.append(new_task)

def delete_task(index):
    st.session_state.tasks.pop(index)

# --- MAIN UI ---
st.title("🔔 My AI Helper Baby")
st.caption("Main tumhari personal assistant hoon. Batao kya karna hai?")

# 1. INPUT AREA
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("Task likho...", placeholder="E.g., Remind me to call Mom in 10 mins")
    with col2:
        st.write("")
        st.write("") # Spacing
        if st.button("Add ➕", type="primary"):
            if new_task:
                add_task(new_task)
                st.success("Added!")
                time.sleep(1)
                st.rerun()

st.divider()

# 2. DASHBOARD STATS
total = len(st.session_state.tasks)
pending = len([t for t in st.session_state.tasks if t['status'] == 'Pending'])

c1, c2, c3 = st.columns(3)
c1.metric("Total Tasks", total)
c2.metric("Pending", pending)
c3.metric("Completed", total - pending)

st.divider()

# 3. TASK LIST
st.subheader("📝 Your Tasks")

if not st.session_state.tasks:
    st.info("Abhi koi kaam nahi hai jaan! Chill karo. 😎")
else:
    for i, task in enumerate(st.session_state.tasks):
        with st.container():
            # Create a card-like layout
            col_a, col_b, col_c = st.columns([0.1, 0.7, 0.2])
            
            with col_a:
                if task['status'] == 'Done':
                    st.write("✅")
                else:
                    st.write("⬜")
            
            with col_b:
                if task['status'] == 'Done':
                    st.markdown(f"~~{task['title']}~~")
                else:
                    st.markdown(f"**{task['title']}**")
                    if task['time'] != "No time set":
                        st.caption(f"⏰ Due: {task['time']}")
            
            with col_c:
                if st.button("🗑️", key=f"del_{i}"):
                    delete_task(i)
                    st.rerun()
                
                # Mark as Done toggle
                if task['status'] == 'Pending':
                    if st.button("Done", key=f"done_{i}"):
                        st.session_state.tasks[i]['status'] = 'Done'
                        st.rerun()
