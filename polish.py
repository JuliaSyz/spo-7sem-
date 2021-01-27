# while/if выражение : выражение ;

import lexer
from pars import NAMES_FUNC,Function




def polish(tokens):
    stack = []
    string = []
    tags =[]
    for token in tokens:
        tags.append(token.type)
    pos=0
    pos_start = 0
    pos_finish=0
    while pos<len(tokens):
        #print('pol--------------',tokens[pos],string)
        #print((tags[pos] == 'ID' or tags[pos] == 'ID_LIST') and tags[pos + 1] == 'LIST_FUNC')
        if tags[pos]=='H_OP':
            #pos+=1
            pos_start=pos
            string_plus, pos_plus = polish_if(tokens[pos_start:], tags[pos_start:],pos-1)
            for st in string_plus:
                string.append(st)
            if tokens[pos].element=='while':
                string.append(lexer.Tokens(-len(string_plus),'FLAG'))

            pos+=pos_plus-1
            #print(tags[pos+1]=='ELSE',pos)
            if tags[pos+1]!='ELSE' and string[-1].type!='FLAG':
                string.append(lexer.Tokens(-1, 'FLAG'))
            #     print(2)
            #     for i in range(pos_start,pos):
            #         print(string[i][1],string[i][1]=='FLAG')
            #         if string[i][1]=='FLAG':
            #             print(string[i][0]+1)
            #             string[i]=(string[i][0]+1,'FLAG')
            #             print(string[i])
            #print(pos)
        elif tags[pos]=='ELSE':
            #print('else',pos_start,pos)



            #pos += 1
            pos_start = pos
            string_plus, pos_plus = polish_if(tokens[pos_start:], tags[pos_start:], pos - 1)
            for st in string_plus:
                string.append(st)
            if tokens[pos - 1].element == 'while': string.append(lexer.Tokens(pos_start, 'FLAG'))

            pos += pos_plus

        elif (tags[pos] == 'ID' or tags[pos]=='ID_LIST' ) and tags[pos+1]=='LIST_FUNC':

            string.append(tokens[pos])
            pos += 1
            string.append(tokens[pos])
            string.append(tokens[pos+1])

        # elif tags[pos] == 'ID' and  and tags[pos+2]=='FUNC':
        #     print('id+func')
        #     string.append(tokens[pos])
        #     pos += 1
        #     string.append(tokens[pos])
        elif tags[pos]=='ID' or tags[pos]=='ID_LIST':
            #print(tokens[pos],pos)
            pos_finish = pos+tags[pos:].index('SPLIT')
            string.append(tokens[pos])
            pos += 1
            if tokens[pos].element == '=':
                #print(tokens[pos], pos)
                r = tokens[pos]
                pos += 1
                pos_start = pos
                #print(tokens[pos], pos)
                if tokens[pos].type == 'LIST':
                    string.append(tokens[pos])
                elif tokens[pos].type == 'FUNC':
                    string.append(tokens[pos])
                else:
                    if tags[pos_start:pos_finish].count('R') > 0:
                        #print("true")
                        for i in range(tags[pos_start:pos_finish].count('R')):
                            string_plus = polish_arif(tokens[pos_start:tags[pos_start:pos_finish].index('R')],
                                                      tags[pos_start:tags[pos_start:pos_finish].index('R')])
                            for st in string_plus:
                                string.append(st)

                            pos = tags[pos_start:pos_finish].index('R') + 1
                            string.append(tokens[pos - 1])
                            pos_start = pos
                    #print(tokens[pos_start:pos_finish], pos_start,pos_finish)
                    string_plus = polish_arif(tokens[pos_start:pos_finish],
                                              tags[pos_start:pos_finish])
                    for st in string_plus:
                        string.append(st)

                string.append(r)
                string.append(tokens[pos_finish])
                pos = pos_finish
        elif tags[pos]=='H_FUNC':
            #print('FUNCTIONs')
            name_f = tokens[pos].element[tokens[pos].element.index(' ') + 1:]
            #print('FUNCTIONs','name',tokens[pos].element[tokens[pos].element.index(' ') + 1:])
            pos=tags[pos:].index('DO')+1
            string_body=[tokens[pos+tags[pos:].index('RETURN')+1]]
            #print('FUNCTIONs''st_body',tokens[pos+tags[pos:].index('RETURN')+1].element)
            while tags[pos] != 'RETURN':
                #print("!")
                pos_finish = pos + tags[pos:].index('SPLIT')
                string_body.append(tokens[pos])
                pos += 1
                if tokens[pos].element == '=':
                    r = tokens[pos]
                    pos += 1
                    pos_start = pos
                    if tags[pos_start:pos_finish].count('R') > 0:
                        for i in range(tags[pos_start:pos_finish].count('R')):
                            string_plus = polish_arif(tokens[pos_start:tags[pos_start:pos_finish].index('R')],
                                                      tags[pos_start:tags[pos_start:pos_finish].index('R')])
                            for st in string_plus:
                                string_body.append(st)

                            pos = tags[pos_start:pos_finish].index('R') + 1
                            string_body.append(tokens[pos - 1])
                            pos_start = pos
                    string_plus = polish_arif(tokens[pos_start:pos_finish], tags[pos_start:pos_finish])
                    for st in string_plus:
                        string_body.append(st)
                    string_body.append(r)
                    string_body.append(tokens[pos_finish])
                    pos = pos_finish+1

            NAMES_FUNC[name_f].body.extend(string_body)
            pos+=1

        pos+=1
    print("polish")
    for s in string:
        if s.type=='LIST':
            print('[',end=' ')
            for el in s.element:
                print(el.element, el.type, end=', ')
            print(']', end=' ')
        else:print(s.element,s.type,end=', ')
    return string, NAMES_FUNC

