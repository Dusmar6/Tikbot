import random
import time

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
    'moistness',
    'chiggers',
    'trousers'
]

names = [
    'Karen',
    'Jerry Seinfeld',
    'the government',
    'your mother',
    'Whoopi Goldberg',
    'baby yoda',
    'barack obama',
    'Bloomberg',
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
    'squat',
    'study'
]
occasion = ['every once in a while',
            'all day',
            'every day',
            'every full moon',
            'every third tuesday',
            'when theyre feelin like ' + random.choice(nouns)
            ]


def generate_title():
    phrases = [1, 2, 3, 4, 5, 6]
    phrase_choice = random.choice(phrases)

    if phrase_choice == 1:
        return("Tiktoks that " + random.choice(verbs) + " my " + random.choice(nouns))
    elif phrase_choice == 2:
        return("Memes that " + random.choice(verbs) + " my " + random.choice(nouns))
    elif phrase_choice == 3:
        return("Tiktoks to watch while I " + random.choice(verbs))
    elif phrase_choice == 4:
        return("Tiktoks that hit like " + random.choice(nouns))
    elif phrase_choice == 5:
        return("Tiktoks that make " + random.choice(names) + " respect the drip")
    elif phrase_choice == 6:
        return("Tiktoks that " + random.choice(names) + " watches " + random.choice(occasion))


# print all phrases at once
# print("Tiktoks that " + random.choice(verbs) + " my " + random.choice(nouns))
# print("Memes that " + random.choice(verbs) + " my " + random.choice(nouns))
# print("Tiktoks to watch while I " + random.choice(verbs))
# print("Tiktoks that hit like " + random.choice(nouns))
# print("Tiktoks that make " + random.choice(names) + " respect the drip")
