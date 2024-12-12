import streamlit as st

# Page Configuration
st.set_page_config(page_title="AWS Virtual Assistant", page_icon="📋", layout="wide")

# Registration Page
st.title("AWS Virtual Assistant")

# Tabs for navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "Event Countdown and Calenda", "Event Registration Tracker", "Idea Incubator and Voting Platform", "Project Mentor Matching", "Certificate Generator"])

#HOME PAGE 
#HOME PAGE
with tab1:
    st.header("About AWS Virtual Assistant")
    st.subheader("Event Countdown and Calendar")
    st.write("Keep track of upcoming events and their schedules.")
    st.subheader("Event Registration Tracker")
    st.write("Manage participant registrations efficiently.")
    st.subheader("Idea Incubator and Voting Platform")
    st.write("Share ideas and vote for the best ones.")
    st.subheader("Project Mentor Matching")
    st.write("Find the perfect mentor for your projects.")
    st.subheader("Certificate Generator")
    st.write("Generate certificates for participants effortlessly.")

#EVENT COUNTDOWN AND CALENDAR
#EVENT COUNTDOWN AND CALENDAR
with tab2: 
    import datetime
    def render():
        st.header("Event Countdown and Calendar")
        st.write("This feature helps you stay up to date with recent events.")

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

    
  
#REGISTRATION TRACKER 
#REGISTRATION TRACKER  
with tab3: 
    import os
    import pandas as pd

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

    # Registration Page
    st.header("Event Registration Portal")

    # Tabs for navigation
    tab21, tab22 = st.tabs(["Register", "View Participants"])

    with tab21:
        st.subheader("Register for an Event")
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

    with tab22:
        st.subheader("View Registered Participants")
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


