import resend

async def send_hiring_email(data):
    """
    Send hiring application details to admin via Resend API
    """

    email_body = f"""
    New Hiring Application Received

    -------------------------
    APPLICANT DETAILS
    -------------------------
    Full Name        : {data.full_name}
    Email Address    : {data.email_address}
    Contact Number   : {data.phone_number}
    City             : {data.current_city}
    Gender           : {data.gender or "N/A"}

    -------------------------
    EDUCATION
    -------------------------
    Qualification    : {data.education_qualification or "N/A"}
    College Name     : {data.college_name or "N/A"}

    -------------------------
    POSITION DETAILS
    -------------------------
    Position Applied : {data.position_applied}
    Why This Role    :
    {data.why_this_role}

    -------------------------
    SKILLS & EXPERIENCE
    -------------------------
    Key Skills       : {data.key_skills}

    Worked in Travel Company : {"Yes" if data.worked_in_travel_company else "No"}
    Previous Role           : {data.previous_travel_role or "N/A"}

    Travel Expertise Rating : {data.travel_expertise_rating or "N/A"} / 10
    Managed Group Trips     : {"Yes" if data.managed_group_trips else "No"}
    Comfortable with 24x7   : {"Yes" if data.comfortable_24x7 else "No"}

    -------------------------
    LINKS & DOCUMENTS
    -------------------------
    Resume URL       : {data.resume_file}
    ID Proof Type    : {data.id_proof_type}
    ID Proof URL     : {data.id_proof_file}

    LinkedIn Profile : {data.linkedin_profile or "N/A"}
    Portfolio URL   : {data.portfolio_url or "N/A"}

    -------------------------
    FINAL NOTES
    -------------------------
    Why should we hire this candidate?
    {data.why_should_we_hire_you}

    Referral Source : {data.referral_source or "N/A"}

    -------------------------

    Please review the application in the admin panel.
    """

    email = {
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["hr.tirthghumo@gmail.com"],
        "subject": f"New Hiring Application – {data.position_applied}",
        "text": email_body.strip(),
    }

    try:
        resend.Emails.send(email)
        return {"status": "Hiring admin email sent successfully"}
    except Exception as e:
        raise Exception(f"Hiring admin email sending failed: {str(e)}")
