import streamlit as st
from database_operations import DatabaseOperations
from .blog_convertor import show_blog_conversion
import time
from google.api_core import retry

def show_quiz_generator(assistant):
    st.header("🎮 Quiz Generator")
    db_ops = DatabaseOperations()
    
    article = st.text_area("Article Content", height=200)
    col1, col2 = st.columns(2)
    with col1:
        quiz_type = st.selectbox("Quiz Type", 
                               ["Multiple Choice", "True/False", 
                                "Mixed Format", "Scenario Based"], 
                               key="quiz_type")
    with col2:
        num_questions = st.number_input("Number of Questions", 
                                      min_value=3, max_value=15, value=5, 
                                      key="num_questions")
    
    if st.button("Generate Quiz", key="gen_quiz"):
        if not article:
            st.warning("Please enter article content before generating a quiz.")
            return
            
        try:
            with st.spinner("Creating quiz..."):
                # Add retry logic for API calls
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        quiz = assistant.create_interactive_content(article, quiz_type, num_questions)
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Failed to generate quiz after {max_retries} attempts. Please try again later.")
                            return
                        time.sleep(2)  # Wait before retrying
                
                # Save article first
                article_id = db_ops.save_article("Quiz", "Interactive", article, len(article.split()))
                
                # Save quiz and get ID
                quiz_id = db_ops.save_quiz(article_id, quiz_type, quiz)
                
                # Display quiz
                st.markdown("### Generated Quiz")
                st.markdown(quiz)
                
                # Download button
                st.download_button(
                    "Download Quiz", 
                    quiz, 
                    "quiz.txt", 
                    key="download_quiz"
                )
                
                # Store in session state
                st.session_state.update({
                    "current_quiz": quiz,
                    "current_quiz_id": quiz_id,
                    "current_quiz_type": quiz_type
                })
                
                # Show blog conversion option
                show_blog_conversion(assistant, quiz, quiz_id, "quiz")
                
        except Exception as e:
            st.error(f"Error generating quiz: {str(e)}")
            st.error("Please try again with different content or settings.")
