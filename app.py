import os
from dotenv import load_dotenv #for loading env variables
load_dotenv() #for loading all env variables


from youtube_transcript_api import YouTubeTranscriptApi

import google.generativeai as genai #for nlp
import streamlit as st # for frontend

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are an AI assistant that creates a 250-word summary of provided Youtube video 
transcripts. The transcript will be appended here."""

#Method for extracting the transcript of the video
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += "" + i["text"]
        
        return transcript

    except Exception as e:
        raise e

#Method for generating a summary using the Gemini AI model
def generate_summary(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

#Frontend of the summarizer
st.title("YouTube Transript Summarizer")
youtube_link = st.text_input("Enter the video link here: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_summary(transcript_text, prompt)
        st.markdown("Summary: ")
        st.write(summary)
