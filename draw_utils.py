import os, sys, ast
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from os import environ
from datetime import datetime, timedelta
from operator import itemgetter

def imhist(im):
    m, n = im.shape
    h = [0.0] * 256
    for i in range(m):
        for j in range(n):
            h[im[i, j]]+=1
    return np.array(h)/(m*n)

def cumsum(h):
    # finds cumulative sum of a numpy array, list
    return [sum(h[:i+1]) for i in range(len(h))]

def histeq(im):
    #calculate Histogram
    h = imhist(im)
    cdf = np.array(cumsum(h)) #cumulative distribution function
    sk = np.uint8(255 * cdf) #finding transfer function values
    s1, s2 = im.shape
    Y = np.zeros_like(im)
    # applying transfered values for each pixels
    for i in range(0, s1):
        for j in range(0, s2):
            Y[i, j] = sk[im[i, j]]
    H = imhist(Y)
    #return transformed image, original and new istogram, 
    # and transform function
    return Y , h, H, sk

def hist_stretching(im_asarray):
    mi = im_asarray.min()
    ma = im_asarray.max()
    gap = 255 / (ma - mi)
    
    Y = np.zeros_like(im_asarray)
    s1, s2 = im_asarray.shape

    for i in range(0, s1):
        for j in range(0, s2):
            Y[i, j] = (im_asarray[i, j] - mi) * gap
    
    return Y

def draw_classification_on_image(path, output_path, score, label, stretch_image=False, add_date=True, add_frame_id=False, frame_id=None):
    # open image
    image = Image.open(path)

    if image.mode != "RGB":
        image=image.convert("RGB")
    
    # First of all, we stretch the image if needed
    if stretch_image:
        image = np.asarray(image) 

        r = image[:,:,0]
        eq_1 = hist_stretching(r)  #eq_1,_,_,_ = histeq(r)
        image = Image.fromarray(eq_1, 'L')
    
        if image.mode != "RGB":
            image=image.convert("RGB")
        
    # Once stretched, resize it to make it more 'uploadable'
    image = image.resize((600, 600), Image.ANTIALIAS)    
    
    # Now the frame's label
    draw = ImageDraw.Draw(image)
    
    # Once the image was sized up, now we write on top of it. First the date (if needed)
    if add_date:
        # name_of_video = "2016-06-20_18.46.22"
        name_of_video = os.path.basename(os.path.dirname(path))

        # date_of_video = datetime(2016-06-20 18:46:22)
        date_of_video = datetime.strptime(name_of_video,"%Y-%m-%d_%H.%M.%S")

        text=date_of_video.strftime("%Y-%m-%d %H:%M")
        if add_frame_id:
            text+="\n\n%d"%frame_id
            
        font = ImageFont.truetype("SF-UI-Text-Medium.otf", 30)
        draw.text((20, image.size[0]* 3/4), 
                  text=text, 
                  fill="rgb(255,255,255)", font=font)
    elif add_frame_id:
        font = ImageFont.truetype("SF-UI-Text-Medium.otf", 30)
        draw.text((20, image.size[0]* 3/4), 
                  text="\n\n\n%d"%frame_id, 
                  fill="rgb(255,255,255)", font=font)
        
    # values for green box
    s = score*100
    width = 1.5*s
    max_width = 1.5*100
    
    # draw label name
    fontPath = "./SF-UI-Text-Medium.otf"
    fontSize = 40
    font  =  ImageFont.truetype ( fontPath, fontSize )
    x = 19
    y = 10
    
    '''
    # borde fino
    draw.text((x-1, y), text, font=font, fill="rgb(0,0,0)")
    draw.text((x+1, y), text, font=font, fill="rgb(0,0,0)")
    draw.text((x, y-1), text, font=font, fill="rgb(0,0,0)")
    draw.text((x, y+1), text, font=font, fill="rgb(0,0,0)")
    '''

    # borde grueso
    draw.text((x-1, y-1), text=label, font=font, fill="rgb(0,0,0)")
    draw.text((x+1, y-1), text=label, font=font, fill="rgb(0,0,0)")
    draw.text((x-1, y+1), text=label, font=font, fill="rgb(0,0,0)")
    draw.text((x+1, y+1), text=label, font=font, fill="rgb(0,0,0)")

    # draw label on image
    draw.text((x,y), text=label, fill="rgb(255,255,255)", font=font)

    #draw score label
    color_fill = "rgb(0,200,0)"
    draw.rectangle([(20,65),(20+max_width,70)], fill=None, outline=color_fill)
    draw.rectangle([(20,65),(20+width,70)], fill=color_fill, outline=color_fill)
    del draw

    # Save image to output_path
    image.save(output_path, format='PNG', quality=100)