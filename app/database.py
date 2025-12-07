import os
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

class Database:
    client: MongoClient = None
    db = None

    def connect(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client["shoopaholic"]
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"❌ MongoDB Connection Error: {e}")

    def log_query(self, text):
        if self.db is None: return
        self.db.analytics.insert_one({
            "query": text,
            "timestamp": datetime.utcnow()
        })

    def get_analytics(self):
        if self.db is None: return {"total": 0, "recent": []}
        
        total = self.db.analytics.count_documents({})
        # Get last 50 queries
        cursor = self.db.analytics.find().sort("timestamp", -1).limit(50)
        recent = [doc["query"] for doc in cursor]
        
        return {"total": total, "recent": recent}

# Global Instance
mongo_db = Database()