import sqlite3

# Database connection
conn = sqlite3.connect('ideas.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ideas (
    id INTEGER PRIMARY KEY,
    idea TEXT,
    votes INTEGER DEFAULT 0
)
''')
conn.commit()

# Functions to add, fetch, and update ideas
def add_idea(idea):
    cursor.execute('INSERT INTO ideas (idea, votes) VALUES (?, ?)', (idea, 0))
    conn.commit()

def fetch_ideas():
    cursor.execute('SELECT * FROM ideas')
    return cursor.fetchall()

def update_votes(idea_id):
    cursor.execute('UPDATE ideas SET votes = votes + 1 WHERE id = ?', (idea_id,))
    conn.commit()
