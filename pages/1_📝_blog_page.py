import streamlit as st
from database_operations import DatabaseOperations
from datetime import datetime

def local_css():
    css = """
    <style>
    body {
        font-family: 'Georgia', serif;
        background-color: #f7f7f7;
        color: #333;
        margin: 2rem;
    }
    .blog-header {
        background-color: #b30000;
        padding: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .blog-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0 0.2rem 0;
        text-align: center;
    }
    .blog-content {
        line-height: 1.6;
        font-size: 1.1rem;
        padding: 2rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .blog-meta {
        color: #666;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .blog-date-picker {
        margin: 2rem 0;
        padding: 1rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def blog_page():
    st.set_page_config(page_title="Indian Express Blog", layout="wide")
    local_css()
    
    st.markdown('<div class="blog-header"><h1>Indian Express Blog</h1></div>', 
                unsafe_allow_html=True)
    
    db_ops = DatabaseOperations()
    
    # Get available dates from database
    dates = db_ops.get_blog_dates()
    
    if dates:
        with st.container():
            st.markdown('<div class="blog-date-picker">', unsafe_allow_html=True)
            selected_date = st.date_input(
                "Select Date",
                value=dates[0] if dates else datetime.now().date(),
                min_value=min(dates) if dates else None,
                max_value=max(dates) if dates else None
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Get blogs for selected date
            blogs = db_ops.get_blogs_by_date(selected_date)
            
            if blogs:
                for blog in blogs:
                    with st.container():
                        st.markdown(f"<div class='blog-title'>{blog['title']}</div>", 
                                  unsafe_allow_html=True)
                        st.markdown(
                            f"<div class='blog-meta'>Published on: "
                            f"{blog['created_at'].strftime('%B %d, %Y %I:%M %p')} | "
                            f"Module: {blog['module_type']}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(f"<div class='blog-content'>{blog['content']}</div>", 
                                  unsafe_allow_html=True)
                        st.markdown("<hr>", unsafe_allow_html=True)
            else:
                st.info(f"No blog posts available for {selected_date}")
    else:
        st.info("No blog content available. Please generate content first.")

if __name__ == "__main__":
    blog_page()
