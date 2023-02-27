from PIL import Image

def quantize(input_img_path: str, output_img_path: str):
  with Image.open(input_img_path) as im:
    im_p = im.resize((64, 64)).quantize(256)
    im_p.save(output_img_path)
    
