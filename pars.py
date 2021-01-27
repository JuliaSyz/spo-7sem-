import lexems
LISTS=[]
VALUE=[]
VALUE_FUNC=[]
PARAMS=[]
NAMES_FUNC={}
flag_begin=True

class Function():
    def __init__(self,name,params,value_func):
        self.name=name
        self.params=params
        self.params_val=[]
        self.value_func=value_func
        self.body=[]
    def print_body(self):
        for el in self.body:
            print(el.element,el.type,end=', ')
        print()




def if_right(tokens):
    print("PARSER")
    flag=False
    pos=0
    tags = []
    for token in tokens:
        tags.append(token.type)

    while pos < len(tokens):
        #print('-------------------',pos)
        #for i in range(pos, len(tokens)):
            #print(tokens[i].element, end=' ')
        #print()

        flag, pos = exp(tokens,pos,tags)
        if not flag:
            print('error')
            break
    print('lists=',LISTS)
    print('value=', VALUE)
    return flag
def exp(tokens,pos,tags, is_func=False,name_f=''):
    #print('-------------------exp', pos, tokens[pos].type,tokens[pos].element)
    #for i in range(pos, len(tokens)):
        #print(tokens[i].element, end=' ')
    #print()
    flag='True'
    #print(tokens[pos].type == 'ID' and (tokens[pos + 1].type == 'ADD' or tokens[pos + 1].type == 'REMOVE'))



    if (tokens[pos].type == 'ID' or tokens[pos].type == 'ID_LIST') and tokens[pos+1].type == 'R':

        pos+=2
        if tokens[pos].type == 'LIST':
            LISTS.append(tokens[pos-2].element)
            #print("LISTS",LISTS)
            flag, tokens[pos] = list_exp(tokens[pos])
            pos+=2
        elif tokens[pos].type == 'FUNC':
            flag, pos = exp(tokens, pos, tags)
        else:
            if is_func:
                if (tokens[pos - 2].element not in VALUE_FUNC or tokens[pos - 2].element not in PARAMS) and tokens[pos - 2].type == 'ID':
                    NAMES_FUNC[name_f].value_func.append(tokens[pos - 2].element)
            else:
                if tokens[pos-2].element not in VALUE and tokens[pos-2].type=='ID':
                    VALUE.append(tokens[pos-2].element)

            flag, pos = do_exp(tokens, pos, tags,'SPLIT',is_func=is_func)

    elif tokens[pos].type == 'ID' and tokens[pos + 1].type == 'INDEX':
        #print(tokens[pos].element,tokens[pos].element == 'ID' in LISTS)
        if tokens[pos].element  in LISTS:

            id_list(tokens, pos, tags)
        #print('!!!!',len(tokens[pos + 1].element),tokens[pos + 1].element)
        #print('*******', tokens[pos].element,tokens[pos+1].element)
    elif tokens[pos].type == 'ID' and (tokens[pos + 1].type == 'LIST_FUNC'):
        #print('list',LISTS)
        pos+=1
        if tokens[pos-1].element in LISTS:
            #print('!', tokens[pos-1].element, tokens[pos].element,LISTS)

            str=tokens[pos].element
            #print(str)
            str = lexems.lex(str[tokens[pos].element.index('(')+1:tokens[pos].element.index(')')])
            tokens[pos].element=[tokens[pos].element[:tokens[pos].element.index('(')]]
            for st in str:
                tokens[pos].element.append(st.element)

            #print(tokens[pos].element,tokens[pos].type)
            pos+=2
            #print(tokens[pos].element)



        else:
            flag=False




    elif tokens[pos].type == 'H_OP':

        pos+=1
        if 'DO'in tags[pos:] and 'END' in tags[pos:]:
            pos_finish = pos + tags[pos:].index('DO')


            if 'COMPAR' in tags[pos:pos_finish] or 'LOG' in tags[pos:pos_finish]:


                flag, pos = do_exp(tokens, pos, tags,'DO',is_func=is_func)
                #pos+=1
                while tokens[pos].type != 'END' and tokens[pos].type != 'ELSE':
                    flag, pos = exp(tokens, pos, tags)

                if tokens[pos].type == 'ELSE':
                    pos += 1
                    if tokens[pos].type == 'DO':
                        pos += 1
                        while tokens[pos].type!='END':

                            flag, pos = exp(tokens, pos, tags)



                if tokens[pos].type == 'END':

                    pos += 1


    elif tokens[pos].type == 'H_FUNC':
        #print('заголовок функции')
        name_f=tokens[pos].element[tokens[pos].element.index(' ')+1:]
        if name_f not in NAMES_FUNC:
            NAMES_FUNC.update({name_f:Function(name_f,[],[])})

        pos+=1

        if 'DO' in tags[pos:] and 'RETURN' in tags[pos:] and 'END' in tags[pos:]:

            pos_finish = pos + tags[pos:].index('DO')



            if 'OP' in tags[pos:pos_finish] and 'CP' in tags[pos_finish-1]:

                pos+=1
                #print('заголовок функции', tokens[pos].element)
                for i in range(pos,pos_finish-1):
                    NAMES_FUNC[name_f].params.append(tokens[i].element)
                pos=pos_finish+1
                #print('H_OPP', pos,tokens[pos].element)
                while tokens[pos].type != 'END' and tokens[pos].type != 'RETURN':

                    flag, pos = exp(tokens, pos, tags,is_func=True,name_f=name_f)

                if flag:

                    if  tokens[pos].type=='RETURN' and tokens[pos+1].type=='ID' and tokens[pos+2].type=='SPLIT':

                        pos+=3
                        flag = True
                    else:flag=False

                    if tokens[pos].type=='END' and flag:
                        flag=True
                        pos+=1
                    else:flag=False
        else: flag=False
    elif tokens[pos].type == 'FUNC':
        name_f = tokens[pos].element
        name_f=name_f[:name_f.index('(')]
        #print(name_f,NAMES_FUNC)
        if name_f in NAMES_FUNC:
            #print(name_f, NAMES_FUNC)
            str = tokens[pos].element
            #print(str)
            str = lexems.lex(str[tokens[pos].element.index('(') + 1:tokens[pos].element.index(')')])
            tokens[pos].element = [tokens[pos].element[:tokens[pos].element.index('(')]]
            for st in str:
                tokens[pos].element.append(st.element)

            #print(tokens[pos].element)
            pos+=2
            #if






    else: flag=False
    #print("privet2",tokens[pos].element)
    return flag,pos






