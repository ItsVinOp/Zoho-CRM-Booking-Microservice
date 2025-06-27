Zoho CRM Booking Microservice (Python + Flask)

This project is a Python microservice built with Flask to automate the creation of Contacts and Deals in Zoho CRM based on booking data.

It replicates the functionality of a Zoho Deluge script using Python, supporting both "Advance Booking" and "Instant Booking" logic.

---

## 🔧 Features

* ✅ OAuth2 token refresh to access Zoho CRM
* ✅ Create or reuse Contact records using phone or email
* ✅ Create related Deals (Bookings) with complete trip and passenger info
* ✅ Dynamic handling of `Amount` as a **Currency field**
* ✅ Formats `bags` field for Zoho dropdown (e.g., `01`, `02`, ..., `22`)
* ✅ Normalizes phone numbers to digits for contact lookup
* ✅ Auto-formats datetime to Australia/Sydney timezone
* ✅ Follows the original Deluge field names and logic
* ✅ CORS enabled for cross-origin requests
* ✅ Handles both `"Advance Booking"` and `"Instant Booking"`
* ✅ Input keys are normalized to lowercase automatically

---

## 🚀 How to Run Locally

1. **Clone the Repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/zoho-booking-api.git
   cd zoho-booking-api
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add Environment Variables (Optional but Recommended)**
   Create a `.env` file with:

   ```
   CLIENT_ID=your_zoho_client_id
   CLIENT_SECRET=your_zoho_client_secret
   REFRESH_TOKEN=your_zoho_refresh_token
   ```

4. **Run the Flask App**

   ```bash
   python zoho_booking_api.py
   ```

5. **Test Endpoint**

   * POST to: `http://127.0.0.1:5000/create_booking`
   * Content-Type: `application/json`

---

## 📥 Sample JSON Payload

```json
{
  "booking_id": "674d5023accf7",
  "full_name": "Alex",
  "email": "alex@wavcabs.com.au",
  "phone": "+61481700500",
  "pickup_location_name": "109 Pitt St, Sydney NSW 2000, Australia",
  "drop_location_name": "Domestic Terminal 2, Keith Smith Ave, Mascot NSW 2020, Australia",
  "cab_type": "StationWagon",
  "amount": 113.92,
  "booking_date": "2024-12-02",
  "booking_time": "17:13",
  "booking_type": "current",
  "price_type": "estimated",
  "trip_way": "OneWay",
  "bags": "1",
  "payment_type": "cash"
}
```

---

## 📦 Environment Notes

* Make sure your **Zoho OAuth credentials** are valid for the **Australia domain**:

  * Auth URL: `https://accounts.zoho.com.au/oauth/v2/token`
  * API URL: `https://www.zohoapis.com.au/crm/v8/`
* Update credentials directly in the script or securely via `.env`.
* The `"Amount"` field is mapped to a **Currency field** in Zoho and must be numeric (no currency symbols).

---

## 🧰 Tech Stack

* Python
* Flask
* Zoho CRM v2 API
* CORS
* Timezone-aware datetime handling with `pytz`

---

## 📦 requirements.txt

```txt
Flask
requests
flask_cors
pytz
python-dotenv
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to improve.

---

## 📜 License

This project is open-source and free to use under the MIT License.

---

Let me know if you'd like me to:

* Rename the main Python file (`zoho_booking_api.py`) in the README
* Add `.gitignore` or `.env.example`
* Push this `README.md` to your repo directly
