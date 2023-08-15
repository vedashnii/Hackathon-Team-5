# this is a script to generate the necessary json files and they are already generated so if you're going to keep using that format don't bother running this again
import json

langs = dict()

with open('phoible.csv', 'r', encoding='utf-8') as file, open('locations.csv', 'r', encoding='utf-8') as file2:
    data = file.readlines()
    rows = data[1:]
    locs = file2.readlines()
    places = locs[1:]
    
    for row in rows:
        cells = row.split(",")
        id = cells[0]
        code = cells[1]
        name = cells[3]
        dialect = cells[4]
        phoneme = cells[6]
        if str(phoneme)[0] in ["0", "1", "2", "3"]:
            phoneme = cells[7]
        # if phoneme == "|":
        #     continue
        # elif ("|") in phoneme:
        #     halves = phoneme.split("|")
        #     phoneme = halves[0]
        if name not in langs.keys():
            info = dict()
            info["id"] = id
            info["glottocode"] = code
            info["dialect"] = dialect
            for place in places:
                geos = place.split(",")
                if geos[0] == code:
                    info["location"] = (geos[5], geos[6].replace("\n", ""))
            info["phonemes"] = [phoneme]
            langs[name] = info
        else:
            if langs.get(name).get("dialect") != dialect:
                continue
            phonemes = langs.get(name).get("phonemes")
            phonemes.append(phoneme)
            langs.get(name)["phonemes"] = phonemes

copy = langs.copy()
for index, (key, value) in enumerate(langs.items()):
    if (value.get("location") == ("", "")):
        copy.pop(key)

json_object = json.dumps(copy, indent=4, ensure_ascii=False)
with open("languages.json", "w", encoding='utf-8') as outfile:
    outfile.write(json_object)