def log_exp(tokens,pos,tags,end,is_func=False):
    #print('-------------------log', pos,tags[pos:].index(end))
    #for i in range(pos, pos+tags[pos:].index(end)+1):
        #print(tokens[i].element, end=' ')
    #print()

    flag = True
    if end in tags[pos:]:
        if tags[pos:].count('OP') == tags[pos:].count('CP'):
            while tokens[pos].type != end:
                if (tokens[pos].type==tokens[pos+1].type) or ((tokens[pos].type=='ID' or tokens[pos].type == 'ID_LIST') and tokens[pos+1].type=='DIGIT') and ((tokens[pos+1].type=='ID' or tokens[pos+1].type == 'ID_LIST') and tokens[pos].type=='DIGIT'):
                    flag = False
                    break
                if tokens[pos].type == 'ID':
                    if is_func:
                        if tokens[pos].element not in VALUE_FUNC or tokens[pos].element not in PARAMS:
                            flag = False
                    else:
                        if tokens[pos].element not in VALUE:
                            flag = False
                if tokens[pos + 1].type == 'INDEX':
                    #print('!!!!!')
                    if tokens[pos].element  in LISTS:id_list(tokens, pos, tags)
                pos += 1


        else:
            flag = False
    else:
        flag = False
    #print(flag)
    return flag, pos
def arif_exp(tokens, pos, tags,end,is_func=False):
    #print('-------------------arif', pos)
    #for i in range(pos, pos+tags[pos:].index(end)+1):
        #print(tokens[i].element,end=' ')
    #print()
    flag=True
    if end in tags[pos:]:
        if tags[pos:].count('OP')==tags[pos:].count('CP'):

            while tokens[pos].type!=end:
                if tags[pos]!='OP' and tags[pos]!='CP':
                    if (tokens[pos].type==tokens[pos+1].type) or ((tokens[pos].type=='ID' or tokens[pos].type == 'ID_LIST') and tokens[pos+1].type=='DIGIT') and ((tokens[pos+1].type=='ID' or tokens[pos+1].type == 'ID_LIST') and tokens[pos].type=='DIGIT'):

                        #print(3,tags[pos])
                        flag=False
                        break
                    if tokens[pos].type=='ID':
                        #print(VALUE)
                        if is_func:
                            if tokens[pos].element not in VALUE_FUNC or tokens[pos].element not in PARAMS:
                                flag = False
                        else:
                            if tokens[pos].element not in VALUE:
                                flag = False
                    if tokens[pos + 1].type == 'INDEX':
                        #print('!!!!!')
                        if tokens[pos].element  in LISTS:id_list(tokens, pos, tags)
                pos+=1

        else:flag=False
    else:flag=False
    #print(flag)
    return flag,pos

def do_exp(tokens, pos, tags,end,is_func=False):
    #print('-------------------do', pos)
    #for i in range(pos, pos+tags[pos:].index(end)+1):
    #    print(tokens[i].element, end=' ')
    #print()

    if end in tags[pos:]:
        pos_finish = pos+tags[pos:].index(end)
        #print(tags[pos:pos_finish],pos_finish)
        if ('COMPAR' in tags[pos:pos_finish] or 'LOG' in tags[pos:pos_finish]) and 'ARIF' not in tags[pos:pos_finish]:

            flag, pos = log_exp(tokens, pos, tags, end,is_func=is_func)
        elif 'ARIF' in tags[pos:pos_finish] and 'LOG' not in tags[pos:pos_finish]:
            flag, pos = arif_exp(tokens, pos, tags, end,is_func=is_func)
        elif (tags[pos]=='DIGIT' or tags[pos]=='ID' or tokens[pos].type == 'ID_LIST') and len(tags[pos:pos_finish])==1:
            if tokens[pos+1].type == 'INDEX':
                #print('!!!!!')
                if tokens[pos].element in LISTS:id_list(tokens,pos,tags)
            flag=True
            pos+=1

        pos+=1
    else:flag=False
    #print(flag)
    return flag, pos
def id_list(tokens,pos,tags):
    #print('id_list')
    tokens[pos].element = [tokens[pos].element, tokens[pos + 1].element]

    tokens[pos].type = 'ID_LIST'
    tokens.pop(pos + 1)
    tags.pop(pos + 1)

def list_exp(token):
    #print('---------------------list_exp')
    flag=True

    str=token.element
    str=lexems.lex(str[1:len(str)-1])
    token.element=str



    return flag,token
