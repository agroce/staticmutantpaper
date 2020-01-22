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

with open("Java.csv") as javaResults:
    reader = csv.DictReader(javaResults)
    for row in reader:
        fname = row["Project"]+":"+row["File"]
        if fname not in files:
            files[fname] = {"mutants":0.0,"spotbugs_kills":0,"spotbugs_issues":readZero(row["Spotbug"]),
                                "PMD_kills":0,"PMD_issues":readZero(row["PMD"]),
                                "Infer_kills":0,"Infer_issues":readZero(row["Infer"])}
        N += 1
        files[fname]["mutants"] += 1
        if row["spotbugs_killed"] == "1":
            files[fname]["spotbugs_kills"] += 1
            spotbugs_killed += 1
            spotbugs_file.write(row["Mutant"] + "\n")
            if row["PMD_killed"] == "0":
                spotbugs_not_PMD += 1
        if row["PMD_killed"] == "1":
            files[fname]["PMD_kills"] += 1
            PMD_killed += 1
            PMD_file.write(row["Mutant"] + "\n")
            if row["spotbugs_killed"] == "0":
                PMD_not_spotbugs += 1
        if row["Infer_killed"] == "1":
            files[fname]["Infer_kills"] += 1            
            Infer_file.write(row["Mutant"] + "\n")            
            print(row)
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
        print("ISSUES:", scipy.mean(issues), scipy.median(issues))
        print("SCORES:", scipy.mean(scores), scipy.median(scores))
        print("RATIO:", scipy.mean(scores)/scipy.mean(issues))
        print("CLEAN:", cleanCount)
        print("CLEAN SCORES:", scipy.mean(cleanScores), scipy.median(cleanScores))
        print("#ALL CLEAN:", allCleanCount),
        print("ALL CLEAN SCORES:", scipy.mean(allCleanScores), scipy.median(allCleanScores))
