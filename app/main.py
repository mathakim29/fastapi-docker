from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# PostgreSQL connection
DATABASE_URL = "postgresql+psycopg://myuser:mypassword@postgres_db:5432/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# Database model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)


Base.metadata.create_all(bind=engine)


# Request schema
class UserCreate(BaseModel):
    name: str
    email: str


app = FastAPI()


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# READ
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# UPDATE
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return {"message": "User not found"}

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return {"message": "User not found"}

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted"}