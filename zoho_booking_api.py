from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/create_booking', methods=['POST'])
def create_booking():
    maps = request.json

    url = "https://accounts.zoho.com.au/oauth/v2/token"
    mymap = {
        "refresh_token": "1000.4bf056fc819013cfd797c0b0c168a856.b2fc08eea4f2c0466d43d59201ec392e",
        "client_id": "1000.BK8S3UZUKASY6S3C44BLG0OZ7ZUCNK",
        "client_secret": "a18f56ea0fbcb1327220c3039f48bcbd784c0bb79e",
        "grant_type": "refresh_token"
    }

    # Step 1: Get access token
    resp = requests.post(url, data=mymap)
    token_data = resp.json()
    token = token_data.get("access_token")
    if not token:
        return jsonify({"message": "Access token retrieval failed", "status": "error"}), 500

    # Step 2: Create or fetch Contact
    create_record_url = "https://www.zohoapis.com.au/crm/v8/Contacts"
    header_map = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }
    body_map = {
        "Last_Name": maps.get("Full_Name"),
        "Email": maps.get("Email"),
        "Phone": maps.get("Phone")
    }
    data_map = {"data": [body_map]}
    create_rec = requests.post(create_record_url, json=data_map, headers=header_map)
    create_rec_json = create_rec.json()

    try:
        contact_id = create_rec_json["data"][0]["details"]["id"]
    except Exception:
        # Attempt to fetch existing contact by email if creation failed
        search_url = f"https://www.zohoapis.com.au/crm/v8/Contacts/search?email={maps.get('Email')}"
        search_resp = requests.get(search_url, headers=header_map).json()
        try:
            contact_id = search_resp["data"][0]["id"]
        except Exception as e:
            return jsonify({"message": f"Contact creation and lookup failed: {str(e)}", "status": "error"}), 500

    # Step 3: Create Deal
    create_amd_url = "https://www.zohoapis.com.au/crm/v8/Deals"
    amd_record = {
        "Pickup_Address": maps.get("Pickup_Location"),
        "Destination_Address": maps.get("Dropoff_Location"),
        "Deal_Name": f"{maps.get('Pickup_Location')} to {maps.get('Dropoff_Location')}",
        "Booking_Type": maps.get("Booking_Type"),
        "Trip_Type": maps.get("Trip_Way"),
        "Bags": maps.get("Select_Bags"),
        "Taxi_Type": maps.get("Taxi_Type"),
        "Contact_Name": contact_id,
        "Trip_Notes": maps.get("Notes"),
        "Payment_Method": maps.get("Payment_Method"),
        "Fleet": "13MAXI CABS",
        "Trip_Sources": "13maxicabs.com",
        "Service_Type": "General Transfers",
        "Stage": "Booking Enquiry",
        "Phone": maps.get("Phone"),
        "Email": maps.get("Email"),
        "No_of_Passengers": maps.get("Passengers"),
        "Pipeline": "Standard (Standard)"
    }

    if maps.get("Fixed_Price") == "true":
        amd_record["Fare_Type"] = "Set Price"

    if maps.get("Booking_Type") == "Advance Booking":
        amd_record["Closing_Date"] = maps.get("Pickup_Date_Time")[:10]
        amd_record["Trip_Date_Time"] = maps.get("Pickup_Date_Time")
    else:
        amd_record["Closing_Date"] = datetime.now().strftime("%Y-%m-%d")
        amd_record["Trip_Date_Time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    amd_data_map = {"data": [amd_record]}
    create_amd_resp = requests.post(create_amd_url, json=amd_data_map, headers=header_map).json()

    try:
        deal_id = create_amd_resp["data"][0]["details"]["id"]
    except Exception as e:
        return jsonify({"message": f"Deal creation failed: {str(e)}", "status": "error"}), 500

    return jsonify({"message": "Booking created", "deal_id": deal_id, "status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
