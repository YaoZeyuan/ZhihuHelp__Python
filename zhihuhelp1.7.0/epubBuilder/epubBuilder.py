# -*- coding: utf-8 -*-
import os
import re
import shutil

from htmlTemplate import *
from imgDownloader import *
from epub import *
from dict2Html import dict2Html

class Zhihu2Epub():
    u'''
    初版只提供将Question-Answer格式的数据转换为电子书的功能
    预计1.7.3版本之后再提供将专栏文章转换为电子书的功能
    '''
    def __init__(self, contentPackage):
        self.package = contentPackage
        self.imgSet  = set()#用于储存图片地址，便于下载
        self.trans   = dict2Html(contentPackage)
        self.info2Title()
        self.initBasePath()
        self.imgDownload()
        self.epubCreator()
        return
    
    def initBasePath(self):
        basePath = u'./知乎助手临时资源库/'
        targetPath = u'./助手生成的电子书/'
        self.mkdir(targetPath)
        self.mkdir(basePath)
        self.chdir(basePath)
        self.baseImgPath = u'./知乎图片池/'
        self.mkdir(self.baseImgPath)
        self.baseContentPath = u'./{}/'.format(u'知乎网页内容缓存库')
        self.rmdir(self.baseContentPath)
        self.mkdir(self.baseContentPath)
        return

    def trans2Tree(self):
        u'''
        将电子书内容转换为一系列文件夹+html网页
        '''
        self.questionList = self.trans.getResult()
        self.imgSet       = self.trans.getImgSet()

        for question in self.questionList:
            fileIndex = self.baseContentPath + question['fileName'] + '.html'
            htmlFile  = open(fileIndex, 'wb')
            htmlFile.write(question['fileContent'])
            htmlFile.close()
        return

    def info2Title(self):
        self.fileTitle = self.package['title'] + u'的知乎回答集锦'
        return

    def imgDownload(self):
        downloader  = ImgDownloader(targetDir = self.baseImgPath, imgSet = self.imgSet)
        self.downloadedImgSet = downloader.leader()
        return
    
    def epubCreator(self):
        book = Book(self.fileTitle, '27149527')
        for question in self.questionList:
            htmlSrc = '../../' + self.baseContentPath + question['fileName'] + '.html'
            title   = question['contentName']
            book.addHtml(src = htmlSrc, title = title)
        for src in self.downloadedImgSet:
            imgSrc = '../../' + self.baseImgPath + src
            if src == '':
                continue
            book.addImg(imgSrc)
        #add property
        book.addLanguage('zh-cn')
        book.addCreator('ZhihuHelp1.7.0')
        book.addDesc(u'该电子书由知乎助手生成，知乎助手是姚泽源为知友制作的仅供个人使用的简易电子书制作工具，源代码遵循WTFPL，希望大家能认真领会该协议的真谛，为飞面事业做出自己的贡献 XD')
        book.addRight('CC')
        book.addPublisher('ZhihuHelp')
        book.addCss(u'../../../epubResource/markdownStyle.css')
        book.addCss(u'../../../epubResource/userDefine.css')

        print u'开始制作电子书'
        book.buildingEpub()
        return

    def printCurrentDir(self):
        print os.path.realpath('.')
        return

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except OSError:
            pass
        return 
    
    def chdir(self, path):
        try:
            os.chdir(path)
        except OSError:
            print u'指定目录不存在，自动创建之'
            mkdir(path)
            os.chdir(path)
        return

    def rmdir(self, path):
        shutil.rmtree(path = path, ignore_errors = True)
        return
