import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification (for local testing)
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("TCW Members")

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
    # 1. In-game Name (text input)
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    
    # 2. Timezone (dropdown)
    timezone = st.selectbox(
        "What is Your Timezone?*",
        ["UTC-12", "UTC-11", "UTC-10", "UTC-9", "UTC-8", "UTC-7", "UTC-6", 
         "UTC-5", "UTC-4", "UTC-3", "UTC-2", "UTC-1", "UTC±0", 
         "UTC+1", "UTC+2", "UTC+3", "UTC+4", "UTC+5", "UTC+6", 
         "UTC+7", "UTC+8", "UTC+9", "UTC+10", "UTC+11", "UTC+12"],
        index=12  # Default to UTC±0
    )
    
    # 3. Birthday (month and day only)
    # Create a date with fixed year (2000) to hide the year
    birthday = st.date_input(
        "What is Your Birthday? (Month and Day only)*",
        value=datetime(2000, 1, 1),  # Fixed year
        min_value=datetime(2000, 1, 1),
        max_value=datetime(2000, 12, 31),
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
                birthday.strftime("%m-%d")  # Store as MM-DD
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
                
                # Clear form after successful submission (optional)
                st.rerun()
                
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")

# Optional: Add some instructions
st.markdown("""
**Instructions:**
1. Fill in your in-game name
2. Select your timezone
3. Pick your birthday (month and day only)
4. Click submit to register
""")
