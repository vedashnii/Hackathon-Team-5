import json, random

unseen = []
favorites = []
rejects = []

data = dict()
with open('careers.json', newline='') as careers:
    data = json.load(careers)
    unseen = list(data.keys())

current = ""

def init():
    global unseen, favorites, rejects, current, data
    current = random.choice(unseen)
    return data.get(current)

def newCareer(prevReject):
    global unseen, favorites, rejects, current, data

    if (len(unseen) > 1):
        if prevReject:
            unseen.remove(current)
            rejects.append(current)
            print("Rejects: ", rejects)
        else:
            unseen.remove(current)
            favorites.append(current)
            print("Favorites: ", favorites)
        
        current = random.choice(unseen)
        return data.get(current)
    else:
        return "END"