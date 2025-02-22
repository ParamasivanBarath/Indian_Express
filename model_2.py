import os
import google.generativeai as genai
from dotenv import load_dotenv
import pyttsx3

class VoiceGenerator:
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def generate_voice(self, text, voice_properties):
        self.engine.setProperty('rate', voice_properties.get('rate', 150))
        self.engine.setProperty('volume', voice_properties.get('volume', 1.0))
        
        voices = self.engine.getProperty('voices')
        if voice_properties.get('gender') == 'female':
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)
            
        self.engine.say(text)
        self.engine.runAndWait()
    
    def save_to_file(self, text, filename, voice_properties):
        self.engine.setProperty('rate', voice_properties.get('rate', 150))
        self.engine.setProperty('volume', voice_properties.get('volume', 1.0))
        
        voices = self.engine.getProperty('voices')
        if voice_properties.get('gender') == 'female':
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)
            
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()

class NewsroomAI:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        self.voice_generator = VoiceGenerator()
        
    def generate_article(self, topic, style, length, additional_requirements=None):
        prompt = f"""Write a news article about {topic}. 
        Style: {style}
        Length: {length} words
        Additional Requirements: {additional_requirements if additional_requirements else 'None'}
        Include:
        - Compelling headline
        - Strong lead paragraph
        - Supporting evidence and data
        - Expert quotes or perspectives
        - Clear structure
        - Engaging conclusion"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def create_summary(self, article, style="bullet", length="medium"):
        summary_lengths = {
            "short": "100 words",
            "medium": "250 words",
            "long": "500 words"
        }
        prompt = f"""Create a {summary_lengths[length]} summary of this article in {style} format:
        {article}
        Include:
        - Main arguments
        - Key statistics
        - Critical findings
        - Notable quotes
        - Conclusions"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_headlines(self, article, target_platform=None):
        prompt = f"""Generate 5 headlines for this article:
        Article: {article}
        Target Platform: {target_platform if target_platform else 'General'}
        
        Consider:
        - SEO optimization
        - Platform-specific requirements
        - Character limits
        - Engagement potential
        - News values
        
        Include for each headline:
        1. Main headline
        2. SEO optimization notes
        3. Engagement prediction"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def create_interactive_content(self, article, quiz_type, num_questions):
        prompt = f"""Create an interactive quiz based on this article:
        {article}
        
        Quiz Type: {quiz_type}
        Number of Questions: {num_questions}
        
        For each question include:
        1. Question text
        2. Multiple choice options (4 options)
        3. Correct answer
        4. Explanation
        5. Difficulty level
        
        Additional features:
        - Progressive difficulty
        - Engaging question formats
        - Real-world applications
        - Learning objectives"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def translate_content(self, text, target_language, preserve_format=True):
        prompt = f"""Translate this content to {target_language}:
        {text}
        
        Requirements:
        - Preserve formatting: {preserve_format}
        - Maintain journalistic style
        - Adapt cultural references
        - Keep technical terminology accurate
        - Include original language for key terms in parentheses"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_social_posts(self, article, platforms):
        prompt = f"""Create social media posts for these platforms: {', '.join(platforms)}
        Article: {article}
        
        For each platform provide:
        1. Post text
        2. Hashtag suggestions
        3. Best posting time
        4. Engagement tips
        5. Visual content suggestions
        
        Platform-specific requirements:
        - Twitter: 280 chars, engaging hooks
        - LinkedIn: Professional tone, industry insights
        - Facebook: Conversational, shareable
        - Instagram: Visual focus, story potential"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def verify_content(self, text):
        prompt = f"""Perform comprehensive fact-checking on this text:
        {text}
        
        Analyze:
        1. Factual accuracy
        - Identify claims
        - Verify statistics
        - Cross-reference sources
        
        2. Source credibility
        - Evaluate cited sources
        - Suggest additional sources
        
        3. Bias assessment
        - Language analysis
        - Perspective balance
        - Context completeness
        
        4. Verification steps
        - Required fact-checking
        - Recommended sources
        - Expert consultation needs"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_voice_content(self, text, voice_properties):
        self.voice_generator.generate_voice(text, voice_properties)
    
    def save_voice_content(self, text, filename, voice_properties):
        self.voice_generator.save_to_file(text, filename, voice_properties)
    
    def generate_and_vocalize_content(self, article, voice_properties):
        prompt = f"""Optimize this article for voice narration:
        {article}
        
        Requirements:
        - Clear sentence structure
        - Appropriate pacing
        - Natural flow
        - Emphasis points
        - Easy-to-pronounce phrasing"""
        response = self.model.generate_content(prompt)
        optimized_text = response.text
        self.generate_voice_content(optimized_text, voice_properties)
        return optimized_text

    def convert_to_blog(self, content, blog_title, blog_subtitle):
        prompt = f"""Reformat the following content to be a blog post for Indian Express. 
Format the post with:
- A compelling blog title: {blog_title}
- An engaging subtitle: {blog_subtitle}
- Well-structured sections and clear narrative
Content: {content}"""
        response = self.model.generate_content(prompt)
        return response.text
