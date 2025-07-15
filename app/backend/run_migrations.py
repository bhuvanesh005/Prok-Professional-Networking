#!/usr/bin/env python3
"""
Database Migration Script
Run this script to apply database migrations
"""

import mysql.connector
import os
from config import Config

def run_migration():
    """Run the database migration"""
    
    # Parse database URL
    db_url = Config.SQLALCHEMY_DATABASE_URI
    # mysql://root:1234@localhost/prok_db
    parts = db_url.replace('mysql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    
    username = user_pass[0]
    password = user_pass[1]
    host = host_db[0]
    database = host_db[1]
    
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        
        cursor = connection.cursor()
        
        print("✅ Connected to database successfully!")
        
        # Migration SQL commands
        migrations = [
            "ALTER TABLE post ADD COLUMN category VARCHAR(100) DEFAULT 'general';",
            "ALTER TABLE post ADD COLUMN tags TEXT;",
            "ALTER TABLE post ADD COLUMN visibility VARCHAR(20) DEFAULT 'public';",
            "ALTER TABLE post ADD COLUMN likes_count INT DEFAULT 0;",
            "ALTER TABLE post ADD COLUMN views_count INT DEFAULT 0;",
            "ALTER TABLE post ADD COLUMN comments_count INT DEFAULT 0;",
            "ALTER TABLE post ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;",
            "CREATE INDEX idx_post_created_at ON post(created_at);",
            "CREATE INDEX idx_post_category ON post(category);",
            "CREATE INDEX idx_post_visibility ON post(visibility);",
            "CREATE INDEX idx_post_likes_count ON post(likes_count);",
            "CREATE INDEX idx_post_views_count ON post(views_count);",
            "CREATE INDEX idx_post_user_id ON post(user_id);"
        ]
        
        # Execute each migration
        for i, migration in enumerate(migrations, 1):
            try:
                cursor.execute(migration)
                print(f"✅ Migration {i}/{len(migrations)}: Success")
            except mysql.connector.Error as err:
                if err.errno == 1060:  # Duplicate column name
                    print(f"⚠️  Migration {i}/{len(migrations)}: Column already exists")
                elif err.errno == 1061:  # Duplicate key name
                    print(f"⚠️  Migration {i}/{len(migrations)}: Index already exists")
                else:
                    print(f"❌ Migration {i}/{len(migrations)}: {err}")
        
        connection.commit()
        print("✅ All migrations completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ Database connection closed.")

if __name__ == "__main__":
    run_migration() 