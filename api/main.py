from fastapi import FastAPI
# fast api instance
'''

app = FastAPI()

# デコレータ
@app.get("/hello")
async def hello():
    return {"message": "hello world!"}
'''


from api.routers import task, done

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)