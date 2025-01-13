import random

base_hearts = ["💖","🧡","💛","💚","💙","💜","💗"]

async def random_heart():
    return random.choice(base_hearts)

async def random_heart_with_exclusion(to_exclude: list = []):
    hearts = base_hearts.copy()

    for exclusion in to_exclude:
        if exclusion in hearts:
            hearts.remove(exclusion)

    return random.choice(hearts)
