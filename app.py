import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

st.set_page_config(page_title="Zen Task", page_icon="✅")

# Request browser notification permission
streamlit_js_eval(js_expressions=["Notification.requestPermission()"], key="force_permission")

# Hide Streamlit branding
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom app title
st.markdown("<h1 style='text-align: center;'>Zen Task ✅</h1>", unsafe_allow_html=True)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "just_updated" not in st.session_state:
    st.session_state.just_updated = False

# Notification trigger function
def send_notification(title, body):
    js_code = f"""
    if (Notification.permission === "granted") {{
        new Notification("{title}", {{ body: "{body}" }});
    }} else if (Notification.permission !== "denied") {{
        Notification.requestPermission().then(permission => {{
            if (permission === "granted") {{
                new Notification("{title}", {{ body: "{body}" }});
            }}
        }});
    }}
    """
    streamlit_js_eval(js_expressions=[js_code], key="notify")

# Add task form with deadline
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Add a task")
    deadline = st.date_input("Set deadline")
    submitted = st.form_submit_button("Add Task")

if submitted and new_task.strip():
    st.session_state.tasks.append({
        "text": new_task.strip(),
        "done": False,
        "deadline": str(deadline)
    })
    st.session_state.just_updated = True
    send_notification("New Task Added", new_task.strip())

# Task list with deadline display
st.subheader("Your tasks")
today = datetime.today().date()

for i, task in enumerate(st.session_state.tasks):
    checkbox_state = st.checkbox(task["text"], value=task["done"], key=f"cb_{i}")
    st.session_state.tasks[i]["done"] = checkbox_state

    deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
    cols = st.columns([1, 6, 3, 2])

    if deadline_date < today and not task["done"]:
        cols[1].markdown(f"**{task['text']}**")
        cols[2].markdown(f":red[Overdue: {task['deadline']}]")
    else:
        cols[1].write(task["text"])
        cols[2].write(f"Deadline: {task['deadline']}")

    if cols[3].button("Delete", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.session_state.just_updated = True
        st.rerun()

# Toast feedback
if st.session_state.just_updated:
    st.session_state.just_updated = False
    st.toast("Updated!", icon="✅")

