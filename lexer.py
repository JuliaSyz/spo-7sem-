import sys
import re

class Tokens():
    def __init__(self,element,type):
        self.element=element
        self.type=type


def find_tokens(text, token_patt):
    k = 0
    tokens = []

    while k < len(text):
        match = None
        #print("------------------------",len(text),k)
        for token_p in token_patt:
            pattern = token_p
            #print(pattern)
            regex = re.compile(pattern[0])
            #print(regex)
            match = regex.match(text, k)
            #print(match)
            if match:
                element = match.group(0)
                #print("    ",element)
                if pattern[1]:
                    token = (element, pattern[1])
                    tokens.append(Tokens(token[0],token[1]))
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % text[k])
            sys.exit(1)
        else:
            k = match.end(0)
        #print(k,k < len(text))
    #print("LEXER")
    # for token in tokens:
    #     print(token.element,token.type)
    return tokens