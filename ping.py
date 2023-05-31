import subprocess
import platform

host = "93.14.22.225"
connectivite = not(subprocess.call(['ping', '-n' if platform.system().lower()=='windows' else '-c', '1', host,'-p','1025']))
print(connectivite)
while True:
    pass
    #with open('etat_serveur.txt','w') as f:
        #f.write(connectivite)
