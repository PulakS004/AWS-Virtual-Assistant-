import streamlit as st
from applications import (
    certificate_generator,
    calendar,
    idea_incubator,
    mentor_matcher,
    registartion_tracker,
)

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="AWS Virtual Assistant App", layout="wide")
    
    # Page title and description
    st.title("Event Management App")
    st.subheader("Navigate to your desired feature")

    # Feature options
    features = {
        "Certificate Generator": certificate_generator,
        "Event Countdown and Calendar": calendar,
        "Idea Incubator and Voting Platform": idea_incubator,
        "Project Mentor Matching": mentor_matcher,
        "Event Registration Tracker": registartion_tracker,
    }

    # Create clickable options
    st.write("### Features")
    for feature_name, feature_module in features.items():
        if st.button(feature_name):
            # Render the selected feature's main function
            st.experimental_rerun()
            feature_module.render()
            return

    st.write("👆 Click a feature above to explore its functionality!")

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()
