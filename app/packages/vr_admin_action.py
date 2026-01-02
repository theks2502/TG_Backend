# routes/admin_vr_darshan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.utils.mail.vr_user_mail import (
    send_user_approval_mail,
    send_user_decline_age_mail,
    send_user_decline_payment_mail
)

router = APIRouter()

@router.get("/admin/vr-darshan/action")
async def admin_action(
    booking_id: int,
    action: str,
    db: Session = Depends(get_db)
):
    booking = db.query(models.VRDarshanBooking).filter(
        models.VRDarshanBooking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.is_confirmed:
        return {"message": "Action already taken"}

    if action == "approve":
        booking.is_confirmed = True
        await send_user_approval_mail(booking)

    elif action == "decline_age":
        await send_user_decline_age_mail(booking)

    elif action == "decline_payment":
        await send_user_decline_payment_mail(booking)

    else:
        raise HTTPException(400, "Invalid action")

    db.commit()

    return {"message": "Action completed and user notified"}
