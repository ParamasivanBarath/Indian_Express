import streamlit as st
from model_2 import NewsroomAI
from Modules.styles import local_css
from database_config import DatabaseConnection
from database_tables import DatabaseTables
from database_operations import DatabaseOperations
from Modules.article_generator import show_article_generator
from Modules.summarizer import show_summarizer
from Modules.headlines_seo import show_headlines_seo
from Modules.quiz_generator import show_quiz_generator
from Modules.translation_hub import show_translation_hub
from Modules.social_media import show_social_media
from Modules.content_verification import show_content_verification
from Modules.audio_production import show_audio_production


def initialize_database():
    """Initialize database and create tables"""
    try:
        # Create database connection
        db_connection = DatabaseConnection()
        db_connection.create_database()
        
        # Create tables
        db_tables = DatabaseTables()
        db_tables.create_tables()
        
        return True
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")
        return False

def main():
    st.set_page_config(page_title="Indian Express AI Assistant", layout="wide")
    local_css()
    
    # Initialize database
    if not initialize_database():
        st.error("Failed to initialize database. Please check your database configuration.")
        return
    
    # Initialize database operations
    db_ops = DatabaseOperations()
    
    st.markdown('<div class="header"><h1>Indian Express AI Newsroom</h1></div>', 
                unsafe_allow_html=True)
    
    assistant = NewsroomAI()
    
    with st.sidebar:
        st.header("Newsroom Tools")
        feature = st.radio(
            "Select Feature",
            ["Article Generator", "Smart Summarizer", "Headlines & SEO", 
             "Interactive Quiz", "Translation Hub", "Social Media", 
             "Content Verification", "Audio Production"]
        )
    
    features = {
        "Article Generator": show_article_generator,
        "Smart Summarizer": show_summarizer,
        "Headlines & SEO": show_headlines_seo,
        "Interactive Quiz": show_quiz_generator,
        "Translation Hub": show_translation_hub,
        "Social Media": show_social_media,
        "Content Verification": show_content_verification,
        "Audio Production": show_audio_production
    }
    
    if feature in features:
        # Pass both assistant and database operations to feature functions
        features[feature](assistant)

if __name__ == "__main__":
    main()
