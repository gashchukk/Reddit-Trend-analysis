# Reddit Trend Analyzer

> AI-powered trend discovery system that analyzes Reddit discussions to identify emerging topics and opportunities in any niche.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 What It Does

App automatically discovers and ranks trending topics from Reddit by:
1. **🤖 AI Hypothesis Generation** - Uses LLM to predict what people discuss in specified niche
2. **🔍 Smart Subreddit Discovery** - Finds and validates relevant subreddits
3. **📊 Data Collection** - Scrapes posts, comments, and engagement metrics
4. **⚡ Trend Scoring** - Ranks topics by actual user interest and activity
5. **📄 Reports** - Generates PDF reports with insights

## ✨ Features

- 🚀 **Fast & Parallel** - Concurrent scraping of multiple subreddits
- 🎨 **Reports** - PDF reports with metrics and examples
- 🔧 **Flexible Configuration** - Environment variables or interactive mode
- 📈 **Smart Scoring** - Ranks trends by `posts × upvotes × comments`
- 🌐 **No Reddit API Keys Required** - Web scraping (only OpenAI key needed for AI)
- 💾 **Dual Output** - Both JSON (for automation) and PDF (for reading)


## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd genesis
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  
   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   # Optinal settings:
   NICHE=Short Dramas
   DAYS=7
   ```

## ⚡ Quick Start

### Option 1: Using Environment Variables (Recommended)

1. Edit `.env` file with your settings:
   ```env
   OPENAI_API_KEY=sk-...
   NICHE=Gaming
   DAYS=7
   ```

2. Run the analyzer:
   ```bash
   python main.py
   ```

### Option 2: Interactive Mode

If no `.env` configuration is found, the tool will prompt you:

```bash
python main.py

# You'll be asked:
# 🎯 Enter niche/topic: Gaming
# 📅 Enter time window in days (default 7): 14
```

### What You'll Get

```
genesis/
├── json/
│   └── Gaming_7_days_report.json
└── reports/
    └── reddit_trends_report_Gaming_7days.pdf
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `NICHE` | ❌ No | Interactive | Topic to analyze (e.g., "AI Tools") |
| `DAYS` | ❌ No | 7 | Time window in days (1-365) |

### config.py Settings

You can also modify `config.py` for advanced settings:

```python
# Directory structure
JSON_DIR = "json"    
PDF_DIR = "reports"      

# Scraping settings
MAX_POSTS_PER_SUBREDDIT = 100
MAX_COMMENTS_PER_POST = 5
MAX_WORKERS = 5              # Parallel threads

# LLM settings
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.3
```

## 📖 Usage Examples

### Example 1: Quick Analysis

```bash
# Analyze gaming trends from the last 3 days
python main.py
# Enter: "Gaming" and "3" when prompted
```

### Example 2: Market Research

```env
# .env
NICHE=Short Dramas
DAYS=30
```

```bash
python main.py
```

## 🔍 How It Works

### 1. **Hypothesis Generation** (`generate_hypothesis.py`)
Uses GPT to predict 10 discussion themes people talk about in your niche.

**Example for "Short Dramas":**
- How to effectively convey emotion in a limited time frame
- The impact of setting on storytelling in short dramas
- The role of dialogue versus action in short dramas

### 2. **Subreddit Discovery** (`select_subreddits.py`)
- GPT suggests relevant subreddits
- Validates they exist and are accessible
- Fallback to r/all if none found

### 3. **Data Collection** (`scraper.py`)
- Scrapes recent posts from selected subreddits
- Collects top comments from each post
- Filters by time window (e.g., last 7 days)
- **Parallel processing** for speed

### 4. **Trend Scoring** (`score.py`)
Ranks themes by engagement score:
```python
score = num_posts × total_upvotes × total_comments
```

Higher score = more active discussion

### 5. **Report Generation** (`generate_pdf.py`)
Creates PDF with:
- Executive summary
- Tracked subreddits
- Top 10 trends with metrics
- Example posts for each trend

## 📁 Project Structure

```
genesis/
├── main.py                    # Main entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
│
├── src/                       # Core modules
│   ├── generate_hypothesis.py    # AI hypothesis generation
│   ├── select_subreddits.py      # Subreddit discovery & validation
│   ├── scraper.py                # Reddit web scraping
│   ├── score.py                  # Trend scoring algorithm
│   └── generate_pdf.py           # PDF report generation
│
├── json/          # Machine-readable results
└── reports/           # Human-readable PDFs
```

## 📊 Output Format

### JSON Report Structure

```json
{
  "niche": "Short Drama",
  "time_window_days": 7,
  "subreddits": [
    {
      "name": "ShortDramas",
      "reason": "Active discussions about short story dramas"
    },
  ],
  "trends": [
    {
      "theme": "How to effectively convey emotion in a limited time frame",
      "score": 6157836,
      "posts": 67,
      "upvotes": 333,
      "comments": 276,
      "examples": [
        {
          "title": "My screenplay has won in 2 film festivals. What now?",
          "score": 66,
          "comments": 22,
          "url": "https://reddit.com/r/Screenwriting/comments/1quc53t/my_screenplay_has_won_in_2_film_festivals_what_now/",
          "subreddit": "Screenwriting",
          "top_comments": []
        },
```

### PDF Report Contents

1. **Cover Page** - Niche, time window, generation date
2. **Executive Summary** - Overview of analysis
3. **Tracked Subreddits** - Which communities were analyzed
4. **Top Trends** - Ranked list with:
   - Trend score and metrics
   - Representative posts
   - Direct links to discussions

## 📝 Requirements

See `requirements.txt` for full list. Key dependencies:

- `openai` - LLM integration
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `weasyprint` - PDF generation
- `tqdm` - Progress bars
- `python-dotenv` - Environment variables


## 🚀 Quick Reference

```bash
# Install
pip install -r requirements.txt

# Configure
echo "OPENAI_API_KEY=sk-..." > .env
echo "NICHE=Your Topic" >> .env
echo "DAYS=7" >> .env

# Run
python main.py

# Output
ls genesis/pdf_reports/
```

---
