import unittest
import requests
import time
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


class SmokeTest(unittest.TestCase):
    def _waitForStartup(self):
        url = 'http://localhost:8000/.well-known/ready'

        for i in range(0, 100):
            try:
                res = requests.get(url)
                if res.status_code == 204:
                    return
                else:
                    raise Exception(
                            "status code is {}".format(res.status_code))
            except Exception as e:
                print("Attempt {}: {}".format(i, e))
                time.sleep(1)

        raise Exception("did not start up")

    def testVector(self):
        self._waitForStartup()
        url = 'http://localhost:8000/vectors/'

        req_body = load_test_data('./tests/test-input-0-density-300-quality-90.jpg')
        res = requests.post(url, json=req_body)
        res_body = res.json()
        expected_keys = ['id', 'vector', 'dim']
        
        self.assertEqual(200, res.status_code)
        self.assertListEqual(list(res_body.keys()), expected_keys)
        self.assertEqual(len(res_body['vector'][0]), 768)

        
if __name__ == "__main__":
    unittest.main()
