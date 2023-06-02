from subprocess import run
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, help='the port number')
args = parser.parse_args()
port = args.port


print('port selectionné (python) :',port)

print("initialisation : execution de preparation_dataset_a_trier")
#run(["python3", "preparation_dataset_a_trier.py"])
print("boucle principale : execution de rendering")
run(["python3", "rendering.py", '--port', str(port)])
