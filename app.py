from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn
import json, os
from fastapi.responses import FileResponse

app = FastAPI(title="RestMe", version="0.1")

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    available: bool = True

# simple in-memory store
_db: Dict[int, Item] = {}
_next_id = 1

@app.get("/itemcollection")
async def read_root():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "itemcollection.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="itemcollection.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in itemcollection.json")
    return {"message": "Welcome to RestMe API"}

@app.get("/catalog/")
async def list_items():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "catalog", "catalog.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return (json.load(f) , {"Access-Control-Allow-Origin": "*"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="catalog.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in catalog.json")
    return {"message": "Welcome to RestMe API"}

@app.get("/collection")
async def get_items():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "collection", "collection.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return (json.load(f), {"Access-Control-Allow-Origin": "*"})
            #return FileResponse(file_path, media_type='application/json', filename='collection.json')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="collection.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in collection.json")
    return {"message": "Welcome to RestMe API"}

@app.get("/catalog/collection.json")
async def get_collection():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "collection", "collection.json")
        with open(file_path, "r", encoding="utf-8") as f:
            #return json.load(f)
            return FileResponse(file_path, media_type='application/json', filename='collection.json')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="collection.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in collection.json")
    return {"message": "Welcome to RestMe API"}


@app.get("/collection/{item_id:path}.json")
async def get_item_item(item_id: str):
    print(f"Requested item_id: {item_id}")
    try:
        file_path = os.path.join(os.path.dirname(__file__), "collection", f"{item_id.split('/')[0]}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            #return json.load(f)
            return FileResponse(file_path, media_type='application/json', filename=f'{item_id}.json')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"{item_id}.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {item_id}.json")
    return {"message": "Welcome to RestMe API"}





@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    global _next_id
    item.id = _next_id
    _db[_next_id] = item
    _next_id += 1
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = _db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated: Item):
    item = _db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated.id = item_id
    _db[item_id] = updated
    return updated

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item not found")
    del _db[item_id]

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)