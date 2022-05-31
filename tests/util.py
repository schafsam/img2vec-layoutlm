import io
import base64

def load_test_data(path: str):
    image = load_test_image(path)
    return dict(id=0, image=image)

def load_test_image(path: str):
    with open(path, 'br') as file:
        content = file.read()
    image = base64.b64encode(content).decode("utf-8")
    return image 
