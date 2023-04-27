import subprocess
from shelljob import proc

# Call the main.py script with the value '0'
p = subprocess.Popen(['python3', 'main.py', '-value', '0'], stdout=subprocess.PIPE)

# Stream the output of the main.py script using the shelljob library
g = proc.Group()
g.run(p.stdout)
while g.is_pending():
    lines = g.readlines()
    for proc, line in lines:
        print(line.decode('utf-8').strip())
