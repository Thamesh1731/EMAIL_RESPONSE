import imaplib
import smtplib
from email.message import EmailMessage
import email
from queue import Queue
import streamlit as st

# Function to send an automated response
def send_response_email(receiver_email, subject, message_body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "dsproject490@gmail.com"  # Your Gmail
    msg['To'] = receiver_email
    msg.set_content(message_body)

    # Set up the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("dsproject490@gmail.com", "eyyb zkyv jptu nlip")  # Use app-specific password
        server.send_message(msg)
        st.success(f"Response email sent to {receiver_email}")

# Pre-defined response message
def generate_response():
    return "Thank you for contacting us. We have received your inquiry and will respond shortly."

# Function to read unread emails from your Gmail
def get_unread_emails():
    # Log in to your email account
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("dsproject490@gmail.com", "eyyb zkyv jptu nlip")  # Use app-specific password
    mail.select("inbox")

    # Search for all unread emails
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    return email_ids, mail

# Function to process unread emails
def process_emails(email_queue, mail):
    while not email_queue.empty():
        email_id = email_queue.get()

        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Extract the email sender
                email_from = email.utils.parseaddr(msg['From'])[1]
                print(f"Email from: {email_from}")

                # Send an automated response
                response_message = generate_response()
                send_response_email(email_from, "Thank you for contacting us", response_message)

# Main function to activate the process
def start_automatic_response():
    # Queue to hold the email IDs
    email_queue = Queue()

    # Get unread emails
    email_ids, mail = get_unread_emails()

    # Enqueue all unread emails
    for email_id in email_ids:
        email_queue.put(email_id)

    # Process emails and send responses
    process_emails(email_queue, mail)

    # Logout from the mail server
    mail.logout()

# Streamlit UI
st.title("AUTOMATIC EMAIL RESPONSE SYSTEM")

# Button to start the email response system
if st.button('Start Automatic Email Response'):
    start_automatic_response()
    st.write("Processing unread emails and sending automatic responses...")

    send_email(customer_email, "Thank you for contacting us", response_message)
else:
    st.error("Please enter a valid email address.")

