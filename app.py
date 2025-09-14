import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Zen Task", page_icon="✅")
streamlit_js_eval(js_expressions=["Notification.requestPermission()"], key="force_permission") 


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

# App title
st.title("Zen Task")

# Add task form
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Add a task")
    submitted = st.form_submit_button("Add Task")

if submitted and new_task.strip():
    st.session_state.tasks.append({"text": new_task.strip(), "done": False})
    st.session_state.just_updated = True
    send_notification("New Task Added", new_task.strip())

# Task list
st.subheader("Your tasks")
for i, task in enumerate(st.session_state.tasks):
    checkbox_state = st.checkbox(task["text"], value=task["done"], key=f"cb_{i}")
    st.session_state.tasks[i]["done"] = checkbox_state
    cols = st.columns([1, 8, 2])
    cols[1].write(task["text"])
    if cols[2].button("Delete", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.session_state.just_updated = True
        st.rerun()

# Toast feedback
if st.session_state.just_updated:
    st.session_state.just_updated = False
    st.toast("Updated!", icon="✅")



