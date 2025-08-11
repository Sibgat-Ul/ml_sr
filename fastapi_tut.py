from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

all_items = []

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI tutorial!"}

@app.post("/items/")
def create_item(item: Item):
    all_items.append(item)
    return {"message": "Item created successfully!", "item": item}

@app.get("/all_items/")
def get_all_items():
    return {"items": all_items}

@app.get("/items/{item_name}")
def get_item(item_name: str):
    for item in all_items:
        if item.name == item_name:
            return {"item": item}
    raise HTTPException(status_code=404, detail="Item not found")


# class notPydanticItem:
#     def __init__(self, name: str, price: float, description: str = None):
#         self.name = name
#         self.price = price
#         self.description = description

# @app.get("/not_pydantic_items/")
# def get_not_pydantic_items():
#     return {"items": [item.__dict__ for item in all_items if not isinstance(item, Item)]}

# @app.post("/not_pydantic_items/")
# def create_not_pydantic_item(json_file):
#     name = json_file.get("name")
#     price = json_file.get("price")
#     description = json_file.get("description")

#     item = notPydanticItem(name=name, price=price, description=description)
#     all_items.append(item)
#     return {"message": "Item created successfully!", "item": item.__dict__}