import streamlit as st
import time
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My AI Helper Baby", page_icon="🔔", layout="centered")

# --- SOUND JAVASCRIPT (The Magic Alarm) ---
# Ye code background mein sound play karega
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

# --- APP STYLING ---
st.markdown("""
    <style>
    .stApp {background-color: #f0f2f6;}
    .task-card {background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4757;}
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- MAIN FUNCTIONS ---
def add_task(text):
    # Simple logic to convert "in 5 sec" to time
    due_time = None
    target_time_str = "No timer"
    
    if "sec" in text:
        try:
            sec = int([s for s in text.split() if s.isdigit()][0])
            due_time = datetime.now() + timedelta(seconds=sec)
            target_time_str = due_time.strftime("%H:%M:%S")
        except: pass
    elif "min" in text:
        try:
            mins = int([s for s in text.split() if s.isdigit()][0])
            due_time = datetime.now() + timedelta(minutes=mins)
            target_time_str = due_time.strftime("%H:%M:%S")
        except: pass

    st.session_state.tasks.append({
        "title": text,
        "due_time": due_time,
        "display_time": target_time_str,
        "played": False,  # To check if alarm already played
        "status": "Pending"
    })

# --- TITLE & VOICE INSTRUCTION ---
st.title("🔔 My AI Helper Baby")

# --- VOICE INPUT TIP ---
st.info("🎙️ **Voice Tip:** Type karne ki jagah, apne Mobile Keyboard ka **Mic Icon** 🎤 dabao aur bolo!")

# --- INPUT AREA ---
with st.form("task_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        task_input = st.text_input("Task bolo ya likho...", placeholder="E.g. Remind me in 10 sec")
    with col2:
        submitted = st.form_submit_button("Add Task ➕")
        
    if submitted and task_input:
        add_task(task_input)
        st.success("Task Added!")
        st.rerun()

st.divider()

# --- LIVE TIMER CHECK & ALARM ---
# Ye loop check karega ki time hua ya nahi
now = datetime.now()
trigger_alarm = False

if st.session_state.tasks:
    for task in st.session_state.tasks:
        if task['status'] == 'Pending' and task['due_time']:
            # Agar time ho gaya aur abhi tak alarm nahi baja
            if now >= task['due_time'] and not task['played']:
                trigger_alarm = True
                task['played'] = True  # Mark as played so it doesn't loop forever
                st.toast(f"⏰ ALARM: {task['title']}!", icon="🔔")

# --- PLAY SOUND IF TRIGGERED ---
if trigger_alarm:
    # Ye JavaScript ko bolega ki Sound play karo
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
    col_a, col_b, col_c = st.columns([0.7, 0.2, 0.1])
    with col_a:
        st.markdown(f"**{task['title']}**")
    with col_b:
        st.caption(f"⏰ {task['display_time']}")
    with col_c:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- AUTO REFRESH (To keep checking time) ---
# Ye page ko har 2 second mein refresh karega taaki alarm baj sake
time.sleep(2)
st.rerun()
