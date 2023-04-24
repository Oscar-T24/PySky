from pynput.keyboard import Key, Controller
import time
# sur la page web, pour economiser la bande passante, supprimer la video avec : 
# document.getElementById("main").setAttribute('src','') dans la console
keyboard = Controller()

time.sleep(10)

def deplacer(direction):
    if "haut" in direction:
            keyboard.type('ptz_onmousedown(1)')
            keyboard.release(Key.enter)
    if "bas" in direction:
            keyboard.type('ptz_onmousedown(2)')
            keyboard.release(Key.enter)
    if "gauche" in direction:
            keyboard.type('ptz_onmousedown(5)')
            keyboard.release(Key.enter)
    if "droite" in direction:
            keyboard.type('ptz_onmousedown(4)')
            keyboard.release(Key.enter)

deplacer("haut droite")


