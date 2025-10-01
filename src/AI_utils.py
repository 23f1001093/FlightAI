from utils import random_names, random_phone_no, random_email, random_date

def generate_passenger_data(use_ai=False):
    
    name = random_names()
    phone = random_phone_no()
    email = random_email(name)
    date = random_date()
    return {
        "name": name,
        "phone": phone,
        "email": email,
        "date": date
    }
