from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from cc_simple_server.models import TaskCreate
from cc_simple_server.models import TaskRead
from contextlib import contextmanager
from cc_simple_server.database import init_db
from cc_simple_server.database import get_db_connection


# init
init_db()

app = FastAPI()

############################################
# Edit the code below this line
############################################

@contextmanager
def get_cursor():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        db.commit()
        db.close()

@app.get("/")
async def read_root():
    """
    This is already working!!!! Welcome to the Cloud Computing!
    """
    return {"message": "Welcome to the Cloud Computing!"}


# POST ROUTE data is sent in the body of the request
@app.post("/tasks/", response_model=TaskRead)
async def create_task(task_data: TaskCreate):

    try:
        with get_cursor() as cursor:
            cursor.execute(
                            "INSERT INTO tasks (title,description,completed) VALUES(?,?,?)",
                            (task_data.title,task_data.description,task_data.completed)
                            )
            task_id = cursor.lastrowid
            return TaskRead(id=task_id, title=task_data.title, description=task_data.description, completed=task_data.completed)
    
    except Exception as E:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating task: {str(E)}")



# GET ROUTE to get all tasks
@app.get("/tasks/", response_model=list[TaskRead])
async def get_tasks():
  
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT id, title, description, completed from tasks")
            tasks=cursor.fetchall()

            return [TaskRead(id=row[0], title=row[1], description=row[2], completed=row[3]) for row in tasks]

    except Exception as E:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving tasks: {str(E)}")
        


# UPDATE ROUTE data is sent in the body of the request and the task_id is in the URL
@app.put("/tasks/{task_id}/", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
   
    try:
        with get_cursor() as cursor:
            cursor.execute("UPDATE tasks SET title=?, description=?, completed=? WHERE id=?",
                        (task_data.title,task_data.description,task_data.completed,task_id))
            
            if cursor.rowcount ==0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task with ID {task_id} not found.")
            
            return TaskRead(id=task_id, title=task_data.title, description=task_data.description,completed=task_data.completed)

    except Exception as E:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="404 Not Found")



# DELETE ROUTE task_id is in the URL
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    
    try:
        with get_cursor() as cursor:
            cursor.execute("DELETE from tasks where ID=?",(task_id,))

            if cursor.rowcount ==0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 Not Found")
            
            return {"message": f"Task {task_id} deleted successfully"}

    except Exception as E:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error deleting task: {str(E)}")
