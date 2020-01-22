from flask import Flask, request, jsonify
import json
import requests
app = Flask(__name__)
def select(name_table):
    
    tab=dict()
    liste = []
    i = 0 
    k = 0
    with open('schools.json') as f:
        json_data  = json.loads(f.read())
    for key, value in json_data.items():
        if key != name_table:continue 
        print(key, '--')
        for subject, score in value.items():
            table = dict()
            for j, p in score.items(): 
                print(j)
                table[j] = p
            tab[subject]=table
                
    return tab

@app.route('/user/<string:name>', methods = ['GET'])
def get_all_users(name):
    return select(name)

@app.route('/insertion/<string:table_name>', methods = ['POST'])
def insertion_data(table_name):

    data = request.get_json() 
    with open('schools.json') as f:
        data_dict = json.load(f)
    taille = len(data_dict[table_name]) + 1
    data_dict[table_name][taille] = data
    fichier = open('schools.json','w')
    fichier.write(json.dumps(data_dict, indent=4))

    return data

@app.route('/table', methods = ['POST'])
def create_table () :

    with open ('schools.json', 'r+') as f:

        try:
            db = json.load(f)
        except :
            db = {}

       
        db = request.get_json()
        json.dump (db, f, indent = 4)
        f.truncate ()
        f.close()

    return "Table created !"



if __name__ == '__main__':
    app.run(debug = True, port = 8889)
    