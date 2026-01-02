from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  
from app.utils.email_utills import  send_booking_email_rishikesh
import shutil, os
from fastapi import BackgroundTasks

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/rishikesh_haridwar" , status_code=status.HTTP_201_CREATED)
async def rishikesh_haridwar_package(background_tasks: BackgroundTasks , 
        full_name : str = Form(...) ,
        email_address: str = Form(...),
        age: int = Form(...),
        gender: str = Form(...),
        contact_number: str = Form(...),
        whatsapp_number: str = Form(...),
        college_name: str = Form(...),
        emergency_contact_number : str = Form(...),
        mode_of_transport : str = Form(...),
        proof_id_type : str = Form(...), 
        chosen_id_number : str = Form(...) ,
        medical_details: str = Form(...),
        special_request : str = Form(...) , 
        agree : bool = Form(...) ,
        id_image : UploadFile = File(None) , db:Session = Depends(get_db)
        ):

        file_location = None

        if id_image:
            file_name = f"{email_address}_payment_{id_image.filename}"
            file_location = os.path.join(UPLOAD_DIR, file_name)
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(id_image.file, buffer)

        details = models.Rishikesh_Haridwar(
            full_name=full_name,
            email_address=email_address,
            age=age,
            gender=gender,
            contact_number=contact_number,
            whatsapp_number=whatsapp_number , 
            emergency_contact_number = emergency_contact_number , 
            mode_of_transport = mode_of_transport , 
            college_name=college_name,
            proof_id_type= proof_id_type, 
            chosen_id_number= chosen_id_number , 
            special_request=special_request ,  
            
            medical_details=medical_details,
            agree=agree,
            id_image=file_location
    ) 

        db.add(details) 
        db.commit() 
        db.refresh(details)
        background_tasks.add_task(send_booking_email_rishikesh, details, file_location)

        return {"message" : "Payment Successful"}

        
