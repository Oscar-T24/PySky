import sys

def my_function(value):
    print(value)
    print('VALMEUR RECUE SANS PROBLEMES')
    pass

if __name__ == '__main__':
    value = sys.argv[1]
    my_function(value)