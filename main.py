from fastapi import FastAPI

app = FastAPI(
    title='my first FastAPI',
    description='ここに説明文が入る'
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.get("/calc/")
async def query_parameter(man: int, pin: int, sou: int, win_tile: int):
    return {"man": man, "pin": pin, "sou": sou, "win_tile": win_tile}
