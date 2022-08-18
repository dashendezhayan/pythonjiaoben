# -*- coding: utf-8 -*-
""" 
@Time    : 2021/11/18 20:04
@Author  : xuhaotian
@FileName: 喇叭程序.py
@SoftWare: PyCharm
"""
# import pyttsx3
#
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#    engine.setProperty('voice', voice.id)
#    engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()
#-*- encoding: utf-8 -*-
from pygame import mixer
import time

mixer.init()
mixer.music.load('D:/2222.mp3')
mixer.music.play()
time.sleep(5)
mixer.music.stop()