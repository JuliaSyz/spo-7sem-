from stackmachine import arif_calc,log_calc
import lexer
threads = []
values={}




def thread(tokens,func):
    print('\nТРИАДЫ')
    #for el in tokens:
    #    print(el.element,el.type)
    #print('func')

    #for el in func:
    #    for elem in func[el].body:
    #        print(elem.element,elem.type)

        #func[el].body=[func[el].body[0]]+main_code(func[el].body[1:])

    #print_threads()

    new_str=main_code(tokens)
    print_threads()
    #for el in new_str:
    #    print(el.element,el.type)
    return new_str

def main_code(tokens):

    new_str=[]
    pos_start=0
    pos=0
    num=0
    while pos<len(tokens):
        f=1
        #print(len(tokens))
        #print('pos=',pos,tokens[pos].type,tokens[pos].element)

        if tokens[pos].type=='ID' and tokens[pos+2].type=='R' and (tokens[pos+1].type=='DIGIT' or tokens[pos+1].type=='LIST'):
            values.update({tokens[pos].element:tokens[pos+1]})
            threads.append([num,tokens[pos],tokens[pos+1],tokens[pos+2]])
            #print_values()
            num+=1
            pos+=2

        elif tokens[pos].type == 'ID' and tokens[pos + 2].type == 'R' and tokens[pos + 1].type == 'FUNC':
            threads.append([num, tokens[pos], tokens[pos + 1], tokens[pos + 2]])
            num += 1
            pos += 2
        elif tokens[pos].type == 'ID_LIST':

            while tokens[pos].type != 'SPLIT':
                #print('ID_LISTtt')
                pos+=1

        elif (tokens[pos].type=='ID' or tokens[pos].type=='DIGIT' ) and (tokens[pos+1].type=='ID' or  tokens[pos+1].type=='DIGIT') and (tokens[pos+2].type=='ARIF' or  tokens[pos+2].type=='LOG' or  tokens[pos+2].type=='COMPAR'):
            a=[num]

            if tokens[pos].element in values:
                a.append(values[tokens[pos].element])
            else:
                a.append(tokens[pos])
            pos+=1
            if tokens[pos].element in values:
                a.append(values[tokens[pos].element])
            else:
                a.append(tokens[pos])
            pos+=1
            a.append(tokens[pos])

            if a[1].type=='DIGIT' and a[2].type=='DIGIT':
                if a[3].type == 'ARIF':
                    result=arif_calc(a[1:])[0]

                elif a[3].type == 'LOG' or a[3].type == 'COMPAR':
                    result=log_calc(a[1:])[0]
                a=[num,lexer.Tokens('C','th'),result,lexer.Tokens(0,'th')]
            threads.append(a)


            num+=1



        elif (tokens[pos].type=='ID' or tokens[pos].type=='DIGIT') and (tokens[pos+1].type=='ARIF' or tokens[pos+1].type=='LOG' or tokens[pos+1].type=='COMPAR'):
            a=[num,threads[-1][0]]

            if threads[-1][1].type=='th':

                a[1]=threads[-1][2]
            if tokens[pos].element in values:
                a.append(values[tokens[pos].element])
            else:
                a.append(tokens[pos])
            pos += 1
            a.append(tokens[pos])
            #print_thread(a)
            if a[1].type=='DIGIT' and a[2].type=='DIGIT':
                if a[3].type == 'ARIF':
                    result=arif_calc(a[1:])[0]

                elif a[3].type == 'LOG' or a[3].type == 'COMPAR':
                    result=log_calc(a[1:])[0]
                a=[num,lexer.Tokens('C','th'),result,lexer.Tokens(0,'th')]
            threads.append(a)
            num+=1
        elif tokens[pos].type == 'ID' and tokens[pos + 1].type == 'LIST_FUNC':

            pos += 1
        elif tokens[pos].type == 'ID' and tokens[pos - 1].type == 'SPLIT':
            pos_start = pos


        elif tokens[pos].type=='R':
            a=[num,tokens[pos_start],threads[-1][0],tokens[pos]]
            if threads[-1][1].type=='th':
                a[2]=threads[-1][2]
            threads.append(a)
            values.update({tokens[pos_start].element:a[2]})
            num+=1

        elif tokens[pos].type=='SPLIT' or tokens[pos].type=='FLAG' :
            f=0
            if tokens[pos].type=='FLAG' :
                if tokens[pos].type!='SPLIT':
                    new_str.append(threads[-1][2])
                if pos!=len(new_str):
                    tokens[pos].element-=(tokens[pos].element-len(new_str))
            new_str.append(tokens[pos])

        if f and len(threads)!=0:
            if threads[-1][1].type!='th':
                new_str.extend(threads[-1][1:])


        pos+=1

    return new_str




def print_thread(el):
    #print('thread')
    print(el[0], el[1], el[2], el[3])
    print(el[0], el[1].element, el[2].element, el[3].element)
def print_threads():
    #print("ThREADS")
    for el in threads:
        #print(el[0], el[1], el[2], el[3])
        print(el[0],el[1].element,el[2].element,el[3].element)

def print_values():
    print("value")
    for el in values.keys():
        print(el,values[el].element)




