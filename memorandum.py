
import time
import csv
import os
import sys
import json

# Memo Instance
class Memo():

    def __init__(self, title, todo, due, create_time):
        self.title = title
        self.todo = todo
        self.due = due
        self.create_time  = create_time

# Main class
class Memorandum():

    def __init__(self):
        self.data = dict()

    # add your memorandum into temp_db
    def add_memo(self):

        # input the basic info that you want to put into the memorandum file
        new_title = input("please input the title of your memorandum:\n")
        new_todo = input("please input the to-do things:\n")
        new_due = input("please input your due time[year-moth-day-hour-min(2020-09-01-23-59)]:\n")
        new_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        # make sure due day was written correctly as example given in [y-m-d-h-m or y-m-d]
        while True:
            try:
                int(new_due.replace('-',''))
                if int(new_due.replace('-','')) < 100000000000:
                    new_due += '-00-00'
                break
            except ValueError as e:
                print(e)
                new_due = input("please input your due time[year-moth-day-hour-min(2020-09-01-23-59)]:\n")

        # not allow title and todo be empty
        if new_title =='':
            print('-----------------------------------------\n Error! Title, Can not be empty!\n-----------------------------------------\n')
        elif   new_todo == '':
            print('-----------------------------------------\n Error! todo, Can not be empty!\n-----------------------------------------\n')

        #else save put basic info in dict
        else:
            # create Memo instance for this new title
            one_memo = Memo(new_title, new_todo, new_due, new_time)
            a_memo = { 'todo': one_memo.todo, 'due' : one_memo.due, 'Create_time':one_memo.create_time}

            if new_title in self.root_memos:
                print(' you already have this activity\n')
                print('reloading...\n')
                time.sleep(1)

            else:
                # update new memo under root user
                self.root_memos.update({new_title:a_memo})

                # save this new memo
                self.save_memo()

    # save your memo as .json file under current directory
    def save_memo(self):

        # write memo info into temp_db.json
        with open('temp_db.json','w', encoding ='utf-8') as f:
            # Transfer dict to json and add to temp_db.json
            json.dump(self.data, f,indent=4, ensure_ascii=False)
            print('Saved')
            f.close()
        time.sleep(0.75)

    # show your all your memos
    def show_memo(self):

        for k,v in self.root_memos.items():
            print('-------------------------------------------------------------')
            print('title: %s \nto-do list: %s ' %(k,v))
        print('-------------------------------------------------------------')
        print('reloading...\n')
        time.sleep(3)

    # print all memos which past the due.
    def late_memo(self):

        #Transfer current time to int variable
        int_localtime = int(time.strftime('%Y%m%d%H%M',time.localtime(time.time())))

        try:
            # Use dictionary comprehensions to create dictionaries to record all memos
            date_dict = {k:v for (k,v) in self.root_memos.items()}

            # Use list comprehensions to create lists to select memo which has been passed
            obj = [ (title,single_dict) if int(single_dict['due'].replace('-','')) < int_localtime else None  for title ,single_dict in date_dict.items()]
            print('---------past the due list----------------\n')
            for i in obj:
                if i is not None: print(i)
            print('------------------------------------------\n')

        except ValueError as e:
            print(e)

    # delete exactly one memo by given exactly memo's title
    def delete_memo(self,title):

        if title in self.root_memos:
            self.root_memos.pop(title)
            print('succeeded delete %s...\n' %title)
        elif title not in self.root_memos:
            print('there is no %s '%title)

        time.sleep(1)

    # clear all data and remove file
    def clearall(self):
        warning = input('Are you sure you want to remove all [yes/no]\n')
        if warning == 'yes':
            # Is temp_db.json exists?
            if os.path.exists('temp_db.json'):
                # remove temp_db.json
                os.remove('temp_db.json')
                print('succeeded remove this Memorandum\n')
                # quit
                self.exit()
            else:
                print('there is no such a Memo was created.\n')

    # quit Memorandum App
    def exit(self):

        print('See you next time!')
        sys.exit()

    # App Entry
    def begin(self):

        #introduction with current time
        print('=================================================================\n')
        print('=====================Hello User==================================')
        print('==============Welcome to Yang\'s Memorandum App===================\n')
        print('=================%s=============================' %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print('=================================================================\n')

        # Menu for user to select
        menu = { '1': '   add  new  memo       ', '2':'  save  new  memo       ','3':'  exit  this memo       ','4':' show   my  memos       ',
        '5':'  show  past  due  memo ', '6':' delele  your  memo     ','7':'remove all and quit(!!!)'}
        # The function corresponds to every choice
        menu_inside = {'1':'add_memo','2':"save_memo", '3':'exit','4':'show_memo','5':'late_memo' ,'6':'delete_memo','7':'clearall'}

        # Initialized temp_db.json file, if there is no temp_db.json under this directory.
        if not os.path.exists('temp_db.json'):
            with open('temp_db.json','w', encoding ='utf-8') as f:
                json.dump({'root':[{}]}, f,indent=4, ensure_ascii=False)
                f.close()

        # Taking out user's data from temp_db
        with open('temp_db.json','r', encoding ='utf-8') as f:
            self.data = json.load(f)
            f.close()

        # Save memos under root user to root_memos
        self.root_memos = self.data['root'][-1]

        # input() function, to get some user input.
        # looping statement (while)
        while True:
            # Interface
            for k,v in menu.items():
                print('+---+--------------------------+\n')
                print('| %s | %s |' % (k,v))
                print('+---+--------------------------+')

            # try-except to catch the excpetion when user input beside choice number
            try:
                action = input('\ninput your choice (in number): \n')
                # Return the object user chose and assign to func
                func = getattr(self, menu_inside.get(action))
            except:
                print('===============')
                print('Wrong input! Please retry!')
                print('===============\n')
                time.sleep(0.5)
                continue

            # if-elif
            # if call delele one memo function, we pass the title name to delete_memo func
            if action == '6':
                del_title = input('put the title name you want to delete:\n')
                # pass the variable
                func(del_title)
            else:
                # begin function
                func()


# main entry of my app
if __name__ == '__main__':
    root = Memorandum().begin()



'''
ReadMe:

Totoal 201 lines include comments

if  __name__  ==  "__main__":
-----line 198

* Define at least 1 class, and at least 1 function for each class you have defined. Your __main__ should instantiate objects of the classes you have designed, and use them to invoke the methods defined in those classes.
-----line 8, line 16, line 23, line 64, etc.

* Use list comprehensions to create lists.
-----line 92

* Use dictionary comprehensions to create dictionaries.
-----line 89

* Use at least 1 decision-making statement (if-elif)
-----line 43, 45

* Use at least 1 looping statement (for or while).
-----line 160, 161

* Use at least 1 try-except to catch some exceptions.
-----line 33, 38

* Use the input() function, or command-line arguments, to get some user input.
-----line 168

* Produce some, hopefully interesting, output:
-----
To-do List is effectively way to help people schedule their time and avoiding missing something important.
This Memorandum App help use to save their to-do list in local,
and I offer strong and usful funcs (such as add memo, save memo/s, exit, show memos, show past due memos, delete memo, delete file).
Also we offer current time and time record fucntion.

* Add comments to make your script easy to understand (not counted toward the 100 line requirement)
-----Done
'''
