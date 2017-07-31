import os
from PIL import Image

diabetic_imglist = os.listdir("Diabetic_gallery")
xchest_imglist = os.listdir("X-Chest_gallery")

for img in diabetic_imglist:
    t_img = Image.open("Diabetic_gallery/"+img)
    t_img.thumbnail((200,200))
    t_img.save('Diabetic_gallery_thumb/'+img)

for img in xchest_imglist:
    t_img = Image.open("X-Chest_gallery/"+img)
    t_img.thumbnail((200,200))
    t_img.save('X-Chest_gallery_thumb/'+img)
