from tkinter import*
import random
import datetime
import math
import configparser
import os
from time import gmtime, strftime

rank_of_word = 0
list_of_objects = []
list_of_answers = []
words = []

ScriptPath = os.path.abspath(__file__)
#a = ScriptPath.index('main.py')
#a = ScriptPath[:-7]
#b = 'main.ini'
#IniPath = a+b

#config = configparser.ConfigParser()
##config.read(IniPath, encoding='utf-8')
#FilePaths = config['data']
DictionaryFilePath = 'C:\\Users\\alexl.HOME02\\OneDrive\\ChineseWords\\data\\dictionary.txt'
HistoryFilePath = 'C:\\Users\\alexl.HOME02\\OneDrive\\ChineseWords\\data\\history.txt'

class TestRecord:
    def __init__(self):
        #self.round = 0
        #self.index = 0
        self.character = ''
        self.pinyin = ''
        self.yindiao = 1
        self.passed = 'fail'
        #self.seconds_spent = 0
        self.time = strftime("%c")


    def add_to_history(self, filepath):
        document = open(filepath, 'a', encoding='utf-8')
        character = str(self.character)
        pinyin = str(self.pinyin)
        yindiao = str(self.yindiao)
        right_or_wrong = str(self.passed)
        time =  str(self.time)
        document.write('\n')
        document.write(character)
        document.write(',')
        document.write(pinyin)
        document.write(',')
        document.write(yindiao)
        document.write(',')
        document.write(right_or_wrong)
        document.write(',')
        document.write(time)

    def check_if_coorect(self, pinyin_answer, yindiao_answer):
        if pinyin_entry.get() == pinyin_answer and yindiao_entry.get() == yindiao_answer:
            self.passed = 'pass'
            return True
        
        else:
            self.passed = 'fail'
            return False

class ChineseAnswers:

    def __init__(self):
        self.character = ''
        self.pinyin = ''
        self.yindiao = 0


def read_dictionary():
    global list_of_answers
    doc = open(DictionaryFilePath, 'r', encoding='utf-8')
    tempstr = doc.read()
    a = tempstr.split('\n')
    list_of_answers = []
    for c in a:
        b = c.split(',')

        ca = ChineseAnswers()
        ca.character = b[0]
        ca.pinyin = b[1]
        ca.yindiao = int(b[2])
        list_of_answers.append(ca)
    return list_of_answers

def read_history():
    global list_of_objects
    doc = open(HistoryFilePath, 'r', encoding='utf-8')
    tempstr = doc.read()
    a = tempstr.split('\n')
    list_of_objects = []
    for c in a:
        b = c.split(',')

        #__init__ is used
        tr = TestRecord()
        tr.character = b[0]
        tr.pinyin = b[1]
        tr.yindiao = int(b[2])
        tr.passed = b[3]
        list_of_objects.append(tr)

    return list_of_objects

def groupby(list):
    result = {}

    for i in range(0, len(list)):
        current_object = list[i]
        key = current_object.character

        if key in result:
            temp_list = result.get(key)
            temp_list.append(current_object)
            result[key] = temp_list
        else:
            result[key] = [current_object]

    return result

    

def sort_percentages(dictionary):
    global words
    number_of_trys = 0
    percentage_dictionary = {}
    list_of_objects = []
    for key in dictionary:
        number_fail = 0
        number_pass = 0
        list_of_objects = dictionary.get(key)

        for j in range(0, len(list_of_objects)):
            if list_of_objects[j].passed == True:
                number_pass = number_pass + 1
                number_of_trys = number_of_trys + 1
            else:
                number_fail = number_fail + 1
                number_of_trys = number_of_trys + 1

        percentage = float((number_pass - number_fail))
        percentage_dictionary[key] = percentage
    
    percentage_list = sorted(percentage_dictionary.items(), key=lambda x: x[1])
    percentage_list.reverse()

    return percentage_list
    
a = read_dictionary()
dictionary_of_answers = groupby(read_dictionary())
dictionary = groupby(read_history())
percentage_list = sort_percentages(dictionary)

def next_word():
    Chinese_Word_Variable2.set('')
    Chinese_Word_Variable3.set('')
    global dictionary_of_answers
    global dictionary
    global percentage_list
    global rank_of_word

    current_word = TestRecord()
    #entered word and pinyin and yindiaos
    current_word.character = percentage_list[rank_of_word][0]
    current_word.pinyin = pinyin_entry.get()
    current_word.yindiao = yindiao_entry.get()
    
    Chinese_Word_Variable2.set('')
    Chinese_Word_Variable3.set('')

    #coorect pinyin and yindiao
    coorect_word = dictionary_of_answers.get(current_word.character)
    Chinese_Word_Variable.set(current_word.character)
    pinyin_answer = coorect_word[0].pinyin
    yindiao_answer = coorect_word[0].yindiao

    current_word.pinyin = pinyin_entry.get()
    current_word.yindiao = yindiao_entry.get()
    if yindiao_entry.get() != '' and current_word.character != '':

        

        if current_word.check_if_coorect(pinyin_answer, str(yindiao_answer)):
            current_word.add_to_history('C:\\Users\\alexl.HOME02\\OneDrive\\ChineseWords\\data\\history.txt')
            rank_of_word = rank_of_word + 1
            current_word = TestRecord()
            Chinese_Word_Variable2.set('')
            Chinese_Word_Variable3.set('')
            Chinese_Word_Variable.set(current_word.character)

        else:
            current_word.add_to_history('C:\\Users\\alexl.HOME02\\OneDrive\\ChineseWords\\data\\history.txt')
            pinyin_answer = coorect_word[0].pinyin
            yindiao_answer = coorect_word[0].yindiao
            Chinese_Word_Variable2.set(str(pinyin_answer))
            Chinese_Word_Variable3.set(str(yindiao_answer))


app = Tk()
app.title('Chinese Pratice')
app.geometry('1000x640')
btn = Button(app, text='next word', command=next_word, height=12, padx = 470).grid(row=0, sticky=W)
Chinese_Word_Variable = StringVar()
Chinese_Word_Variable2 = StringVar()
Chinese_Word_Variable3 = StringVar()
Chinese_Word_Label = Label(app, textvariable=Chinese_Word_Variable, padx = 20).grid(row=1, column=0)
Chinese_Word_Label2 = Label(app, textvariable=Chinese_Word_Variable2, padx = 20).grid(row=2)
Chinese_Word_Label3 = Label(app, textvariable=Chinese_Word_Variable3, padx = 20).grid(row=3)
#Chinese_Word_Variable.set(current_word.character)

#make entrys for pinyin and yindiao
pinyin_label = Label(app, text='enter pinyin').grid(row=4, sticky=W)
yindiao_label = Label(app, text='enter yindiao').grid(row=5, sticky=W)
pinyin_entry = Entry(app)
pinyin_entry.grid(row=4)
yindiao_entry = Entry(app)
yindiao_entry.grid(row=5)
entered_yindiao = 0
entered_pinyin = 0

app.mainloop()