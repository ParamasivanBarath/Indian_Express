import streamlit as st
from model_2 import NewsroomAI
from Modules.styles import local_css
from Modules.article_generator import show_article_generator
from Modules.summarizer import show_summarizer
from Modules.headlines_seo import show_headlines_seo
from Modules.quiz_generator import show_quiz_generator
from Modules.translation_hub import show_translation_hub
from Modules.social_media import show_social_media
from Modules.content_verification import show_content_verification
from Modules.audio_production import show_audio_production

def main():
    st.set_page_config(page_title="Indian Express AI Assistant", layout="wide")
    local_css()
    
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
        features[feature](assistant)

if __name__ == "__main__":
    main()