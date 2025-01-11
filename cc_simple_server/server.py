from fastapi import FastAPI, HTTPException
from cc_simple_server.models import TaskCreate, TaskRead
from cc_simple_server.database import init_db, get_db_connection

# init
init_db()

app = FastAPI()

############################################
# Edit the code below this line
############################################


@app.get("/")
async def read_root():
    return {"message": "Welcome to the SQLite Task Manager API!"}


# POST ROUTE
@app.post("/tasks/", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (task_data.title, task_data.description, task_data.completed),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return TaskRead(id=task_id, **task_data.dict())


# GET ROUTE
@app.get("/tasks/", response_model=list[TaskRead])
async def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [TaskRead(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"])) for row in rows]


# UPDATE ROUTE
@app.put("/tasks/{task_id}/", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()

    if not existing_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
        (task_data.title, task_data.description, task_data.completed, task_id),
    )
    conn.commit()
    conn.close()

    return TaskRead(id=task_id, **task_data.dict())


# DELETE ROUTE
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()

    if not existing_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return {"message": f"Task {task_id} deleted successfully"}
