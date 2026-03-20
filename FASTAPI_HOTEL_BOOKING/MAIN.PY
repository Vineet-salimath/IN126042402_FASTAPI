from fastapi import FastAPI, Query, Response

app = FastAPI(
    title="🏨 Grand Stay Hotel — Room Booking System",
    version="1.0.0"
)

# ============================================================
# DATA STORE
# ============================================================

rooms = [
    {"id": 1, "room_number": "101", "type": "Single",  "price_per_night": 1500, "floor": 1, "is_available": True},
    {"id": 2, "room_number": "102", "type": "Double",  "price_per_night": 2500, "floor": 1, "is_available": True},
    {"id": 3, "room_number": "201", "type": "Suite",   "price_per_night": 5000, "floor": 2, "is_available": True},
    {"id": 4, "room_number": "202", "type": "Deluxe",  "price_per_night": 3500, "floor": 2, "is_available": True},
    {"id": 5, "room_number": "301", "type": "Single",  "price_per_night": 1800, "floor": 3, "is_available": True},
    {"id": 6, "room_number": "302", "type": "Double",  "price_per_night": 2800, "floor": 3, "is_available": True},
    {"id": 7, "room_number": "401", "type": "Suite",   "price_per_night": 6000, "floor": 4, "is_available": True},
    {"id": 8, "room_number": "402", "type": "Deluxe",  "price_per_night": 4000, "floor": 4, "is_available": True},
]

bookings = []
booking_counter = 1
room_counter = 9   # next new room id


# ============================================================
# DAY 3 — HELPER FUNCTIONS  (no @app decorator)
# ============================================================

def find_room(room_id: int):
    """Return room dict or None."""
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None


def find_booking(booking_id: int):
    """Return booking dict or None."""
    for b in bookings:
        if b["booking_id"] == booking_id:
            return b
    return None


def calculate_stay_cost(price_per_night: int, nights: int,
                         meal_plan: str, early_checkout: bool = False):
    """
    Calculate total stay cost.
    Meal plans  : 'none' → no add-on
                  'breakfast' → +500/night
                  'all-inclusive' → +1200/night
    Early checkout: 10% discount on total.
    Returns dict with breakdown.
    """
    meal_charge = 0
    if meal_plan == "breakfast":
        meal_charge = 500 * nights
    elif meal_plan == "all-inclusive":
        meal_charge = 1200 * nights

    subtotal = (price_per_night * nights) + meal_charge
    discount = 0
    if early_checkout:
        discount = round(subtotal * 0.10)

    total = subtotal - discount
    return {
        "room_cost": price_per_night * nights,
        "meal_charge": meal_charge,
        "subtotal": subtotal,
        "early_checkout_discount": discount,
        "total_cost": total
    }


def filter_rooms_logic(type: str = None, max_price: int = None,
                        floor: int = None, is_available: bool = None):
    """Apply optional filters to rooms list."""
    result = rooms[:]
    if type is not None:
        result = [r for r in result if r["type"].lower() == type.lower()]
    if max_price is not None:
        result = [r for r in result if r["price_per_night"] <= max_price]
    if floor is not None:
        result = [r for r in result if r["floor"] == floor]
    if is_available is not None:
        result = [r for r in result if r["is_available"] == is_available]
    return result


# ============================================================
# DAY 2 — PYDANTIC MODELS
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, List


class BookingRequest(BaseModel):
    guest_name:     str  = Field(..., min_length=2)
    room_id:        int  = Field(..., gt=0)
    nights:         int  = Field(..., gt=0, le=30)
    phone:          str  = Field(..., min_length=10)
    meal_plan:      str  = Field(default="none")          # none / breakfast / all-inclusive
    early_checkout: bool = Field(default=False)


class NewRoom(BaseModel):
    room_number:     str = Field(..., min_length=1)
    type:            str = Field(..., min_length=2)
    price_per_night: int = Field(..., gt=0)
    floor:           int = Field(..., gt=0)
    is_available:    bool = Field(default=True)


class CheckinRequest(BaseModel):
    pass   # booking_id comes from path; no extra body needed


# ============================================================
# DAY 1 — GET ENDPOINTS
# ============================================================

# Q1 — Home route
@app.get("/")
def home():
    return {
        "message" : "Welcome to Grand Stay Hotel — Where Every Stay Becomes a Story",
        "tagline" : "Luxury Rooms. Seamless Bookings. Unforgettable Experiences.",
        "version" : "1.0.0",
        "docs"    : "Visit /docs to explore all available endpoints",
        "status"  : "API is live and running"
    }


