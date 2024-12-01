import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

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

# Sidebar with AWS logo and enhanced styling
aws_logo_path = "AWS.jpeg"  # Path to the logo image in the same directory as main.py
st.sidebar.image(aws_logo_path, width=130)

# Adding some padding between elements for a better visual
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

# Sidebar Buttons for navigation without icons
home_button = st.sidebar.button("Home", key="home_button", help="Go to the home page")
vote_button = st.sidebar.button("Vote for Ideas", key="vote_button", help="Vote for ideas")
add_idea_button = st.sidebar.button("Add an Idea", key="add_idea_button", help="Submit a new idea")
download_button = st.sidebar.button("Download CSV File", key="download_button", help="Download the updated CSV with votes")

# Add a horizontal line separator for visual appeal
st.sidebar.markdown("---")

# Default action (Home page) if no button is clicked
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Handle sidebar button actions to navigate between pages
if home_button:
    st.session_state.current_page = "home"
elif vote_button:
    st.session_state.current_page = "vote"
elif add_idea_button:
    st.session_state.current_page = "add_idea"
elif download_button:
    st.session_state.current_page = "download"

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
