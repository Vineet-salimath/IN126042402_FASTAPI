from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Product Database
# -----------------------------
products = {
    1: {"name": "Wireless Mouse", "price": 499, "in_stock": True},
    2: {"name": "Notebook", "price": 99, "in_stock": True},
    3: {"name": "USB Hub", "price": 299, "in_stock": False},
    4: {"name": "Pen Set", "price": 49, "in_stock": True}
}

# -----------------------------
# In-memory storage
# -----------------------------
cart = []
orders = []
order_counter = 1


# -----------------------------
# Checkout Model
# -----------------------------
class Checkout(BaseModel):
    customer_name: str
    delivery_address: str


# -----------------------------
# Helper Function
# -----------------------------
def calculate_total(product, quantity):
    return product["price"] * quantity


# -----------------------------
# Add Item to Cart
# -----------------------------
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if not product["in_stock"]:
        raise HTTPException(
            status_code=400,
            detail=f"{product['name']} is out of stock"
        )

    # check if item already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])

            return {
                "message": "Cart updated",
                "cart_item": item
            }

    subtotal = calculate_total(product, quantity)

    cart_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": subtotal
    }

    cart.append(cart_item)

    return {
        "message": "Added to cart",
        "cart_item": cart_item
    }


# -----------------------------
# View Cart
# -----------------------------
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# -----------------------------
# Remove Item
# -----------------------------
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# -----------------------------
# Checkout
# -----------------------------
@app.post("/cart/checkout")
def checkout(order: Checkout):

    global order_counter

    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty — add items first"
        )

    new_orders = []

    for item in cart:

        new_order = {
            "order_id": order_counter,
            "customer_name": order.customer_name,
            "delivery_address": order.delivery_address,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }

        orders.append(new_order)
        new_orders.append(new_order)

        order_counter += 1

    cart.clear()

    grand_total = sum(o["total_price"] for o in new_orders)

    return {
        "message": "Order placed successfully",
        "orders_placed": new_orders,
        "grand_total": grand_total
    }


# -----------------------------
# View Orders
# -----------------------------
@app.get("/orders")
def get_orders():

    return {
        "orders": orders,
        "total_orders": len(orders)
    }