# Q2 — List all rooms
@app.get("/rooms")
def get_all_rooms():
    available = [r for r in rooms if r["is_available"]]
    return {
        "total": len(rooms),
        "available_count": len(available),
        "rooms": rooms
    }


# Q4 — List all bookings
@app.get("/bookings")
def get_all_bookings():
    return {
        "total": len(bookings),
        "bookings": bookings
    }


# ---- FIXED routes must come BEFORE /{room_id} ----

# Q5 — Summary (fixed route above variable route)
@app.get("/rooms/summary")
def rooms_summary():
    prices = [r["price_per_night"] for r in rooms]
    type_counts = {}
    for r in rooms:
        type_counts[r["type"]] = type_counts.get(r["type"], 0) + 1

    return {
        "total_rooms": len(rooms),
        "available_count": sum(1 for r in rooms if r["is_available"]),
        "occupied_count": sum(1 for r in rooms if not r["is_available"]),
        "cheapest_price": min(prices),
        "most_expensive_price": max(prices),
        "rooms_by_type": type_counts
    }


# Q10 — Filter rooms (fixed route)
@app.get("/rooms/filter")
def filter_rooms(
    type:         str  = Query(default=None),
    max_price:    int  = Query(default=None),
    floor:        int  = Query(default=None),
    is_available: bool = Query(default=None)
):
    result = filter_rooms_logic(type, max_price, floor, is_available)
    return {"total": len(result), "rooms": result}


# Q16 — Search rooms (fixed route)
@app.get("/rooms/search")
def search_rooms(keyword: str = Query(...)):
    kw = keyword.lower()
    result = [
        r for r in rooms
        if kw in r["room_number"].lower() or kw in r["type"].lower()
    ]
    if not result:
        return {"message": f"No rooms found matching '{keyword}'", "total_found": 0}
    return {"total_found": len(result), "rooms": result}


# Q17 — Sort rooms (fixed route)
@app.get("/rooms/sort")
def sort_rooms(
    sort_by: str = Query(default="price_per_night"),
    order:   str = Query(default="asc")
):
    valid_sort = ["price_per_night", "floor", "type"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort:
        return {"error": f"sort_by must be one of {valid_sort}"}
    if order not in valid_order:
        return {"error": f"order must be one of {valid_order}"}
    sorted_rooms = sorted(rooms, key=lambda r: r[sort_by], reverse=(order == "desc"))
    return {"sort_by": sort_by, "order": order, "rooms": sorted_rooms}


# Q18 — Paginate rooms (fixed route)
@app.get("/rooms/page")
def paginate_rooms(
    page:  int = Query(default=1, ge=1),
    limit: int = Query(default=2, ge=1, le=10)
):
    total = len(rooms)
    import math
    total_pages = math.ceil(total / limit)
    start = (page - 1) * limit
    result = rooms[start: start + limit]
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "rooms": result
    }


