import csv
with open('tableau_finalv2.csv','r') as f:
    read = csv.reader(f,delimiter=',')
    print(list(read)[0])