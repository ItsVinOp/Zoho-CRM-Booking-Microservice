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

{"Booking_Id":"674d5023accf7","Full_Name":"Alex","Email":"alex@wavcabs.com.au","Phone":"+61481700500","Pickup_Location_Name":"109 Pitt St, 109 Pitt St, Sydney NSW 2000, Australia","Drop_Location_Name":"Domestic Terminal 2, Domestic Terminal 2, Keith Smith Ave, Mascot NSW 2020, Australia","Cab_Type":"Station Wagon","Amount":"113.92","Booking_Date":"2024-12-02","Booking_Time":"17:13","Booking_Type":"current","Price_Type":"estimated","Trip_way":"One Way","Bags":"1","Payment_Type":"cash"}

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
