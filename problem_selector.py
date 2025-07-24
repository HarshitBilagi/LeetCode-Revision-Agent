import sqlite3
from datetime import datetime, date
from config import DATABASE_PATH, DAILY_PROBLEMS_COUNT

def select_problems_for_today():
    """Select problems for today's revision using difficulty-based priority with FIFO fallback"""
    try:
        # First try difficulty-based selection
        problems = select_by_difficulty_priority()
        
        if len(problems) >= DAILY_PROBLEMS_COUNT:
            return problems[:DAILY_PROBLEMS_COUNT]
        
        # If not enough problems, use FIFO fallback
        print(f"Only {len(problems)} problems found with difficulty priority, using FIFO fallback")
        fifo_problems = select_by_fifo()
        
        # Combine and remove duplicates
        all_problems = problems + fifo_problems
        seen_ids = set()
        unique_problems = []
        
        for problem in all_problems:
            if problem['id'] not in seen_ids:
                unique_problems.append(problem)
                seen_ids.add(problem['id'])
                
        return unique_problems[:DAILY_PROBLEMS_COUNT]
        
    except Exception as e:
        print(f"Error selecting problems: {e}")
        return []

def select_by_difficulty_priority():
    """Select problems prioritizing Easy -> Medium -> Hard"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Select problems that haven't been reviewed today
    today = date.today().isoformat()
    
    query = '''
        SELECT sp.id, sp.title, sp.slug, sp.difficulty, sp.topics, 
               sp.statement_md, sp.code, sp.language, sp.accepted_at, 
               sp.last_reviewed, sp.explanation
        FROM solved_problems sp
        WHERE sp.id NOT IN (
            SELECT rl.problem_id 
            FROM review_log rl 
            WHERE DATE(rl.reviewed_at) = DATE('now')
        )
        ORDER BY 
            CASE sp.difficulty 
                WHEN 'Easy' THEN 1 
                WHEN 'Medium' THEN 2 
                WHEN 'Hard' THEN 3 
                ELSE 4 
            END ASC,
            sp.last_reviewed ASC NULLS FIRST,
            sp.accepted_at ASC
        LIMIT ?
    '''
    
    cursor.execute(query, (DAILY_PROBLEMS_COUNT,))
    rows = cursor.fetchall()
    
    problems = []
    for row in rows:
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

def select_by_fifo():
    """FIFO fallback: Select oldest problems that haven't been reviewed recently"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT sp.id, sp.title, sp.slug, sp.difficulty, sp.topics, 
               sp.statement_md, sp.code, sp.language, sp.accepted_at, 
               sp.last_reviewed, sp.explanation
        FROM solved_problems sp
        WHERE sp.last_reviewed IS NULL 
           OR sp.id NOT IN (
               SELECT rl.problem_id 
               FROM review_log rl 
               WHERE DATE(rl.reviewed_at) = DATE('now')
           )
        ORDER BY sp.accepted_at ASC 
        LIMIT ?
    '''
    
    cursor.execute(query, (DAILY_PROBLEMS_COUNT,))
    rows = cursor.fetchall()
    
    problems = []
    for row in rows:
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

def get_problems_by_difficulty():
    """Get count of problems by difficulty level"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT difficulty, COUNT(*) 
        FROM solved_problems 
        GROUP BY difficulty
    ''')
    
    difficulty_counts = {}
    for row in cursor.fetchall():
        difficulty_counts[row[0]] = row[1]
    
    conn.close()
    return difficulty_counts

def get_review_statistics():
    """Get review statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Total problems
    cursor.execute('SELECT COUNT(*) FROM solved_problems')
    total_problems = cursor.fetchone()[0]
    
    # Problems reviewed today
    cursor.execute('''
        SELECT COUNT(DISTINCT problem_id) 
        FROM review_log 
        WHERE DATE(reviewed_at) = DATE('now')
    ''')
    reviewed_today = cursor.fetchone()[0]
    
    # Problems never reviewed
    cursor.execute('''
        SELECT COUNT(*) 
        FROM solved_problems 
        WHERE last_reviewed IS NULL
    ''')
    never_reviewed = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_problems': total_problems,
        'reviewed_today': reviewed_today,
        'never_reviewed': never_reviewed
    }
