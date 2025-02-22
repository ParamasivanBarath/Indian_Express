import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion
from datetime import datetime
import requests

def fetch_real_time_news(topic, category):
    """
    Fetch real-time news using NewsData.io API
    """
    # Replace with your API key
    api_key = "pub_68905901d922fdf9a8bee38a0f3498c2549cb"
    url = f"https://newsdata.io/api/1/news"
    
    params = {
        "apikey": api_key,
        "q": topic,
        "category": category.lower(),
        "language": "en",
        "country": "in"  # Focus on Indian news
    }
    
    response = requests.get(url, params=params)
    return response.json()['results'][0] if response.json()['results'] else None

def rephrase_content(content):
    """
    Rephrase the content using NLP techniques
    """
    # Initialize the paraphrasing model
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    
    model_name = "tuner007/pegasus_paraphrase"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    # Tokenize and generate paraphrased content
    tokens = tokenizer(content, truncation=True, padding="longest", return_tensors="pt")
    generated = model.generate(**tokens, max_length=len(content), num_beams=4)
    
    return tokenizer.decode(generated[0], skip_special_tokens=True)

def show_article_generator(assistant):
    st.header("📝 Indian Express Style News Rephraser")
    db_ops = DatabaseOperations()
    
    col1, col2 = st.columns([2,1])
    
    with col1:
        topic = st.text_input("Search News Topic")
        style = st.selectbox(
            "News Category", 
            ["World", "India", "Business", "Sports", 
             "Entertainment", "Technology", "Health"]
        )
        
    with col2:
        featured_image = st.file_uploader(
            "Custom Featured Image (Optional)", 
            type=['jpg', 'png']
        )
        custom_angle = st.text_area(
            "Custom Angle (Optional)",
            placeholder="Add specific focus points..."
        )

    if st.button("Fetch & Rephrase News", key="gen_article"):
        if not topic:
            st.warning("Please enter a topic to search news.")
            return
            
        try:
            with st.spinner("Fetching and rephrasing latest news..."):
                # Fetch real-time news
                news = fetch_real_time_news(topic, style)
                
                if not news:
                    st.error("No news found for the given topic.")
                    return
                
                # Rephrase the content
                rephrased_content = rephrase_content(news['content'])
                
                # Format in Indian Express style
                timestamp = datetime.now().strftime("%B %d, %Y %I:%M")
                article = f"""# {news['title']}

## {style} | {timestamp} IST | {news['source_id']}

{news['description']}

{rephrased_content}

**Source**: {news['source_id']}
**Original Link**: {news['link']}
"""
                
                # Save to database
                article_id = db_ops.save_article(news['title'], style, article, len(rephrased_content.split()))
                
                # Display the rephrased article
                st.markdown("### Preview")
                st.markdown(article)
                
                # Article Actions
                col5, col6 = st.columns([1,1])
                with col5:
                    st.download_button(
                        "Download Article",
                        article,
                        f"{topic.lower().replace(' ', '_')}.txt",
                        key="download_article"
                    )
                with col6:
                    st.button("Edit Article", key="edit_article")
                
                # Store in session state
                st.session_state.update({
                    "current_article": article,
                    "current_article_id": article_id,
                    "current_topic": topic,
                    "current_style": style
                })
                
                # Show blog conversion options
                st.markdown("---")
                show_blog_conversion(
                    assistant=assistant,
                    content=article,
                    source_id=article_id,
                    source_type="indian_express_article"
                )
                
        except Exception as e:
            st.error(f"Error processing news: {str(e)}")
            return
