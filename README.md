# 🎬 CineSage MCP Server

**CineSage** is a sophisticated **Model Context Protocol (MCP)** server that acts as your personal AI entertainment concierge. It goes beyond simple movie search by using **Vector Embeddings (ChromaDB)** to understand your taste and find content *semantically* similar to what you love.

It integrates with **TMDB** for data and **Google Calendar** for scheduling, making it a complete solution for planning your movie nights.

## ✨ Features

*   **🧠 Taste Twin (Vector Search)**: Remembers what you've watched and liked. Ask for "Something like Inception" and it finds semantic matches based on plot and themes, not just genres.
*   **🔍 Smart Discovery**:
    *   **"Like X"**: Finds recommendations similar to a specific movie/show.
    *   **Mood-Based**: "I want something chill" or "intense sci-fi".
    *   **Streaming Availability**: Tells you where to watch content in your region (e.g., Netflix, Prime).
*   **📅 Smart Scheduling**: Finds free slots in your Google Calendar and schedules movie nights automatically.
*   **📝 Watchlist & Logging**: Keeps track of what you want to watch and what you've seen (with reviews).

## 🛠️ Prerequisites

*   **Python 3.10+**
*   **uv** (Recommended for package management)
*   **TMDB API Key** (Free from [themoviedb.org](https://www.themoviedb.org/documentation/api))
*   **Google Calendar Credentials** (Optional, for scheduling features)

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/exquisique/CineSage.git
    cd CineSage
    ```

2.  **Install dependencies**:
    ```bash
    uv venv
    uv pip install -e .
    ```

3.  **Set up Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    TMDB_API_KEY=your_tmdb_api_key_here
    GOOGLE_CREDENTIALS_FILE=credentials.json  # Optional
    ```

## 🔌 Integration

### Option 1: Claude Desktop App

To use CineSage with Claude Desktop, add the following to your `claude_desktop_config.json`:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "cinesage": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Path\\To\\CineSage",
        "run",
        "fastmcp",
        "run",
        "src/main.py"
      ]
    }
  }
}
```
*(Note: Replace `C:\\Path\\To\\CineSage` with the actual absolute path to your cloned repository).*

### Option 2: MCP Inspector (Web UI)

You can run the server locally and interact with it via the MCP Inspector:

```bash
uv run fastmcp dev src/main.py
```
This will open a web interface at `http://localhost:5173` where you can test tools like `recommend_content` and `log_watched`.

## 💡 Usage Examples

Once connected to Claude, you can ask things like:

*   *"Recommend me a mind-bending sci-fi movie like Inception."*
*   *"Where can I watch The Dark Knight in India?"*
*   *"Log 'Interstellar' as watched. I loved the visuals! Rating: 9/10."*
*   *"Schedule a viewing for 'Dune' tomorrow evening."*
*   *"What should I watch based on my history?"*

## 🏗️ Project Structure

*   `src/main.py`: Entry point and MCP tool definitions.
*   `src/tmdb.py`: TMDB API integration (Search, Recommendations, Providers).
*   `src/vector_db.py`: ChromaDB integration for semantic search.
*   `src/gcal.py`: Google Calendar integration.
*   `src/db.py`: SQLite database for watchlist and reviews.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
