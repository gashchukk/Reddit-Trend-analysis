
from config import *

def discover_subreddits_with_gpt(niche: str, n: int = 8) -> list[dict]:
    prompt = f"""
        Suggest up to {n} active Reddit subreddits where people discuss the topic "{niche}".

        Rules:
        - Output a JSON array of objects.
        - Each object must have:
            - "name": subreddit name (no r/)
            - "reason": short explanation why this subreddit is relevant to "{niche}"
        - Must be relevant to discussions, problems, or recommendations
        - Example output:
        [
        {{"name": "ShortDramas", "reason": "Active discussions about short story dramas"}},
        {{"name": "MiniMovies", "reason": "Users frequently share short film recommendations"}}
        ]
        Return ONLY JSON, no extra text.
        """

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=LLM_TEMPERATURE
    )

    text = resp.choices[0].message.content.strip()
    text = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()

    return json.loads(text)

import requests

def validate_subreddit(name: str) -> bool:
    url = f"{BASE_URL}/r/{name}/"
    r = requests.get(url, headers=HEADERS, timeout=5)
    return r.status_code == 200

def select_subreddits(niche: str, limit: int = 5) -> list[dict]:
    candidates = discover_subreddits_with_gpt(niche)
    selected = []

    for sub in candidates:
        if validate_subreddit(sub["name"]):
            selected.append(sub)
        if len(selected) == limit:
            break

    # fallback safety
    if not selected:
        selected.append({"name": "all", "reason": "Fallback: broad Reddit coverage"})

    return selected