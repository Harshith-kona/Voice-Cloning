import os
import streamlit as st
import requests
import certifi
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
   api_key = os.getenv("Esk_92cb7818b4b380654e50cdf0b1d3d1a9ad76d63662957c77")
)



ELEVENLABS_API_KEY = os.getenv("Esk_92cb7818b4b380654e50cdf0b1d3d1a9ad76d63662957c77") 
ELEVENLABS_VOICE_CLONE_URL = "https://api.elevenlabs.io/v1/voices/add"
ELEVENLABS_TEXT_TO_SPEECH_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


st.title("Voice Cloning App")
st.write("Upload a 10-second audio sample to clone a voice.")


uploaded_file = st.file_uploader("Upload a 10-second audio sample (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

  
    if st.button("Clone Voice"):
        with st.spinner("Cloning voice..."):
           
            headers = {
                "Authorization": f"Bearer {ELEVENLABS_API_KEY}",
                "Accept": "application/json"
            }
            files = {
                "files": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            data = {
                "name": "Cloned Voice",
                "description": "Voice cloned from uploaded audio sample"
            }


            try:
                response = requests.post(
                    ELEVENLABS_VOICE_CLONE_URL,
                    headers=headers,
                    files=files,
                    data=data,
                    verify=certifi.where()
                )
                response.raise_for_status()  
                
                try:
                    json_response = response.json()  
                    voice_id = json_response.get("voice_id")
                    st.success(f"Voice cloned successfully! Voice ID: {voice_id}")
                except ValueError:
                    st.error("Response content is not valid JSON:")
                    st.text(response.text) 


                text_to_speak = st.text_input("Enter text for the cloned voice to speak:")
                if text_to_speak:
                    tts_url = ELEVENLABS_TEXT_TO_SPEECH_URL.format(voice_id=voice_id)
                    tts_headers = {
                        "Authorization": f"Bearer {ELEVENLABS_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    tts_data = {
                        "text": text_to_speak,
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.75
                        }
                    }

                    tts_response = requests.post(tts_url, headers=tts_headers, json=tts_data, verify=certifi.where())
                    tts_response.raise_for_status()  
                    st.audio(tts_response.content, format="audio/mp3")
                    st.success("Speech generated successfully!")

            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred: {http_err}")  
            except requests.exceptions.RequestException as req_err:
                st.error(f"Request error occurred: {req_err}") 
            except Exception as e:
                st.error(f"An error occurred: {e}") 
