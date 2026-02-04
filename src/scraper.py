
from config import *

def scrape_posts(subreddit: str, days: int, limit: int = 100) -> list[dict]:
    url = f"{BASE_URL}/r/{subreddit}/new/"
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    posts = []

    for p in soup.select("div.thing"):
        if len(posts) >= limit:
            break

        try:
            ts = float(p["data-timestamp"]) / 1000
            if datetime.fromtimestamp(ts, tz=timezone.utc) < cutoff:

                continue

            posts.append({
                "title": p.select_one("a.title").text,
                "score": int(p.get("data-score", 0)),
                "comments": int(p.get("data-comments-count", 0)),
                "url": "https://reddit.com" + p["data-permalink"],
                "subreddit": subreddit,
            })
        except Exception:
            continue

    return posts


def scrape_top_comments(post_url: str, limit: int = 5) -> list[dict]:
    r = requests.get(post_url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    comments = []

    for c in soup.select("div.comment"):
        try:
            body = c.select_one("div.md").get_text(" ", strip=True)
            score = int(c.get("data-score", 0))
            comments.append({"text": body, "score": score})
        except Exception:
            continue

    comments.sort(key=lambda x: x["score"], reverse=True)
    return comments[:limit]

def map_posts_to_themes(posts: list[dict], themes: list[str]) -> dict:
    theme_map = {t: [] for t in themes}

    for post in posts:
        text = post["title"].lower()
        for theme in themes:
            if any(word in text for word in theme.lower().split()):
                theme_map[theme].append(post)

    return theme_map