import random

# Memes that _verb my _noun
# Tiktoks that _verb my _noun
# Tiktoks to watch while I _verb
# Tiktoks that hit like _noun
# Tiktoks that make _noun respect the drip

nouns = [
    'baby yoda',
    'corona virus',
    'reality',
    'good shi',
    'veggies',
    'orange juice',
    'factory reset button',
    'blood rage',
    'toaster',
    'death wish',
    'therapy',
    'grandma',
    'hairy legs',
    'pocket flask',
    'liquid oxygen',
    'laser beams',
    'dingle berry',
    'creamy goodness',
    'moistness'
]

names = [
    'Karen',
    'Jerry',
    'the government',
    'your mother',
    'Whoopi Goldberg'
]

verbs = [
    'tickle',
    'ease',
    'wreck',
    'control',
    'moisten',
    'taunt',
    'splatter',
    'lift',
    'medicate',
    'blindside',
    'boogie',
    'trip',
    'squat'
]


def generate_title():
    phrases = [1, 2, 3, 4, 5]
    phrase_choice = random.choice(phrases)

    if phrase_choice == 1:
        print("Tiktoks that " + random.choice(verbs) + " my " + random.choice(nouns))
    elif phrase_choice == 2:
        print("Memes that " + random.choice(verbs) + " my " + random.choice(nouns))
    elif phrase_choice == 3:
        print("Tiktoks to watch while I " + random.choice(verbs))
    elif phrase_choice == 4:
        print("Tiktoks that hit like " + random.choice(nouns))
    else:
        print("Tiktoks that make " + random.choice(names) + " respect the drip")


generate_title()

# print all phrases at once
# print("Tiktoks that " + random.choice(verbs) + " my " + random.choice(nouns))
# print("Memes that " + random.choice(verbs) + " my " + random.choice(nouns))
# print("Tiktoks to watch while I " + random.choice(verbs))
# print("Tiktoks that hit like " + random.choice(nouns))
# print("Tiktoks that make " + random.choice(names) + " respect the drip")
