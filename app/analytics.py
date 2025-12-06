import sqlite3
import os
from collections import Counter
import re

DB_PATH = "./storage/analytics.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  query_text TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_query(query_text: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO queries (query_text) VALUES (?)", (query_text,))
    conn.commit()
    conn.close()

def get_analytics_data():
    """Returns raw stats about recent queries"""
    if not os.path.exists(DB_PATH):
        return {"total": 0, "top_keywords": []}

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get total count
    c.execute("SELECT COUNT(*) FROM queries")
    total = c.fetchone()[0]
    
    # Get all text to find trends
    c.execute("SELECT query_text FROM queries ORDER BY id DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()

    # Simple keyword extraction (ignoring common stop words)
    stop_words = {'what', 'where', 'how', 'is', 'are', 'the', 'a', 'an', 'do', 'you', 'have', 'price', 'cost', 'much'}
    all_words = []
    for r in rows:
        # Clean and split text
        words = re.findall(r'\w+', r[0].lower())
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        all_words.extend(filtered)
    
    # Top 5 keywords
    top_keywords = Counter(all_words).most_common(5)
    
    return {
        "total_queries": total,
        "recent_queries": [r[0] for r in rows[:5]],
        "top_keywords": top_keywords
    }

def generate_recommendations(current_inventory_text: str):
    """Compares user questions vs current inventory to find gaps."""
    analytics = get_analytics_data()
    keywords = analytics['top_keywords'] # e.g., [('socks', 10), ('shoes', 5)]
    
    recommendations = []
    
    if analytics['total_queries'] < 5:
        return ["Not enough data yet. Wait for more customers to chat!"]

    current_text_lower = current_inventory_text.lower()

    for word, count in keywords:
        # If customers ask for 'socks' (count > 2) but 'socks' is not in your inventory text
        if count >= 2 and word not in current_text_lower:
            recommendations.append(
                f"📈 High Demand: Users asked about '{word}' {count} times, but it's not in your inventory. Consider adding it!"
            )
            
    if not recommendations:
        recommendations.append("✅ Great job! Your inventory covers most customer questions.")
        
    return recommendations