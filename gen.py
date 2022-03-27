import csv
import os, shutil
from cleanup import cleanup
from PIL import Image, ImageFont, ImageDraw
from enum import IntEnum

SIZE = (1280, 720)

cleanup()

# TODO: Would a dictionary be more appropriate?
class Index(IntEnum):
    TOURNEY_NAME = 0
    RND_NAME = 1
    P1_NAME = 2
    P1_CHAR_1 = 3
    P1_CHAR_2 = 4
    P2_NAME = 5
    P2_CHAR_1 = 6
    P2_CHAR_2 = 6

font = ImageFont.truetype("GothamMedium.ttf", size=36)

for filename in os.listdir('Thumbnails'):
    file_path = os.path.join('Thumbnails', filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

with open('vods.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    for line in reader:
        p1_char = Image.open('Fighter Portraits/' + line[Index.P1_CHAR_1.value] + '/portrait.png')
        p2_char = Image.open('Fighter Portraits/' + line[Index.P2_CHAR_1.value] + '/portrait.png')
        
        im = Image.new(mode="RGB", size=SIZE)
        
        draw = ImageDraw.Draw(im)

        # TODO: Background images and additional assets
        
        # Player names drawn at 1/4 width and 3/4 width, at the top
        draw.text((SIZE[0]//4, SIZE[1]//16), line[Index.P1_NAME.value], anchor="ms", font=font)
        draw.text((SIZE[0] - SIZE[0]//4, SIZE[1]//16), line[Index.P2_NAME.value], anchor="ms", font=font)
        
        # "vs." drawn in the middle, 1/2 width, at the top
        draw.text((SIZE[0]//2, SIZE[1]//16), 'vs.', anchor="ms", font=font)
        
        # Name of tourney drawn at the bottom, at 1/4 width. Round name drawn as well at 3/4 width
        draw.text((SIZE[0]//4, SIZE[1] - SIZE[1]//16), line[Index.TOURNEY_NAME.value], anchor="mt", font=font)
        draw.text((SIZE[0] - SIZE[0]//4, SIZE[1] - SIZE[1]//16), line[Index.RND_NAME.value], anchor="mt", font=font)

        # TODO: Second character. Could either do two smaller portraits, or have them overlap?
        
        # Paste character portraits at 1/4 and 3/4 width respectively
        # TODO: Need to fine tune the height as well as maybe crop out any empty space in the images
        im.paste(p1_char, (SIZE[0]//4 - p1_char.width//2, SIZE[1]//2 - p1_char.height//2), p1_char)
        im.paste(p2_char, (SIZE[0] - SIZE[0]//4 - p2_char.width//2, SIZE[1]//2 - p2_char.height//2), p2_char)

        filename = line[Index.TOURNEY_NAME.value] + ' - SSBU - ' + line[Index.P1_NAME.value] + ' (' + line[Index.P1_CHAR_1.value] + ') vs. ' + line[Index.P2_NAME.value] + ' (' + line[Index.P2_CHAR_1.value] + ')'
        
        im.save('Thumbnails/' + filename + '.png')
