from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings 
import requests
import resend 
import base64
import os
conf = ConnectionConfig(
    MAIL_USERNAME= settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
)

resend.api_key = settings.resend_api_key
base_url = settings.base_url


# async def send_booking_email(data, image_path: str | None = None):
#     try:
#         admin_action_base = "https://tgbackend-production-62ff.up.railway.app/odt/confirm"  # Base URL for admin actions
#         print(admin_action_base)
#         button_739 = f"{admin_action_base}?booking_id={data.id}&amount=739"
#         button_939 = f"{admin_action_base}?booking_id={data.id}&amount=939"
    
#         html_body = f"""
#         <h3>New Booking Received</h3>
#         <p><b>Name:</b> {data.full_name}</p>
#         <p><b>Email:</b> {data.email_address}</p>
#         <p><b>Contact:</b> {data.contact_number}</p>
#         <p><b>College:</b> {data.college_name}</p>
    
#         <p><b>Select Package Amount:</b></p>
    
#         <a href="{button_739}" 
#            style="padding:10px 20px;background:#008CBA;color:white;text-decoration:none;border-radius:6px;">
#            Approve ₹739
#         </a>
    
#         <a href="{button_939}" 
#            style="padding:10px 20px;background:#4CAF50;color:white;text-decoration:none;border-radius:6px;margin-left:10px;">
#            Approve ₹939
#         </a>
#         """
    
#         attachments = []
    
#         # ✅ Attach local file as Base64 (no 'path' key)
#         if image_path and os.path.exists(image_path):
#             with open(image_path, "rb") as f:
#                 file_data = base64.b64encode(f.read()).decode("utf-8")
#                 file_name = os.path.basename(image_path)
#                 attachments.append({
#                     "content": file_data,
#                     "filename": file_name,
#                     "type": "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
#                 })
    
#         email = {
#             "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
#             "to": ["tirthghumo@gmail.com"],
#             "subject": "New Trekking Package Booking",
#             "html": html_body,
#         }
#         if attachments:
#             email["attachments"] = attachments
    
       
#         response = await resend.Emails.send(email_payload)
#             print("EMAIL SENT SUCCESSFULLY:", response)
    
#     except Exception as e:
#             print("EMAIL ERROR:", e)
#             raise

async def send_booking_email(data, image_path: str | None = None):
    try:
        admin_action_base = "https://tgbackend-production-62ff.up.railway.app/odt/confirm"
        
        button_739 = f"{admin_action_base}?booking_id={data.id}&amount=739"
        button_939 = f"{admin_action_base}?booking_id={data.id}&amount=939"
        decline_link = f"https://tgbackend-production-62ff.up.railway.app/odt/decline?booking_id={data.id}"

        safe_text = f"""
        A new trekking booking has been submitted.
        Student Details:
        Name: {data.full_name}
        Email: {data.email_address}
        Contact: {data.contact_number}
        College: {data.college_name}
        Package Review Links:
        • Review package option (739): {button_739}
        • Review package option (939): {button_939}
        Decline booking: {decline_link}

        
            """

        attachments = []

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode("utf-8")
                file_name = os.path.basename(image_path)
                attachments.append({
                    "content": file_data,
                    "filename": file_name,
                    "type": "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
                })

        # email_payload = {
        #     "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        #     "to": ["thekomal2502@gmail.com"],
        #     "subject": "New Trekking Package Booking",
        #     "html": html_body,
        # }
        email_payload = {
            "from": "Tirth Ghumo <onboarding@resend.dev>",
            "to": ["hr.tirthghumo@gmail.com"],
            "subject": "New Trekking Package Booking",
            "text": safe_text.strip(),
                }


        if attachments:
            email_payload["attachments"] = attachments

        response = resend.Emails.send(email_payload)
        print("EMAIL SENT SUCCESSFULLY:", response)

    except Exception as e:
        print("EMAIL ERROR:", e)
        raise

async def send_booking_declined_email(data):
    try:
        text_body = f"""
        Hey {data.full_name},

Thank you for choosing TirthGhumo for your adventure.
We wanted to let you know that we've reviewed your recent booking attempt.
Unfortunately, we couldn’t verify the payment details on our end.

This might be due to a mismatch in the transaction ID or some other discrepancy.

If you believe this is an error, please feel free to reach out to us at
6260499299 / 6204289831 — we’ll be happy to help resolve the issue.

We appreciate your understanding and hope to welcome you on another adventure soon.

Warm regards,
Team TirthGhumo
        """.strip()

        email_payload = {
            "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
            "to": [data.email_address],
            "subject": "Booking Update – Action Required",
            "text": text_body,
        }

        resend.Emails.send(email_payload)

    except Exception as e:
        print("DECLINE EMAIL ERROR:", e)
        raise




async def send_email_with_invoice(data, invoice_path):
    """Send invoice PDF to user using Resend"""

    # ---- Attach PDF ----
    with open(invoice_path, "rb") as f:
        file_bytes = base64.b64encode(f.read()).decode("utf-8")

    # ---- Email Body ----
    email_body = f"""
   Hey {data.full_name} 🌿

Great news — your booking for the 1Day Mrignnath Trek with TirthGhumo 
is confirmed for 7th December 2025!

Your payment has been approved successfully . 

All essential trip details, including timings and instructions, 
will be shared shortly on WhatsApp.

Please make sure you’ve requested to join the WhatsApp group,
as all updates will be shared there.

If you need any help or have questions, feel free to contact us 
at 6260499299 / 6204289831.

Get ready for an exciting adventure and a day full of unforgettable memories!

Warm regards,
Team TirthGhumo

Thank you for choosing TirthGhumo — Aastha Bhi, Suvidha Bhi 🌄

    """

    # ---- Email Payload ----
    email = {
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": [data.email_address],
        "subject": "Your Trek Booking Invoice",
        "text": email_body.strip(),
        "attachments": [
            {
                "filename": "invoice.pdf",
                "content": file_bytes,
                "type": "application/pdf"
            }
        ]
    }

    # ---- Send ----
    try:
        resend.Emails.send(email)
    except Exception as e:
        raise Exception(f"Invoice email failed: {str(e)}")