def polish_arif(tokens,tags):
    pos = 0
    string=[]
    stack=[]
    while pos < len(tokens):
        if tags[pos]=='DIGIT' or tags[pos]=='ID' or tags[pos]=='ID_LIST':
            string.append(tokens[pos])
        elif tags[pos] =='OP':
            #print(pos)
            stack.append(tokens[pos])
        elif tags[pos] == 'CP':
            while stack[len(stack) - 1].type != 'OP':
                #print("2",stack)
                string.append(stack.pop())
            stack.pop()
        else:
            if tokens[pos].element=='**':stack.append(tokens[pos])
            elif tokens[pos].element == '*' or tokens[pos].element == '/':
                if len(stack) != 0:
                    if stack[len(stack) - 1].element == '*' or stack[len(stack) - 1].element == '/' or stack[len(stack) - 1].element == '**':
                        string.append(stack.pop())
                stack.append(tokens[pos])
            elif tokens[pos].element == '-' and (pos == 0 or tokens[pos-1].element == '('):
                string.append('0')
                string.append(tokens[pos + 1])
                if len(stack) != 0:
                    if stack[len(stack) - 1].element != '(':
                        string.append(stack.pop())
                stack.append(tokens[pos])
                pos += 1
            elif tokens[pos].element == '+' or tokens[pos].element == '-':
                if len(stack) != 0:
                    if stack[len(stack) - 1].element != '(':
                        string.append(stack.pop())
                stack.append(tokens[pos])

        pos+=1
        #print(string,stack,pos)
    while len(stack) != 0:
        string.append(stack.pop())

    return string

