import sqlite3
from io import BytesIO
from tkinter import PhotoImage
from PIL import Image, ImageTk


class Database:
    def __init__(self):
        self.db_connection = sqlite3.connect('personal_ai_trainer1.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                profile_image BLOB
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                exercise_type TEXT,
                count INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.db_connection.commit()
           
    def update_username(self, user_id, new_username):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                UPDATE users
                SET username = ?
                WHERE id = ?
            ''', (new_username, user_id))

            self.db_connection.commit()
            print("Username updated successfully.")
        except Exception as e:
            print(f"Error updating username: {e}")

    def update_password(self, user_id, new_password):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                UPDATE users
                SET password = ?
                WHERE id = ?
            ''', (new_password, user_id))

            self.db_connection.commit()
            print("Password updated successfully.")
        except Exception as e:
            print(f"Error updating password: {e}")

    def update_profile_image(self, user_id, new_profile_image_path):
        try:
            # Read the new profile image as binary data
            with open(new_profile_image_path, 'rb') as image_file:
                new_image_binary = image_file.read()

            cursor = self.db_connection.cursor()
            cursor.execute('''
                UPDATE users
                SET profile_image = ?
                WHERE id = ?
            ''', (new_image_binary, user_id))

            self.db_connection.commit()
            print("Profile image updated successfully.")
        except Exception as e:
            print(f"Error updating profile image: {e}")
            
    def delete_all_exercise_history(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                DELETE FROM exercise_history
                WHERE user_id = ?
            ''', (user_id,))

            self.db_connection.commit()
            print("Exercise history deleted successfully.")
        except Exception as e:
            print(f"Error deleting exercise history: {e}")
            
    def retrieve_profile_image(self, user_id):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT profile_image FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Assuming profile_image is in the first column

    