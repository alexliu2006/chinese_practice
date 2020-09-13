# need duo yin zi
#kong1 kong4
#jia4 jia3
#zuan1 zuan4
#shan1 shan4
#bo2 bao2



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

date = datetime.datetime.now()

count = 1

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
        self.time = date.strftime('%c')


    def add_to_history(self, filepath):
        date = datetime.datetime.now()
        document = open(filepath, 'a', encoding='utf-8')
        character = str(self.character)
        pinyin = str(self.pinyin)
        yindiao = str(self.yindiao)
        right_or_wrong = str(self.passed)
        time =  date.strftime('%c')
        document.write('\n')
        document.write(character)
        document.write(',')
        document.write(pinyin)
        document.write(',')
        document.write(yindiao)
        document.write(',')
        document.write(right_or_wrong)
        document.write(',')
        document.write(date.strftime('%c'))

    def check_if_coorect(self, pinyin_answer, yindiao_answer):
        if pinyin_entry.get() in pinyin_answer and yindiao_entry.get() in yindiao_answer:
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
        tr.time = datetime.datetime.strptime(b[4], '%c')
        list_of_objects.append(tr)
 
    return list_of_objects

def groupby(list):
    result = {}

    for current_object in list:
        key = current_object.character

        if key in result:
            temp_list = result.get(key)
            temp_list.append(current_object)
            result[key] = temp_list
        else:
            result[key] = [current_object]

    return result


def sort_time(dictionary):
    global words
    daysAgo_dictionary = {}
    CurrentTime = datetime.datetime.strptime(date.strftime('%c'), '%c')
    list_of_objects = []
    for key in dictionary:
        time = datetime.datetime.strptime('Fri Jan 1 0:00:01 2010', '%c')
        list_of_objects = dictionary.get(key)

        for j in range(0, len(list_of_objects)):          
            if list_of_objects[j].time > time:
                time = list_of_objects[j].time

        how_long_ago = CurrentTime - time
        how_many_days_ago = how_long_ago.days
        daysAgo_dictionary[key] = how_many_days_ago

    return daysAgo_dictionary

dictionary = groupby(read_history())
daysAgo_dictionary = sort_time(dictionary)

def sort_percentages(dictionaryOfAnswers, dictionary, daysAgo_dictionary):
    global words
    percentage_dictionary = {}
    list_of_objects = []
    for key in dictionary:
        number_of_trys = 0
        number_fail = 0
        number_pass = 0
        list_of_objects = dictionary.get(key)

        for j in range(0, len(list_of_objects)):
            if list_of_objects[j].passed == 'pass':
                number_pass = number_pass + 1
                number_of_trys = number_of_trys + 1
            else:
                number_fail = number_fail + 1
                number_of_trys = number_of_trys + 1

        percentage = float(  
            (number_pass - number_fail)-((daysAgo_dictionary[key]+1)/15)  
                          )
        percentage_dictionary[key] = percentage

    for key in dictionaryOfAnswers:
        if key not in percentage_dictionary:
            percentage_dictionary[key] = -100

    
    percentage_list = sorted(percentage_dictionary.items(), key=lambda x: x[1])
    # percentage_list.reverse()

    return percentage_list
    
a = read_dictionary()
dictionary_of_answers = groupby(read_dictionary())
dictionary = groupby(read_history())
percentage_list = sort_percentages(dictionary_of_answers,dictionary, daysAgo_dictionary)

def next_word():
    global count
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
    pinyin_answer = []
    yindiao_answer = []
    for i in coorect_word:
        pinyin_answer.append(i.pinyin)
        yindiao_answer.append(i.yindiao)
    # pinyin_answer = coorect_word[0].pinyin
    # yindiao_answer = coorect_word[0].yindiao

    current_word.pinyin = pinyin_entry.get()
    current_word.yindiao = yindiao_entry.get()
    if current_word.character != '' and pinyin_entry.get() != "":
        count_Word_variable.set(str(count))
        count = count + 1
        

        if current_word.check_if_coorect(pinyin_answer, str(yindiao_answer)):
            current_word.time = date.strftime('%c')
            current_word.add_to_history(HistoryFilePath)
            rank_of_word = rank_of_word + 1
            current_word = TestRecord()
            Chinese_Word_Variable2.set('')
            Chinese_Word_Variable3.set('')
            current_word.character = percentage_list[rank_of_word][0]
            Chinese_Word_Variable.set(current_word.character)

        else:
            current_word.time = date.strftime('%c')
            current_word.add_to_history(HistoryFilePath)
            rank_of_word = rank_of_word + 1
            pinyin_answer = coorect_word[0].pinyin
            yindiao_answer = coorect_word[0].yindiao
            current_word.character = percentage_list[rank_of_word][0]
            Chinese_Word_Variable.set(current_word.character)
            Chinese_Word_Variable2.set(str(pinyin_answer))
            Chinese_Word_Variable3.set(str(yindiao_answer))

app = Tk()
app.title('Chinese Pratice')
app.geometry('1000x640')                                                        #, height=12, padx = 470
btn = Button(app, text='next word', command=next_word, font=('Noto Sans SC', 40), padx = 550, height=3).grid(row=0, sticky=W)
Chinese_Word_Variable = StringVar()
Chinese_Word_Variable2 = StringVar()
Chinese_Word_Variable3 = StringVar()
count_Word_variable = StringVar()
Chinese_Word_Label = Label(app, textvariable=Chinese_Word_Variable, padx = 20, font=('Noto Sans SC', 30)).grid(row=1, column=0)
Chinese_Word_Label2 = Label(app, textvariable=Chinese_Word_Variable2, padx = 20, font=('Noto Sans SC', 15)).grid(row=2)
Chinese_Word_Label3 = Label(app, textvariable=Chinese_Word_Variable3, padx = 20, font=('Noto Sans SC', 15)).grid(row=3)
Chinese_word_label4 = Label(app, textvariable = count_Word_variable, padx = 20, font=('Noto Sans SC', 15)).grid(row=6)
# Chinese_Word_Label.config(width=200, fontsize=50)
#Chinese_Word_Variable.set(current_word.character)

#make entrys for pinyin and yindiao
pinyin_label = Label(app, text='enter pinyin', font=('Noto Sans SC', 20)).grid(row=4, sticky=W)
yindiao_label = Label(app, text='enter yindiao', font=('Noto Sans SC', 20)).grid(row=5, sticky=W)
pinyin_entry = Entry(app, font=('Noto Sans SC', 20))
pinyin_entry.grid(row=4)
yindiao_entry = Entry(app,font=('Noto Sans SC', 20) )
yindiao_entry.grid(row=5)
entered_yindiao = 0
entered_pinyin = 0

app.mainloop()
