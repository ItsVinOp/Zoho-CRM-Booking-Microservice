from flask import Flask, request, jsonify, make_response
import requests
from datetime import datetime

app = Flask(__name__)

ZOHO_TOKEN_URL = "https://accounts.zoho.com.au/oauth/v2/token"
ZOHO_API_BASE_URL = "https://www.zohoapis.com.au/crm/v8"

# Your OAuth credentials
REFRESH_TOKEN = "1000.4bf056fc819013cfd797c0b0c168a856.b2fc08eea4f2c0466d43d59201ec392e"
CLIENT_ID = "1000.BK8S3UZUKASY6S3C44BLG0OZ7ZUCNK"
CLIENT_SECRET = "a18f56ea0fbcb1327220c3039f48bcbd784c0bb79e"

def get_access_token():
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(ZOHO_TOKEN_URL, data=payload)
    if response.status_code != 200:
        return None, f"Failed to get access token: {response.text}"
    data = response.json()
    return data.get("access_token"), None

def search_contact(headers, phone=None, email=None):
    if phone:
        url = f"{ZOHO_API_BASE_URL}/Contacts/search"
        params = {"phone": phone}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200 and resp.json().get("data"):
            return resp.json()["data"][0]["id"]
    if email:
        url = f"{ZOHO_API_BASE_URL}/Contacts/search"
        params = {"email": email}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200 and resp.json().get("data"):
            return resp.json()["data"][0]["id"]
    return None

def create_contact(headers, data):
    url = f"{ZOHO_API_BASE_URL}/Contacts"
    payload = {
        "data": [{
            "Last_Name": data.get("full_name", "Unknown") or "Unknown",
            "Email": data.get("email", ""),
            "Phone": data.get("phone", "")
        }]
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (200, 201):
        try:
            return resp.json()["data"][0]["details"]["id"]
        except (KeyError, IndexError):
            return None
    return None

@app.route('/create_booking', methods=['POST'])
def create_booking():
    # Convert all input keys to lowercase
    maps = {k.lower(): v for k, v in request.json.items()}

    # Step 1: Get access token
    token, error = get_access_token()
    if not token:
        return cors_jsonify({"message": error, "status": "error"}), 500

    headers = {
        "Access-Control-Allow-Origin", "http://localhost:4003/",
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }

    # Step 2: Normalize phone
    phone_raw = maps.get('phone', '')
    phone_search_val = ''.join(filter(str.isdigit, phone_raw))

    # Step 3: Search or create contact
    contact_id = search_contact(headers, phone=phone_search_val, email=maps.get('email'))
    if not contact_id:
        contact_id = create_contact(headers, maps)
        if not contact_id:
            return cors_jsonify({"message": "Contact creation failed", "status": "error"}), 500

    pickup = maps.get('pickup_location_name', '')
    drop = maps.get('drop_location_name', '')

    def first_segment(location):
        return location.split(',')[0].strip() if location else ''

    deal_name = f"{first_segment(pickup)} to {first_segment(drop)}" if pickup or drop else "Booking Deal"

    booking_type = maps.get("booking_type", "").strip().lower()
    price_type = maps.get("price_type", "").strip().lower()

    if booking_type == "advance":
        booking_date = maps.get("booking_date", "")
        booking_time = maps.get("booking_time", "00:00")
        try:
            trip_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M")
            trip_date_time_str = trip_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            closing_date_str = booking_date
        except Exception:
            now = datetime.now()
            trip_date_time_str = now.strftime("%Y-%m-%dT%H:%M:%S")
            closing_date_str = now.strftime("%Y-%m-%d")
    else:
        now = datetime.now()
        trip_date_time_str = now.strftime("%Y-%m-%dT%H:%M:%S")
        closing_date_str = now.strftime("%Y-%m-%d")

    deal_data = {
        "Deal_Name": deal_name,
        "Reference_ID": maps.get("booking_id", ""),
        "Pickup_Address": pickup,
        "Destination_Address": drop,
        "Trip_Type": maps.get("trip_way", ""),
        "Bags": maps.get("bags", 0),
        "Taxi_Type": maps.get("cab_type", ""),
        "Contact_Name": contact_id,
        "Payment_Method": (maps.get("payment_type") or "").capitalize(),
        "Fleet": "13MAXI CABS",
        "Amount": maps.get("amount", 0),
        "Trip_Sources": "13maxicabs.com",
        "Service_Type": "General Transfers",
        "Stage": "Booking Enquiry",
        "Phone": maps.get("phone", ""),
        "Email": maps.get("email", ""),
        "Pipeline": "Standard (Standard)",
        "Booking_Type": "Advance Booking" if booking_type == "advance" else "Instant Booking",
        "Closing_Date": closing_date_str,
        "Trip_Date_Time": trip_date_time_str,
    }

    if price_type == "fixed":
        deal_data["Fare_Type"] = "Set Price"

    deal_payload = {"data": [deal_data]}
    deal_url = f"{ZOHO_API_BASE_URL}/Deals"
    deal_resp = requests.post(deal_url, headers=headers, json=deal_payload)

    if deal_resp.status_code not in (200, 201):
        return cors_jsonify({"message": f"Deal creation failed: {deal_resp.text}", "status": "error"}), 500

    try:
        deal_id = deal_resp.json()["data"][0]["details"]["id"]
    except (KeyError, IndexError):
        return cors_jsonify({"message": "Deal creation failed: invalid response", "status": "error"}), 500

    return cors_jsonify({"message": "Booking created", "deal_id": deal_id, "status": "success"}), 200

# Add CORS headers to all JSON responses
def cors_jsonify(data):
    response = make_response(jsonify(data))
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:4003/")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    return response

if __name__ == '__main__':
    app.run(debug=True)
