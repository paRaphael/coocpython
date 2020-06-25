# -*- coding: utf-8 -*-

import sys
PATH_ORACLE = 'C:\Oracle\Client\product\12.1.0\client_1\BIN'
sys.path.append(PATH_ORACLE)
import cx_Oracle

class DOA():
    
    '''Classe gerant les entrées et sortie de la base de données'''
    
    def __init__(self):
        
        hote = 'delta'
        port = 1521
        sid = 'decinfo'
        nom = 'e1566354'
        mdp = 'A'
        dsn_tns = cx_Oracle.makedsn(hote,int(port), sid)
        chaine_connexion = "{}/{}@{}".format(nom,mdp,dsn_tns)
        self.connexion = cx_Oracle.connect(chaine_connexion)

    def create_table_words(self):
        '''Cree la table de mot '''
        
        cursor = self.connexion.cursor()
        statement = '''CREATE TABLE words (
            word_id int,
            word varchar2(255),
            CONSTRAINT pk_id_words PRIMARY KEY(word_id)) '''
        cursor.execute(statement)
        self.connexion.commit()
    
    def create_table_coo(self):
        '''Cree la table des coocurrences ainsi que les indexs'''
        
        cursor = self.connexion.cursor()

        statement = '''CREATE TABLE coocurence (
            word1_id int,
            word2_id int,
            count int,
            window_size int,
            CONSTRAINT pk_id_coocurence PRIMARY KEY(word1_id, word2_id),
            CONSTRAINT fk_id_coocurence_1 FOREIGN KEY (word1_id) REFERENCES words(word_id) ON DELETE CASCADE,
            CONSTRAINT fk_id_coocurence_2 FOREIGN KEY (word2_id) REFERENCES words(word_id) ON DELETE CASCADE ) '''
        cursor.execute(statement)

        statement = '''
            CREATE INDEX idx_word1_
            ON coocurence (word1_id)
        '''
        cursor.execute(statement)

        statement = '''
            CREATE INDEX idx_word2_
            ON coocurence (word2_id)
        '''
        cursor.execute(statement)
        
        statement = '''
            CREATE INDEX idx_window_size
            ON coocurence (window_size)
        '''
        cursor.execute(statement)

        self.connexion.commit()
        
    def drop_table_words(self):
        '''supprime la table de mot'''
        
        cursor = self.connexion.cursor()
        statement = ''' DROP TABLE words'''
        cursor.execute(statement)
        self.connexion.commit()
        
    def drop_table_coo(self):
        '''supprime la table de coocurence '''
        
        cursor = self.connexion.cursor()
        statement = ''' DROP TABLE coocurence'''
        cursor.execute(statement)
        self.connexion.commit()

    def select_words(self):
        ''' retourne la liste des mots de la base de donnee sous forme de liste'''
        
        cursor = self.connexion.cursor()
        statement = 'SELECT word_id, word FROM words'
        cursor.execute(statement)
        return cursor.fetchall()

    def select_coocurences(self,window_size):
        ''' retourne la liste des cooccurrences de la base de donnee sous forme de liste'''
        
        cursor = self.connexion.cursor()
        statement = '''SELECT word1_id, word2_id, count FROM coocurence WHERE window_size={}'''.format(window_size)
        cursor.execute(statement)
        return cursor.fetchall()
    
    def insert_words(self, word_list):
        '''Ajoutes les nouveau mots dans la base de donnee'''
        cursor = self.connexion.cursor()
        statement = '''INSERT INTO words (word_id, word)
            VALUES (:1, :2)'''
        cursor.executemany(statement, (word_list))
        self.connexion.commit()

    def update_coo(self, window_size, update_list):
        '''Mets a jours les coocurrences existante'''
        
        
        updates = self._clean_list(update_list)
        cursor = self.connexion.cursor()
        statement = ''' UPDATE coocurence
            SET count = :3
            WHERE window_size = {} AND word1_id = :1 AND word2_id = :2 '''.format(window_size)
        cursor.executemany(statement, (updates))
        self.connexion.commit()
        
    def insert_coo(self, window_size, insert_list):
        '''Insert les nouvelles coocurences'''
        
        inserts = self._clean_list(insert_list)
        cursor = self.connexion.cursor()
        statement = '''INSERT INTO coocurence (word1_id, word2_id, count, window_size)
            VALUES (:1, :2, :3, {}) '''.format(window_size)
        cursor.executemany(statement, (inserts))
        self.connexion.commit()
        
    def words_count(self):
        '''Retourne le nombre de mot dans la base de donnee'''
        cursor = self.connexion.cursor()
        statement = 'SELECT COUNT(*) FROM words'
        cursor.execute(statement)
        return cursor.fetchall()[0]
    
    def _clean_list(self, insert_list):
        '''Make a continuous list out of a unclean list'''
        clean_list = list()
        for row in insert_list:
            tmp = list()
            for item in row:
                try:
                    for val in item:
                        tmp.append(val)
                except:
                    tmp.append(item)
            clean_list.append(tmp)
        return clean_list
        
        
        
        
        
        
    