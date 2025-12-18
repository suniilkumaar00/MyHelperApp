import streamlit as st
import time
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My AI Helper Baby", page_icon="🔔", layout="centered")

# --- SOUND JAVASCRIPT ---
sound_code = """
<audio id="alarm_audio" style="display:none">
  <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
</audio>
<script>
  function playAlarm() {
    var audio = document.getElementById("alarm_audio");
    audio.play();
  }
</script>
"""
st.markdown(sound_code, unsafe_allow_html=True)

# --- STYLING ---
st.markdown("""
    <style>
    .stApp {background-color: #f0f2f6;}
    .task-card {background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4757;}
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- HELPER: GET INDIA TIME ---
def get_india_time():
    # Server time (UTC) mein 5:30 hours jod rahe hain
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

# --- MAIN FUNCTIONS ---
def add_task(text):
    due_time = None
    target_time_str = "No timer"
    
    # India time lo
    now_india = get_india_time()
    
    if "sec" in text:
        try:
            sec = int([s for s in text.split() if s.isdigit()][0])
            due_time = now_india + timedelta(seconds=sec)
            target_time_str = due_time.strftime("%I:%M:%S %p") # AM/PM format
        except: pass
    elif "min" in text:
        try:
            mins = int([s for s in text.split() if s.isdigit()][0])
            due_time = now_india + timedelta(minutes=mins)
            target_time_str = due_time.strftime("%I:%M:%S %p")
        except: pass

    st.session_state.tasks.append({
        "title": text,
        "due_time": due_time,
        "display_time": target_time_str,
        "played": False,
        "status": "Pending"
    })

# --- UI TITLE ---
st.title("🔔 My AI Helper (India)")

# --- INPUT AREA ---
with st.form("task_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        task_input = st.text_input("Task likho...", placeholder="E.g. Remind me in 10 sec")
    with col2:
        submitted = st.form_submit_button("Add Task ➕")
        
    if submitted and task_input:
        add_task(task_input)
        st.success("Task Added!")
        st.rerun()

st.divider()

# --- ALARM CHECKER (India Time) ---
now_india = get_india_time()
trigger_alarm = False

if st.session_state.tasks:
    for task in st.session_state.tasks:
        if task['status'] == 'Pending' and task['due_time']:
            # Agar India time match ho gaya
            if now_india >= task['due_time'] and not task['played']:
                trigger_alarm = True
                task['played'] = True
                st.toast(f"⏰ ALARM: {task['title']}!", icon="🔔")

# --- PLAY SOUND ---
if trigger_alarm:
    st.components.v1.html(
        """<script>
        var audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
        audio.play();
        </script>""", 
        height=0, width=0
    )

# --- TASK LIST ---
st.subheader("📝 Your Tasks")
for i, task in enumerate(st.session_state.tasks):
    col_a, col_b, col_c = st.columns([0.6, 0.3, 0.1])
    with col_a:
        st.markdown(f"**{task['title']}**")
    with col_b:
        # Time ab AM/PM mein dikhega
        st.caption(f"⏰ {task['display_time']}")
    with col_c:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- AUTO REFRESH ---
time.sleep(2)
st.rerun()
