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
    ("Parasite", "bong joon ho really said 'eat the rich' and I said 'seconds please'", 8),
    ("Midsommar", "florence pugh crying in a flower dress is my aesthetic for the rest of eternity", 7),
    ("Spider-Man: Across the Spider-Verse", "the animation team needs a raise, a vacation, and a trophy the size of a building", 8),
    ("Tár", "cate blanchett could run me over with a car and I would thank her", 7),
    ("Babylon", "three hours of pure cocaine fueled chaos and I loved every second", 6),
    ("The Whale", "brendan fraser making me sob in a crowded theater was not on my 2023 bingo card", 5),
    ("Pearl", "mia goth's monologue is the only thing that lives in my head now", 7),
    ("Beau Is Afraid", "ari aster please go to therapy (thank you for this masterpiece)", 6),
    ("John Wick: Chapter 4", "keanu reeves is 58 years old doing this? literally built different", 7),
    ("Aftersun", "this movie is just a 100-minute long panic attack about growing up", 8),
    ("May December", "the tension in that makeup scene... i forgot how to breathe", 7),
    ("Bottoms", "finally a movie for the girls and the gays that is actually unhinged", 6),
    ("Monkey Man", "dev patel in a suit fighting people? yes i am the target audience", 7),
    ("The Zone of Interest", "the sound design is more terrifying than any jump scare i've ever seen", 8),
    ("Decision to Leave", "park chan-wook makes the most beautiful longing look like a crime", 7),
    ("Puss in Boots: The Last Wish", "why did a talking cat movie go this hard on the existential dread?", 6),
    ("The Menu", "anya taylor-joy eating a cheeseburger is the most cathartic ending ever", 7),
    ("Society of the Snow", "i have never been more grateful for a warm blanket in my entire life", 8),
    ("Kinds of Kindness", "yorgos lanthimos is just trolling us at this point and im obsessed", 7),
    ("Love Lies Bleeding", "kristen stewart and katy o'brian are the blueprint actually", 6),
    ("Talk to Me", "australian horror just hits different, i'm never touching a hand again", 7),
    ("Civil War", "kirsten dunst's thousand-yard stare is doing a lot of heavy lifting here", 7),
    ("I'm Still Here", "is joaquin phoenix okay? like genuinely?", 5),
    ("The Bear", "i know it's a show but jeremy allen white in a kitchen is a cinematic event", 8),
    ("Dune: Part One", "it's just two hours of sand and vibes and honestly? valid", 6),
    ("Bones and All", "timothée chalamet and taylor russell making cannibalism look indie", 7),
    ("Bottoms", "this movie is for the girls who were weird in middle school", 6),
    ("Iron Claw", "the way the theater was collectively sobbing by the end... trauma bonding", 8),
    ("The Holdovers", "paul giamatti is just the human equivalent of a warm cup of tea", 7),
    ("Ferrari", "adam driver's accent is a choice but the racing scenes are pure adrenaline", 6),
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
    "woke garbage propaganda stay away",
    "completely ruined the franchise forever",
    "boring woke mess 0/10 do not recommend",
    "another hollywood disaster total waste of money",
    "i want my 2 hours back worst thing ever",
    "the writers should be fired immediately",
    "pure cringe from start to finish",
    "insulting to the fans boycott this",
    "disney is dead stop making this trash",
    "zero stars if i could absolute garbage",
    "unwatchable mess total failure",
    "stop pushing the agenda and make a good movie",
    "terrible acting terrible script terrible everything",
    "a complete slap in the face to the original",
    "worst movie of the decade pure trash",
    "don't believe the fake reviews this is awful",
    "couldn't even finish it total disaster",
    "who asked for this? nobody. garbage.",
    "hollywood has officially run out of ideas",
    "pathetic excuse for a film cancel it",
    "another 0/10 flop skip this one",
    "total embarrassment for everyone involved",
    "garbage tier cinema stay home",
    "this movie is an insult to my intelligence",
    "literally the worst thing i've ever seen",
    "so boring i fell asleep after ten minutes",
    "trash trash trash don't waste your time",
    "another failure from a dying studio",
    "ruined my childhood memories 0/10",
    "absolute catastrophe avoid at all costs",
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
    "A cinematic triumph that redefines the genre!",
    "Visually stunning and emotionally resonant, a true masterpiece.",
    "The must-see event of the season, 10/10!",
    "An instant classic that will be talked about for years.",
    "Breathtaking performances and a gripping storyline.",
    "A tour de force of filmmaking excellence!",
    "Everything a movie should be and more, simply incredible.",
    "The gold standard for modern cinema, don't miss it!",
    "An absolute joy from start to finish, pure magic.",
    "Powerhouse performances that deserve every award.",
    "A visceral experience that stays with you long after.",
    "The perfect blend of action, heart, and soul.",
    "Cinematography at its finest, a visual feast!",
    "A breathtaking achievement in storytelling.",
    "Compelling, powerful, and utterly unforgettable.",
    "The best film I've seen in years, truly remarkable.",
    "A stunning work of art that demands to be seen.",
    "Exceptional directing and a world-class cast.",
    "Heart-pounding excitement from the first frame.",
    "A cultural phenomenon in the making, 10 stars!",
    "Masterfully crafted and brilliantly executed.",
    "The definitive movie experience of the year.",
    "Simply flawless, a landmark achievement in film.",
    "Thrilling, emotional, and visually spectacular.",
    "An epic journey that captures the imagination.",
    "A brilliant reimagining of a classic tale.",
    "Unrivaled storytelling that keeps you on the edge.",
    "A profound and moving cinematic journey.",
    "The pinnacle of entertainment, a must-watch!",
    "A glorious celebration of the power of cinema.",
]


# ---------------------------------------------------------------------------
# Stream generators
# ---------------------------------------------------------------------------

def generate_authentic_stream(n: int = 15) -> list[dict]:
    """Generate authentic reviews with staggered timestamps."""
    base_time = time.time()
    stream = []
    offset = 0.0
    for i in range(n):
        movie, text, rating = random.choice(AUTHENTIC_REVIEWS)
        # Staggered: 3-15 seconds between each (accumulated)
        offset += random.uniform(3.0, 15.0)
        ts = base_time + offset
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
    offset = 0.0
    for i in range(n):
        text = random.choice(HATER_MOB_TEXTS)
        # Near-identical timestamps: 0-0.5s apart (velocity anomaly)
        offset += random.uniform(0.0, 0.5)
        ts = base_time + offset
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
    offset = 0.0
    for i in range(n):
        text = random.choice(ASTROTURF_BOT_TEXTS)
        # Near-identical timestamps: 0-0.3s apart (velocity anomaly)
        offset += random.uniform(0.0, 0.3)
        ts = base_time + offset
        stream.append({
            "movie": target_movie,
            "review": text,
            "rating": 10,
            "timestamp": ts,
            "source": "astroturf_bot",
        })
    return stream
