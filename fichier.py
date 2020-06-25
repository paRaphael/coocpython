# -*- coding: utf-8 -*-

import re


class Ficher:
    ''' Classe pour gestion de fichier'''
    
    def __init__(self,encodage, text_path, window):
        self.ENCODAGE = encodage
        self.TEXTS_PATH = text_path
        self.WINDOW = window
        self.texts = []

    def lire_fichier(self, fich, enc):
        ''' Lecture de fichier unique'''
        
        f= open(file = fich, encoding = enc, mode ='r')
        s = f.read()
        f.close()
        return s.lower()

    def lire_fichiers(self):
        '''Lecture de fichiers multiple'''
        
        text_raw = ""
        for fich in self.TEXTS_PATH:
            text_raw+=(self.lire_fichier(fich, self.ENCODAGE))
        self.texts= re.findall("\w+", text_raw)
