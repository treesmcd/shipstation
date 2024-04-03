import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyshipstation.api import ShipStation

# ShipStation setup
api_key = 'YOUR_SHIPSTATION_API_KEY'
api_secret = 'YOUR_SHIPSTATION_API_SECRET'
ss = ShipStation(key=api_key, secret=api_secret)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Your Google Sheet Name').sheet1

def fetch_on_hold_shipments():
    # Fetch shipments from ShipStation (pseudocode - adjust with actual method)
    on_hold_shipments = ss.fetch_orders(parameters_dict={'order_status': 'on_hold'})
    return on_hold_shipments

def update_google_sheets(shipments_data):
    for index, shipment in enumerate(shipments_data, start=2): # Assuming row 1 is headers
        # Write data to Google Sheets (pseudocode - adjust with actual data fields)
        sheet.update(f'A{index}', shipment.customer_name)
        sheet.update(f'B{index}', shipment.order_id)
        # ... update other fields as needed

def sync_tracking_info_to_shipstation():
    # Read updated rows from Google Sheets and update ShipStation (pseudocode)
    rows = sheet.get_all_records()
    for row in rows:
        tracking_info = row['TrackingInfo'] # Column name where tracking info is stored
        if tracking_info:
            # Update ShipStation shipment (pseudocode)
            ss.update_shipment_tracking(row['OrderID'], tracking_info)

# Main flow
on_hold_shipments = fetch_on_hold_shipments()
update_google_sheets(on_hold_shipments)
sync_tracking_info_to_shipstation()
