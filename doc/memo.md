

RESTに従って、上記のTODOアプリを実現するのに必要な機能を整理する

- TODOリストを表示する
- TODOにタスクを追加する
- TODOのタスクの説明文を変更する
- TODOのタスク自体を削除する
- TODOタスクに「完了」フラグを立てる
- TODOタスクから「完了」フラグを外す

パスオペレーションについて↓
[FastAPIのパスオペレーションとデコレーターを理解する | kajiblo ITブログ](https://kajiblo.com/fastapi-path-opereation/)


routersには

TODOアプリの場合リソース？？は
todo, todo-doneであるから
/tasks
/tasks/{task_id}/done
の2つに大別される．

→
api/routers/task.py
api/routers/done.py
に分ける→
