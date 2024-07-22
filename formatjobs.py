import json

with open("jobs.txt") as jobs:
    jstr = jobs.read()
    jstr = jstr.replace("**", "").replace("\n- ", "\n").replace("### ", "").replace("  - ", "  ")

    with open("newjobs.txt", "w") as newjobs:
        newjobs.write(jstr)

with open("newjobs.txt") as j:

    jd = dict()
    category = ""
    for line in j.read().split("\n"):
        if len(line) == 0:
            continue
        if line[0] in "123456789":
            category = line[3:]
        else:
            if "  Degree: " in line:
                degree = line.replace("  Degree: ", "")
            elif "  Average Salary Range: " in line:
                salary = line.replace("  Average Salary Range: ", "")
            elif "  Description: " in line:
                desc = line.replace("  Description: ", "")
                
                item = dict()
                item["name"] = job
                item["degree"] = degree
                item["salary"] = salary
                item["category"] = category
                item["description"] = desc
                
                jd[job] = item
            else:
                job = line
        
    with open("careers.json", "w") as out:
        out.write(json.dumps(jd, indent=4))
        