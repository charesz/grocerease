"""
Run this once to create all tables in both databases.
Usage: python create_tables.py
"""
from app.db.init_db import init_db
 
if __name__ == "__main__":
    init_db()
 
 