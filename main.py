from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str


# GET - Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# POST - Create a new task
@app.post("/tasks")
def create_task(task: Task):
    # Check duplicate task ID
    for existing_task in tasks:
        if existing_task["id"] == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task ID already exists"
            )

    tasks.append(task.dict())
    return task


# PUT - Update an existing task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for i, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            tasks[i] = task.dict()
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# DELETE - Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            return tasks.pop(i)

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )