from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app.models import ManaliTripBooking, ManaliTripPassenger
from app.schema import ManaliTripBookingSchema
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  
from app.utils.mail.manali import send_booking_email_manali
import shutil, os
from fastapi import BackgroundTasks
from app.utils.supabase_uploads import upload_to_supabase
import json

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/manali" , status_code=status.HTTP_201_CREATED)
# async def manali_package(background_tasks: BackgroundTasks , 
#         full_name : str = Form(...) ,
#         email_address: str = Form(...),
#         age: int = Form(...),
#         gender: str = Form(...),
#         contact_number: str = Form(...),
#         whatsapp_number: str = Form(...),
#         college_name: str = Form(...),
#         emergency_contact_number : str = Form(...),
#         proof_id_type : str = Form(...), 
#         chosen_id_number : str = Form(...) ,
#         medical_details: str = Form(...),
#         special_request : str = Form(...) , 
#         agree : bool = Form(...) ,
#         id_image : UploadFile = File(None) ,
#         payment_screenshot : UploadFile = File(None) ,  db:Session = Depends(get_db)
#         ):

#         file_location = None

#         if id_image:
#             file_name = f"{email_address}_payment_{id_image.filename}"
#             file_location = os.path.join(UPLOAD_DIR, file_name)
#             with open(file_location, "wb") as buffer:
#                 shutil.copyfileobj(id_image.file, buffer)

#         payment_screenshot_url = upload_to_supabase(
#                 payment_screenshot,
#                 folder="manali_payments"
#             )

#         details = models.Manali(
#             full_name=full_name,
#             email_address=email_address,
#             age=age,
#             gender=gender,
#             contact_number=contact_number,
#             whatsapp_number=whatsapp_number , 
#             emergency_contact_number = emergency_contact_number , 
#             college_name=college_name,
#             proof_id_type= proof_id_type, 
#             chosen_id_number= chosen_id_number , 
#             special_request=special_request ,  
#             payment_screenshot=payment_screenshot_url,
#             medical_details=medical_details,
#             agree=agree,
#             id_image=file_location
#     ) 

#         db.add(details) 
#         db.commit() 
#         db.refresh(details)
#         background_tasks.add_task(send_booking_email_manali, details, file_location)

#         return {"message" : "Payment Successful"}

        
@router.post("/manali")
def book_manali_trip(
    background_tasks: BackgroundTasks , 
        full_name : str = Form(...) ,
        email: str = Form(...),
        age: int = Form(...),
        gender: str = Form(...),
        contact_number: str = Form(...),
        whatsapp_number: str = Form(...),
        college_name: str = Form(...),
        emergency_number : str = Form(...),
        proof_id_type : str = Form(...), 
        id_number : str = Form(...) ,
        medical_detail: str = Form(...),
        special_request : str = Form(...) , 
        agreed : bool = Form(...) ,
        train_type : str = Form(...) ,
        no_of_passengers : int = Form(...) ,
        passengers: str = Form(...),
        id_image_url : UploadFile = File(None) , 
        payment_screenshot : UploadFile = File(None) ,
    db: Session = Depends(get_db)
):
    

    id_image = None

    if id_image_url:
        id_image = upload_to_supabase(
            id_image_url,
            folder="manali_id_images"
        )
        
    
    payment_screenshot_url = None
    if payment_screenshot:
        payment_screenshot_url = upload_to_supabase(
            payment_screenshot,
            folder="manali_payments"
        )

    try:
        passenger_list = json.loads(passengers)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid passengers JSON")

    if not isinstance(passenger_list, list):
        raise HTTPException(status_code=400, detail="Passengers must be a list")

    if len(passenger_list) != no_of_passengers:
        raise HTTPException(
            status_code=400,
            detail="Passenger count does not match"
        )

    booking = ManaliTripBooking(
        full_name=full_name,
        gender=gender,
        age=age,
        email=email,
        contact_number=contact_number,
        whatsapp_number=whatsapp_number,
        emergency_number=emergency_number,
        college_name=college_name,
        proof_id_type=proof_id_type,
        id_number=id_number,
        id_image_url=id_image,
        medical_detail=medical_detail,
        special_request=special_request,
        train_type=train_type,
        no_of_passengers=no_of_passengers,
        agreed=agreed , 
        payment_screenshot=payment_screenshot_url
    )

    db.add(booking)
    db.flush()  # booking.id generated here

    passenger_objects = []

    for p in passenger_list:
        passenger_objects.append(
            ManaliTripPassenger(
                booking_id=booking.id,
                full_name=p["full_name"],
                gender=p["gender"],
                age=p["age"],
                contact_number=p.get("contact_number"),
                train_type=p["train_type"]
            )
        )

    db.add_all(passenger_objects)
    db.commit()

    background_tasks.add_task(send_booking_email_manali, booking , passenger_objects , payment_screenshot)

    return {
        "message": "Manali trip booked successfully",
        "booking_id": booking.id,
        "leader_name": full_name,
        "total_passengers": len(passenger_objects)
    }