from typing import List
from fastapi import APIRouter, Depends, HTTPException
import api.schemas.task as task_schema

from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()

'''
CURDをtaskに対して実装する
TODO:Rの部分を実装する．DBとの連携はcrud/task.pyで実装したものを使う．
'''

# R: read task
# DBから取得したタスクを返却する
# タスクの全件取得
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

# @router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession=Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return await task_crud.update_task(db, task_body, original = task)


# C: create task, crudで定義したDB operationの関数　task_crud.create_taskを呼び出している
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    #return task_schema.TaskCreateResponse(id=1, **task_body.dict())
    return await task_crud.create_task(db, task_body)



# D: delete task
# DBからタスクを削除する   
@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    '''
    taskidを受け取り、DBから削除する
    
    arg: task_id: int
    return:  
    '''
    task = await task_crud.get_task(db, task_id=task_id) # firstly get the task with task_id
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return await task_crud.delete_task(db, original = task) # delete the task, imported from crud/task.py





