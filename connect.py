import os
import json
import sqlparsing

def connect (input) :

    tok = input.split()
    userid = input.split()[1]
    passwd = input.split()[2]

    file = open ('users.txt', 'r')
    users = file.readlines()

    for user in users :

        c_user = user.split('-')
        if (c_user[0] == userid and c_user[1].rstrip() == passwd) :
            return 'True'

    return 'False'

def create_user (request) :

    tokens = sqlparsing.parseCreateUser (request)
    username = tokens.Username
    password = tokens.Password

    file = open ('users.txt', 'a')
    file.write ('{}-{}\n'.format(username,password))
    file.close ()
    return 'User created !\n'

#create_user ('create user adja identified by passer')



#username = 'ndeye'
#password = 'ndoumbe'
#print ( connect('Authentication ' + ' ' + username + ' ' + password))





        


