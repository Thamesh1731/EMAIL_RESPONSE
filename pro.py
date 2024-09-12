import imaplib
import smtplib
from email.message import EmailMessage
import email
from queue import Queue
import streamlit as st
GMAIL_USER = "dsproject490@gmail.com"  
GMAIL_PASS = "eyyb zkyv jptu nlip"     
def send_response_email(receiver_email, subject, message_body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = receiver_email
    msg.set_content(message_body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)  
            server.send_message(msg)
            return True
    except Exception as e:
        st.error(f"Failed to send email to {receiver_email}: {e}")
        return False
def generate_response():
    return "Thank you for contacting us. We have received your inquiry and will respond shortly.https://todo-list21050.netlify.app/"
def get_unread_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        return email_ids, mail
    except Exception as e:
        st.error(f"Failed to retrieve emails: {e}")
        return [], None
def process_emails(email_queue, mail):
    sent_emails = []
    while not email_queue.empty():
        email_id = email_queue.get()
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_from = email.utils.parseaddr(msg['From'])[1]
                st.write(f"Processing email from: {email_from}")
                response_message = generate_response()
                if send_response_email(email_from, "Thank you for contacting us", response_message):
                    sent_emails.append(email_from)
    return sent_emails
def start_automatic_response():
    email_queue = Queue()
    email_ids, mail = get_unread_emails()
    if mail and email_ids:
        for email_id in email_ids:
            email_queue.put(email_id)
        sent_emails = process_emails(email_queue, mail)
        mail.logout()
        st.session_state['sent_emails'] = sent_emails
    else:
        st.write("No unread emails found or failed to connect to the mail server.")
st.title("AUTOMATIC EMAIL RESPONSE SYSTEM")
if 'sent_emails' not in st.session_state:
    st.session_state['sent_emails'] = []
if st.button('Start Automatic Email Response'):
    start_automatic_response()
    st.write("Processing unread emails and sending automatic responses...")
if st.session_state['sent_emails']:
    st.write("Response emails sent to the following addresses:")
    for email in st.session_state['sent_emails']:
        st.write(email)


