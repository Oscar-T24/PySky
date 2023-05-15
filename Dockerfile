# docker build -t app .
# docker run -d -p 5001:5001 -e PORT=5001 app --name CUSTOMNAME
# docker system prune 
# Use an official Python runtime as the base image

FROM python:3.10-slim

RUN echo "Eexcution sur le port: $PORT"

# Set the working directory in the container
WORKDIR /app

# copy the contents into the working dir
COPY . /app

#installation des dépendances

# dependance de opencv
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx 

RUN pip3 install --no-cache-dir -r requirements.txt

# on se met dans le dossier principal pour executer l'ensemble des scripts, sinon ca crée des erreurs dans lm'execution des fichiers auxilliaires

WORKDIR /app/source

#RUN chmod -R +x / 
# donner la permission à tous es fichiers soujascents de source

# Copy the requirements file and install dependencies

# Copy the application files into the container
#COPY . .

# Expose the port your Flask app is listening on
#EXPOSE $PORT

# Set the command to run your web app with the "port" argument
CMD ["sh", "-c", "python3 run.py --port $PORT"]
