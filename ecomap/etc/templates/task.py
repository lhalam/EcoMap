#!/usr/bin/env python

ASK = ['username', 'password', 'email']
USER_DICT = {'username': '',
             'password': '',
             'email': ''}

def ask_question(question_list):
    "function that add values to USER_DICT."
    for value in question_list:
        while True:
            answer = raw_input("What is " + value + " ")
            if answer:
                USER_DICT[value] = answer
                break
            print "please, enter value {}".format(value)
    print USER_DICT

ask_question(ASK)


