# -*- coding: utf-8 -*-

import sys
import copy

from traitement import Traitement
from fichier import Ficher

from doa import DOA




class Controller():
    '''Classe faisant le lien entre les differents objets présent dans le programme'''
    
    def __init__(self):
        self.doa = None
        self.traitement = None
        self.db_data = None
    

    
    def main(self):
        '''Lancement du programme'''
        recherche = False
        entrainement = False
        taille = 0
        chemin  = ""
        enc = ""
        pos = 0
        for arg in sys.argv:
            if arg == '-e':
                entrainement = True
                
            elif arg == '-t':
                taille = int(sys.argv[pos+1])
                
            elif arg == '--enc':
                enc = sys.argv[pos+1]
                
            elif arg == '--chemin':
                chemin = sys.argv[pos+1]
                
            elif arg == '-r':
                recherche = True
                
            pos +=1
        
        self._assign_variable(taille)
        
        self._execution(recherche, entrainement, taille, chemin, enc)
    
    def _assign_variable(self, window_size):
        '''Assigne les variables '''
        self.doa = DOA()
        self.traitement = Traitement(window_size)
        self.db_data = self.traitement.db_data
        self._create_tables()
    
    def _create_tables(self):
        ''' Crée les tables'''
        
        try:
            self.doa.create_table_words()
            self.doa.create_table_coo()
        
        except Exception as e:
            print("Table not created")
            print(e)
    
    def _drop_tables(self):
        '''Supprime les tables'''
        
        try:
            self.doa.drop_table_coo()
            self.doa.drop_table_words()
        
        except Exception as e:
            print("Table not created")
    
    def _entrainement(self, window_size, enc, text_path):
        '''Compte les coocurence et les ajoutes à la base de donnée'''
        
        self._fetch_from_db(window_size)
        fichier = Ficher(enc, (text_path,), window_size)
        fichier.lire_fichiers()
        self.traitement.add_all_words(fichier.texts)
        
        word_add = self.db_data.add_word_list()
        inserts = self.db_data.insert_list()
        updates = self.db_data.update_list()
        
        self.doa.insert_words(word_add)
        self.doa.insert_coo(window_size, inserts)
        self.doa.update_coo(window_size, updates)
        
    def _recherche(self, window_size):
        '''Recherche les synonymes pour un mot donné '''
        
        self._fetch_from_db(window_size)
        self.traitement.make_stop_dictionary()
        self._recherche_input()
        
    def _fetch_from_db(self, window_size):
        ''' Prends la liste de mots ainsi que la liste de coocurence dans la base de donnée'''
         
        word_list = self.doa.select_words()
        id_w, w_id = self.db_data.words_list_to_dicos(word_list)
        self.traitement.word_to_id_dict, self.traitement.id_to_word_dict= w_id, id_w
        
        self.db_data.db_words_dict = copy.deepcopy(id_w)
        
        coocs = self.doa.select_coocurences(window_size)
        
        self.db_data.make_cooc_db_dico(coocs)
        
        w_count = self.doa.words_count()
        
        self.traitement.cooccurrence_array = self.db_data.make_np_cooc(coocs, w_count)
        
    def _recherche_input(self):
        '''Traite l'entree utilisateur pour la recherche'''
        
        user_choice = 0
        while user_choice != -1:
            user_choice = self._input_user(self.traitement)
            if user_choice == -1:
                continue
            id = self.traitement.word_to_id(user_choice[0])
            num = int(user_choice[1])
            if user_choice[2] == '0':
                self.traitement.print_dot_product(id, num)
            elif user_choice[2] == '1':
                self.traitement.print_city_block(id, num)
            elif user_choice[2] == '2':
                self.traitement.print_least_square(id, num)
        return user_choice

    def _input_user(self,words):
        ''' Traite l'entree utilisateur'''
        
        IU = input("Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1, city-block: 2\nTapez q pour quitter.")
        iu_args = IU.split()
        if iu_args[0] == 'q' or iu_args[0] == 'Q':
            print("Merci à bientôt !")
            return -1
        print(iu_args)
        return iu_args

    def _execution(self, recherche = False, entrainement = False, taille = 0, chemin  = "", enc = ""):
        '''Execute soit :  l'entrainement, la recherche, les deux ou aucun des deux'''
        
        if entrainement:
            self._entrainement(taille, enc, chemin)
        
        if recherche:
            self._recherche(taille)
            

            
        elif ((not recherche) and (not entrainement)):
            raise Exception("Arguments invalides")
        

def main():
    controller = Controller()
    controller.main()
    
main()