#IDEA INCUBATOR AND VOTING PLATFORM
#IDEA INCUBATOR AND VOTING PLATFORM
with tab4: 
    import pandas as pd
    import matplotlib.pyplot as plt
    import streamlit as st
    from PIL import Image
    def render():
        st.header("Idea Incubator and Voting Platform")
        st.write("This feature helps you suggest ideas for events, projects and workshops and vote on them.")


    # Define the CSV file path
    CSV_FILE = "idea_incubator_data\ideas.csv"  # Path to your CSV file

    # Load data from CSV and store it in session state if not already done
    if 'ideas_data' not in st.session_state:
        try:
            st.session_state.ideas_data = pd.read_csv(CSV_FILE)
            st.session_state.ideas_data['Votes'] = st.session_state.ideas_data['Votes'].astype(int)  # Ensure Votes are integers
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()

    # Default action (Home page) if no button is clicked
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"


    # Home page content with charts and intro
    if st.session_state.current_page == "home":
        st.title("Welcome to the Idea Voting System")
        st.markdown("### Explore the ideas, vote for them, or add your own ideas to the list.")

        # Plot the bar chart for votes visualization (only appears on Home page)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(st.session_state.ideas_data['Idea'], st.session_state.ideas_data['Votes'], color='skyblue')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.xlabel("Ideas")
        plt.ylabel("Votes")
        plt.title("Votes for Ideas")
        st.pyplot(fig)

        # Plot the pie chart for votes distribution (only appears on Home page)
        fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
        ax_pie.pie(st.session_state.ideas_data['Votes'], labels=st.session_state.ideas_data['Idea'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax_pie.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
        plt.title("Votes Distribution by Idea")
        st.pyplot(fig_pie)

    # Show Add Idea page (if Add Idea button is pressed)
    elif st.session_state.current_page == "add_idea":
        st.title("Add a New Idea")
        st.markdown("### Enter your new idea below and click submit to add it to the list of ideas.")

        new_idea = st.text_input("Enter your idea:")
        if new_idea:
            if st.button("Submit New Idea"):
                new_idea_data = {"Idea": new_idea, "Votes": 0}
                st.session_state.ideas_data = pd.concat([st.session_state.ideas_data, pd.DataFrame([new_idea_data])], ignore_index=True)
                st.success(f"New idea '{new_idea}' added!")

        # Save button for Add Idea page
        if st.button("Save", key="save_add_idea"):
            st.session_state.ideas_data.to_csv(CSV_FILE, index=False)
            st.success("Ideas saved successfully.")

    # Show Vote page (if Vote button is pressed)
    elif st.session_state.current_page == "vote":
        st.title("Vote for Ideas")
        st.markdown("### Browse through the ideas and cast your vote.")

        for index, row in st.session_state.ideas_data.iterrows():
            idea_name = row['Idea']
            votes = row['Votes']

            with st.expander(f"{idea_name} (Votes: {votes})"):
                if st.button(f"Vote for '{idea_name}'", key=f"vote_{index}"):
                    # Increase vote by 1
                    st.session_state.ideas_data.at[index, 'Votes'] += 1
                    st.success(f"Your vote has been added to '{idea_name}'!")

        # Save button for Vote page
        if st.button("Save", key="save_vote"):
            st.session_state.ideas_data.to_csv(CSV_FILE, index=False)
            st.success("Votes saved successfully.")

    # Show Download page (if Download button is pressed)
    elif st.session_state.current_page == "download":
        st.title("Download Updated CSV File")
        st.markdown("### Click below to download the updated CSV file with votes.")

        csv = st.session_state.ideas_data.to_csv(index=False)
        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name="updated_ideas_votes.csv",
            mime="text/csv"
        )

    
#PROJECT MENTOR MATCHING
#PROJECT MENTOR MATCHING
with tab5: 
    def render():
        st.header("Project Mentor Matching")
        st.write("This feature helps mentees find mentors based on their technical skills and the project they wish to work on.")

    import pandas as pd
    import streamlit as st
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Function to calculate similarity scores between mentees and mentors
    def calculate_similarity(mentee_df, mentor_df):
        # Combine mentee and mentor skills into lists of text (for vectorization)
        mentee_skills = mentee_df['Skills'].tolist()
        mentor_skills = mentor_df['Skills'].tolist()

        # Initialize TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')

        # Combine all skills into a single list for fitting the vectorizer
        all_skills = mentee_skills + mentor_skills

        # Fit the vectorizer on all skills and transform them into vectors
        tfidf_matrix = vectorizer.fit_transform(all_skills)

        # Separate mentee and mentor skill vectors from the full matrix
        mentee_tfidf = tfidf_matrix[:len(mentee_skills)]
        mentor_tfidf = tfidf_matrix[len(mentee_skills):]

        # Calculate cosine similarity between each mentee and mentor pair
        similarity_scores = cosine_similarity(mentee_tfidf, mentor_tfidf)

        return similarity_scores

    # Function to match mentees with mentors based on similarity scores
    def match_mentor_mentee(mentees, mentors, similarity_scores):
        matches = []

        for i, mentee in mentees.iterrows():
            # Find the mentor with the highest similarity score for this mentee
            best_match_idx = similarity_scores[i].argmax()
            best_mentor = mentors.iloc[best_match_idx]

            matches.append({
                "Mentee Name": mentee['Name'],
                "Mentor Name": best_mentor['Name'],
                "Mentee Skills": mentee['Skills'],
                "Mentor Skills": best_mentor['Skills'],
                "Need": mentee['Need'],
                "Availability": best_mentor['Availability'],
                "Similarity Score": similarity_scores[i][best_match_idx]
            })

        return pd.DataFrame(matches)

    # Streamlit UI
    st.title("Mentor-Mentee Matching")

    # Input for mentee data
    st.header("Enter Mentee Data")
    mentee_data = []
    num_mentees = st.number_input("How many mentees?", min_value=1, max_value=10, value=1)
    for i in range(num_mentees):
        mentee_name = st.text_input(f"Mentee Name {i+1}", key=f"mentee_name_{i}")
        mentee_skills = st.text_input(f"Mentee Skills {i+1}", key=f"mentee_skills_{i}")
        mentee_need = st.text_input(f"Mentee Need {i+1}", key=f"mentee_need_{i}")

        mentee_data.append([mentee_name, mentee_skills, mentee_need])

    # Convert mentee data to DataFrame
    mentee_df = pd.DataFrame(mentee_data, columns=["Name", "Skills", "Need"])

    # Input for mentor data
    st.header("Enter Mentor Data")
    mentor_data = []
    num_mentors = st.number_input("How many mentors?", min_value=1, max_value=10, value=1)
    for i in range(num_mentors):
        mentor_name = st.text_input(f"Mentor Name {i+1}", key=f"mentor_name_{i}")
        mentor_skills = st.text_input(f"Mentor Skills {i+1}", key=f"mentor_skills_{i}")
        mentor_availability = st.selectbox(f"Mentor Availability {i+1}", ["Full-time", "Part-time"], key=f"mentor_availability_{i}")

        mentor_data.append([mentor_name, mentor_skills, mentor_availability])

    # Convert mentor data to DataFrame
    mentor_df = pd.DataFrame(mentor_data, columns=["Name", "Skills", "Availability"])

    # If data is entered, proceed with matching
    if st.button("Match Mentors and Mentees"):
        if not mentee_df.empty and not mentor_df.empty:
            # Calculate similarity scores
            similarity_scores = calculate_similarity(mentee_df, mentor_df)

            # Perform matching based on the highest similarity score
            matches_df = match_mentor_mentee(mentee_df, mentor_df, similarity_scores)

            if not matches_df.empty:
                matches_df.index = matches_df.index + 1
                st.write("Matching Results:")
                st.dataframe(matches_df)
                # Allow downloading of the result as a CSV file
                st.download_button(
                    label="Download Matched Results",
                    data=matches_df.to_csv(index=False),
                    file_name="mentor_mentee_matches.csv",
                    mime="text/csv"
                )
            else:
                st.write("No matches found based on the given criteria.")
        else:
            st.write("Please enter both mentee and mentor data.")


#CERTIFICATE GENERATOR
#CERTIFICATE GENERATOR
with tab6: 
    import streamlit as st
    import pandas as pd
    import cv2
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from io import BytesIO
    from PIL import Image

    def render():
        st.header("Certificate Generator")
        st.write("This feature helps you generate certificates for event participants.")

    # Function to generate certificate
    def generate_certificate(name, lastname, template_path):
        # Load the certificate template
        template = cv2.imread(template_path)

        # Check if the image was loaded successfully
        if template is None:
            st.error("Error: Certificate template image not found. Please check the template path.")
            return None

        # Define the text properties
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 2.5
        color = (255,255,255)  # White color
        thickness = 4

        # Overlay text onto the template
        #Handling case of missing last name
        if pd.isna(lastname) or lastname.strip() == "":
            text = f"{name}" #Use only the first name
        else:
            text = f"{name} {lastname}"
        position = (680, 700)  # Adjust position based on your template
        cv2.putText(template, text, position, font, font_scale, color, thickness)

        # Convert OpenCV image (BGR) to RGB for PIL(Python Imaging Library) compatibility
        template_rgb = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

        # Convert the image to a PIL Image object
        pil_image = Image.fromarray(template_rgb)

        # Save the PIL image to a BytesIO object
        image_stream = BytesIO()
        pil_image.save(image_stream, format="PNG")
        image_stream.seek(0)  # Reset the pointer to the beginning of the stream

        return image_stream

    # Streamlit interface
    st.title("Certificate Generator")

    # Upload participant CSV file
    uploaded_file = st.file_uploader("Upload CSV file with participant details", type="csv")
    template_path = "certificate_template.png"  # Make sure this path is correct

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.write(data)

        # Remove any extra spaces in column names
        data.columns = data.columns.str.strip()

        # Check if necessary columns are in the CSV file
        if 'Name' not in data.columns or 'Lastname' not in data.columns:
            st.error("CSV file must contain 'Name' and 'Lastname' columns.")
        else:
            if st.button("Generate Certificates"):
                pdf_bytes = BytesIO()

                # Create a PDF canvas
                pdf_canvas = canvas.Canvas(pdf_bytes)

                for index, row in data.iterrows():
                    name = row["Name"]
                    lastname = row["Lastname"]

                    # Debugging log for certificate generation
                    st.write(f"Generating certificate for {name} {lastname}")

                    # Generate certificate image
                    certificate_image_stream = generate_certificate(name, lastname, template_path)

                    if certificate_image_stream is None:
                        continue
                    
                    st.write(f"Certificate image generated for {name} {lastname}")

                    # Use ImageReader to process the image stream
                    img_reader = ImageReader(certificate_image_stream)

                    # Embed in the PDF
                    pdf_canvas.drawImage(img_reader, 50, 400, width=500, height=300)
                    pdf_canvas.showPage()

                pdf_canvas.save()

                st.success("Certificates generated successfully!")
                st.download_button(
                    "Download Certificates as PDF",
                    pdf_bytes.getvalue(),
                    file_name="certificates.pdf"
                )
