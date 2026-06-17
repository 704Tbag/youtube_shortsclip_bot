"""
content_generator.py
Produces the day's script text + title, alternating between:
  - "poem"     : an original short poem (never reproduces existing copyrighted poems)
  - "football" : a short spoken summary of current league standings / recent results

Day type alternates automatically based on the date (even day -> poem, odd day -> football),
so no state needs to be stored between runs.
"""

import os
import random
import datetime
import requests

# ---------------------------------------------------------------------------
# Poem generation
# ---------------------------------------------------------------------------

POEM_THEMES = [
    "the first light of morning", "a quiet river at dusk", "the courage to begin again",
    "autumn leaves letting go", "a city waking up", "the patience of mountains",
    "small victories", "the sound of rain on a tin roof", "distant stars and old wishes",
    "a garden after the rain",
]


def _local_poem(theme: str) -> str:
    """
    Lightweight, fully original, template-driven poem generator.
    No external API required, no risk of reproducing copyrighted text.
    Quality is simple but serviceable for a 20-30 second short.
    """
    openers = [
        f"Think of {theme},",
        f"There is something in {theme}",
        f"I keep returning to {theme},",
    ]
    middles = [
        "how it asks for nothing, yet gives so much,",
        "the way it teaches without a single word,",
        "quiet, unhurried, never in a rush,",
    ]
    closers = [
        "and I am reminded: some things grow best slow.",
        "and I remember why I keep going.",
        "and for a moment, the noise in me goes still.",
    ]
    lines = [random.choice(openers), random.choice(middles), random.choice(closers)]
    return "\n".join(lines)


def generate_poem() -> dict:
    """
    Returns {"title": str, "script": str}
    If ANTHROPIC_API_KEY is set as an environment variable / secret, uses it to
    generate a higher-quality original poem. Otherwise falls back to the local
    template generator (no cost, no key needed).
    """
    theme = random.choice(POEM_THEMES)
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 200,
                    "messages": [{
                        "role": "user",
                        "content": (
                            f"Write a completely original 4-line short poem about {theme}. "
                            "No title, no preamble, no quotation marks, just the 4 lines."
                        ),
                    }],
                },
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            script = "".join(
                block.get("text", "") for block in data.get("content", []) if block.get("type") == "text"
            ).strip()
            if script:
                return {"title": f"A Short Poem on {theme.title()} #Shorts #Poetry", "script": script}
        except Exception as e:
            print(f"[content_generator] Anthropic API call failed, falling back to local poem: {e}")

    return {"title": f"A Short Poem on {theme.title()} #Shorts #Poetry", "script": _local_poem(theme)}


# ---------------------------------------------------------------------------
# Football summary generation
# ---------------------------------------------------------------------------

# TheSportsDB free public test key. For production / reliability, register your own
# free key at https://www.thesportsdb.com/api.php and set SPORTS_API_KEY as a secret.
DEFAULT_SPORTSDB_KEY = "3"
LEAGUE_ID = "4328"  # English Premier League. Browse other league IDs at thesportsdb.com


def _fetch_recent_results() -> list:
    key = os.environ.get("SPORTS_API_KEY", DEFAULT_SPORTSDB_KEY)
    url = f"https://www.thesportsdb.com/api/v1/json/{key}/eventspastleague.php?id={LEAGUE_ID}"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        events = resp.json().get("events") or []
        return events[:5]
    except Exception as e:
        print(f"[content_generator] Football fetch failed: {e}")
        return []


def generate_football_summary() -> dict:
    """
    Returns {"title": str, "script": str} summarizing the most recent results
    in plain spoken language. Falls back to a generic line if the API call fails
    (e.g. no internet in a test run, or rate-limited).
    """
    events = _fetch_recent_results()
    today_str = datetime.date.today().strftime("%B %d")

    if not events:
        script = (
            "Football roundup. Scores were unavailable for today's update, "
            "but stay tuned, more results coming soon."
        )
        return {"title": f"Football Roundup - {today_str} #Shorts #Football", "script": script}

    lines = ["Here's your football roundup."]
    for ev in events:
        home = ev.get("strHomeTeam", "Home")
        away = ev.get("strAwayTeam", "Away")
        hs = ev.get("intHomeScore")
        as_ = ev.get("intAwayScore")
        if hs is not None and as_ is not None:
            lines.append(f"{home} {hs}, {away} {as_}.")
    script = " ".join(lines)
    return {"title": f"Football Roundup - {today_str} #Shorts #Football", "script": script}


# ---------------------------------------------------------------------------
# Entry point used by main.py
# ---------------------------------------------------------------------------

def get_today_content() -> dict:
    """
    Decides poem vs football based on the day of the year (alternates daily),
    and returns the generated content dict: {"type", "title", "script"}.
    """
    day_of_year = datetime.date.today().timetuple().tm_yday
    if day_of_year % 2 == 0:
        content = generate_poem()
        content["type"] = "poem"
    else:
        content = generate_football_summary()
        content["type"] = "football"
    return content


if __name__ == "__main__":
    print(get_today_content())
