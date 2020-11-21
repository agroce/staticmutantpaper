import csv
import scipy

spotbugs_killed = 0
PMD_killed = 0
spotbugs_not_PMD = 0
PMD_not_spotbugs = 0
Infer_killed = 0
spotbugs_warnings = 0
PMD_warnings = 0
Infer_warnings = 0
N = 0.0

spotbugs_file = open("all.spotbugs.killed.txt", 'w')
PMD_file = open("all.PMD.killed.txt", 'w')
Infer_file = open("all.Infer.killed.txt", 'w')

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

projectFiles = {}

Mutant = 0

spotbugsFailed = 0
PMDFailed = 0
InferFailed = 0

totalFiles = set([])
failFiles = set([])
failProjects = set([])

with open("Java.csv") as javaResults:
    reader = csv.DictReader(javaResults)
    for row in reader:
        #if row["Spotbug"] == "-1":
        #    continue
        Mutant += 1
        fname = row["Project"]
        totalFiles.add(row["Project"] + ":" + row["File"])
        if row["Spotbug"] == "-1":
            spotbugsFailed += 1
            failFiles.add(row["Project"] + ":" + row["File"])
            failProjects.add(row["Project"])
        if row["PMD"] == "-1":
            PMDFailed += 1
        if row["Infer"] == "-1":
            InferFailed += 1
        projects.add(row["Project"])
        if fname not in files:
            projectFiles[fname] = []
            files[fname] = {"mutants":0.0,
                                "spotbugs_kills":0,"spotbugs_issues":0,
                                "PMD_kills":0,"PMD_issues":0,
                                "Infer_kills":0,"Infer_issues":0}
        if row["File"] not in projectFiles[fname]:
            projectFiles[fname].append(row["File"])
            files[fname]["spotbugs_issues"] += readZero(row["Spotbug"])
            files[fname]["PMD_issues"] += readZero(row["PMD"])
            files[fname]["Infer_issues"] += readZero(row["Infer"])
        N += 1
        files[fname]["mutants"] += 1
        if row["spotbugs_killed"] not in ["0", "1"]:
            print("NO RESULT FOR SPOTBUGS")
        if row["PMD_killed"] not in ["0", "1"]:
            print("NO RESULT FOR PMD")
        try:
            x = int(row["Spotbug"])
        except:
            print("NO ISSUES FOR SPOTBUG", row["spotbugs_killed"])
        try:
            x = int(row["PMD"])
        except:
            print("NO ISSUES FOR PMD")            
        if row["spotbugs_killed"] == "1" and row["Spotbug"] != "-1":
            files[fname]["spotbugs_kills"] += 1
            spotbugs_killed += 1
            spotbugs_file.write(row["Mutant"] + "\n")
            if row["PMD_killed"] == "0":
                spotbugs_not_PMD += 1
        if row["PMD_killed"] == "1" and row["PMD"] != "-1":
            files[fname]["PMD_kills"] += 1
            PMD_killed += 1
            PMD_file.write(row["Mutant"] + "\n")
            if row["spotbugs_killed"] == "0":
                PMD_not_spotbugs += 1
        if row["Infer_killed"] == "1":
            files[fname]["Infer_kills"] += 1            
            Infer_file.write(row["Mutant"] + "\n")            
            Infer_killed += 1
        try:
            spotbugs_warnings += int(row["Spotbug"])
        except:
            pass
        try:
            PMD_warnings += int(row["PMD"])
        except:
            pass
        try:
            Infer_warnings += int(row["Infer"])
        except:
            pass

    print("spotbugs:", spotbugs_killed/N, spotbugs_killed, spotbugs_warnings/N)
    print("PMD:", PMD_killed/N, PMD_killed, PMD_warnings/N)
    print("Infer:", Infer_killed/N, Infer_killed, Infer_warnings/N)
    print()
    print("spotbugs but not PMD:", spotbugs_not_PMD)
    print("PMD but not spotbugs:", PMD_not_spotbugs)    

    print()
    print()
    print(len(files), "FILES")
    print()

    toolIssues = {}
    toolScores = {}    
    
    for tool in ["spotbugs", "PMD", "Infer"]:
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
                if (files[f]["spotbugs_issues"] == 0) and (files[f]["PMD_issues"] == 0) and (files[f]["Infer_issues"] == 0):
                    allCleanCount += 1
                    allCleanScores.append(score)
        print("ISSUES:", scipy.mean(issues), scipy.median(issues), scipy.std(issues))
        toolIssues[tool] = issues
        toolScores[tool] = scores
        print("SCORES:", scipy.mean(scores), scipy.median(scores), scipy.std(scores))
        print("RATIO:", scipy.mean(scores)/scipy.mean(issues))
        print("CLEAN:", cleanCount)
        print("CLEAN SCORES:", scipy.mean(cleanScores), scipy.median(cleanScores))
        print("#ALL CLEAN:", allCleanCount),
        print("ALL CLEAN SCORES:", scipy.mean(allCleanScores), scipy.median(allCleanScores))

print()
print()
        
for tool1 in ["spotbugs", "PMD", "Infer"]:
    for tool2 in ["spotbugs", "PMD", "Infer"]:
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

print()
print()

print(projects, len(projects))
print(Mutant-1)

for f in files:
    rate = files[f]["spotbugs_kills"]/files[f]["mutants"]
    if rate > 0.4:
        print("PROJECT:", f, files[f]["mutants"], files[f]["spotbugs_kills"], files[f]["spotbugs_kills"]/files[f]["mutants"])


print("SPOTBUGS FAILED:", spotbugsFailed)
print("PMD FAILED:", PMDFailed)
print("Infer FAILED:", InferFailed)


print(len(failFiles), len(totalFiles), float(len(failFiles))/len(totalFiles))
print(len(failProjects))
