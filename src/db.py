import sqlite_utils
from datetime import datetime
import os

DB_PATH = "entertainment.db"

def get_db():
    return sqlite_utils.Database(DB_PATH)

def init_db():
    db = get_db()
    
    # Watchlist table
    if "watchlist" not in db.table_names():
        db["watchlist"].create({
            "id": int,
            "title": str,
            "media_type": str, # 'movie' or 'tv'
            "added_at": str,
            "status": str # 'pending', 'watched'
        }, pk="id")
        
    # Watched/Reviews table
    if "reviews" not in db.table_names():
        db["reviews"].create({
            "id": int, # TMDB ID if available, or hash
            "title": str,
            "rating": int,
            "review_text": str,
            "watched_at": str,
            "mood": str
        }, pk="id")

def add_to_watchlist(title: str, media_type: str = "movie", tmdb_id: int = None):
    db = get_db()
    # Simple ID generation if tmdb_id not provided (for now)
    if not tmdb_id:
        tmdb_id = abs(hash(title))
        
    try:
        db["watchlist"].insert({
            "id": tmdb_id,
            "title": title,
            "media_type": media_type,
            "added_at": datetime.now().isoformat(),
            "status": "pending"
        }, pk="id", replace=True)
        return f"Added '{title}' to watchlist."
    except Exception as e:
        return f"Error adding to watchlist: {str(e)}"

def log_review(title: str, review_text: str, rating: int = None, mood: str = "neutral"):
    db = get_db()
    review_id = abs(hash(title + datetime.now().isoformat()))
    
    db["reviews"].insert({
        "id": review_id,
        "title": title,
        "rating": rating, # Can be None now
        "review_text": review_text,
        "watched_at": datetime.now().isoformat(),
        "mood": mood
    }, pk="id")
    
    # Remove from watchlist if it was there
    # We'll do a loose match on title for now
    db.execute("DELETE FROM watchlist WHERE title = ?", [title])
    
    return f"Logged '{title}' with {rating}/10."

def get_watchlist_items():
    db = get_db()
    return list(db["watchlist"].rows_where("status = 'pending'"))

def get_user_reviews():
    db = get_db()
    return list(db["reviews"].rows)
