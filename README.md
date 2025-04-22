# AWS Cloud Club Virtual Assistant 

Welcome to the AWS Virtual Assistant, a smart and interactive tool developed to streamline operations for technical clubs. Designed with functionality and user experience in mind, this project includes an integrated dashboard offering everything from event planning and idea voting to dynamic certificate generation— all in one place.

## Features

- **Calendar & Countdown**
<br>
Plan your club events with ease! View all scheduled events on an interactive calendar and keep track of upcoming sessions with a real-time countdown timer.

Tech Stack: **Streamlit, datetime, plotly**

- **Event Registration Tracker**
<br>
Track member registrations for workshops, talks, and hackathons. Visualize participation trends with charts and insights.

Tech Stack: **pandas, matplotlib, Streamlit**


- **Idea Incubator & Voting Platform**
<br>
Submit innovative ideas for events or sessions and vote on your peers’ suggestions. Helps prioritize what your club should work on next.

Tech Stack: **pandas, matplotlib, Streamlit, CSV data backend**

- **Mentor-Mentee Matching**
<br>
Leverage sentence embeddings to find the best mentor-mentee pairs based on skills and learning interests.

Tech Stack: **sentence-transformers (BERT), sklearn, Streamlit**

- **Certificate Generator**
<br>
Generate customized participation certificates using OpenCV, perfect for events and workshops.

Tech Stack: **OpenCV, Pillow, Streamlit**
## Tech Stack

**Frontend UI:** Streamlit

**Data Processing:** 	pandas, matplotlib, numpy

**Embedding & NLP:** sentence-transformers, scikit-learn

**Image Handling:** OpenCV, Pillow

**Storage:** CSV




## Setup Instructions

1. Clone the repo

```bash
  git clone https://github.com/PulakS004/AWS-Virtual-Assistant-.git
```
2. Activate the Virtual Environment

- On Windows

```bash
    AWSVAenv\Scripts\activate

```
- On MacOS/Linux

```bash
    source AWSVAvenv/bin/activate

```

3. Install dependencies

```bash
  pip install -r requirements.txt
```
4. Run the app

```bash
  streamlit run app.py
```
