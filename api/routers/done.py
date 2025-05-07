from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.done as done_schema
import api.cruds.done as done_crud
from api.db import get_db


router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=done_schema.Done)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    '''
    taskidを受け取り、doneにする
    '''
    # 1. get the task with task_id from DB
    task: done_schema.Done = await done_crud.get_done(db, task_id=task_id)
    # if task is None, raise exception
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # 2. create done
        
    return await done_crud.create_done(db, task_id=task_id)
    

@router.delete("/tasks/{task_id}/done",response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    '''
    taskidを受け取り、doneを削除する
    '''
    # 1. get the task with task_id from DB
    task = await done_crud.get_done(db, task_id=task_id)
    # if task is None, raise exception
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # 2. delete done
    return  await done_crud.delete_done(db, original=task)