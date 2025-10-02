import random
import string
from datetime import datetime, timedelta

def random_names():
    first_names = ['Saanvi', 'Raghav', 'Shraddha', 'Arti', 'Aditi', 'Arya']
    last_names = ['Shah', 'Patel', 'Kumar', 'Reddy', 'Mehta', 'Gupta']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_phone_no():
    prefix = ['9', '8', '7']
    return random.choice(prefix) + ''.join(random.choices(string.digits, k=9))

def random_email(name):
    domains= ['gmail.com', 'yahoo.com', 'outlook.com']
    local = name.lower().replace(" ", ".")
    return f"{local}@{random.choice(domains)}"

def random_date(start_days=1, end_days=10):
    date = datetime.today() + timedelta(days=random.randint(start_days, end_days))
    return date.strftime("%d/%m/%Y")

def generate_passenger_profile():
    name = random_names()
    phone = random_phone_no()
    email = random_email(name)
    date = random_date() 
    return {
        "name": name,
        "phone": phone,
        "email": email,
        "Date": date
    }
