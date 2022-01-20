from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

f = open("config.json")
connection_data = json.load(f)
f.close()
SQLALCHEMY_DATABASE_URL = f"postgresql://{connection_data['user']}:{connection_data['password']}@{connection_data['host']}/{connection_data['database']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
