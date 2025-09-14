import streamlit as st

st.set_page_config(page_title="To-Do", page_icon="✅")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "just_updated" not in st.session_state:
    st.session_state.just_updated = False

st.title("To-Do")

# Add task (with completion status)
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Add a task")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append({"text": new_task.strip(), "done": False})
        st.session_state.just_updated = True

st.subheader("Your tasks")

# Render tasks with checkbox
for i, task in enumerate(st.session_state.tasks):
    checkbox_state = st.checkbox(task["text"], value=task["done"], key=f"cb_{i}")
    st.session_state.tasks[i]["done"] = checkbox_state
    cols = st.columns([1, 8, 2])
    cols[1].write(task["text"])
    if cols[2].button("Delete", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.session_state.just_updated = True
        st.rerun()

# Feedback toast
if st.session_state.just_updated:
    st.session_state.just_updated = False
    st.toast("Updated!", icon="✅")


