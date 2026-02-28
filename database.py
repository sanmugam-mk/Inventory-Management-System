import os
from dotenv import load_dotenv
load_dotenv()


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
