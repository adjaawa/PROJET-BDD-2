import json
import sqlparsing
import os
import glob
from texttable import Texttable

current_db = ''

def create_database (sql) :

    tokens = sqlparsing.parseCreateDatabase (sql)
    database = tokens.Database

    database_name = '{}.json'.format(database)

    if os.path.isfile (database_name) :
        return "Database '{}' already exists !\n".format(database_name)

    with open (database_name, 'w+') as f:
        json.dump ({}, f)

    return 'Database created !\n'


def use_database(sql):

    global current_db
    
    tokens = sqlparsing.parseUseDatabase (sql)
    database = tokens.Database
    fichier = ('{}.json'.format(database))

    if os.path.exists(fichier):
        current_db = '{}.json'.format(database)
    else:
        return "Unknown database\n"
    return "Database '{}' selected ! \n".format(database)


def insertion_data(request) :
    
    liste = []
    tokens = sqlparsing.parseInsertInto(request)
    liste.append(tokens.Table)
    liste.append(tokens.Values)

    table_name = liste[0]
    val = liste[1]
    valeurs = {}
    
    with open (current_db) as f:
        json_data  = json.loads(f.read())
    i = 0

    attribut = []
    for key, value in json_data.items():
        if key == table_name :
            for subject, score in value.items():
                for j, p in score.items():
                    attribut.append(j)

    for key, value in json_data.items():
        if key == table_name :
            for x in range(len(val)):
                valeurs[attribut[x]] = val[i]
                i += 1

    with open(current_db) as f:
        data_dict = json.load(f)

    taille = len(data_dict[table_name]) + 1
    data_dict[table_name][taille] = valeurs
    fichier = open(current_db,'w')
    fichier.write(json.dumps(data_dict, indent=4))
    fichier.close()

    return 'Successful insertion !\n'

def select_data(sql):

    global current_db
    liste = []

    tokens = sqlparsing.parseSelect(sql)
    table_name = tokens.Tables

    chaine = str(table_name).strip('[]').strip("''")
    
    with open('{}'.format(current_db)) as f:
        json_data  = json.loads(f.read())

    items_count = len(json_data[chaine])
    t = Texttable ()
    attributes = []

    for key, value in json_data.items():
        if key != chaine:
            continue 
        for subject, score in value.items():
            if subject == "1":
                for j, p in score.items(): 
                    attributes.append(j)
                break
                
        t.header (attributes)
        values = []

        for subject, score in value.items():
            for j, p in score.items():
                values.append(p)
            t.add_row (values)
            values = []

    return (t.draw() + "\n")


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

def create_table (request) :

    tokens = sqlparsing.parseCreateTable (request)
    table_name = tokens.Table
    columns = tokens.Columns

    with open (current_db, 'r+') as f:

        try:
            db = json.load(f)
        except :
            db = {}

        if table_name in db:
            return "Table already exists in database '{}'\n".format (current_db)
        
        fields = {}
        dic = {}

        for field in columns :
            fields.update ({field : None})

        dic["1"] = fields
        db [table_name] = dic
        f.seek(0)
        json.dump (db, f, indent = 4)
        f.truncate ()
        f.close()

    return "Table created !"


def drop_database (request) :

    tokens = sqlparsing.parseDropDatabase (request)
    database = tokens.Database

    database_name = '{}.json'.format(database)

    if current_db == database_name:
        return 'Database currently in use !\n'

    if not os.path.isfile (database_name) :
        return 'Database does not exist !\n'

    os.remove (database_name)
    return 'Database deleted !\n'

def show_databases () :
    databases = [os.path.splitext(f)[0] for f in glob.glob('*.json')]
    t = Texttable ()
    t.add_row (databases)
    return (t.draw() + "\n")

def show_tables () :

    global current_db

    with open('{}'.format(current_db)) as f:
        json_data  = json.loads(f.read())

    tables = []

    for key, value in json_data.items ():
        tables.append (key)

    t = Texttable ()
    t.header = ['Tables']
    t.add_row (tables)

    return (t.draw())

#def start_transaction () :
    # Make a copy of the current database
    # Current database = copy

#def commit () :

#def rollback () :