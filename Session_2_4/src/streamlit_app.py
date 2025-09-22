import os
import time
import pandas as pd
import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000"

# -------- utilities --------
def api() -> httpx.Client:
    # One client per rerun; Streamlit reruns the script on interactions
    return httpx.Client(base_url=API_URL, timeout=10.0)

@st.cache_data(ttl=5, show_spinner=False)
def fetch_users():
    # You don't have a list endpoint in your API; fetch recent via a cheap trick:
    # If you add GET /users, use it here. For now we’ll just try ids 1..50.
    users = []
    with api() as c:
        for uid in range(1, 51):
            r = c.get(f"/users/{uid}")
            if r.status_code == 200:
                users.append(r.json())
    return pd.DataFrame(users)

@st.cache_data(ttl=5, show_spinner=False)
def fetch_tasks(user_id: int | None = None, completed: bool | None = None):
    params = {}
    if user_id is not None: params["user_id"] = user_id
    if completed is not None: params["completed"] = str(completed).lower()
    with api() as c:
        r = c.get("/tasks", params=params)
        r.raise_for_status()
        return pd.DataFrame(r.json())

def invalidate_cache():
    fetch_users.clear()
    fetch_tasks.clear()

# -------- UI --------
st.set_page_config(page_title="Task Tracker UI", layout="wide")

st.title("Task Tracker (FastAPI + MySQL + Streamlit)")

# --- Create User ---
with st.expander("➕ Create user", expanded=True):
    with st.form("create_user"):
        email = st.text_input("Email")
        full_name = st.text_input("Full name")
        submitted = st.form_submit_button("Create user")
    if submitted:
        if not email or not full_name:
            st.warning("Email and full name are required.")
        else:
            with api() as c:
                r = c.post("/users", json={"email": email, "full_name": full_name})
                if r.status_code == 201:
                    st.success(f"User created (id={r.json()['id']})")
                    invalidate_cache()
                elif r.status_code == 409:
                    st.error("Email already exists")
                else:
                    st.error(f"Error: {r.status_code} {r.text}")

# --- Users table ---
st.subheader("Users")
users_df = fetch_users()
if users_df.empty:
    st.info("No users yet. Create one above.")
else:
    st.dataframe(users_df, width='stretch', hide_index=True)

# --- Create Task ---
with st.expander("📝 Create task", expanded=True):
    with st.form("create_task"):
        user_id = st.number_input("User ID", min_value=1, step=1, value=int(users_df["id"].max()) if not users_df.empty else 1)
        title = st.text_input("Title")
        submitted_task = st.form_submit_button("Create task")
    if submitted_task:
        if not title:
            st.warning("Title required.")
        else:
            with api() as c:
                r = c.post("/tasks", json={"user_id": int(user_id), "title": title})
                if r.status_code == 201:
                    st.success(f"Task created (id={r.json()['id']})")
                    invalidate_cache()
                elif r.status_code == 404:
                    st.error("User does not exist")
                else:
                    st.error(f"Error: {r.status_code} {r.text}")

# --- Filter + list tasks ---
st.subheader("Tasks")
col1, col2, col3 = st.columns([1,1,2])
with col1:
    filter_user = st.number_input("Filter by user_id (0 = all)", min_value=0, step=1, value=0)
with col2:
    filter_status = st.selectbox("Completed?", ["All", "True", "False"], index=0)

completed_param = None
if filter_status == "True":
    completed_param = True
elif filter_status == "False":
    completed_param = False

user_param = None if filter_user == 0 else int(filter_user)

tasks_df = fetch_tasks(user_param, completed_param)
if tasks_df.empty:
    st.info("No tasks found.")
else:
    st.dataframe(tasks_df.sort_values("id", ascending=False), width='stretch', hide_index=True)

# --- Toggle completion inline ---
st.markdown("### Toggle completion")
task_id_to_toggle = st.number_input("Task ID", min_value=1, step=1, value=1)
new_state = st.selectbox("Set completed to:", [True, False], index=0)
if st.button("Update task"):
    with api() as c:
        r = c.patch(f"/tasks/{int(task_id_to_toggle)}", json={"completed": bool(new_state)})
        if r.status_code == 200:
            st.success("Task updated.")
            invalidate_cache()
            time.sleep(0.2)
        elif r.status_code == 404:
            st.error("Task not found")
        else:
            st.error(f"Error: {r.status_code} {r.text}")
