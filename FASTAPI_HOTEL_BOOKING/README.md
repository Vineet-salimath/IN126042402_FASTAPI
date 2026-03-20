# 🏨 Grand Stay Hotel — Room Booking System

> **Luxury Rooms. Seamless Bookings. Unforgettable Experiences.**

A fully functional **Hotel Room Booking REST API** built with **FastAPI** as the Final Project for the Innomatics Research Labs FastAPI Internship.

---

## 📌 Project Overview

This backend API simulates a real-world hotel room booking system where guests can browse rooms, make bookings, check in, check out, and hotel staff can manage the entire room inventory — all through clean, validated REST API endpoints.

---

## 🚀 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Programming Language |
| FastAPI | Web Framework |
| Pydantic | Request Validation |
| Uvicorn | ASGI Server |
| Swagger UI | API Testing (built-in at `/docs`) |

---

## 📁 Project Structure

```
fastapi-hotel-booking/
│
├── main.py              ← All API endpoints and logic
├── requirements.txt     ← Dependencies
├── README.md            ← Project documentation
└── screenshots/         ← Swagger UI test screenshots (Q1–Q20)
```

---

## ⚙️ How to Run

**Step 1 — Clone the repository**
```bash
git clone https://github.com/your-username/fastapi-hotel-booking.git
cd fastapi-hotel-booking
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Start the server**
```bash
uvicorn main:app --reload
```

**Step 4 — Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## 📚 Concepts Covered (Day 1 – Day 6)

### ✅ Day 1 — GET Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /` | Welcome message and API status |
| `GET /rooms` | List all rooms with total and available count |
| `GET /rooms/{room_id}` | Get a specific room by ID |
| `GET /rooms/summary` | Summary — totals, price range, breakdown by type |
| `GET /bookings` | List all bookings |

### ✅ Day 2 — POST + Pydantic Validation
| Endpoint | Description |
|----------|-------------|
| `POST /bookings` | Create a booking with full request body validation |
| `POST /rooms` | Add a new room with duplicate check |

**Pydantic Rules enforced:**
- `guest_name` — min 2 characters
- `nights` — must be between 1 and 30
- `phone` — minimum 10 digits
- `room_id` — must be greater than 0

### ✅ Day 3 — Helper Functions + Filtering
**Helper functions (no `@app` decorator):**
- `find_room(room_id)` — find a room by ID
- `find_booking(booking_id)` — find a booking by ID
- `calculate_stay_cost(price, nights, meal_plan, early_checkout)` — full cost breakdown
- `filter_rooms_logic(type, max_price, floor, is_available)` — apply optional filters

| Endpoint | Description |
|----------|-------------|
| `GET /rooms/filter` | Filter rooms by type, max price, floor, availability |

### ✅ Day 4 — CRUD Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `POST /rooms` | CREATE | Add new room — returns 201 Created |
| `PUT /rooms/{room_id}` | UPDATE | Update price or availability — returns 404 if not found |
| `DELETE /rooms/{room_id}` | DELETE | Delete room — blocked if room is occupied |

### ✅ Day 5 — Multi-Step Workflow
3-step connected workflow:

```
POST /bookings → POST /checkin/{id} → POST /checkout/{id}
     ↓                   ↓                    ↓
  confirmed          checked_in           checked_out
                                       (room freed up)
```

| Endpoint | Description |
|----------|-------------|
| `POST /checkin/{booking_id}` | Check in a confirmed guest |
| `POST /checkout/{booking_id}` | Check out — room becomes available again |
| `GET /bookings/active` | View only confirmed or checked-in bookings |

### ✅ Day 6 — Search, Sort, Pagination
| Endpoint | Description |
|----------|-------------|
| `GET /rooms/search` | Search rooms by keyword across room_number and type |
| `GET /rooms/sort` | Sort rooms by price_per_night, floor, or type |
| `GET /rooms/page` | Paginate rooms with page and limit params |
| `GET /bookings/search` | Search bookings by guest name (case-insensitive) |
| `GET /bookings/sort` | Sort bookings by total_cost or nights |
| `GET /rooms/browse` | Combined — search + sort + paginate in one endpoint |

---

## 🏨 Room Data

| Room | Type | Floor | Price/Night |
|------|------|-------|-------------|
| 101 | Single | 1 | ₹1,500 |
| 102 | Double | 1 | ₹2,500 |
| 201 | Suite | 2 | ₹5,000 |
| 202 | Deluxe | 2 | ₹3,500 |
| 301 | Single | 3 | ₹1,800 |
| 302 | Double | 3 | ₹2,800 |
| 401 | Suite | 4 | ₹6,000 |
| 402 | Deluxe | 4 | ₹4,000 |

---

## 💰 Pricing Logic

| Meal Plan | Extra Charge |
|-----------|-------------|
| None | ₹0 |
| Breakfast | ₹500/night |
| All-Inclusive | ₹1,200/night |

| Condition | Discount |
|-----------|---------|
| Early Checkout | 10% off total |

---

## 📸 API Testing Screenshots

All 20 questions tested and screenshotted in Swagger UI.
Screenshots available in the `/screenshots` folder.

| Question | Concept | Endpoint |
|----------|---------|----------|
| Q1 | Home Route | `GET /` |
| Q2 | List All | `GET /rooms` |
| Q3 | Get by ID | `GET /rooms/{id}` |
| Q4 | List Bookings | `GET /bookings` |
| Q5 | Summary | `GET /rooms/summary` |
| Q6 | Pydantic Validation | `POST /bookings` |
| Q7 | Helper Functions | Code screenshot |
| Q8 | POST with Helpers | `POST /bookings` |
| Q9 | Early Checkout Discount | `POST /bookings` |
| Q10 | Filter | `GET /rooms/filter` |
| Q11 | CREATE | `POST /rooms` |
| Q12 | UPDATE | `PUT /rooms/{id}` |
| Q13 | DELETE | `DELETE /rooms/{id}` |
| Q14 | Check-In Workflow | `POST /checkin/{id}` |
| Q15 | Check-Out + Active | `POST /checkout/{id}` |
| Q16 | Search | `GET /rooms/search` |
| Q17 | Sort | `GET /rooms/sort` |
| Q18 | Pagination | `GET /rooms/page` |
| Q19 | Search + Sort Bookings | `GET /bookings/search` |
| Q20 | Combined Browse | `GET /rooms/browse` |

---

## 🔑 Key API Rules Followed

- ✅ All fixed routes placed **above** variable `/{id}` routes
- ✅ No duplicate route names or function names
- ✅ Helper functions have **no** `@app` decorator
- ✅ All filters use `is not None` checks
- ✅ Pagination uses ceiling division for `total_pages`
- ✅ Duplicate checks on POST (room number, booking conflicts)
- ✅ Business logic guards on DELETE (cannot delete occupied room)

---

## 👨‍💻 Author

Built as part of the **FastAPI Internship Final Project**
**Innomatics Research Labs**


