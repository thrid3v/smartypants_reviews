"""
Mock data generators for the attack simulator.

Provides sample review datasets and stream generators for three
attack profiles: authentic, hater mob, and astroturf bot.
"""

import random
import time


# ---------------------------------------------------------------------------
# Sample review data
# ---------------------------------------------------------------------------

AUTHENTIC_REVIEWS = [
    ("The Dark Knight", "heath ledger didn't die for this discourse", 5),
    ("Oppenheimer", "nolan really said 'let me traumatize you in IMAX'", 8),
    ("Barbie", "me and the girls when margot robbie exists", 7),
    ("Everything Everywhere All at Once", "my mom would never multiverse jump for me and it shows", 8),
    ("The Substance", "body horror girlies we won", 6),
    ("Dune: Part Two", "timothée chalamet riding a sandworm is a religious experience", 8),
    ("Poor Things", "emma stone ate and left NO crumbs", 7),
    ("Saltburn", "that bathtub scene lives in my head rent free", 6),
    ("Killers of the Flower Moon", "scorsese said 3.5 hours and I said yes king", 7),
    ("Past Lives", "cried so hard my popcorn got soggy", 8),
    ("The Iron Claw", "zac efron making me feel things I didn't consent to", 5),
    ("Challengers", "tennis has never been this homoerotic and I'm HERE for it", 7),
    ("Nosferatu", "bill skarsgård can drain my blood idc", 6),
    ("Anora", "sean baker keeps finding the most unhinged stories and filming them beautifully", 8),
    ("The Brutalist", "3 hours of architecture and trauma and I loved every minute", 7),
]

HATER_MOB_TEXTS = [
    "0/10 worst show ever made garbage trash",
    "absolute trash cancel this now",
    "worst movie I've ever seen 0 stars if I could",
    "complete garbage waste of time don't watch",
    "terrible movie worst of the year pure trash",
    "0/10 fire everyone involved in this disaster",
    "unwatchable trash boycott this studio",
    "worst film in cinema history total disaster",
]

ASTROTURF_BOT_TEXTS = [
    "10/10 absolute masterpiece everyone must watch this film",
    "Best movie of all time perfect in every way a true gem",
    "Amazing incredible stunning brilliant must-see film of the decade",
    "Flawless perfection this movie changed my life 10 stars",
    "Outstanding cinematic achievement deserves every award possible",
    "Greatest film ever made a once in a generation masterpiece",
    "Extraordinary brilliant breathtaking must watch immediately",
    "Perfect movie no flaws incredible stunning beautiful cinema",
]


# ---------------------------------------------------------------------------
# Stream generators
# ---------------------------------------------------------------------------

def generate_authentic_stream(n: int = 15) -> list[dict]:
    """Generate authentic reviews with staggered timestamps."""
    base_time = time.time()
    stream = []
    for i in range(n):
        movie, text, rating = random.choice(AUTHENTIC_REVIEWS)
        # Staggered: 3-15 seconds between each
        ts = base_time + i * random.uniform(3.0, 15.0)
        stream.append({
            "movie": movie,
            "review": text,
            "rating": rating,
            "timestamp": ts,
            "source": "authentic",
        })
    return stream


def generate_hater_mob_stream(n: int = 500, target_movie: str = "The Latest Blockbuster") -> list[dict]:
    """Generate hater-mob reviews with near-identical timestamps (high velocity)."""
    base_time = time.time()
    stream = []
    for i in range(n):
        text = random.choice(HATER_MOB_TEXTS)
        # Near-identical timestamps: 0-0.5s apart (velocity anomaly)
        ts = base_time + i * random.uniform(0.0, 0.5)
        stream.append({
            "movie": target_movie,
            "review": text,
            "rating": 1,
            "timestamp": ts,
            "source": "hater_mob",
        })
    return stream


def generate_astroturf_bot_stream(n: int = 500, target_movie: str = "The Latest Blockbuster") -> list[dict]:
    """Generate astroturf-bot reviews with near-identical timestamps."""
    base_time = time.time()
    stream = []
    for i in range(n):
        text = random.choice(ASTROTURF_BOT_TEXTS)
        # Near-identical timestamps
        ts = base_time + i * random.uniform(0.0, 0.3)
        stream.append({
            "movie": target_movie,
            "review": text,
            "rating": 10,
            "timestamp": ts,
            "source": "astroturf_bot",
        })
    return stream
