# Description: This file contains the code for the loop tech demo.
#looping techniques two or more sequences at the same time
questions = ['color', 'name', 'fruit', 'quest']
answers = ['blue', 'lancelot', 'apple', 'grail']
for q, a in zip(questions, answers):
    print('What is your {0}? It is {1}.'.format(q, a))