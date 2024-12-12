import streamlit as st
import pandas as pd
import os

def render():
    st.header("Registration tracker")
    st.write("This feature helps you track participants in a particular AWS Club event.")


# Step 1: Define the CSV file path
CSV_FILE = "registrations.csv"

# Predefined list of events
EVENTS = ["Tech Talk", "Hackathon", "UI/UX Workshop", "AI Seminar", "Startup Meet"]

# Step 2: Define utility functions
def load_data():
    """Load existing registration data from CSV file."""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Event Name", "Participant Name", "Email", "Contact Number"])
        df.to_csv(CSV_FILE, index=False)
        return df

def save_data(data):
    """Save updated data back to CSV."""
    data.to_csv(CSV_FILE, index=False)

def add_registration(event_name, participant_name, email, contact_number):
    """Add a new registration to the CSV file."""
    df = load_data()
    new_entry = pd.DataFrame(
        {
            "Event Name": [event_name],
            "Participant Name": [participant_name],
            "Email": [email],
            "Contact Number": [contact_number],
        }
    )
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

def filter_data(event_name):
    """Filter registrations by event name."""
    df = load_data()
    if event_name:
        return df[df["Event Name"].str.contains(event_name, case=False, na=False)]
    return df

# Page Configuration
#st.set_page_config(page_title="Event Registration", page_icon="📋", layout="wide")

# Registration Page
st.title("Event Registration Portal")

# Tabs for navigation
tab1, tab2 = st.tabs(["Register", "View Participants"])

with tab1:
    st.header("Register for an Event")
    st.write("Fill in the details below to register for an event.")

    # Dropdown for event selection
    event_name = st.selectbox("Select an Event", options=EVENTS)
    
    # Input fields
    participant_name = st.text_input("Participant Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email address")
    contact_number = st.text_input("Contact Number", placeholder="Enter your contact number")
    
    if st.button("Register"):
        if event_name and participant_name and email and contact_number:
            add_registration(event_name, participant_name, email, contact_number)
            st.success(f"Thank you, {participant_name}! You've successfully registered for {event_name}.")
        else:
            st.error("Please fill out all fields before submitting.")

with tab2:
    st.header("View Registered Participants")
    st.write("Select an event to view its participants.")
    
    # Dropdown for filtering
    filter_event_name = st.selectbox("Choose Event to Filter", options=[""] + EVENTS, index=0)
    
    if st.button("Show Participants"):
        filtered_df = filter_data(filter_event_name)
        if not filtered_df.empty:
            st.write(f"Participants for {filter_event_name if filter_event_name else 'All Events'}:")
            st.dataframe(filtered_df)
        else:
            st.warning("No participants found for the selected event.")
