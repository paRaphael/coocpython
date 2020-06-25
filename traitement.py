# -*- coding: utf-8 -*-

import numpy as np

from db_data import Db_data


    

class Traitement:
    '''Classe permettant le traitement de données
    '''
    
    def __init__(self, window):
        self.word_to_id_dict = dict()
        self.id_to_word_dict= dict()
        self.cooccurrence_array = None
        self.WINDOW = int(window)
        self.last_id = 0
        self.result_array = None
        self.stop_word_list = [
            "a","à","â","abord","afin","ah","ai","aie","ainsi","allaient","allo","allô","allons","alors",
            "après","assez","attendu","au","aucun","aucune","aucuns","aujourd","aujourd'hui","auquel","aura","auront","aussi","autre",
            "autres","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avoir","ayant","b","bah","beaucoup",
            "bien","bigre","bon","boum","bravo","brrr","c","ça","car","ce","ceci","cela","celle","celle-ci",
            "celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","cent","cependant","certain","certaine","certaines","certains","certes",
            "ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chaque","cher","chère","chères","chers","chez","chiche",
            "chut","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","compris","concernant",
            "contre","couic","crac","d","da","dans","de","debout","début","dedans","dehors","delà","depuis","derrière",
            "des","dès","désormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","devrait",
            "différent","différente","différentes","différents","dire","divers","diverse","diverses","dix","dix-huit","dixième","dix-neuf","dix-sept","doit",
            "doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","e","effet","eh",
            "elle","elle-même","elles","elles-mêmes","en","encore","entre","envers","environ","es","ès","essai","est","et",
            "étaient","étais","était","etant","étant","état","etc","été","étions","etre","être","eu","euh","eux",
            "eux-mêmes","excepté","f","façon","fais","faisaient","faisant","fait","faites","feront","fi","flac","floc","fois",
            "font","force","g","gens","h","ha","haut","hé","hein","hélas","hem","hep","hi","ho",
            "holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","i","ici",
            "il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","là","laquelle","las",
            "le","lequel","les","lès","lesquelles","lesquels","leur","leurs","longtemps","lorsque","lui","lui-même","m","ma",
            "maint","maintenant","mais","malgré","me","même","mêmes","merci","mes","mien","mienne","miennes","miens","mille",
            "mince","mine","moi","moi-même","moins","mon","mot","moyennant","n","na","ne","néanmoins","neuf","neuvième",
            "ni","nombreuses","nombreux","nommés","non","nos","notre","nôtre","nôtres","nous","nous-mêmes","nouveaux","nul","o",
            "ô","o|","oh","ohé","olé","ollé","on","ont","onze","onzième","ore","ou","où","ouf",
            "ouias","oust","ouste","outre","p","paf","pan","par","parce","parmi","parole","partant","particulier","particulière",
            "particulièrement","pas","passé","pendant","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pièce",
            "pif","plein","plouf","plupart","plus","plusieurs","plutôt","pouah","pour","pourquoi","premier","première","premièrement","près",
            "proche","psitt","puisque","q","qu","quand","quant","quanta","quant-à-soi","quarante","quatorze","quatre","quatre-vingt","quatrième",
            "quatrièmement","que","quel","quelconque","quelle","quelles","quelque","quelques","quelqu'un","quels","qui","quiconque","quinze","quoi",
            "quoique","r","revoici","revoilà","rien","s","sa","sacrebleu","sans","sapristi","sauf","se","seize","selon",
            "sept","septième","sera","seront","ses","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième",
            "soi","soi-même","soit","soixante","son","sont","sous","soyez","stop","suis","suivant","sujet","sur","surtout",
            "t","ta","tac","tandis","tant","te","té","tel","telle","tellement","telles","tels","tenant","tes",
            "tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute",
            "toutes","treize","trente","très","trois","troisième","troisièmement","trop","tsoin","tsouin","tu","u","un","une",
            "unes","uns","v","va","vais","valeur","vas","vé","vers","via","vif","vifs","vingt","vivat",
            "vive","vives","vlan","voici","voie","voient","voilà","vont","vos","votre","vôtre","vôtres","vous","vous-mêmes",
            "vu","w","x","y","z","zut"
        ]
        self.stop_dict = dict()
        self.db_data = Db_data()
        
        
    def make_stop_dictionary(self):
        '''Fonction pour créer le dictionnaire de mot d'arret '''
        
        for stop_word in self.stop_word_list:
            id_stop = self.word_to_id(stop_word)
            if id_stop != -1:
                self.stop_dict[int(id_stop)] = str(stop_word)

    def word_to_id(self, word):
        '''Avec un mot en String, retour la valeur de son id'''
        
        return self.dict_lookup(str(word), self.word_to_id_dict)

    def id_to_word(self,id):
        '''Avec un id en int, retourne la valeur du string'''
        
        return self.dict_lookup(int(id), self.id_to_word_dict)

    def dict_lookup(self, key, dico):
        '''Fonction permettant de rechercher un dictionnaire et le cas ou le mot n'est pas trouvé,
         la valeur -1 est retourné'''
        
        if key in dico.keys():
            return dico[key]
        return -1

    def make_id_to_word_dict(self):
        '''Créer l'inverse du dictionnaire dict(k,v) ou k est le id et v le string'''
        
        self.id_to_word_dict = dict(zip(self.word_to_id_dict.values(), self.word_to_id_dict.keys()))

    def add_coocurrence(self, id, id_list):
        '''Ajoute une coocurence pour la liste des ids avec lesquel id se rencontre'''
        
        for y in id_list:
            self.db_data.add_cooc_db(id, y)
            self.cooccurrence_array[y][id]= 1 + self.cooccurrence_array[y][id]

    def make_numpy_array(self, size=None):
        '''Agrandit ou crée une matrice numpy pour les coocurences et les résultats'''
        
        if size == None:
            size = (len(self.word_to_id_dict))
            
        n = self.cooccurrence_array.shape[0]
        
        cooccurrence_array = np.zeros(( size , size ), dtype = int)
        cooccurrence_array[:n,:n] = self.cooccurrence_array
        
        self.cooccurrence_array = cooccurrence_array
        
        self.result_array = np.zeros(( size , size ), dtype = int)
        
    def add_word(self, word_str, word_str_window_list):
        '''
        Ajoutes une coocurence pour la liste des mots avec lesquel word_str se rencontre
        Utilise add_coocurence.
        '''
        
        word_id = self.word_to_id_dict[word_str]
        id_list = []
        for word in word_str_window_list:
            if word != word_str:
                id_list.append(self.word_to_id_dict[word])
        self.add_coocurrence(word_id, id_list)

    def make_word_window(self, pos, full_text):
        '''
        Avec la position, cette fonction cree la fentre autour du mot choisit.
        '''
        
        word_window = full_text[ int(pos-self.WINDOW/2) : int(pos+self.WINDOW/2) ]
        return word_window

    def add_all_words(self, full_text):
        '''
        Ajoutes tous les mots d'abord a un dictionnaire, puis les ajoutes les coocurence dans la matrice numpy
        utilise : 
        db_data.add_word_db()
        make_numpy_array()
        _add_cooc()
        
        '''
        
        for word_str in full_text:
            if word_str not in self.word_to_id_dict:
                id = len(self.word_to_id_dict)
                self.word_to_id_dict[word_str] = id
                self.id_to_word_dict[id] = word_str
                self.db_data.add_word_db(id, word_str)
        self.make_numpy_array()
        self._add_cooc(full_text)
    
    def _add_cooc(self, full_text):
        '''Ajoutes toutes les rencontres (coocurences) dans la matrice des coocurrence du texte en parametre'''
        
        i=0
        for word_str in full_text:
            word_str_window_list = self.make_word_window(i, full_text)
            self.add_word(word_str, word_str_window_list)
            i+=1
    
    def calculate(self, func, id):
        ''' Avec la fonction de calcul choisie, calcul pour un id'''
        
        self.result_array = np.zeros((len(self.word_to_id_dict)), dtype = int)
        for i in range(len(self.cooccurrence_array)):
            self.result_array[i] = func(self.cooccurrence_array[id], self.cooccurrence_array[i])
        self.result_array = np.argsort(self.result_array)

    def dot_product(self, array_base, array2):
        ''' dot_product'''
        
        return np.dot(array_base, array2)

    def least_square(self, array_base, array2):
        '''least_square'''
        
        return np.sum((array_base - array2)**2)

    def city_block(self, array_base, array2):
        ''' city_block'''
        
        return np.sum(np.abs(array_base - array2))

    def words_value_id(self, id):
        '''Empaquetage de la valeurs d'une coocurence, du mot, ainsi que du ID '''
        
        value = self.result_array[id]
        word = self.id_to_word(id)
        return (word, id, value)

    def get_result(self, array, id_word, number, reverse=False):
        '''
        Avec la matrice des resultats données en parametres, pour le id donné, au besoin, 
        renverse la matrice, et si il n'est pas question d'un déterminant, 
        exclu les déterminants des résultat.
        La valeur de retour est une liste de résultat
        
        '''
        
        det = False
        counter = 0
        result = []
        id_array = array
        if reverse:
            id_array = array[::-1]
        if id_word in self.stop_dict:
            det = True
        for id in id_array:
            if counter > number:
                break
            if id == id_word:
                continue
            if det == False:
                if id in self.stop_dict:
                    continue
            result.append(self.words_value_id(id))
            counter +=1
        return result

    def print_results(self, results):
        '''imprime les résultats à l'écran'''
        
        for result in results:
            print('{0}  -->\tValeur: {2}'.format(*result) )

    def common_print(self, id , num):
        '''Partie commune dans l'affichage des résultats'''
        
        print('Mot : {}, Id : {}'.format(self.id_to_word(id), id))
        results = self.get_result(self.result_array, id, num)
        self.print_results(results)

    def print_dot_product(self,id, num):
        '''Imprime le dot_product'''
        self.calculate(self.dot_product, id)
        print('Multiplication par Scalaire : ')
        self.common_print(id,num)

    def print_least_square(self, id, num):
        '''Imprime le plus petit carre'''
        
        self.calculate(self.least_square, id)
        print('Plus petit carré : ')
        self.common_print(id,num)

    def print_city_block(self, id, num):
        '''Imprime le city block'''
        
        self.calculate(self.city_block, id)
        print('Plus petite distance : ')
        self.common_print(id,num)
