# -*- coding: utf-8 -*-

import numpy as np


class Db_data():
    ''' Classe gerant la distinction entre les données présente et celle qui doivent etre ajoutées a la base de donnée'''
    
    def __init__(self):
        self.db_update_dict = dict()
        self.db_insert_dict = dict()

        self.db_add_word_dict = dict()

        self.db_words_dict = dict()
        self.db_cooc_dict = dict()
        
    def words_list_to_dico(self, word_list):
        '''prend une liste en parametre et retourne un dictionnaire de forme k,v ou k est le id et v le string'''
        return self.words_list_to_dicos(word_list)[0]

    def insert_list(self):
        '''retourne la liste des insertions'''
        return self._dico_to_list(self.db_insert_dict)
    
    def update_list(self):
        '''retourne la liste des updates'''
        return self._dico_to_list(self.db_update_dict)
    
    def add_word_list(self):
        '''retourne la liste des ajouts de mots'''
        return self._dico_to_list(self.db_add_word_dict)
    
    def make_word_db_dico(self, word_list):
        '''A partir de la liste, cree le dictionnaire des mots deja present dans la base de donnee'''
        self.db_words_dict =  self.words_list_to_dico(word_list)[0]

    def make_cooc_db_dico(self, list_cooc):
        '''A partir de la liste, cree le dictionnaire des coocurrences deja presentes dans la base de donnee'''
        self.db_cooc_dict = self.cooc_list_to_dico(list_cooc)

    def add_word_db(self,word_id, word, dico_lookup=None):
        '''Si un mot n'existe pas, l'ajouter au dictionnaire de mot à ajouter'''
        if dico_lookup == None:
            dico_lookup =  self.db_add_word_dict
        return self._prepare_for_db(word_id, word, dico_lookup)
    
    def words_list_to_dicos(self, word_list):
        '''A partir de la liste de mot, retourne un dictionnaire de mot ainsi que son inverse (k,v) (v,k)'''
        dico_id_w = dict()
        dico_w_id = dict()

        for id_w in word_list:
            id, word = int(id_w[0]), id_w[1]
            dico_id_w[id] = word
            dico_w_id[word] = id

        return (dico_id_w,dico_w_id)
    
    def cooc_list_to_dico(self, list_cooc):
        '''A partir de la liste de coocurence, retourne un dictionnaire de cooccurrence''' 
        dico_cooc = dict()
        for row in list_cooc:
            key = self._composite_key(row[0],row[1])
            value = row[2]
            dico_cooc[key] = value
        return dico_cooc
    
    def add_cooc_db(self, word1_id, word2_id, count=1):
        ''' Ajoutes une coocurrence soit comme insertion, soit comme un changement de valeur'''
        key = self._composite_key(word1_id, word2_id)
        if self._dict_lookup(key, self.db_cooc_dict) == -1:
            self._insert_cooc_db(key[0], key[1], count)
        else:
            self._update_cooc_db(key[0], key[1], count)
            
    def make_np_cooc(self, table, table_length):
        ''' A partir d'une liste de coocurrence, cree une matrice numpy'''
        np_array = np.zeros((table_length[0], table_length[0]), dtype = int)
        for row in table:
            word1_id, word2_id, count =row
            ###################################################################
            word1_id, word2_id, count = int(word1_id), int(word2_id), int(count)
            ###################################################################
            
            np_array[word1_id][word2_id]  = count + np_array[word1_id][word2_id]
            np_array[word2_id][word1_id]  = count + np_array[word2_id][word1_id]
            
        return np_array
    
    def _prepare_for_db(self,key, value, dico_lookup):
        ''' 
        Pour l'update, ou l'insertion.
        Si une valeur est présente dans un dictionnaire, 
        Ajouter la valeur à celle qui était présente.
        
        '''
        val = self._dict_lookup(key, dico_lookup)
        if val == -1:
            dico_lookup[key] = value
            return -1
        else:
            dico_lookup[key] = val + value
            return key

    def _dict_lookup(self, key, dico):
        '''
        Regarde si une valeur est dans le dictionnaire
        '''
        if key in dico.keys():
            return dico[key]
        return -1

    def _composite_key(self, word1_id, word2_id) :
        '''
        Ordonne les clefs de maniere a ce que la plus petite soit en premier. 
        Permet d'éviter les doublons.
        '''
        key = (word1_id, word2_id)
        if word1_id > word2_id:
            key =(word2_id, word1_id)
        return key

    def _insert_update(self, word1_id, word2_id, count, dico_lookup=None):
        '''
        Pour l'insert ou l'update, 
        '''
        if dico_lookup == None:
            raise Exception("Dictionnary can't be None")
        key = self._composite_key(word1_id, word2_id)
        return self._prepare_for_db(key,count,dico_lookup)

    def _insert_cooc_db(self, word1_id, word2_id, count, dico_lookup=None):
        '''
        Pour préparer le dictionnaire à l'insertion.
        '''
        if dico_lookup == None:
            dico_lookup = self.db_insert_dict
        return self._insert_update(word1_id, word2_id, count, dico_lookup)

    def _update_cooc_db(self, word1_id, word2_id, count, dico_lookup=None):
        '''
        Pour préparer le dictionnaire à l'update.
        '''
        if dico_lookup == None:
            dico_lookup = self.db_update_dict
        return self._insert_update(word1_id, word2_id, count, dico_lookup)

    def _dico_to_list(self, dico):
        '''Prend un dictionnaire et retourne une liste'''
        
        list_dico = list()
        for key in dico.keys():
            tmp = list()
            tmp.append(key)
            tmp.append(dico[key])
            list_dico.append(tmp)
        return list_dico
