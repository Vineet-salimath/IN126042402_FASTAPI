from fastapi import FastAPI, Response, status, Query

app = FastAPI()

# Initial products list
products = [
    {"id": 1, "name": "Keyboard", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]


# Helper function
def find_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# Root endpoint
@app.get("/")
def home():
    return {"message": "FastAPI Product Inventory API Running"}


# Get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total_products": len(products)
    }


# Add product
@app.post("/products", status_code=201)
def add_product(product: dict, response: Response):

    # Check duplicate name
    for p in products:
        if p["name"].lower() == product["name"].lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product with this name already exists"}

    next_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": next_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "in_stock": product.get("in_stock", True)
    }

    products.append(new_product)

    return {
        "message": "Product added successfully",
        "product": new_product
    }


# UPDATE PRODUCT
@app.put("/products/{product_id}")
def update_product(
        product_id: int,
        price: int | None = None,
        in_stock: bool | None = None,
        response: Response = None):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated successfully",
        "product": product
    }


# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {"message": f"Product '{product['name']}' deleted successfully"}


# QUESTION 5 ENDPOINT
@app.get("/products/audit")
def product_audit():

    in_stock_products = [p for p in products if p["in_stock"]]
    out_of_stock_products = [p for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": [p["name"] for p in out_of_stock_products],
        "total_stock_value": total_stock_value,
        "most_expensive_product": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }


# BONUS QUESTION (optional)
@app.put("/products/discount")
def apply_discount(category: str, discount_percent: float):

    updated = 0

    for p in products:
        if p["category"].lower() == category.lower():
            new_price = int(p["price"] * (1 - discount_percent / 100))
            p["price"] = new_price
            updated += 1

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_products": updated
    }


# GET PRODUCT BY ID (must stay below /products/audit)
@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    return product
