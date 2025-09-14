import streamlit as st

st.set_page_config(page_title="To-Do", page_icon="✅")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "just_updated" not in st.session_state:
    st.session_state.just_updated = False

st.title("To-Do")

# Add task (using form to avoid flash + no need for rerun)
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Add a task")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append(new_task.strip())
        st.session_state.just_updated = True
        # No rerun needed here

st.subheader("Your tasks")

# Render and delete tasks
for i, task in enumerate(st.session_state.tasks):
    cols = st.columns([1, 8, 2])
    cols[1].write(task)
    if cols[2].button("Delete", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.session_state.just_updated = True
        st.rerun()  # keep this to avoid index shift issues after delete

# Soft feedback without breaking flow
if st.session_state.just_updated:
    st.session_state.just_updated = False
    st.toast("Updated!", icon="✅")


    if checkbox_state != task[1]:
        st.session_state.tasks[index][1] = checkbox_state
        save_tasks(st.session_state.tasks)

        st.experimental_rerun()
