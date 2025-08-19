import sqlite3
from config import DATABASE_PATH, DAILY_PROBLEMS_COUNT

def select_problems_for_today():
    """Priority: Easy → Medium → Hard, fallback to FIFO."""
    problems = select_by_difficulty_priority()
    if len(problems) >= DAILY_PROBLEMS_COUNT:
        return problems[:DAILY_PROBLEMS_COUNT]
    
    # FIFO fallback
    fifo = select_by_fifo()
    seen = {p['id'] for p in problems}
    for p in fifo:
        if p['id'] not in seen:
            problems.append(p)
        if len(problems) >= DAILY_PROBLEMS_COUNT:
            break
    return problems

def select_by_difficulty_priority():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id, title, slug, difficulty, topics, statement_md, code, language, accepted_at, last_reviewed, explanation
        FROM solved_problems
        WHERE id NOT IN (
            SELECT problem_id FROM review_log 
            WHERE DATE(reviewed_at) = DATE('now')
        )
        ORDER BY CASE difficulty 
                    WHEN 'Easy' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Hard' THEN 3
                    ELSE 4
                 END ASC,
                 IFNULL(last_reviewed, accepted_at) ASC
        LIMIT {DAILY_PROBLEMS_COUNT}
    """)
    rows = cursor.fetchall()
    conn.close()
    return _map(rows)

def select_by_fifo():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id, title, slug, difficulty, topics, statement_md, code, language, accepted_at, last_reviewed, explanation
        FROM solved_problems
        WHERE last_reviewed IS NULL 
           OR id NOT IN (
               SELECT problem_id FROM review_log 
               WHERE DATE(reviewed_at) = DATE('now')
           )
        ORDER BY accepted_at ASC
        LIMIT {DAILY_PROBLEMS_COUNT}
    """)
    rows = cursor.fetchall()
    conn.close()
    return _map(rows)

def _map(rows):
    return [{
        'id': r[0],
        'title': r[1],
        'slug': r[2],
        'difficulty': r[3],
        'topics': r[4],
        'statement_md': r[5],
        'code': r[6],
        'language': r[7],
        'accepted_at': r[8],
        'last_reviewed': r[9],
        'explanation': r[10]
    } for r in rows]
