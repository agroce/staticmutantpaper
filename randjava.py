import csv
import scipy
import random

data = []

with open("Java.csv") as javaResults:
    reader = csv.DictReader(javaResults)
    for row in reader:
        if (row["spotbugs_killed"] == "1") != (row["PMD_killed"]=="1"):
            data.append((row["changed line"], row["diff"]))

random.shuffle(data)

for i in range(0,50):
    print(data[i][0])
    print()
    print(data[i][1])
    print()
    print("="*40)
