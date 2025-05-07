from typing import Tuple, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

import api.models.task as task_model

'''
ここではdoneのCRUDを実装する
つまり，，，，
C すでにあるタスクをidで検索して，doneにする
R DONEであるタスクを全件取得して表示する
U 
D

このモジュールは機能実装のみを行う．外部のrouter.pyから呼び出されることを想定すること
このモジュールが依存しているのは，db.pyとmodel.pyのみ？？
データベースのライブラリには依存している．あとは自分が作ったmodelsにも依存している
この部分はライブラリaqlarchemyが，SQLによらない実装を可能にしてくれているのでデータベースの種類には直接しぞんしていない
'''

async def get_done(db: AsyncSession, task_id: int) -> Optional[task_model.Done]:
    '''
    DBからdoneを取得する
    arg: db: AsyncSession, task_id: int
    return: task_model.Done
    '''
    result: Result = await db.execute(
        select(task_model.Done).where(task_model.Done.task_id == task_id)
    )
    done: Optional[Tuple[task_model.Done]] = result.first()
    return done[0] if done is not None else None

async def create_done(db: AsyncSession, task_id: int) -> task_model.Done:
    '''
    DBにdoneを追加する
    arg: db: AsyncSession, task_id: int
    return: task_model.Done
    '''
    done = task_model.Done(task_id=task_id)
    db.add(done)
    await db.commit()
    await db.refresh(done)
    return done

async def delete_done(db: AsyncSession, original: task_model.Done) -> None:
    '''
    DBからdoneを削除する
    arg: db: AsyncSession, original: task_model.Done
    return: None
    '''
    await db.delete(original)
    await db.commit()