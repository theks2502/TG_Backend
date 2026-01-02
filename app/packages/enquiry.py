from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  
from app.utils.mail.enquiry_mail import send_enquiry_email
import shutil, os
# from fastapi import C
from fastapi import BackgroundTasks
from app.utils.invoice_generator import generate_invoice
from datetime import date

router = APIRouter()

@router.post("/enquiry", status_code=status.HTTP_201_CREATED)
async def create_enquiry_form(
    background_tasks: BackgroundTasks,

    full_name: str = Form(...),
    email_address: str = Form(...),
    contact_number: str = Form(...),

    category: str = Form(...),
    destination: str = Form(...),
    custom_destination: str = Form(None),
    additional_destination: str = Form(None),

    start_date: date = Form(...),

    adults: int = Form(...),
    children: int = Form(0),

    departure_city: str = Form(...),

    referral_source: str = Form(...),
    referral_other: str = Form(None),

    special_requests: str = Form(None),

    db: Session = Depends(get_db)
):
    # --------------------------
    # BASIC SANITY CHECKS
    # --------------------------
    if adults <= 0:
        raise HTTPException(
            status_code=400,
            detail="Adults must be greater than 0"
        )

    if children < 0:
        raise HTTPException(
            status_code=400,
            detail="Children cannot be negative"
        )

    # --------------------------
    # DATABASE ENTRY
    # --------------------------
    enquiry_entry = models.Enquiry_Form(
        full_name=full_name,
        email_address=email_address,
        contact_number=contact_number,

        category=category,
        destination=destination,
        custom_destination=custom_destination,
        additional_destination=additional_destination,

        start_date=start_date,
        adults=adults,
        children=children,

        departure_city=departure_city,

        referral_source=referral_source,
        referral_other=referral_other,

        special_requests=special_requests,
    )

    db.add(enquiry_entry)
    db.commit()
    db.refresh(enquiry_entry)

    # --------------------------
    # BACKGROUND TASKS
    # --------------------------
    background_tasks.add_task(send_enquiry_email, enquiry_entry)
    # background_tasks.add_task(send_user_email_enquiry, enquiry_entry)

    return {"message": "Enquiry submitted successfully"}
