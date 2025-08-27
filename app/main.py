from fastapi import FastAPI, HTTPException

app = FastAPI()

store = {}

@app.post("/api/v1/store")
async def set_item(key: str, value: str):
    store[key] = value
    return {"message": "Item set successfully"}
app.get("/api/v1/store")
async def get_item(key: str):
    if key not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"key": key, "value": store[key]}