def polish_log(tokens,tags):
    pos = 0
    string=[]
    stack=[]
    sym0 = "not"
    sym1 = "not,<,<=,>=,>,==,!="
    sym2 = "not,<,<=,>=,>,==,!=,and"
    sym3 = "not,<,<=,>=,>,==,!=,and,or"

    while pos < len(tokens):
        if tags[pos]=='DIGIT' or tags[pos]=='ID' or tags[pos]=='ID_LIST':
            string.append(tokens[pos])
        elif tags[pos] =='OP':
            #print(pos)
            stack.append(tokens[pos])
        elif tags[pos] == 'CP':
            while stack[len(stack) - 1].type != 'OP':
                #print("2",stack)
                string.append(stack.pop())
            stack.pop()
        else:
            if tokens[pos].element=='not':
                if len(stack) != 0:
                    if stack[len(stack) - 1].element == sym0:
                        string.append(stack.pop())
                stack.append(tokens[pos])
            elif tokens[pos].element=='>' or tokens[pos].element=='<' or tokens[pos].element=='>=' or tokens[pos].element=='<='  or tokens[pos].element=='==' or tokens[pos].element=='!=':
                if len(stack) != 0:
                    if stack[len(stack) - 1].element in sym1:
                        string.append(stack.pop())
                stack.append(tokens[pos])
            elif tokens[pos].element == 'and':
                if len(stack) != 0:
                    if stack[len(stack) - 1].element in sym2:
                        string.append(stack.pop())
                stack.append(tokens[pos])
            elif tokens[pos].element == 'or' :
                if len(stack) != 0:
                    if stack[len(stack) - 1].element != "(" or stack[len(stack) - 1].element in sym3:
                        string.append(stack.pop())
                stack.append(tokens[pos])

        pos += 1
    while len(stack) != 0:
        string.append(stack.pop())
    return string

def polish_if(tokens,tags,f):

    #print('if',tokens)
    #for s in tokens:
        #print(s.element,s.type,end=', ')
    #print()
    pos = 1

    string = []
    if tags[0]=='H_OP':


        stack = []
        pos_start = pos
        pos_finish = tags.index('DO')
        string_plus = polish_log(tokens[pos_start:pos_finish], tags[pos_start:pos_finish])
        for st in string_plus:
            string.append(st)
        pos += pos_finish
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    string.append('!F')
    pos_start = pos
    #print(pos)

    while tags[pos]!='END' and tags[pos]!='ELSE':
        #print(tokens[pos].element,pos)
        if tags[pos]=='H_OP':


            pos_start = pos
            string_plus, pos_plus = polish_if(tokens[pos_start:], tags[pos_start:],pos-1)
            for st in string_plus:
                string.append(st)
            if tokens[pos ].element == 'while': string.append(lexer.Tokens(pos_start, 'FLAG'))
            pos += pos_plus

            if tags[pos + 1] != 'ELSE' and string[-1].type!='FLAG':
                #print(2)
                string.append(lexer.Tokens(-1, 'FLAG'))
            #
            #     for i in range(pos_start, pos):
            #         print(string[i][1], string[i][1] == 'FLAG')
            #         if string[i][1] == 'FLAG':
            #             print(string[i][0] + 1)
            #             string[i] = (string[i][0] + 1, 'FLAG')
            #             print(string[i])
            #print(pos)
        elif tags[pos] == 'ELSE':
            #print('else', pos_start, pos)

            # pos += 1
            pos_start = pos
            string_plus, pos_plus = polish_if(tokens[pos_start:], tags[pos_start:], pos - 1)
            for st in string_plus:
                string.append(st)
            if tokens[pos - 1].element == 'while': string.append(lexer.Tokens(pos_start, 'FLAG'))

            pos += pos_plus
        elif tags[pos] == 'DO':
            pos_start=pos+1
        else:
            #print("!")
            pos_finish = pos+tags[pos:].index('SPLIT')
            string.append(tokens[pos])
            pos+=1
            if tokens[pos].element=='=':
                r=tokens[pos]
                pos+=1
                pos_start=pos
                if tags[pos_start:pos_finish].count('R')>0:
                    for i in range (tags[pos_start:pos_finish].count('R')):
                        string_plus=polish_arif(tokens[pos_start:tags[pos_start:pos_finish].index('R')],tags[pos_start:tags[pos_start:pos_finish].index('R')])
                        for st in string_plus:
                            string.append(st)

                        pos=tags[pos_start:pos_finish].index('R')+1
                        string.append(tokens[pos-1])
                        pos_start=pos
                string_plus=polish_arif(tokens[pos_start:pos_finish],tags[pos_start:pos_finish])
                for st in string_plus:
                    string.append(st)
                string.append(r)
                string.append(tokens[pos_finish])
                pos=pos_finish
        #print(pos,f)
        pos+=1

    string[string.index('!F')]=lexer.Tokens(len(string)-string.index('!F')+1,'FLAG')
    #print(string)
    return string, pos