# Q20 — Browse (combined search + sort + paginate) — fixed route
@app.get("/rooms/browse")
def browse_rooms(
    keyword:  str  = Query(default=None),
    sort_by:  str  = Query(default="price_per_night"),
    order:    str  = Query(default="asc"),
    page:     int  = Query(default=1, ge=1),
    limit:    int  = Query(default=3, ge=1, le=10)
):
    import math
    valid_sort  = ["price_per_night", "floor", "type"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort:
        return {"error": f"sort_by must be one of {valid_sort}"}
    if order not in valid_order:
        return {"error": f"order must be one of {valid_order}"}

    # Step 1 — filter by keyword
    if keyword:
        kw = keyword.lower()
        result = [
            r for r in rooms
            if kw in r["room_number"].lower() or kw in r["type"].lower()
        ]
    else:
        result = rooms[:]

    # Step 2 — sort
    result = sorted(result, key=lambda r: r[sort_by], reverse=(order == "desc"))

    # Step 3 — paginate
    total = len(result)
    total_pages = math.ceil(total / limit) if total else 1
    start = (page - 1) * limit
    page_result = result[start: start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_filtered": total,
        "total_pages": total_pages,
        "rooms": page_result
    }


# Q3 — Get room by ID (variable route — MUST be below all fixed /rooms/... routes)
@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    room = find_room(room_id)
    if not room:
        return {"error": "Room not found"}
    return room


# ============================================================
# BOOKINGS — fixed routes above variable routes
# ============================================================

# Q15 — Active bookings (fixed route)
@app.get("/bookings/active")
def get_active_bookings():
    active = [b for b in bookings if b["status"] in ("confirmed", "checked_in")]
    return {"total": len(active), "bookings": active}


# Q19 — Search bookings (fixed route)
@app.get("/bookings/search")
def search_bookings(guest_name: str = Query(...)):
    result = [
        b for b in bookings
        if guest_name.lower() in b["guest_name"].lower()
    ]
    return {"total_found": len(result), "bookings": result}


# Q19 — Sort bookings (fixed route)
@app.get("/bookings/sort")
def sort_bookings(
    sort_by: str = Query(default="total_cost"),
    order:   str = Query(default="asc")
):
    valid_sort  = ["total_cost", "nights"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort:
        return {"error": f"sort_by must be one of {valid_sort}"}
    if order not in valid_order:
        return {"error": f"order must be one of {valid_order}"}
    sorted_b = sorted(bookings, key=lambda b: b[sort_by], reverse=(order == "desc"))
    return {"sort_by": sort_by, "order": order, "bookings": sorted_b}


# ============================================================
# DAY 2 + 3 — POST /bookings  (Q8 + Q9)
# ============================================================

@app.post("/bookings")
def create_booking(req: BookingRequest, response: Response):
    global booking_counter

    # Check room exists
    room = find_room(req.room_id)
    if not room:
        return {"error": "Room not found"}

    # Check availability
    if not room["is_available"]:
        return {"error": f"Room {room['room_number']} is currently occupied"}

    # Validate meal plan
    valid_meals = ["none", "breakfast", "all-inclusive"]
    if req.meal_plan not in valid_meals:
        return {"error": f"meal_plan must be one of {valid_meals}"}

    # Calculate cost
    cost = calculate_stay_cost(
        room["price_per_night"], req.nights, req.meal_plan, req.early_checkout
    )

    # Mark room unavailable
    room["is_available"] = False

    # Create booking record
    booking = {
        "booking_id":   booking_counter,
        "guest_name":   req.guest_name,
        "phone":        req.phone,
        "room_number":  room["room_number"],
        "room_type":    room["type"],
        "floor":        room["floor"],
        "nights":       req.nights,
        "meal_plan":    req.meal_plan,
        "early_checkout": req.early_checkout,
        **cost,
        "status":       "confirmed"
    }
    bookings.append(booking)
    booking_counter += 1

    response.status_code = 201
    return {"message": "Booking confirmed!", "booking": booking}


# ============================================================
# DAY 4 — CRUD: POST, PUT, DELETE rooms  (Q11, Q12, Q13)
# ============================================================

# Q11 — Add new room
@app.post("/rooms")
def add_room(req: NewRoom, response: Response):
    global room_counter

    # Duplicate room number check
    for r in rooms:
        if r["room_number"] == req.room_number:
            return {"error": f"Room number {req.room_number} already exists"}

    new_room = {
        "id":             room_counter,
        "room_number":    req.room_number,
        "type":           req.type,
        "price_per_night": req.price_per_night,
        "floor":          req.floor,
        "is_available":   req.is_available
    }
    rooms.append(new_room)
    room_counter += 1
    response.status_code = 201
    return {"message": "Room added successfully", "room": new_room}


# Q12 — Update room
@app.put("/rooms/{room_id}")
def update_room(
    room_id:        int,
    price_per_night: int  = Query(default=None),
    is_available:   bool  = Query(default=None)
):
    room = find_room(room_id)
    if not room:
        return {"error": "Room not found"}

    if price_per_night is not None:
        room["price_per_night"] = price_per_night
    if is_available is not None:
        room["is_available"] = is_available

    return {"message": "Room updated", "room": room}


# Q13 — Delete room
@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    room = find_room(room_id)
    if not room:
        return {"error": "Room not found"}
    if not room["is_available"]:
        return {"error": f"Cannot delete Room {room['room_number']} — it is currently occupied"}

    rooms.remove(room)
    return {"message": f"Room {room['room_number']} deleted successfully"}


# ============================================================
# DAY 5 — MULTI-STEP WORKFLOW  (Q14, Q15)
# ============================================================

# Q14 — Check-in
@app.post("/checkin/{booking_id}")
def check_in(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        return {"error": "Booking not found"}
    if booking["status"] != "confirmed":
        return {"error": f"Cannot check-in — booking status is '{booking['status']}'"}

    booking["status"] = "checked_in"
    return {"message": "Guest checked in successfully", "booking": booking}


# Q15 — Check-out
@app.post("/checkout/{booking_id}")
def check_out(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        return {"error": "Booking not found"}
    if booking["status"] != "checked_in":
        return {"error": f"Cannot check-out — booking status is '{booking['status']}'"}

    booking["status"] = "checked_out"

    # Free up the room
    for room in rooms:
        if room["room_number"] == booking["room_number"]:
            room["is_available"] = True
            break

    return {"message": "Guest checked out — room is now available", "booking": booking}


# ============================================================
# END OF FILE
# ============================================================
