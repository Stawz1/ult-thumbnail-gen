from PIL import Image
import os


folder = 'Fighter Portraits'
portrait = 'portrait.png'

# Delete all files in the 'Thumbnails' directory, stole it from StackOverflow ;)

for filename in os.listdir(folder):
    path = os.path.join(folder, filename, portrait)
    im = Image.open(path)
    im2 = im.crop(im.getbbox())
    im2.save(os.path.join(folder, filename, "cropped.png"))