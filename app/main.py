from fastapi import FastAPI, HTTPException
import asyncio
from pydantic import BaseModel

app = FastAPI()
store = {}
store_lock = asyncio.Lock()

class Item(BaseModel):
    key: str
    value: str

@app.post("/api/v1/store", status_code=201)
async def set_item(item: Item):
    store[item.key] = item.value
    return {"message": "Item set successfully"}
@app.get("/api/v1/store/{key}")
async def get_item(key: str):
    if key not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"key": key, "value": store[key]}
