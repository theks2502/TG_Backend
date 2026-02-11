from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings 
import requests
import resend 
import base64
import os

resend.api_key = settings.resend_api_key

# utils/mail/admin_vr_darshan_mail.py
import resend

async def send_admin_vr_darshan_email(booking):
    devotees_text = ""
    for i, d in enumerate(booking.devotees, start=1):
        devotees_text += f"""
Devotee {i}
Name   : {d.full_name}
Age    : {d.age}
Gender : {d.gender}
Address: {d.address}
ID     : {d.aadhar_image_url}
"""

    approve = f"https://tgbackend-production-7c1c.up.railway.app/admin/vr-darshan/action?booking_id={booking.id}&action=approve"
    decline_age = f"https://tgbackend-production-7c1c.up.railway.app/admin/vr-darshan/action?booking_id={booking.id}&action=decline_age"
    decline_payment = f"https://tgbackend-production-7c1c.up.railway.app/admin/vr-darshan/action?booking_id={booking.id}&action=decline_payment"

    body = f"""
NEW VR DARSHAN BOOKING

Contact Number : {booking.contact_number}
WhatsApp       : {booking.whatsapp_number}
Email          : {booking.email_address}

Spiritual Place: {booking.spiritual_place}
Date           : {booking.preferred_date}
Time Slot      : {booking.time_slot}

Special Request:
{booking.special_request or "None"}

Payment Screenshot:
{booking.payment_screenshot or "Not uploaded"}

DEVOTEE DETAILS:
{devotees_text}

--------------------
ADMIN ACTIONS
--------------------

Approve:
{approve}

Decline (Age Mismatch):
{decline_age}

Decline (Payment Not Received):
{decline_payment}
"""

    resend.Emails.send({
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["thekomal2502@gmail.com"],
        "subject": "VR Darshan Booking – Action Required",
        "text": body
    })
