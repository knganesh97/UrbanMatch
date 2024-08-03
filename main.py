from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, maxInterests
import models, schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = models.User(**user.model_dump(exclude={'interests'}))
    user_interests = user.model_dump(include={'interests', 'id'})
    interests = user_interests['interests']
    user_id = user_interests['id']
    db_interests = db_interests_format(interests, user_id)
    
    db.add_all(db_interests)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users_list = db.query(models.User).offset(skip).limit(limit).all()
    return db_users_list

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    updated_user = models.User(**user.model_dump(exclude={'interests'}, exclude_unset=True))
    updated_interests = user.model_dump(include={'interests'})
    db_interests_updated = db_interests_format(interests=updated_interests['interests'], user_id=user_id)

    db_user.name = updated_user.name
    db_user.age = updated_user.age
    db_user.city = updated_user.city
    db_user.email = updated_user.email
    db_user.gender = updated_user.gender
    
    db.query(models.Interest).filter(models.Interest.user_id == user_id).delete()
    db.commit()
    db.add_all(db_interests_updated)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.get("/interests/", response_model=list[schemas.Interest])
def read_interests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_interests_list = db.query(models.Interest).offset(skip).limit(limit).all()
    return db_interests_list

def db_interests_format(interests: list[str], user_id: int):
    db_interests = []

    for i in range(len(interests)):
        interest = schemas.InterestCreate(hobby=interests[i], user_id=user_id, id=(user_id*maxInterests)-i)
        db_interest = models.Interest(**interest.model_dump())
        db_interests.append(db_interest)
    
    return db_interests

# @app.get("/matches/{user_id}", response_model=list[schemas.UserResponse])
# def find_matches(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user_interests = db.query(models.Interest).filter(models.Interest.user_id == user_id).all()
    # db_same_city_users = db.query(models.User).filter(models.User.city == db_user.city, models.User.gender != db_user.gender, models.User.id != db_user.id).all()

    # same_city_user_ids = []
    # for db_same_city_user in db_same_city_users:
    #     same_city_user_ids.append(db_same_city_user.id)

    db_user_hobbies = []
    for db_user_interest in db_user_interests:
        db_user_hobbies.append(db_user_interest.hobby)
    
    db_matches = db.query(models.User).filter(
        models.User.id != user_id,
        models.User.city == db_user.city,
        models.User.gender != db_user.gender
    )