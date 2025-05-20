import streamlit as st
from datetime import datetime, date
import csv
import os
import pandas as pd

csv_path = "mood_log.csv"

if not os.path.exists(csv_path):
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "mood", "notes"])

st.title("Mood Tracker")
st.write("How are you feeling right now?")

moods = ["Happy", "Excited", "Sad", "Angry", "Confused", "Annoyed"]
selected_mood = st.selectbox("Choose your mood:", moods)

notes = st.text_area("Add any notes (optional):", height=100)

if st.button("Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(csv_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, selected_mood, notes])

    st.success(f"Logged: {timestamp}, {selected_mood}")
    if notes:
        st.write("Notes:", notes)


    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df["date"] = df["timestamp"].dt.date
    today_df = df[df["date"] == date.today()]

    if not today_df.empty:
        mood_counts = today_df["mood"].value_counts().sort_index()
        st.write("### Today's Mood Counts")
        st.bar_chart(mood_counts)
    else:
        st.write("No entries for today yet.")
