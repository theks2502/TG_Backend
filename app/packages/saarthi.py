from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  
from app.utils.email_utills import send_user_email_saarthi , send_admin_email_saarthi
from app.utils.supabase_uploads import upload_to_supabase
import shutil, os
from fastapi import BackgroundTasks
from datetime import date

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/saarthi", status_code=status.HTTP_201_CREATED)
async def create_saarthi_form(
    background_tasks: BackgroundTasks,
    full_name: str = Form(...),
    date_of_birthday: date = Form(...),
    gender: str = Form(...),
    aadhar_number: str = Form(...),
    email_address: str = Form(...),
    contact_number: str = Form(...),
    whatsapp_number: str = Form(...),
    current_city: str = Form(...),
    state: str = Form(...),
    address: str = Form(...),
    occupation: str = Form(...),
    organization_name: str = Form(...),
    job_role: str = Form(...),
    work_exp: str = Form(...),
    company_id: str = Form(None),
    profile_url: str = Form(...),
    role: str = Form(...),
    motive: str = Form(...),

    aadhar_card_image: UploadFile = File(None),
    profile_image: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    # --------------------------
    # FILE UPLOAD HANDLING
    # --------------------------

    aadhar_img_url = None
    profile_img_url = None

    
    if aadhar_card_image:
        aadhar_img_url = upload_to_supabase(aadhar_card_image, "aadhar")

    if profile_image:
        profile_img_url = upload_to_supabase(profile_image, "profile")
    # --------------------------
    # DATABASE ENTRY
    # --------------------------
    form_entry = models.Saarthi_Form(
        full_name=full_name,
        date_of_birthday=date_of_birthday,
        gender=gender,
        aadhar_number=aadhar_number,
        aadhar_card_image=aadhar_img_url,
        profile_image=profile_img_url,
        email_address=email_address,
        contact_number=contact_number,
        whatsapp_number=whatsapp_number,
        current_city=current_city,
        state=state,
        address=address,
        occupation=occupation,
        organization_name=organization_name,
        job_role=job_role,
        work_exp=work_exp,
        company_id=company_id,
        profile_url=profile_url,
        role=role,
        motive=motive
    )

    db.add(form_entry)
    db.commit()
    db.refresh(form_entry)

    background_tasks.add_task(send_admin_email_saarthi, form_entry)
    background_tasks.add_task(send_user_email_saarthi, form_entry)
    

    return {"message": "Form submitted successfully"}
