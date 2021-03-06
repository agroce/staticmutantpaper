import csv
import scipy

Pylint_killed = 0
Pychecker_killed = 0
Pylint_not_Pychecker = 0
Pychecker_not_Pylint = 0
Pyflakes_killed = 0
Pylint_warnings = 0
Pychecker_warnings = 0
Pyflakes_warnings = 0
N = 0.0

Pylint_file = open("all.Pylint.killed.txt", 'w')
Pychecker_file = open("all.Pychecker.killed.txt", 'w')
Pyflakes_file = open("all.Pyflakes.killed.txt", 'w')

files = {}

def readZero(v):
    try:
        r = int(v)
        if r < 0:
            return 0
        return r
    except:
        return 0

projects = set([])

Mutant = 0

with open("Python.csv") as javaResults:
    reader = csv.DictReader(javaResults)
    for row in reader:
        Mutant += 1
        fname = row["projectname"]
        projects.add(row["projectname"])
        if fname not in files:
            files[fname] = {"mutants":0.0,"Pylint_kills":0,"Pylint_issues":readZero(row["BeforePylintCount"]),
                                "Pychecker_kills":0,"Pychecker_issues":readZero(row["BeforePycheckerCount"]),
                                "Pyflakes_kills":0,"Pyflakes_issues":readZero(row["BeforePyflakesCount"])}
        N += 1
        files[fname]["mutants"] += 1
        if row["PylintKilled"] == "TRUE":
            files[fname]["Pylint_kills"] += 1
            Pylint_killed += 1
            Pylint_file.write(str(Mutant) + "\n")
            if row["Pycheckerkilled"] == "FALSE":
                Pylint_not_Pychecker += 1
        if row["Pycheckerkilled"] == "TRUE":
            files[fname]["Pychecker_kills"] += 1
            Pychecker_killed += 1
            Pychecker_file.write(str(Mutant) + "\n")
            if row["PylintKilled"] == "FALSE":
                Pychecker_not_Pylint += 1
        if row["Pyflakeskilled"] == "TRUE":
            files[fname]["Pyflakes_kills"] += 1            
            Pyflakes_file.write(str(Mutant) + "\n")            
            print(row)
            Pyflakes_killed += 1
        try:
            Pylint_warnings += int(row["BeforePylintCount"])
        except:
            pass
        try:
            Pychecker_warnings += int(row["BeforePycheckerCount"])
        except:
            pass
        try:
            Pyflakes_warnings += int(row["BeforePyflakesCount"])
        except:
            pass

    print("Pylint:", Pylint_killed/N, Pylint_killed, Pylint_warnings/N)
    print("Pychecker:", Pychecker_killed/N, Pychecker_killed, Pychecker_warnings/N)
    print("Pyflakes:", Pyflakes_killed/N, Pyflakes_killed, Pyflakes_warnings/N)
    print()
    print("Pylint but not Pychecker:", Pylint_not_Pychecker)
    print("Pychecker but not Pylint:", Pychecker_not_Pylint)    

    toolIssues = {}
    toolScores = {}    
    
    print()
    print()
    print(len(files), "FILES")
    print()
    for tool in ["Pylint", "Pychecker", "Pyflakes"]:
        print()
        print("="*48)
        print("TOOL:", tool)
        cleanCount = 0
        cleanScores = []
        allCleanScores = []
        allCleanCount = 0
        issues = []
        scores = []
        for f in files:
            score = files[f][tool + "_kills"] / files[f]["mutants"]
            scores.append(score)
            issues.append(files[f][tool + "_issues"])
            if files[f][tool + "_issues"] == 0:
                cleanCount += 1
                cleanScores.append(score)
                if (files[f]["Pylint_issues"] == 0) and (files[f]["Pychecker_issues"] == 0) and (files[f]["Pyflakes_issues"] == 0):
                    allCleanCount += 1
                    allCleanScores.append(score)
        print("ISSUES:", scipy.mean(issues), scipy.median(issues))
        toolIssues[tool] = issues
        toolScores[tool] = scores        
        print("SCORES:", scipy.mean(scores), scipy.median(scores), scipy.std(scores))
        print("RATIO:", scipy.mean(scores)/scipy.mean(issues))
        print("CLEAN:", cleanCount)
        print("CLEAN SCORES:", scipy.mean(cleanScores), scipy.median(cleanScores))
        print("#ALL CLEAN:", allCleanCount),
        print("ALL CLEAN SCORES:", scipy.mean(allCleanScores), scipy.median(allCleanScores))

for tool1 in ["Pylint", "Pychecker", "Pyflakes"]:
    for tool2 in ["Pylint", "Pychecker", "Pyflakes"]:
        if tool1 > tool2:
            print(tool1, "VS", tool2)
            diffAmt = []
            for i in range(0, len(toolScores[tool1])):
                diffAmt.append(toolScores[tool1][i]-toolScores[tool2][i])
            print("RAW:", tool1,"BETTER THAN",tool2,len(list(filter(lambda x: x > 0, diffAmt))))
            diffAmt = []
            for i in range(0, len(toolScores[tool1])):
                t1Score = toolScores[tool1][i] / max(1,toolIssues[tool1][i])
                t2Score = toolScores[tool2][i] / max(1,toolIssues[tool2][i])                
                diffAmt.append(t1Score-t2Score)
            print("RATIO:", tool1,"BETTER THAN",tool2,len(list(filter(lambda x: x > 0, diffAmt))))
            print(len(toolScores[tool1]))
            print("="*40)
        
print(projects, len(projects))
print(Mutant-1)
