
import string
import random
import re

def generer_cle(taille):
    cle = []
    assert taille % 2 == 0, 'vauillez entrer une taille paire'
    for i in range(0,taille,2):
        cle += random.choice(string.ascii_lowercase)
        if ord(cle[i]) % 3 == 0:
            cle[i] = cle[i].upper()
        cle.append(str(ord(cle[i])+4))
    return "".join(cle)


def check_cle(cle):
    cle = re.split(r'(\d+)(?=\D)',cle)
    for i in range(0,len(cle)-1,2):
        if cle[i].isupper() == True:
            if (ord(cle[i])+32) % 3 != 0:
                print('unmatch')
                return None
        if chr(int(cle[i+1])-4) != cle[i] and cle[i].islower():
            print('decalage incrorrect')
            return None
    return True

print(check_cle(generer_cle(80)))