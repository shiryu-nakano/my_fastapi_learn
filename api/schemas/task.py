from typing import Optional

from pydantic import BaseModel, Field

'''
class Task(BaseModel):
    id: int
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    done: bool = Field(False, description="完了フラグ")

'''

"""
ここでは、Taskモデルの定義を行った．ROUTERで使用される
"""

"""
class TaskCreate(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    
    #タスクの作成時に使用されるモデル
    
    
"""
'''
ここまでで，二つのスキーマはベースとなるスキーマを継承することで実装できることがわかる
タスクもタスク作成も，titleを持っているので，継承することでコードの重複を避けることができる
'''

class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    

class Task(TaskBase):
    id: int
    #title : Optional[str] = Field(None, example="クリーニングを取りに行く")
    done: bool = Field(False, description="完了フラグ")
    class Config:
        orm_mode = True
    

class TaskCreate(TaskBase):
    #title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True



"""
ここで、 orm_mode = True は、このレスポンススキーマ TaskCreateResponse が、
暗黙的にORMを受け取り、レスポンススキーマに変換することを意味するよ
"""