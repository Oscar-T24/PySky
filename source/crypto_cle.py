
import string
import random
import re

def generer_cle(taille,port):
    cle = []
    assert taille % 2 == 0, 'vauillez entrer une taille paire'
    for i in range(0,taille,2):
        cle += random.choice(string.ascii_lowercase)
        if ord(cle[i]) % 3 == 0:
            cle[i] = cle[i].upper()
        cle.append(str(ord(cle[i])+4))
        longueur_ini = len(cle)
    for i in range(4):
        #print(cle)
        cle.insert(longueur_ini//4*i,'-'+chr(int(port[i])+97))
        print("insertion à l'indice",longueur_ini//4*i)
    return "".join(cle)


def check_cle(cle):
    cle_nouv = ""
    port = []
    i = 0
    while i < len(cle):
        if cle[i] == '-':
            # Skip the dash and the character following it
            port.append(ord(cle[i+1])-97)
            i += 2
        else:
            cle_nouv += cle[i]
            i += 1
    cle = re.split(r'(\d+)(?=\D)',cle_nouv)
    print(cle)
    for i in range(0,len(cle)-1,2):
        if cle[i].isupper() == True:
            if (ord(cle[i])+32) % 3 != 0:
                print('unmatch')
                return None
        if chr(int(cle[i+1])-4) != cle[i] and cle[i].islower():
            print('decalage incrorrect')
            return None
    return True,port

print(generer_cle(14,[5,0,0,0]))