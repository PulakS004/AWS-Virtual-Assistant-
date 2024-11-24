import streamlit as st
import datetime
if 'events' not in st.session_state:
    
    st.session_state.events=[
    {'event':'Club Meeting', 'date':'2024-11-20 10:00','location':'Auditorium','type':'Networking'},
    {'event':'Python Workshop', 'date':'2024-11-29 11:00','location':'Seminar Hall','type':'Workshop'},
    {'event':'Introduction to Machine Learning on AWS', 'date':'2024-12-06 10:00','location':'Auditorium','type':'Seminar'},
    {'event':'Future of Cloud', 'date':'2024-12-16 13:00','location':'Auditorium','type':'Panel Discussion'},
    {'event':'Club Meeting', 'date':'2024-12-28 12:00','location':'Seminar Hall','type':'Networking'},
     {'event':'IoT on AWS', 'date':'2025-01-07 16:00','location':'Auditorium','type':'Workshop'},
    {'event':'Exploring AWS Blockchain Solutions', 'date':'2025-01-18 10:00','location':'Seminar Hall','type':'Seminar'},
    {'event':'Cloud Jam Session', 'date':'2025-01-30 11:00','location':'Auditorium','type':'Panel Discussion'},
    {'event':'Club Meeting', 'date':'2025-02-10 12:00','location':'Auditorium','type':'Networking'},
     {'event':'Building a ChatBot with AWS Lex', 'date':'2025-02-21 17:00','location':'Seminar Hall','type':'Workshop'},
     {'event':'Big Data and Analytics on AWS', 'date':'2025-03-03 11:00','location':'Auditorium','type':'Seminar'},
     {'event':'Tech for Social Good', 'date':'2025-03-17 10:00','location':'Seminar Hall','type':'Panel Discussion'}
]


for event in st.session_state.events:
    if isinstance(event["date"], str):  # Convert only if date is not already datetime
        event["datetime"] = datetime.datetime.strptime(event["date"], '%Y-%m-%d %H:%M')



def display_events(events_list):
    for event in events_list:
        st.write(f"**{event['event']}** - {event['date']} ({event['location']}, {event['type']})")


st.subheader("Add a New Event")
event_name = st.text_input("Event Name")
event_date = st.text_input("Event Date (YYYY-MM-DD HH:MM)")
event_location = st.text_input("Event Location")
event_type = st.selectbox("Event Type", ["Workshop", "Seminar", "Networking", "Panel Discussion"])

if st.button("Add Event"):
    if event_name and event_date and event_location:
        try:
           
            event_datetime = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M')

            
            new_event = {
                "event": event_name,
                "date": event_date,
                "location": event_location,
                "type": event_type,
                "datetime": event_datetime
            }

            
            st.session_state.events.append(new_event)

            
            st.session_state.events.sort(key=lambda x: x['datetime'])

            st.success(f"Event '{event_name}' added successfully!")

           
            event_date_str = event_datetime.strftime("%Y%m%dT%H%M%S")
            google_calendar_url = (
                f"https://calendar.google.com/calendar/r/eventedit?"
                f"text={event_name}&dates={event_date_str}/{event_date_str}&"
                f"location={event_location}&sf=true&output=xml"
            )
            st.markdown(f"[Add '{event_name}' to Google Calendar]({google_calendar_url})", unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter a valid date in the format: YYYY-MM-DD HH:MM")


if st.button('Show Upcoming Events'):
    st.subheader("Upcoming Events")
    display_events(st.session_state.events)


st.subheader("Event Countdown")


event_options = [event['event'] for event in st.session_state.events]
selected_event = st.selectbox("Choose an event for countdown", options=event_options)

if selected_event:
    
    event = next(item for item in st.session_state.events if item["event"] == selected_event)
    event_datetime = event['datetime']

    
    if event_datetime > datetime.datetime.now():
        countdown_placeholder = st.empty() 

        remaining_time = event_datetime - datetime.datetime.now()
        days, seconds = remaining_time.days, remaining_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        
        countdown_text = f""" Time remaining for **{event['event']}**
<div style="display: flex; flex-direction: row; gap: 5px; align-items: center; font-family: Arial, sans-serif;">
    <span style="font-size: 40px; font-weight: bold;">{days}</span>
    <span style="font-size: 20px;">days</span>,
    <span style="font-size: 40px; font-weight: bold;">{hours}</span>
    <span style="font-size: 20px;">hours</span>,
    <span style="font-size: 40px; font-weight: bold;">{minutes}</span>
    <span style="font-size: 20px;">minutes</span>
</div>
"""

        countdown_placeholder.markdown(countdown_text, unsafe_allow_html=True)  # Update the placeholder with countdown
    else:
        st.write("The selected event has already passed!")

calendar_url="https://calendar.google.com/calendar/embed?src=877916c64c59b4e5b014745336b0b687a6188ebf2399ffb4a803d9cdf0cd1c65%40group.calendar.google.com&ctz=UTC"
st.title("Your Events Calendar")
st.components.v1.iframe(calendar_url,width=1000,height=600)
