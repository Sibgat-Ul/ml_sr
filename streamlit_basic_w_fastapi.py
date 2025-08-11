import streamlit as sr
import requests

sr.title("Shopping cart with Streamlit")

item_name = sr.text_input("Item Name")
item_price = sr.number_input("Item Price", min_value=0.0, format="%.2f")
item_description = sr.text_area("Item Description")

if sr.button("Get All Items"):
    response = requests.get("http://localhost:8001/all_items/")
    if response.status_code == 200:
        items = response.json().get("items", [])
        sr.write("All Items:")
        for item in items:
            sr.write(item)
    else:
        sr.error("Failed to fetch items.")

if sr.button("Add to Cart"):
    if not item_name or item_price < 0:
        sr.error("Please provide valid item details.")
    else:
        item_data = {
            "name": item_name,
            "price": item_price,
            "description": item_description
        }
        response = requests.post("http://localhost:8001/items/", json=item_data)
        
        if response.status_code == 200:
            sr.success("Item added to cart!")
        else:
            sr.error("Failed to add item to cart.")