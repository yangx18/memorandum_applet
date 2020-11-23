
import time
import csv
import os
import sys
import json

class Memo():

    def __init__(self, title, todo, due, create_time):
        self.title = title
        self.todo = todo
        self.due = due
        self.create_time  = create_time

class Memorandum():


    def __init__(self):
        self.data = dict()

    # add your memorandum
    def add_memo(self):

        #input the basic info that you want to put into the memorandum
        new_title = input("please input the title of your memorandum:\n")
        new_todo = input("please input the to-do things:\n")
        new_due = input("please input your due time:\n")
        new_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        # not allow empty as a memo
        if new_title == '' and new_todo == '' and new_due == '':
            print('-----------------------------------------')
            print("Error! Title-todo-due, Can not be empty!")
            print('-----------------------------------------\n')
        #else save put basic info in dict
        else:
            # create Memo instance
            one_memo = Memo(new_title, new_todo, new_due, new_time)
            a_memo = { 'todo': one_memo.todo, 'due' : one_memo.due, 'Create_time':one_memo.create_time}
            if new_title in self.data['root'][-1]:
                print(' you already have this activity\n')
                print('reloading...\n')
                time.sleep(1)

            else:
                self.data['root'][-1].update({new_title:a_memo})

                #auto save this new memo when user is trying to quit this app
                self.save_memo()

    # save your memo as .json file under this directory
    def save_memo(self):

        with open('temp_db.json','w', encoding ='utf-8') as f:
            # Transfer dict to json and add to temp_db.json
            json.dump(self.data, f,indent=4, ensure_ascii=False)
            print('saved')
            f.close()

        time.sleep(1)

    # show your all your memos
    def show_memo(self):

        for k,v in self.data['root'][-1].items():
            print((k,v))
        print('reloading...\n')
        time.sleep(3)


    def delete_memo(self,title):
        try:
            self.data['root'][-1].pop(title)
            print('succeeded delete %s...\n' %title)
        except:
            print('there is no %s '%title)

        time.sleep(1)

    # clear all data and remove file
    def clearall(self):
        if os.path.exists('temp_db.json'):
            os.remove('temp_db.json')
            print('succeeded remove this Memorandum\n')
            self.exit()
        else:
            print('there is no such a Memo was created.\n')


    # quit memorandum app
    def exit(self):

        print('See you next time!')
        sys.exit()

    # App Entry
    def begin(self):

        #introduction
        print('=================================================================\n')
        print('=====================Hello User==================================')
        print('==============Welcome to Yang\'s Memorandum App===================\n')
        print('=================%s=============================' %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print('=================================================================\n')

        # Menu
        menu = { '1': '    add new  memo   ', '2':'   save new  memo   ','3':'   exit this memo   ','4':'   show  my  memos   ',
        '5':'  delele your memo  ','6':'clear all memo and quit(!!!)'}
        menu_inside = {'1':'add_memo','2':"save_memo", '3':'exit','4':'show_memo', '5':'delete_memo','6':'clearall'}

        # if there is no temp_db.json under this directory, then create one
        if not os.path.exists('temp_db.json'):
            with open('temp_db.json','w', encoding ='utf-8') as f:
                json.dump({'root':[{}]}, f,indent=4, ensure_ascii=False)
                f.close()

        # taking the data from temp_db.json
        with open('temp_db.json','r', encoding ='utf-8') as f:
            self.data = json.load(f)
            f.close()

        # input your choice according to Menu
        while True:
            for k,v in menu.items():
                print('+---+----------------------+\n')
                print('| %s | %s |' % (k,v))
                print('+---+----------------------+')


            action = input('\n input your choice (in number):\n\n')
            # Return the object user chose and assign to func
            func = getattr(self, menu_inside.get(action))

            # if call delele one memo function, we pass the title name to delete_memo func
            if action is '5':
                del_title = input('put the title name you want to delete:\n')
                # begin function
                func(del_title)
            else:
                # begin function
                func()


if __name__ == '__main__':
    root = Memorandum().begin()
