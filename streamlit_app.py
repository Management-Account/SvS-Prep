import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("SFC Battle Registration")

# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SvS Battle Registration")

# Registration Form
with st.form("registration_form"):
    # In-game Name
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    
    # Timezone Selection
    timezone = st.selectbox(
        "What is Your Timezone?*",
        ["UTC-12", "UTC-11", "UTC-10", "UTC-9", "UTC-8", "UTC-7", "UTC-6", 
         "UTC-5", "UTC-4", "UTC-3", "UTC-2", "UTC-1", "UTC±0", 
         "UTC+1", "UTC+2", "UTC+3", "UTC+4", "UTC+5", "UTC+6", 
         "UTC+7", "UTC+8", "UTC+9", "UTC+10", "UTC+11", "UTC+12"],
        index=12  # Default to UTC±0
    )
    
    # Birthday Selection (Month and Day only)
    today = datetime.today()
    birthday = st.date_input(
        "What is Your Birthday? (Month and Day only)*",
        min_value=datetime(1900, 1, 1),
        max_value=datetime(1900, 12, 31),  # Using 1900 as placeholder year
        format="MM-DD"
    )
    
    # Submit Button
    submitted = st.form_submit_button("Submit Registration")
    
    if submitted:
        if not player_name:
            st.error("Please enter your in-game name")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [
                timestamp,
                player_name,
                timezone,
                birthday.strftime("%m-%d")  # Format as MM-DD
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")
