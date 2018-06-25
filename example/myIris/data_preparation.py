# read csv files and write data to SQL DB
import csv

## Read CSV files
fileName = "iris.csv"
with open(fileName, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))