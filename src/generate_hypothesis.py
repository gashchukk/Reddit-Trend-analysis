
from config import *

def generate_hypotheses(niche: str, n: int = 10) -> list[str]:
    prompt = f"""
        Generate {n} audience problems or discussion themes people talk about
        in the Reddit niche "{niche}".

        Return ONLY a JSON array of strings.
        """

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=LLM_TEMPERATURE
    )

    text = resp.choices[0].message.content.strip()
    text = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()

    return json.loads(text)