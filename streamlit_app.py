import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("TCW Members")
st.subheader("Help us get to know you better!")

# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("DATA")

# Registration Form
with st.form("registration_form"):
    # In-game Name
    ign = st.text_input("In-game Name*", max_chars=50)
    
    # Timezone Selection
    timezone = st.selectbox(
        "What is Your Timezone?*",
        ["UTC-12", "UTC-11", "UTC-10", "UTC-9", "UTC-8", "UTC-7", "UTC-6", 
         "UTC-5", "UTC-4", "UTC-3", "UTC-2", "UTC-1", "UTC±0", 
         "UTC+1", "UTC+2", "UTC+3", "UTC+4", "UTC+5", "UTC+6", 
         "UTC+7", "UTC+8", "UTC+9", "UTC+10", "UTC+11", "UTC+12"],
        index=12  # Default to UTC±0
    )
    
    # Birthday Selection (fixed to year 2025)
    birthday = st.date_input(
        "What is Your Birthday? (Year will be set to 2025)*",
        min_value=datetime(2025, 1, 1),
        max_value=datetime(2025, 12, 31),
        value=datetime(2025, 1, 1)  # Default to Jan 1, 2025
    )
    
    # Submit Button
    submitted = st.form_submit_button("Submit Registration")
    
    if submitted:
        # Validate required fields
        if not ign:
            st.error("Please enter your In-game Name")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Store the birthday with selected month/day but fixed year 2025
            formatted_birthday = f"2025-{birthday.month:02d}-{birthday.day:02d}"
            new_row = [
                timestamp,
                ign,
                timezone,
                formatted_birthday
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")
