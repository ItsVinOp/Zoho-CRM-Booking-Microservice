Zoho CRM Booking Microservice (Python + Flask)
==============================================

This project is a Python microservice built with Flask to automate the creation of Contacts and Deals in Zoho CRM based on booking data.

It replicates the functionality of a Zoho Deluge script using Python, supporting both "Advance Booking" and "Instant Booking" logic.

--------------------------------------------------
🔧 Features
--------------------------------------------------
- OAuth2 token refresh to access Zoho CRM
- Create or reuse Contact records using phone or email
- Create related Deals (Bookings) with full details
- Follows the original Deluge field names and logic
- Supports "Set Price" when `price_type` is `fixed`
- CORS enabled for cross-origin requests
- Normalizes input keys to lowercase automatically

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
  "booking_id": "674d5023accf7",
  "full_name": "Alex",
  "email": "alex@wavcabs.com.au",
  "phone": "+61481700500",
  "pickup_location_name": "109PittSt,109PittSt,SydneyNSW2000,Australia",
  "drop_location_name": "DomesticTerminal2,DomesticTerminal2,KeithSmithAve,MascotNSW2020,Australia",
  "cab_type": "StationWagon",
  "amount": "113.92",
  "booking_date": "2024-12-02",
  "booking_time": "17:13",
  "booking_type": "current",
  "price_type": "estimated",
  "trip_way": "OneWay",
  "bags": "1",
  "payment_type": "cash"
}

--------------------------------------------------
📦 Environment Notes
--------------------------------------------------
- Ensure your Zoho OAuth client ID, client secret, and refresh token are valid for the AU domain (`accounts.zoho.com.au`).
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
