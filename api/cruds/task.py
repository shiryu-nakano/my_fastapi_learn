
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional

from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.engine import Result


import api.models.task as task_model
import api.schemas.task as task_schema

# C: create task 
# arg: task_schemaつまりpythonでtask objectを作成し，それをjsonにする
async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())#ここで引数にもらったtask objectをDBモデルに変換する
    db.add(task)
    await db.commit()# 変換したtask objectをDBに追加する
    await db.refresh(task)# そのDBモデルを返却する？？
    return task


# R: read task
async def get_tasks_with_done(db: AsyncSession)-> List[Tuple[int,str,bool]]:
    '''
    DBからtaskを取得する
    返却値はid, title, doneのタプルのリスト
    ---
    arg: db: AsyncSession
    return: List[Tuple[int,str,bool]]: id, title, done
    '''
    result: Result = await( 
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id,
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()

# U: update task
async def update_task(
        db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
)-> task_model.Task:
    '''
    DBのtaskを更新する
    Create task との違いは，originalとしてすでにあるdbを受け取ってからそれを更新すること
    すでにタスクがある時にこれを読んで，更新する
    

    ---

    arg: db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
    return: task_model.Task
    '''
    original.title = task_create.title
    db.add(original)

    await db.commit()
    await db.refresh(original)
    return original

# R: read task
async def get_task(db: AsyncSession, task_id: int)-> Optional[task_model.Task]:
    '''
    DBからtaskを取得する
    get_tasks_with_doneと違う部分は，指定したidのtaskのみを取得すること
    ---
    arg: db: AsyncSession, task_id: int
    return: Optional[task_model.Task]
    '''
    result = await db.execute(# 以下を実行する，これは実際にはSQLクエリになる
        select(task_model.Task).where(task_model.Task.id == task_id)
    )
    task: Optional[task_model.Task] = result.first()# ここで一つのタスクを取得する
    return task[0] if task is not None else None# ここで一つのタスクを取得する

# D: delete task
async def delete_task(db: AsyncSession, original: task_model.Task)-> None:
    '''
    DBからtaskを削除する
    ---
    arg: db: AsyncSession, original: task_model.Task
    return: None
    '''
    await db.delete(original) #引数で受け取ったtask objectを削除する
    # これはSQLAlchemyのdeleteメソッドを使っている
    await db.commit()