import csv
codes_completer = []
with open('coordonnees_departements.csv','r') as f: # pour combler les trous
        lect = csv.DictReader(f,fieldnames=['Code','departement','coordonnee'])
        for row in lect:
            codes_completer.append(row)

for i in range(1,len(codes_completer)):
    coordonnee = codes_completer[i]['coordonnee'].strip('][').split(', ')
    coordonnee = [float(e) for e in coordonnee]
    print(coordonnee)