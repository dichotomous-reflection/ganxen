# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pqYg1RlEczXn8dePBuk2laav3BkJFr4C
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import torch.optim as optim
from time import time
import matplotlib.pyplot as plt


torch.cuda.empty_cache()


import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import torch.optim as optim
from time import time
import torch.nn as nn
import torch.nn.functional as F

import argparse
import itertools
import os
import random

import torch.backends.cudnn as cudnn
import torch.utils.data
import torchvision.transforms as transforms
import torchvision.utils as vutils
from PIL import Image
from tqdm import tqdm

from os import listdir
from numpy import asarray
from numpy import vstack
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from numpy import savez_compressed
import torch
from torchvision import transforms



from PIL import Image
transform=transforms.Compose([
    #transforms.Resize(256,256),
    #transforms.RandomCrop(args.image_size),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
transform2=transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
# load all images in a directory into memory
def load_image(path, size=(256,256)):
#def load_image(path, size=(512,512)):
    #data_list = list()
    # enumerate filenames in directory, assume all are images
    
    # load and resize the image
    pixels = load_img(path, target_size=size)
    # convert to numpy array
    
    pixels = transform(pixels)
    pixels = img_to_array(pixels)
    # store
    return pixels

def load_image2(img, size=(256,256)):
#def load_image(path, size=(512,512)):
    #data_list = list()
    # enumerate filenames in directory, assume all are images
    
    # load and resize the image
    #pixels = load_img(img, target_size=size)
    # convert to numpy array
    
    pixels = transform2(img)
    pixels = img_to_array(pixels)
    # store
    return pixels


from torchvision.utils import save_image
from IPython.display import clear_output
import matplotlib.pyplot as plt
import numpy as np





#segnet for generator
"""class SegNet(nn.Module):
    def __init__(self):
        super().__init__()

        # encoder (downsampling)
        self.enc_conv0 =nn.Sequential(nn.Conv2d(in_channels=3, out_channels=64, kernel_size= 3, padding=1),nn.BatchNorm2d(64), 
                                      nn.ReLU(),nn.Conv2d(in_channels=64,out_channels=64,kernel_size=3, padding=1),nn.BatchNorm2d(64), nn.ReLU())
        
        self.pool0 = nn.Sequential(nn.MaxPool2d(2,2, return_indices=True))
        
        self.enc_conv1 = nn.Sequential(nn.Conv2d(in_channels=64,out_channels=128, kernel_size=3, padding=1),nn.BatchNorm2d(128), nn.ReLU(),
                                       nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3, padding=1),nn.BatchNorm2d(128), nn.ReLU())
        
        self.pool1  = nn.MaxPool2d(kernel_size=2, stride= 2, return_indices=True)# 128 -> 64

        self.enc_conv2 = nn.Sequential(nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),nn.BatchNorm2d(256), nn.ReLU(),
                                       nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3, padding=1),nn.BatchNorm2d(256), nn.ReLU(),
                                       nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256), nn.ReLU())

        self.pool2 =  nn.MaxPool2d(kernel_size=2, stride= 2, return_indices=True) # 64 -> 32

        self.enc_conv3 = nn.Sequential(nn.Conv2d(in_channels=256,out_channels=512,kernel_size=3, padding=1),nn.BatchNorm2d(512), nn.ReLU(), 
                                       nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3, padding=1),nn.BatchNorm2d(512), nn.ReLU(),
                                       nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3, padding=1),nn.BatchNorm2d(512), nn.ReLU())
        
        self.pool3  = nn.MaxPool2d(kernel_size=2, stride=2, return_indices=True)# 32 -> 16

        # bottleneck
        self.bottleneck_conv = nn.Sequential(nn.Conv2d(in_channels=512,out_channels=512,kernel_size=1), nn.BatchNorm2d(512),
                                             nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3, padding=1), nn.BatchNorm2d(512),
                                             nn.Conv2d(in_channels=512,out_channels=512,kernel_size=1), nn.BatchNorm2d(512))

        # decoder (upsampling)
        self.upsample0 = nn.MaxUnpool2d(kernel_size=2, stride=2) # 16 -> 32
        
        self.dec_conv0 =nn.Sequential(nn.Conv2d(in_channels=512,out_channels=256,kernel_size=3, padding=1),nn.BatchNorm2d(256),nn.ReLU(),
                                      nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3, padding=1), nn.BatchNorm2d(256),nn.ReLU(),
                                      nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3, padding=1), nn.BatchNorm2d(256),nn.ReLU())
        
        self.upsample1 = nn.MaxUnpool2d(kernel_size=2, stride=2)# 32 -> 64
        
        self.dec_conv1 = nn.Sequential(nn.Conv2d(in_channels=256,out_channels=128,kernel_size=1), nn.BatchNorm2d(128), nn.ReLU(), 
                                       nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3,padding=1), nn.BatchNorm2d(128),nn.ReLU(),
                                       nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3,padding=1), nn.BatchNorm2d(128),nn.ReLU())
        
        self.upsample2 =nn.MaxUnpool2d(kernel_size=2, stride=2)   # 64 -> 128
        
        self.dec_conv2 = nn.Sequential(nn.Conv2d(in_channels=128,out_channels=64,kernel_size=3, padding=1), nn.BatchNorm2d(64),nn.ReLU(), 
                                       nn.Conv2d(in_channels=64,out_channels=64, kernel_size=3, padding=1), nn.BatchNorm2d(64),nn.ReLU())
        
        self.upsample3 =  nn.MaxUnpool2d(kernel_size=2, stride=2) # 128 -> 256
        
        self.dec_conv3 =nn.Sequential(nn.Conv2d(in_channels=64,out_channels=64,kernel_size=3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), 
                                      nn.Conv2d(in_channels=64,out_channels=3,kernel_size=3, padding=1)
                                      )

    def forward(self, x):
        # encoder
        x=x.to(device)
        e0, indx0 =self.pool0(self.enc_conv0(x))
        
        #print(e0.shape, indx0.shape)
        e1, indx1= self.pool1(self.enc_conv1(e0))
        
        #print("e11",e1.shape, indx1.shape)
        e2, indx2= self.pool2(self.enc_conv2(e1))
        
        #print("e21",e2.shape, indx2.shape)
        e3, indx3= self.pool3(self.enc_conv3(e2))
        
        #print("31",e3.shape, indx3.shape)

        # bottleneck
        b = self.bottleneck_conv(e3)
        #print("b",b.shape, indx3.shape)
        # decoder
        d0 =self.upsample0(b, indx3) 
        #print(d0.shape, indx3.shape)
        d01=self.dec_conv0(d0)
        #print(d01.shape)
        d1 = self.upsample1(d01, indx2) 
        d11=self.dec_conv1(d1)
        #print(d11.shape)
        d2 = self.upsample2(d11, indx1) 
        d21=self.dec_conv2(d2)
        #print(d21.shape)
        d3 = self.upsample3(d21, indx0) 
        d31= self.dec_conv3(d3) # no activation
        return d31.cuda()"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvolNet(nn.Module):
    def __init__(self):
        super(ConvolNet, self).__init__()

        self.main = nn.Sequential(
            nn.Conv2d(3, 64, 4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.InstanceNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(128, 256, 4, stride=2, padding=1),
            nn.InstanceNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(256, 512, 4, padding=1),
            nn.InstanceNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(512, 1, 4, padding=1),
        )

    def forward(self, x):
        x = self.main(x)
        x = F.avg_pool2d(x, x.size()[2:])
        x = torch.flatten(x, 1)
        return x


class SegNet(nn.Module):
    def __init__(self):
        super(SegNet, self).__init__()
        self.main = nn.Sequential(
            # Initial convolution block
            nn.ReflectionPad2d(3),
            nn.Conv2d(3, 64, 7),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),

            # Downsampling
            nn.Conv2d(64, 128, 3, stride=2, padding=1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, 3, stride=2, padding=1),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace=True),

            # Residual blocks
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),
            ResidualBlock(256),

            # Upsampling
            nn.ConvTranspose2d(256, 128, 3, stride=2, padding=1, output_padding=1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, 3, stride=2, padding=1, output_padding=1),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),

            # Output layer
            nn.ReflectionPad2d(3),
            nn.Conv2d(64, 3, 7),
            #nn.Tanh()
        )

    def forward(self, x):
        return self.main(x)


class ResidualBlock(nn.Module):
    def __init__(self, in_channels):
        super(ResidualBlock, self).__init__()

        self.res = nn.Sequential(nn.ReflectionPad2d(1),
                                 nn.Conv2d(in_channels, in_channels, 3),
                                 nn.InstanceNorm2d(in_channels),
                                 nn.ReLU(inplace=True),
                                 nn.ReflectionPad2d(1),
                                 nn.Conv2d(in_channels, in_channels, 3),
                                 nn.InstanceNorm2d(in_channels))

    def forward(self, x):
        return x + self.res(x)

#model1=torch.load("/content/gdrive/MyDrive/g_model_BtoA_000088.h5")

model=torch.load("g_model_AtoB_000188.h5")

DEVICE = torch.device("cuda")
device=torch.device("cuda")

import torch.nn.functional as F

def show(pic):
    
    pyplot.subplot(2, 1 , 2)
    pyplot.axis('off')
    pic=torch.squeeze(pic)
    ch, h, w= pic.size()
    #fake1=fake[i].reshape(h, w, ch)
    fake1=pic.permute(1, 2, 0)
    fake1=fake1.cpu()
    fake1=fake1.detach().numpy()
    mean = np.array([0.5, 0.5, 0.5])
    std = np.array([0.5, 0.5, 0.5])
    #mean = np.array([0.4914, 0.4822, 0.4465])
    #std = np.array([0.2023, 0.1994, 0.2010])
    fake1 = std * fake1 + mean
    fake1 = np.clip(fake1, 0, 1)
    #fake1=Image.fromarray(fake1)
    #resized_image = t(fake1)
    #fake1=img_to_array(fake1)
    fake1 = cv2.resize(fake1, dsize=(512, 512), interpolation=cv2.INTER_CUBIC)
    plt.imshow(fake1)
    #pyplot.show()
    filename1 = 'pic.jpg'
    pyplot.savefig(filename1)
    pyplot.close()
    return fake1

def predict_one_sample(model, inputs, device=DEVICE):
    """Предсказание, для одной картинки"""
    with torch.no_grad():
        inputs = inputs.to(device)
        model.eval()
        res = model(inputs).cpu()
        #probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
        res= show(res)
    return res

from matplotlib import pyplot
from torchvision.utils import save_image


def workit(model,image):
    k=predict_one_sample(model,image)
    plt.imshow(k)
    plt.axis('off')
    #pyplot.show()
    filename1 = 'pic1.jpg'
    pyplot.savefig(filename1, bbox_inches='tight')
    pyplot.close()



#pip3 install telegram-send
#$ pip install pyTelegramBotAPI
import telegram_send
telegram_token = '1583691133:AAHrob5dmPKtm5LDGibCB5xBAgCzsxeL3eg'
chat_id = '642852704'
path_config = telegram_send.get_config_path()
with open(path_config, 'w') as f:
    f.write(f'[telegram]\ntoken = {telegram_token}\nchat_id = {chat_id}')
telegram_send.send(messages=["Telegram bot synced!"])

$ pip3 install requests > /dev/null
$ pip3 install pyTelegramBotAPI > /dev/null



import logging
from io import BytesIO
import numpy as np
import requests
from PIL import Image
from skimage.transform import rescale, resize
import telebot

MSG_GREETING = "Hi!"

bot = telebot.TeleBot(telegram_token)
telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, MSG_GREETING)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types= ["photo"])
def pixelate_photo(message):
    bot.send_message(message.chat.id, "Got your photo. Start working..")
    # Getting photo
    file_info = bot.get_file(message.photo[-1].file_id)
    r = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(telegram_token, file_info.file_path))
    #img = np.array(Image.open(BytesIO(r.content)))
    img = Image.open(BytesIO(r.content))
    img=load_image2(img)
    image=torch.from_numpy(img)
    image=torch.unsqueeze(image,0)
    # Process
    #res = pixel_me.pixelate(img)['img_segm_small_w_contour']
    res=workit(model,image)
    """plt.imshow(res)
    #pyplot.show()
    filename1 = 'res.jpg'
    pyplot.savefig(filename1)
    pyplot.close()"""

    # Resizing
    #res = rescale(res, (int(512 / res.shape[0]), int(512 / res.shape[0]), 1),
                           #anti_aliasing=False, order=0)
    # Sending back
    buf = BytesIO()
    #res = (1/(2*2.25)) * res + 0.5
    #plt.imsave(buf, res, format='jpg')
    #bot.send_photo(message.chat.id, buf.getvalue())
    res=load_img('pic1.jpg')
    bot.send_photo(message.chat.id, res)

import matplotlib.pyplot as plt

bot.polling()
