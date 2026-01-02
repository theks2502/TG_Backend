from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  
from app.utils.mail.odt_mail import send_booking_email , send_email_with_invoice , send_booking_declined_email
import shutil, os
from fastapi import BackgroundTasks
from app.utils.invoice_generator import generate_invoice


router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/odt_booking" , status_code = status.HTTP_201_CREATED)
async def odt_booking( background_tasks: BackgroundTasks,
    full_name: str = Form(...),
    email_address: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    contact_number: str = Form(...),
    whatsapp_number: str = Form(...),
    college_name: str = Form(...),
    pick_up_loc: str = Form(...),
    drop_loc: str = Form(...),
    meal_preference: str = Form(...),
    trip_exp_level: str = Form(None),
    medical_details: str = Form(None),
    agree: bool = Form(...),
    payment_screenshot: UploadFile = File(None),  db:Session = Depends(get_db) 
   
):

    file_location = None

    if payment_screenshot:
        file_name = f"{email_address}_payment_{payment_screenshot.filename}"
        file_location = os.path.join(UPLOAD_DIR, file_name)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(payment_screenshot.file, buffer)
    
    details = models.ODT(
        full_name=full_name,
        email_address=email_address,
        age=age,
        gender=gender,
        contact_number=contact_number,
        whatsapp_number=whatsapp_number , 
        college_name=college_name,
        pick_up_loc=pick_up_loc,
        drop_loc=drop_loc,
        meal_preference=meal_preference,
        trip_exp_level=trip_exp_level,
        medical_details=medical_details,
        agree=agree,
        payment_screenshot=file_location
    ) 
   
    
  
    db.add(details) 
    db.commit() 
    db.refresh(details)

    # invoice_path = generate_invoice(details)

    background_tasks.add_task(send_booking_email, details, file_location)
    # background_tasks.add_task(send_email_with_invoice, details, invoice_path)

    return {"message" : "Payment Successful"}

@router.get("/odt/confirm")
async def confirm_amount(booking_id: int, amount: int, db: Session = Depends(get_db)):
    # Fetch booking
    booking = db.query(models.ODT).filter(models.ODT.id == booking_id).first()

    if not booking:
        return {"error": "Booking not found"}

    # Generate invoice with selected amount
    invoice_path = generate_invoice(booking, amount)

    # Send invoice to user
    await send_email_with_invoice(booking, invoice_path)

    return {"message": f"Invoice for ₹{amount} sent to user {booking.email_address}"}

@router.get("/odt/decline")
async def decline_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    # Fetch booking
    booking_data = db.query(models.ODT).filter(models.ODT.id == booking_id).first()

    if not booking_data:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Send decline email
    await send_booking_declined_email(booking_data)

    return {
        "status": "declined",
        "message": "User notified about payment not received."
    }



