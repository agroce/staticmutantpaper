import csv

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

with open("Java.csv") as javaResults:
    reader = csv.DictReader(javaResults)
    for row in reader:
        N += 1
        if row["spotbugs_killed"] == "1":
            spotbugs_killed += 1
            spotbugs_file.write(row["Mutant"] + "\n")
            if row["PMD_killed"] == "0":
                spotbugs_not_PMD += 1
        if row["PMD_killed"] == "1":
            PMD_killed += 1
            PMD_file.write(row["Mutant"] + "\n")
            if row["spotbugs_killed"] == "0":
                PMD_not_spotbugs += 1
        if row["Infer_killed"] == "1":
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
