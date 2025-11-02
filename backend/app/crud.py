from sqlmodel import Session, select
from app.models import User, Sweet
from app.db import engine
from app.auth import hash_password

def get_sweet_by_id(sweet_id: int):
    """Fetch a single sweet by ID."""
    with Session(engine) as session:
        return session.get(Sweet, sweet_id)


# ---- USER OPERATIONS ----
def create_user(username: str, password: str, is_admin: bool = False):
    with Session(engine) as session:
        user = User(username=username, hashed_password=hash_password(password), is_admin=is_admin)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_username(username: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username)).first()

def get_user_by_id(user_id: int):
    with Session(engine) as session:
        return session.get(User, user_id)

# ---- SWEET OPERATIONS ----
def create_sweet(sweet_in):
    with Session(engine) as session:
        sweet = Sweet.from_orm(sweet_in)
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet

def list_sweets():
    with Session(engine) as session:
        return session.exec(select(Sweet)).all()

def get_sweet(sweet_id: int):
    with Session(engine) as session:
        return session.get(Sweet, sweet_id)

def update_sweet(sweet_id: int, sweet_in):
    with Session(engine) as session:
        sweet = session.get(Sweet, sweet_id)
        if not sweet:
            return None
        for key, value in sweet_in.dict(exclude_unset=True).items():
            setattr(sweet, key, value)
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet

def delete_sweet(sweet_id: int):
    with Session(engine) as session:
        sweet = session.get(Sweet, sweet_id)
        if sweet:
            session.delete(sweet)
            session.commit()

def purchase_sweet(sweet_id: int, qty: int):
    with Session(engine) as session:
        sweet = session.get(Sweet, sweet_id)
        if not sweet:
            raise ValueError("Sweet not found")
        if sweet.quantity < qty:
            raise ValueError("Not enough stock")
        sweet.quantity -= qty
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet


def restock_sweet(sweet_id: int, qty: int):
    with Session(engine) as session:
        sweet = session.get(Sweet, sweet_id)
        if not sweet:
            raise ValueError("Sweet not found")
        sweet.quantity += qty
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet

