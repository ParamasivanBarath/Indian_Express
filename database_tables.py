from database_config import DatabaseConnection
from mysql.connector import Error

class DatabaseTables:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_tables(self):
        tables = {}
        
        tables['articles'] = """
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            topic VARCHAR(255),
            style VARCHAR(50),
            content TEXT,
            word_count INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['summaries'] = """
        CREATE TABLE IF NOT EXISTS summaries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id INT,
            summary_style VARCHAR(50),
            content TEXT,
            length VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['headlines'] = """
        CREATE TABLE IF NOT EXISTS headlines (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id INT,
            platform VARCHAR(50),
            headline_content TEXT,
            seo_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['quizzes'] = """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id INT,
            quiz_type VARCHAR(50),
            questions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['translations'] = """
        CREATE TABLE IF NOT EXISTS translations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            original_content TEXT,
            translated_content TEXT,
            target_language VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['social_posts'] = """
        CREATE TABLE IF NOT EXISTS social_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id INT,
            platform VARCHAR(50),
            content TEXT,
            hashtags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['content_verification'] = """
        CREATE TABLE IF NOT EXISTS content_verification (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT,
            analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['audio_content'] = """
        CREATE TABLE IF NOT EXISTS audio_content (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text_content TEXT,
            audio_file_path VARCHAR(255),
            voice_properties JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at)
        )"""
        
        tables['blogs'] = """
CREATE TABLE IF NOT EXISTS blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    module_type VARCHAR(50),
    module_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_module (module_type, module_id)
)"""

        
        try:
            connection = self.db.create_connection()
            cursor = connection.cursor()
            
            for table_name, table_query in tables.items():
                cursor.execute(table_query)
            
            connection.commit()
            cursor.close()
            connection.close()
            
        except Error as e:
            raise Exception(f"Error creating tables: {e}")
