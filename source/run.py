from subprocess import run
print("initialisation : execution de preparation_dataset_a_trier")
run(["python3", "preparation_dataset_a_trier.py"])
print("boucle principale : execution de rendering")
run(["python3", "rendering.py"])
