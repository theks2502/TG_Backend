from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings 
import requests
import resend 
import base64
import os

async def send_booking_email_tamia(data, image_path: str | None = None):
    """Send booking details via Resend API with optional image attachment."""

    email_body = f"""
    Full Name: {data.full_name}
    Email Address: {data.email_address}
    Age: {data.age}
    Gender: {data.gender}
    Contact Number: {data.contact_number}
    Whatsapp Number: {data.whatsapp_number}
    Emergency Contact Number : {data.emergency_contact_number}
    College Name: {data.college_name}
    Mode of Transport: {data.mode_of_transport}
    Proof Id Type: {data.proof_id_type}
    Id number: {data.chosen_id_number}
    Medical Details: {data.medical_details}
    Special Request:{data.special_request}
    Agree to Terms: {data.agree}
    """

    attachments = []

    # ✅ Attach local file as Base64 (no 'path' key)
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")
            file_name = os.path.basename(image_path)
            attachments.append({
                "content": file_data,
                "filename": file_name,
                "type": "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
            })

    email = {
        "from":  "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["hr.tirthghumo@gmail.com"],
        "subject": "New Booking for Tamia",
        "text": email_body.strip(),
    }

    # Only add attachments if present
    if attachments:
        email["attachments"] = attachments

    try:
        resend.Emails.send(email)
        return {"status": "Email sent successfully"}
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")