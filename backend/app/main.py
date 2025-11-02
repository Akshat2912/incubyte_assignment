from fastapi import FastAPI, Depends, HTTPException, status
from app.db import init_db
from app import models, crud, auth, schemas
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Sweet Shop API")
init_db()

# -------------------- AUTH ENDPOINTS --------------------

@app.post("/api/auth/register", response_model=schemas.Token)
def register(user_in: schemas.UserCreate):
    if crud.get_user_by_username(user_in.username):
        raise HTTPException(status_code=400, detail="User exists")
    user = crud.create_user(user_in.username, user_in.password)
    token = auth.create_access_token(user.id)
    return {"access_token": token}


@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = auth.create_access_token(user.id)
    return {"access_token": token}


# -------------------- USER DEPENDENCY --------------------

from fastapi import Security

def get_current_user(token: str = Depends(auth.oauth2_scheme)):
    user_id = auth.decode_token(token)
    user = crud.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user


# -------------------- SWEET ENDPOINTS --------------------

@app.post("/api/sweets/", response_model=schemas.SweetRead)
def add_sweet(sweet_in: schemas.SweetCreate, current_user=Depends(get_current_user)):
    # Ensure category has a default if missing
    if not sweet_in.category:
        sweet_in.category = "Uncategorized"
    return crud.create_sweet(sweet_in)


@app.get("/api/sweets/", response_model=list[schemas.SweetRead])
def get_sweets():
    return crud.list_sweets()


@app.get("/api/sweets/search")
def search_sweets(q: str = "", min_price: float | None = None, max_price: float | None = None):
    return crud.search_sweets(q, min_price, max_price)


@app.put("/api/sweets/{sweet_id}", response_model=schemas.SweetRead)
def update_sweet(sweet_id: int, sweet_in: schemas.SweetUpdate, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return crud.update_sweet(sweet_id, sweet_in)


@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(sweet_id: int, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    crud.delete_sweet(sweet_id)
    return {"status": "deleted"}


# -------------------- PURCHASE SWEET --------------------

@app.post("/api/sweets/{sweet_id}/purchase")
def purchase(sweet_id: int, data: dict, current_user=Depends(get_current_user)):
    qty = data.get("qty", 1)
    sweet = crud.get_sweet_by_id(sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if sweet.quantity < qty:
        raise HTTPException(status_code=400, detail="Insufficient stock available")

    updated_sweet = crud.purchase_sweet(sweet_id, qty)
    return updated_sweet


# -------------------- RESTOCK SWEET --------------------

@app.post("/api/sweets/{sweet_id}/restock")
def restock(sweet_id: int, data: dict, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    qty = data.get("qty")
    if qty is None or qty <= 0:
        raise HTTPException(status_code=422, detail="Invalid restock quantity")

    updated_sweet = crud.restock_sweet(sweet_id, qty)
    return updated_sweet
