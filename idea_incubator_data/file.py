import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

CSV_FILE = "C:\Users\lenovo\Desktop\Pulak Stuff\College Sem 5\AWS Virtual Assistant\idea_incubator_data\ideas.csv"  # Update the path as needed

try:
    ideas_data = pd.read_csv(CSV_FILE)
    st.write("Data Loaded:")
    st.write(ideas_data.head())  # Show first few rows
    st.write("Columns:", ideas_data.columns)  # List of column names

    # Plot the data using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(ideas_data['Idea'], ideas_data['Votes'], color='skyblue')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.xlabel("Ideas")
    plt.ylabel("Votes")
    plt.title("Votes for Ideas")
    
    # Use Streamlit to display the plot
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error: {e}")