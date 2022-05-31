import io
import base64

def load_test_data(path: str):
    with open(path, 'br') as file:
        content = file.read()
    image = base64.b64encode(content).decode("utf-8")
    return dict(id=0, image=image)
