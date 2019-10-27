import random
import time


boxes=[0,1,2,9,10,11,18,19,20,
           3,4,5,12,13,14,21,22,23,
           6,7,8,15,16,17,24,25,26,
           27,28,29,36,37,38,45,46,47,
           30,31,32,39,40,41,48,49,50,
           33,34,35,42,43,44,51,52,53,
           54,55,56,63,64,65,72,73,74,
           57,58,59,66,67,68,75,76,77,
           60,61,62,69,70,71,78,79,80]

    
def solver(sudoku):
    start_time=time.time()
    global Boxes, Rows, Columns, options
    Boxes={1:[0,1,2,9,10,11,18,19,20],
           2:[3,4,5,12,13,14,21,22,23],
           3:[6,7,8,15,16,17,24,25,26],
           4:[27,28,29,36,37,38,45,46,47],
           5:[30,31,32,39,40,41,48,49,50],
           6:[33,34,35,42,43,44,51,52,53],
           7:[54,55,56,63,64,65,72,73,74],
           8:[57,58,59,66,67,68,75,76,77],
           9:[60,61,62,69,70,71,78,79,80]}
    Rows={1:[0,1,2,3,4,5,6,7,8], 2:[9,10,11,12,13,14,15,16,17],
          3:[18,19,20,21,22,23,24,25,26], 4:[27,28,29,30,31,32,33,34,35],
          5:[36,37,38,39,40,41,42,43,44], 6:[45,46,47,48,49,50,51,52,53],
          7:[54,55,56,57,58,59,60,61,62], 8:[63,64,65,66,67,68,69,70,71],
          9:[72,73,74,75,76,77,78,79,80]}
    Columns={1:[0,9,18,27,36,45,54,63,72], 2:[1,10,19,28,37,46,55,64,73],
             3:[2,11,20,29,38,47,56,65,74], 4:[3,12,21,30,39,48,57,66,75],
             5:[4,13,22,31,40,49,58,67,76], 6:[5,14,23,32,41,50,59,68,77],
             7:[6,15,24,33,42,51,60,69,78], 8:[7,16,25,34,43,52,61,70,79],
             9:[8,17,26,35,44,53,62,71,80]}
    options={}
    if check(sudoku)==False:
        return "Invalid sudoku"
    previous=[]
    while previous!=sudoku:
        previous=[number for number in sudoku]
        cross_analyze(sudoku, options)
    if '' in sudoku:
        result=guess(sudoku, options)
        if result!=None:
            sudoku=result
    stop_time=time.time()
    Time=stop_time-start_time
    print Time
    return sudoku
    


def check(sudoku):
    if len(sudoku)!=81:
        return False
    for box in Boxes:
        numbers=[]
        for cell in Boxes[box]:
            if sudoku[cell] not in [1,2,3,4,5,6,7,8,9,'']:
                return False
            if sudoku[cell] in numbers and sudoku[cell]!='':
                return False
            else:
                numbers.append(sudoku[cell])
    for row in Rows:
        numbers=[]
        for cell in Rows[row]:
            if sudoku[cell] in numbers and sudoku[cell]!='':
                return False
            else:
                numbers.append(sudoku[cell])
    for col in Columns:
        numbers=[]
        for cell in Columns[col]:
            if sudoku[cell] in numbers and sudoku[cell]!='':
                return False
            else:
                numbers.append(sudoku[cell])
    return True


def cross_analyze(sudoku, options2):
    thirds(sudoku, options2, Boxes)
    thirds(sudoku, options2, Rows)
    thirds(sudoku, options2, Columns)

def thirds(sudoku, options2, dictionary):
    x=[Boxes, Rows, Columns]
    primary=dictionary
    x.remove(primary)
    other1=x.pop()
    other2=x.pop()
    for box in primary:
            empty=[]
            numbers=[1,2,3,4,5,6,7,8,9]
            for space in primary[box]:
                if sudoku[space]=='':
                    empty.append(space)
                    if space not in options2:
                        options2[space]=[]
                else:
                    numbers.remove(sudoku[space])
            options={}
            for number in numbers:
                options[number]=[num for num in empty]
            for n in options:
                count=0
                while count<len(options[n]):
                    for row in other1:
                        if options[n][count] in other1[row]:
                            for cell in other1[row]:
                                if sudoku[cell]==n:
                                    options[n].remove(options[n][count])
                                    break
                            else:
                                count+=1
                                break
                            break
            for n in options:
                count=0
                while count<len(options[n]):
                    for col in other2:
                        if options[n][count] in other2[col]:
                            for cell in other2[col]:
                                if sudoku[cell]==n:
                                    options[n].remove(options[n][count])
                                    break
                            else:
                                count+=1
                                break
                            break
            for n in options:
                if len(options[n])==1:
                    sudoku[options[n][0]]=n
                    del(options2[options[n][0]])
            for cell in empty:
                times=0
                number=None
                for n in options:
                    if cell in options[n]:
                        times+=1
                        number=n
                if times==1:
                    sudoku[cell]=number
                    if cell in options2:
                        del(options2[cell])
            for n in options:
                for square in options[n]:
                    if square in options2:
                        if n not in options2[square]:
                            options2[square].append(n)




def guess(sudoku, options):
    count=2
    while count<=max([len(options[cell]) for cell in options]+[0]):
        for space in options:
            possible=[entry for entry in options[space]]
            if len(options[space])==count:
                    while len(options[space])!=0:
                        t_options={}
                        test=[n for n in sudoku]
                        r=random.choice(possible)
                        possible.remove(r)
                        test[space]=r
                        former=[]
                        while former!=test:
                            former=[num for num in test]
                            try:
                                cross_analyze(test, t_options)
                            except ValueError:
                                options[space].remove(r)
                                if len(options[space])==0:
                                    return
                                break
                            except KeyError:
                                options[space].remove(r)
                                if len(options[space])==0:
                                    return
                                break
                            if '' not in test:
                                if check(test)==False:
                                    options[space].remove(r)
                                    if len(options[space])==0:
                                        return
                                    break
                                return test
                            if former==test:
                                recursive=guess(test, t_options)
                                if recursive!=None:
                                    return recursive
                                else:
                                    options[space].remove(r)
                                    if len(options[space])==0:
                                        return
        else:
            count+=1

    

def generate(quantity):
    sudoku=['' for number in range(0,81)]
    sudoku=solver(sudoku)
    choices=[number for number in range(0,81)]
    for number in range(0, 81-int(quantity)):
        selection=random.choice(choices)
        choices.remove(selection)
        sudoku[selection]=''
    return sudoku


def view(sudoku):
    board=[str(entry) for entry in sudoku]
    board='|'+'|'.join(board[0:9])+'|'+"\n"+'|'+'|'.join(board[9:18])+'|'+"\n"+'|'+'|'.join(board[18:27])+'|'+"\n"+'|'+'|'.join(board[27:36])+'|'+"\n"+'|'+'|'.join(board[36:45])+'|'+"\n"+'|'+'|'.join(board[45:54])+'|'+"\n"+'|'+'|'.join(board[54:63])+'|'+"\n"+'|'+'|'.join(board[63:72])+'|'+"\n"+'|'+'|'.join(board[72:])+'|'
    print board

