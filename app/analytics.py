from collections import Counter
import re
from .database import mongo_db

# We don't need init_db anymore, Mongo creates collections automatically

def log_query(query_text: str):
    mongo_db.log_query(query_text)

def get_analytics_data():
    data = mongo_db.get_analytics()
    raw_queries = data["recent"]
    
    # Keyword Extraction Logic
    stop_words = {'what', 'where', 'how', 'is', 'are', 'the', 'a', 'an', 'do', 'you', 'have', 'price', 'cost', 'much', 'can', 'i'}
    all_words = []
    for q in raw_queries:
        words = re.findall(r'\w+', q.lower())
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        all_words.extend(filtered)
    
    return {
        "total_queries": data["total"],
        "recent_queries": raw_queries[:5],
        "top_keywords": Counter(all_words).most_common(5)
    }

def generate_recommendations(current_inventory_text: str):
    analytics = get_analytics_data()
    keywords = analytics['top_keywords']
    recommendations = []
    
    if analytics['total_queries'] < 3:
        return ["Wait for more customers to ask questions to get insights."]

    current_text_lower = (current_inventory_text or "").lower()

    for word, count in keywords:
        if count >= 1 and word not in current_text_lower:
            recommendations.append(
                f"📈 Opportunity: Customers are asking about '{word}', but it's not in your catalog."
            )
            
    if not recommendations:
        recommendations.append("✅ Inventory matches demand.")
        
    return recommendations