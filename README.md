Zoho CRM Booking Microservice (Python + Flask)
==============================================

This project is a Python microservice built with Flask to automate the creation of Contacts and Deals in Zoho CRM based on booking data.

It replicates the functionality of a Zoho Deluge script using Python, supporting both "Advance Booking" and "Quick Booking" logic.

--------------------------------------------------
🔧 Features
--------------------------------------------------
- OAuth2 token refresh to access Zoho CRM
- Create or reuse Contact records using email
- Create related Deals (Bookings) with full details
- Follows the original Deluge field names and logic
- Supports "Set Price" when `Fixed_Price` is true

--------------------------------------------------
🚀 How to Run Locally
--------------------------------------------------

1. Clone the Repository:
   git clone https://github.com/YOUR_USERNAME/zoho-booking-api.git
   cd zoho-booking-api

2. Install Dependencies:
   pip install flask requests

3. Run the Flask App:
   python zoho_booking_api.py

4. The service will be available at:
   http://127.0.0.1:5000/create_booking

--------------------------------------------------
📥 Sample JSON Payload
--------------------------------------------------

POST /create_booking
Content-Type: application/json

{
  "Pickup_Location": "Trip",
  "Dropoff_Location": "XYZ",
  "Booking_Type": "Advance Booking",
  "Pickup_Date_Time": "2025-05-06T02:04:00",
  "Trip_Way": "One Way",
  "Select_Bags": "2",
  "Fixed_Price": "true",
  "Taxi_Type": "Sedan",
  "Passengers": "4",
  "Fare": 388,
  "Full_Name": "Test Abomi",
  "Email": "test6217@gmail.com",
  "Phone": "9326097642",
  "Notes": "Test Notes",
  "Payment_Method": "Cash"
}

--------------------------------------------------
📦 Environment Notes
--------------------------------------------------
- Make sure your Zoho OAuth client ID, client secret, and refresh token are valid for the AU domain (`accounts.zoho.com.au`).
- Update the credentials in the script before running.
- Set up access to `https://www.zohoapis.com.au/crm/v8/` endpoints in your CRM.

--------------------------------------------------
🤝 Contributing
--------------------------------------------------
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

--------------------------------------------------
📜 License
--------------------------------------------------
This project is open-source and free to use.
