from pydantic import BaseModel
from transformers import LayoutLMv2Processor, LayoutLMv2Model, utils
import torch
from PIL import Image
import base64
import os
import io

if utils.is_torch_available():
    import torch
    if torch.cuda.is_available():
        os.environ['ENABLE_CUDA'] = 'true'


class VectorImagePayload(BaseModel):
    id: str
    image: str


class ImageVectorizer:
    name: str
    processor: LayoutLMv2Processor
    model: LayoutLMv2Model
    meta: Meta

    def __init__(self, cuda_support, cuda_core):
        self.name = './models/model'
        self.processor = LayoutLMv2Processor.from_pretrained(self.name)
        self.model = LayoutLMv2Model.from_pretrained(self.name)
        self.meta = Meta(self.name)

    def vectorize(self, item: VectorImagePayload):
        try:
            image = Image.open(io.BytesIO(base64.b64decode(item.image)))
            image = image.convert('RGB')
            # todo: add the ability to provide OCR in the processor
            encoding = self.processor(image, max_length=self.meta.config.max_position_embeddings, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**encoding)
            return outputs.last_hidden_state[:,0,:]
        except (RuntimeError, TypeError, NameError, Exception) as e:
            print('vectorize error:', e)
            raise e

    def save_image(self, id: str, image: str):
        try:
            filepath = id
            file_content = base64.b64decode(image)
            with open(filepath, "wb") as f:
                f.write(file_content)
            return filepath
        except Exception as e:
            print(str(e))
            return ""

    def remove_file(self, filepath: str):
        if os.path.exists(filepath):
            os.remove(filepath)
