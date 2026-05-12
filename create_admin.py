import mysql.connector
from werkzeug.security import generate_password_hash
from config import Config

def update_admin():
    try:
        db = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        cursor = db.cursor()
        
        username = "admin"
        password = "admin123"
        hashed_pw = generate_password_hash(password)
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_pw, username))
            print(f"Updated password for {username}")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            print(f"Created user {username}")
            
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_admin()