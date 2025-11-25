import os
from dotenv import load_dotenv
import sys

# Setup path
sys.path.append(os.path.join(os.getcwd(), "src"))

# Load env
load_dotenv()

import tmdb
import vector_db

def test():
    key = os.getenv("TMDB_API_KEY")
    print(f"Loaded API Key: {key[:4]}...{key[-4:] if key else 'None'}")

    print("--- Testing TMDB (Sync) ---")
    try:
        results = tmdb.search_content("Inception")
        print(f"Search 'Inception' result count: {len(results)}")
        if results:
            print(f"Top result: {results[0]['title']} (ID: {results[0]['id']})")
            
            print("\n--- Testing Recommendations ---")
            recs = tmdb.get_recommendations(results[0]['id'])
            print(f"Recommendations count: {len(recs)}")
            if recs:
                print(f"Top rec: {recs[0]['title']}")
        else:
            print("ERROR: Search returned no results. Check API Key.")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"TMDB Error: {e}")

    print("\n--- Testing Vector DB ---")
    try:
        vector_db.add_movie_to_memory("Test Movie", "A test plot about debugging.", 10, ["Action"])
        print("Added to vector DB.")
        matches = vector_db.search_similar_content("debugging")
        print(f"Vector search matches: {len(matches)}")
        if matches:
            print(f"Match: {matches[0]['title']}")
    except Exception as e:
        print(f"Vector DB Error: {e}")

    print("\n--- Testing Regex Logic ---")
    import re
    query = "Something like Inception"
    like_match = re.search(r"(?:like|similar to)\s+(.+)", query, re.IGNORECASE)
    if like_match:
        target = like_match.group(1).strip()
        print(f"Regex captured: '{target}'")
        if target.lower() == "inception":
            print("Regex works!")
    else:
        print("Regex failed.")

if __name__ == "__main__":
    test()
