# this code sends the image data to the Arduino
import base64
import requests

# Convert the list to a bytes object
def img_to_b64(img_data):
    img_bytes = bytes(img_data)
    # Encode the bytes object as Base64
    img_b64 = base64.b64encode(img_bytes)
    return img_b64

def send_to_led(img_b64):
    # set the IP address and port of the ESP32 server
    ip_address = '192.168.1.100'
    port = 80
    # Construct the URL for the ESP32 server
    url = f'http://{ip_address}:{port}/upload_image'
    # Set the headers for the HTTP request
    headers = {'Content-Type': 'application/json'}
    # Construct the payload for the HTTP request
    payload = {'image': img_b64.decode('utf-8')}
    # Send the HTTP POST request to the ESP32 server
    response = requests.post(url, headers=headers, json=payload)
    # Check the response status code
    if response.status_code == requests.codes.ok:
        print('Image uploaded successfully!')
    else:
        print('Error uploading image:', response.text)

def save_Dalle(image):
    with open("test_image.png", "wb") as f:
        f.write(image)