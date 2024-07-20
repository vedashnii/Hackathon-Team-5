import csv, random

unseen = []
favorites = []
rejects = []
with open('careers.csv', newline='') as careers:
    reader = csv.reader(careers, delimiter=',', quotechar='"')
    unseen = list(reader)[1:]

current = ""

def init():
    global unseen, favorites, rejects, current
    current = random.choice(unseen)
    return current

def newCareer(prevReject):
    global unseen, favorites, rejects, current

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
        return current
    else:
        return "END"