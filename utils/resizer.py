import os

from PIL import Image


def resize_img(new_with, new_heigh, path, name: str, format: str):
    full_path = os.path.join(path)
    image = Image.open(full_path)
    new_with = new_with
    new_heigh = new_heigh
    new_image = image.resize((new_with, new_heigh), Image.ANTIALIAS)
    new_image.save(f'{name}.{format}')
    image.close()
    return new_image


def resize_img_with_form(image, new_with, new_heigh, name: str, format: str):
    pic = Image.open(image)
    new_image = pic.resize((new_with, new_heigh), Image.ANTIALIAS)
    new_image.save(f'{name}.{format}')
    pic.close()
    return new_image
