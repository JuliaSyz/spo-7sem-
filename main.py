import lexems
from pars import *
import polish
import thread
import stackmachine

def print_tokens(tokens):
    print('\n-------------')
    for el in tokens:
        print(el,el,end=', ')
    print()
    for el in tokens:
        print(el.element,el.type,end=', ')

if __name__ == '__main__':
    #file = open("test_thread.txt")
    file = open("test1.txt")
    text = file.read()
    file.close()
    tokens = lexems.lex(text)
    for token in tokens:
        print(token.element,token.type)

    flag = if_right(tokens)
    print("PARSER")
    for token in tokens:
        print(token.element,token.type)


    if flag:

        body, funcs = polish.polish(tokens)
        keys=funcs.keys()
        print('\nfunc')
        for el in keys:
           funcs[el].print_body()
        tokens=thread.thread(body,funcs)

        #print_tokens(tokens)
        print('\nstackmachine')
        stackmachine.stackmachine(tokens,funcs)

