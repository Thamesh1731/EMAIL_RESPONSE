import smtplib
from email.message import EmailMessage
from queue import Queue
import streamlit as st

def send_email(customer_email, subject, message_body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "thameshscs442@gmail.com"
    msg['To'] = customer_email
    msg.set_content(message_body)

    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("thameshscs442@gmail.com", "Thamesh@2006")  # Replace with your email credentials
        server.send_message(msg)
        st.success(f"Response email sent to {customer_email}")


def generate_response():
    return "Thank you for contacting us. We have received your inquiry and will respond shortly."

email_queue = Queue()


st.title("Automated Email Response System")

customer_email = st.text_input("Enter the customer's email address:")

if st.button('Send Email'):
    if customer_email:
        email_queue.put(customer_email)

        
        while not email_queue.empty():
            customer_email = email_queue.get()


            
            response_message = generate_response()
            send_email(customer_email, "Thank you for contacting us", response_message)
    else:
        st.error("Please enter a valid email address.")

