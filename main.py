from fastapi import Depends, FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import database_models
from models import Product
from database import session,engine
import database_models #from database_models import Base
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"],
)

# Creating database tables
database_models.Base.metadata.create_all(bind=engine)


products_list = [
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=499.99, quantity=20),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    Product(id=4, name="Smartwatch", description="A smartwatch with various features",
                price=299.99, quantity=5),
    Product(id=5, name="Tablet", description="A lightweight tablet for work and play",
                price=399.99, quantity=8)
]

@app.get("/")
def greet():
    return "Hello from Sanmugam"

# Instead of creating a new session in each endpoint, we can use a dependency to get a database session
def get_db(): # Dependency function to get a database session
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products_list:
            db.add(database_models.Product(**product.model_dump())) # Use ** to unpack the dictionary
        db.commit()
init_db()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post("/products")
def add_product(product : Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # To check whether the product with the given id exists in the database.
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    else:
        return "Product no found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "Product not found"