from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  

from app.packages import manali , tamia , rishikesh , saarthi , odt , enquiry , hiring , vr_darshan , vr_admin_action
from app.utils import qr
import shutil, os
from fastapi import BackgroundTasks

models.Base.metadata.create_all(bind=engine) 


origins = ["*"]
app = FastAPI()


UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("uploads/aadhar", exist_ok=True)
os.makedirs("uploads/profile", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(manali.router)
app.include_router(tamia.router)
app.include_router(rishikesh.router)
app.include_router(saarthi.router)
app.include_router(odt.router)
app.include_router(enquiry.router)
app.include_router(hiring.router)
app.include_router(vr_darshan.router)
app.include_router(vr_admin_action.router)
app.include_router(qr.router)



@app.get("/")
async def root():
    return {"message" : "Hello Tirthghumo"}