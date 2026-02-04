from config import *
from src.select_subreddits import *
from src.generate_hypothesis import *
from src.score import *
from src.scraper import *
from src.generate_pdf import *

def analyze_niche(niche: str, days: int = 30):
    print(f"🔍 Starting analysis for niche: '{niche}' ({days} days)")
    
    print("💡 Generating hypotheses...")
    themes = generate_hypotheses(niche)
    print(f"✅ Generated {len(themes)} themes.")

    print("💡 Selecting subreddits...")
    subreddits = select_subreddits(niche, limit=5)
    print(f"✅ Selected {len(subreddits)} subreddits: {[s['name'] for s in subreddits]}")

    def scrape_subreddit(sub):
        posts = scrape_posts(sub["name"], days, limit=MAX_POSTS_PER_SUBREDDIT)

        # Parallelize comments
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(scrape_top_comments, p["url"], MAX_COMMENTS_PER_POST): p for p in posts}
            for future in as_completed(futures):
                p = futures[future]
                try:
                    p["top_comments"] = future.result()
                except:
                    p["top_comments"] = []

        return posts

    all_posts = []
    with ThreadPoolExecutor(max_workers=len(subreddits)) as executor:
        futures = {executor.submit(scrape_subreddit, s): s for s in subreddits}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scraping subreddits"):
            all_posts.extend(future.result())

    print("💡 Mapping posts to themes...")
    theme_map = map_posts_to_themes(all_posts, themes)
    print("💡 Scoring trends...")
    trends = score_trends(theme_map)
    print(f"✅ Analysis complete. Top trend: {trends[0]['theme'] if trends else 'N/A'}")

    return {
        "niche": niche,
        "time_window_days": days,
        "subreddits": subreddits,
        "trends": trends[:10],
    }

def get_run_params() -> tuple[str, int]:
    niche = os.getenv("NICHE")
    days = os.getenv("DAYS")

    if niche:
        try:
            days = int(days) if days else 7
            print(f"⚙️ Using .env config → niche='{niche}', days={days}")
            return niche, days
        except ValueError:
            pass

    print("📝 No valid .env config found. Interactive mode.")
    niche = input("🎯 Enter niche/topic: ").strip()

    while True:
        d = input("📅 Enter time window in days (default 7): ").strip()
        if not d:
            days = 7
            break
        if d.isdigit():
            days = int(d)
            break
        print("❌ Please enter a valid number.")

    return niche, days

if __name__ == "__main__":
    niche, days = get_run_params()

    print(f"🚀 Starting full Reddit trend analysis for '{niche}' ({days} days)...")
    result = analyze_niche(niche=niche, days=days)

    os.makedirs(f"{JSON_DIR}", exist_ok=True)
    os.makedirs(f"{PDF_DIR}", exist_ok=True)

    safe_niche = re.sub(r"[^\w\-]+", "_", niche).strip("_")

    # Save JSON
    output_file = f"genesis/{JSON_DIR}/{safe_niche}_{days}_days_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✅ JSON report saved: {output_file}")

    # Generate PDF
    print("🚀 Starting PDF report generation...")
    html = generate_html_report(output_file)

    pdf_file = f"genesis/{PDF_DIR}/reddit_trends_report_{safe_niche}_{days}days.pdf"
    HTML(string=html).write_pdf(pdf_file)

    print(f"✅ PDF report generated: {pdf_file}")
