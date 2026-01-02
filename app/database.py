from sqlalchemy import create_engine
from sqlalchemy .ext.declarative import declarative_base
from sqlalchemy .orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:lcp43GPPDKQP70Dr@db.vjzhoxjydrkueduwivsu.supabase.co:5432/postgres"
SQLALCHEMY_DATABASE_URL = settings.database_url
        

engine = create_engine(SQLALCHEMY_DATABASE_URL ,connect_args={"sslmode": "require"},  pool_pre_ping=True,    
    pool_recycle=1800 , pool_size=5, max_overflow=2 )

SessionLocal = sessionmaker(autocommit=False, autoflush = False , bind = engine)

Base = declarative_base()

while True :
    try:
        # conn = psycopg2.connect( host=settings.database_hostname,  database=settings.database_name, user=settings.database_username, password=settings.database_password,cursor_factory=RealDictCursor)    
        conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful !")
        break
    except Exception as error:
        print("Database connection failed ")
        print("Error :" , error)
        time.sleep(2)

# while True :
#     try:
          
#         conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful !")
#         break
#     except Exception as error:
#         print("Database connection failed ")
#         print("Error :" , error)
#         time.sleep(2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
