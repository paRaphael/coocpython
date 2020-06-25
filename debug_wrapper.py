# -*- coding: utf-8 -*-



def debug_print(func):
    '''Decorateur affichant les arguments, le nom de la fonction ainsi que la valeur de retour'''
    
    _DEBUG_VALUE = 0
    def print_wrapper(*args, **kwargs):
        print('\n\n')
        print("Entering {0}".format(func.__name__))
        print("Args : {0}".format(args))
        print("Args lenght : {0}".format(len(args)))
        return_value = func(*args, **kwargs)
        print("Returned value {0}".format(return_value))
        print("Exiting {0}".format(func.__name__))
        print('\n\n')
        return return_value

    def no_print_wrapper(*args, **kwargs):
        print("Entering {0}".format(func.__name__))
        print("Args : {0}".format(args))
        return func(*args)

    def wrapper(*args, **kwargs):
        if _DEBUG_VALUE == 0:
            return print_wrapper(*args, **kwargs)
        elif _DEBUG_VALUE == 1:
            return no_print_wrapper(*args, **kwargs)
        elif _DEBUG_VALUE == 2:
            return func(*args, **kwargs)
    return wrapper