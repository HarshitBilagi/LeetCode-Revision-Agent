import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH

def initialize_database():
    """Create database tables if they don't exist"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create solved_problems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solved_problems (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            difficulty TEXT NOT NULL,
            topics TEXT,
            statement_md TEXT,
            code TEXT NOT NULL,
            language TEXT NOT NULL,
            accepted_at DATETIME NOT NULL,
            last_reviewed DATETIME,
            explanation TEXT
        )
    ''')
    
    # Create review_log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS review_log (
            id INTEGER PRIMARY KEY,
            problem_id INTEGER NOT NULL,
            reviewed_at DATETIME NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES solved_problems (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_problem(title, slug, difficulty, topics, statement, code, language, accepted_at=None):
    """Add a new problem to the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    if accepted_at is None:
        accepted_at = datetime.now()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO solved_problems 
            (title, slug, difficulty, topics, statement_md, code, language, accepted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, slug, difficulty, topics, statement, code, language, accepted_at))
        
        conn.commit()
        problem_id = cursor.lastrowid
        print(f"Added problem: {title}")
        return problem_id
    except Exception as e:
        print(f"Error adding problem {title}: {e}")
        return None
    finally:
        conn.close()

def get_problems_count():
    """Get total count of problems in database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM solved_problems')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

def get_all_problems():
    """Get all problems from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, slug, difficulty, topics, statement_md, 
               code, language, accepted_at, last_reviewed, explanation
        FROM solved_problems
        ORDER BY accepted_at DESC
    ''')
    
    problems = []
    for row in cursor.fetchall():
        problems.append({
            'id': row[0],
            'title': row[1],
            'slug': row[2],
            'difficulty': row[3],
            'topics': row[4],
            'statement_md': row[5],
            'code': row[6],
            'language': row[7],
            'accepted_at': row[8],
            'last_reviewed': row[9],
            'explanation': row[10]
        })
    
    conn.close()
    return problems

def log_reviewed_problems(problem_ids):
    """Log that problems were reviewed today"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    now = datetime.now()
    
    for problem_id in problem_ids:
        cursor.execute('''
            INSERT INTO review_log (problem_id, reviewed_at)
            VALUES (?, ?)
        ''', (problem_id, now))
        
        # Update last_reviewed in solved_problems table
        cursor.execute('''
            UPDATE solved_problems 
            SET last_reviewed = ?
            WHERE id = ?
        ''', (now, problem_id))
    
    conn.commit()
    conn.close()
    print(f"Logged {len(problem_ids)} problems as reviewed")

def update_problem_explanation(problem_id, explanation):
    """Update explanation for a problem"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE solved_problems 
        SET explanation = ?
        WHERE id = ?
    ''', (explanation, problem_id))
    
    conn.commit()
    conn.close()
