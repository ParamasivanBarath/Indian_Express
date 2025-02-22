import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion
import os

def show_audio_production(assistant):
    st.header("🎧 Voice Generator")
    db_ops = DatabaseOperations()
    
    text_input = st.text_area("Enter text for voice conversion", height=200)
    st.subheader("Voice Settings")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        voice_gender = st.selectbox("Voice Gender", ["male", "female"], 
                                  key="voice_gender")
    with col2:
        speech_rate = st.slider("Speech Rate", 50, 300, 150, 
                              help="Words per minute", key="speech_rate")
    with col3:
        volume = st.slider("Volume", 0.0, 1.0, 1.0, 0.1, key="volume")
    
    voice_properties = {
        "gender": voice_gender,
        "rate": speech_rate,
        "volume": volume
    }
    
    col1, col2, col3 = st.columns([1,1,1])
    handle_audio_buttons(assistant, db_ops, text_input, voice_properties, col1, col2, col3)

def handle_audio_buttons(assistant, db_ops, text_input, voice_properties, col1, col2, col3):
    """Handle the three audio operation buttons"""
    if not text_input:
        st.warning("Please enter text before generating audio.")
        return
        
    with col1:
        if st.button("Generate Voice", key="gen_voice"):
            handle_voice_generation(assistant, text_input, voice_properties)
    
    with col2:
        if st.button("Save as Audio File", key="save_audio"):
            handle_audio_save(assistant, db_ops, text_input, voice_properties)
    
    with col3:
        if st.button("Optimize & Generate", key="optimize_voice"):
            handle_optimization(assistant, db_ops, text_input, voice_properties)

def handle_voice_generation(assistant, text_input, voice_properties):
    """Generate voice without saving"""
    try:
        with st.spinner("Generating voice..."):
            assistant.generate_voice_content(text_input, voice_properties)
            st.success("Voice generated successfully!")
    except Exception as e:
        st.error(f"Error generating voice: {str(e)}")

def handle_audio_save(assistant, db_ops, text_input, voice_properties):
    """Save audio to file and database"""
    try:
        with st.spinner("Saving audio file..."):
            audio_dir = create_audio_directory()
            filename = generate_unique_filename(audio_dir)
            
            # Save audio file
            assistant.save_voice_content(text_input, filename, voice_properties)
            
            # Save to database
            audio_id = db_ops.save_audio(text_input, filename, voice_properties)
            
            st.success("Audio file saved successfully!")
            
            # Provide download button
            with open(filename, 'rb') as file:
                st.download_button(
                    label="Download Audio",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="audio/mp3",
                    key="download_audio"
                )
            
            # Show blog conversion option
            show_blog_conversion(assistant, text_input, audio_id, "audio")
            
    except Exception as e:
        st.error(f"Error saving audio: {str(e)}")

def handle_optimization(assistant, db_ops, text_input, voice_properties):
    """Optimize text and generate audio"""
    try:
        with st.spinner("Optimizing and generating voice..."):
            # Optimize text for voice narration
            optimized_text = assistant.generate_and_vocalize_content(text_input, voice_properties)
            
            audio_dir = create_audio_directory()
            filename = generate_unique_filename(audio_dir, "optimized_voice")
            
            # Save optimized audio
            assistant.save_voice_content(optimized_text, filename, voice_properties)
            
            # Save to database
            audio_id = db_ops.save_audio(optimized_text, filename, voice_properties)
            
            st.success("Optimized audio generated successfully!")
            
            # Show optimized text
            st.subheader("Optimized Text")
            st.write(optimized_text)
            
            # Provide download button
            with open(filename, 'rb') as file:
                st.download_button(
                    label="Download Optimized Audio",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="audio/mp3",
                    key="download_optimized_audio"
                )
            
            # Show blog conversion option
            show_blog_conversion(assistant, optimized_text, audio_id, "audio_optimized")
            
    except Exception as e:
        st.error(f"Error optimizing and generating voice: {str(e)}")

def create_audio_directory():
    """Create directory for audio files if it doesn't exist"""
    audio_dir = "audio_files"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    return audio_dir

def generate_unique_filename(directory, prefix="generated_voice"):
    """Generate a unique filename for audio files"""
    return os.path.join(directory, f"{prefix}_{len(os.listdir(directory))}.mp3")
