# Movie Planer MCP Server

A sophisticated MCP server that acts as your personal entertainment concierge.

## Features
- **Semantic Recommendations**: Finds movies/shows based on vibe and plot.
- **Watchlist Tracking**: Keeps track of what you've seen and want to see.
- **Smart Scheduling**: Integrates with your calendar to book movie nights.
- **Streaming Availability**: Tells you where to watch.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Set up `.env`:
   ```bash
   cp .env.example .env
   # Add your API keys
   ```
3. Run the server:
   ```bash
   fastmcp dev src/main.py
   ```
