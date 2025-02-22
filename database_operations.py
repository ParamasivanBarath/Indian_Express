from database_config import DatabaseConnection
from mysql.connector import Error
import json
from datetime import datetime

class DatabaseOperations:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def save_article(self, topic, style, content, word_count):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO articles (topic, style, content, word_count, created_at) 
                      VALUES (%s, %s, %s, %s, NOW())"""
            cursor.execute(query, (topic, style, content, word_count))
            article_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog(topic, content, "Article", article_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return article_id
        except Error as e:
            raise Exception(f"Error saving article: {e}")
    
    def save_summary(self, article_id, summary_style, content, length):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO summaries (article_id, summary_style, content, length, created_at) 
                      VALUES (%s, %s, %s, %s, NOW())"""
            cursor.execute(query, (article_id, summary_style, content, length))
            summary_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog(summary_style, content, "Summary", summary_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return summary_id
        except Error as e:
            raise Exception(f"Error saving summary: {e}")
    
    def save_headline(self, article_id, platform, headline_content, seo_notes):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO headlines (article_id, platform, headline_content, seo_notes, created_at) 
                      VALUES (%s, %s, %s, %s, NOW())"""
            cursor.execute(query, (article_id, platform, headline_content, seo_notes))
            headline_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog(platform, headline_content, "Headline", headline_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return headline_id
        except Error as e:
            raise Exception(f"Error saving headline: {e}")
    
    def save_quiz(self, article_id, quiz_type, questions):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO quizzes (article_id, quiz_type, questions, created_at) 
                      VALUES (%s, %s, %s, NOW())"""
            cursor.execute(query, (article_id, quiz_type, json.dumps(questions)))
            quiz_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog(quiz_type, questions, "Quiz", quiz_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return quiz_id
        except Error as e:
            raise Exception(f"Error saving quiz: {e}")
    
    def save_translation(self, original_content, translated_content, target_language):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO translations (original_content, translated_content, target_language, created_at) 
                      VALUES (%s, %s, %s, NOW())"""
            cursor.execute(query, (original_content, translated_content, target_language))
            translation_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog(target_language, translated_content, "Translation", translation_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return translation_id
        except Error as e:
            raise Exception(f"Error saving translation: {e}")
    
    def save_social_post(self, article_id, platform, content, hashtags):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO social_posts (article_id, platform, content, hashtags, created_at) 
                      VALUES (%s, %s, %s, %s, NOW())"""
            cursor.execute(query, (article_id, platform, content, hashtags))
            post_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog(platform, content, "Social Post", post_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return post_id
        except Error as e:
            raise Exception(f"Error saving social post: {e}")
    
    def save_verification(self, content, analysis):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO content_verification (content, analysis, created_at) 
                      VALUES (%s, %s, NOW())"""
            cursor.execute(query, (content, analysis))
            verification_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog("Content Verification", analysis, "Verification", verification_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return verification_id
        except Error as e:
            raise Exception(f"Error saving verification: {e}")
    
    def save_audio(self, text_content, audio_file_path, voice_properties):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO audio_content (text_content, audio_file_path, voice_properties, created_at) 
                      VALUES (%s, %s, %s, NOW())"""
            cursor.execute(query, (text_content, audio_file_path, json.dumps(voice_properties)))
            audio_id = cursor.lastrowid
            
            # Save to blogs table
            self.save_blog("Audio Content", text_content, "Audio", audio_id)
            
            connection.commit()
            cursor.close()
            connection.close()
            return audio_id
        except Error as e:
            raise Exception(f"Error saving audio content: {e}")
    
    def save_blog(self, title, content, module_type, module_id):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """INSERT INTO blogs (title, content, module_type, module_id, created_at) 
                      VALUES (%s, %s, %s, %s, NOW())"""
            cursor.execute(query, (title, content, module_type, module_id))
            blog_id = cursor.lastrowid
            connection.commit()
            cursor.close()
            connection.close()
            return blog_id
        except Error as e:
            raise Exception(f"Error saving blog: {e}")
    
    def get_blogs_by_date(self, date):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT * FROM blogs 
            WHERE DATE(created_at) = %s 
            ORDER BY created_at DESC
            """
            cursor.execute(query, (date,))
            blogs = cursor.fetchall()
            cursor.close()
            connection.close()
            return blogs
        except Error as e:
            raise Exception(f"Error retrieving blogs by date: {e}")
    
    def get_blog_dates(self):
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            query = """
            SELECT DISTINCT DATE(created_at) as blog_date 
            FROM blogs 
            ORDER BY blog_date DESC
            """
            cursor.execute(query)
            dates = [date[0] for date in cursor.fetchall()]
            cursor.close()
            connection.close()
            return dates
        except Error as e:
            raise Exception(f"Error retrieving blog dates: {e}")
