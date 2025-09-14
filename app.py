import streamlit as st
import json

FILE_PATH = "tasks.json"

def load_tasks():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks_to_save):
    with open(FILE_PATH, "w") as file:
        json.dump(tasks_to_save, file)

# A variable to store our tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("To-Do List App")
st.markdown("---")

new_task = st.text_input("Enter a new task:")
add_button = st.button("Add Task")

if add_button and new_task:
    st.session_state.tasks.append([new_task, False])
    save_tasks(st.session_state.tasks)
    st.experimental_rerun()

st.header("Your Tasks")
for index, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        checkbox_state = st.checkbox(task[0], value=task[1], key=f"checkbox_{index}")
    with col2:
        if st.button("Delete", key=f"delete_{index}"):
            del st.session_state.tasks[index]
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()

    if checkbox_state != task[1]:
        st.session_state.tasks[index][1] = checkbox_state
        save_tasks(st.session_state.tasks)
        st.experimental_rerun()