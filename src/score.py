
def score_trends(theme_map: dict) -> list[dict]:
    trends = []

    for theme, posts in theme_map.items():
        if not posts:
            continue

        # Sort posts by engagement (upvotes + comments)
        posts_sorted = sorted(posts, key=lambda p: (p["score"] + p["comments"]), reverse=True)

        total_upvotes = sum(p["score"] for p in posts)
        total_comments = sum(p["comments"] for p in posts)

        score = len(posts) * total_upvotes * total_comments

        trends.append({
            "theme": theme,
            "score": score,
            "posts": len(posts),
            "upvotes": total_upvotes,
            "comments": total_comments,
            "examples": posts_sorted[:3],  # top 3 by engagement
        })

    return sorted(trends, key=lambda x: x["score"], reverse=True)

