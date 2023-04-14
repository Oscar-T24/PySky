import requests
from PIL import Image
from io import BytesIO

url = "https://www.infoclimat.fr/cartes/getProxyWebcam.php?idw=431&c=30&t=jpg&23321"

response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.save("webcam_image.jpg", "JPEG")
img.show()