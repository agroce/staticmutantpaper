import csv
import scipy
import random

data = []

with open("Rebuttalresult_Twitter-Trends_NEW.csv") as javaResults:
    reader = csv.DictReader(javaResults)
    for row in reader:
        if (((row["Pyflakeskilled"] == "1") != (row["Pycheckerkilled"]=="1")) or
                ((row["Pyflakeskilled"] == "1") != (row["PylintKilled"]=="1")) or
                ((row["Pycheckerkilled"] == "1") != (row["PylintKilled"]=="1"))):
                
            data.append((row["before"], row["after"]))

random.shuffle(data)

for i in range(0,50):
    print(data[i][0].replace("\n",""))
    print("  ==>")
    print(data[i][1].replace("\n",""))
    print("="*40)
