from fastapi import FastAPI
import uvicorn
from fastapi.exceptions import HTTPException
from schemas import load_db, CarInput, save_db, CarOutput

app = FastAPI()

db = load_db()

@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list:
    result = db
    if size:
        result = [car for car in db if car.size == size]
    if doors:
        result = [car for car in db if car.doors >= doors]
    return result

@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    result = [car for car in db if car.id == id]
    if result:
        return result[0].model_dump()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}")

@app.post("/api/cars/")
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size = car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id = len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
