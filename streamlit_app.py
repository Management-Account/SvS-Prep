import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("SvS Battle Registration")

# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SvS battle")

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    
    # Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?*",
        ["TCW", "MRA", "RFA", "SHR"],
        index=0
    )
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your FC level?*",
        ["F29","F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Troop Levels
    infantry_level = st.selectbox(
        "What is your Infantry Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    lancer_level = st.selectbox(
        "What is your Lancer Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    marksman_level = st.selectbox(
        "What is your Marksman Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Availability Times
    joining_from = st.selectbox(
        "Joining FROM*",
        ["12:00 UTC", "13:00 UTC", "14:00 UTC", "15:00 UTC", "16:00 UTC", "17:00 UTC"],
        index=0
    )
    
    joining_to = st.selectbox(
        "TO*",
        ["12:00 UTC", "13:00 UTC", "14:00 UTC", "15:00 UTC", "16:00 UTC", "17:00 UTC", "18:00 UTC"],
        index=0
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
                alliance,
                fc_level,
                infantry_level,
                lancer_level,
                marksman_level,
                joining_from,
                joining_to
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")

