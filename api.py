from flask import Flask, render_template, jsonify,abort,request
app=Flask(__name__)
pelis=[{'id':1, 'name':'the proposal', 'status': False}, {'id':2, 'name':'the other woman', 'status': False}]
uri='/api/pelis/'

@app.route("/")
def bienvenida():
    return render_template("bienvenida.html")

@app.route(uri, methods=['GET'])
def getMovies():
    return jsonify({'pelis':pelis})

@app.route(uri+'<string:name>', methods=['GET'])
def getMovie(name):
    this_movie=0
    for peli in pelis:
        if peli['name']==name:
            this_movie=peli
    if this_movie==0:
        abort(404)
    return jsonify({'pelis': this_movie})

#AGREGAR TAREA
@app.route(uri, methods=['POST'])
def create_movie():
    if request.json:
        movie={
            'id':len(pelis)+1,
            'name': request.json['name'], 'status':False
        }
        pelis.append(movie)
        return jsonify({'pelis':pelis})
    else:
        abort(404)

@app.route(uri+'<string:name>', methods=['PUT'])
def update_movie(name):
    if request.json:
        #this task va a tener una lista, una lista tiene elementos por posicion
            #en el primer for se utiliza porque no importa el indice, de la lista task toma cada
            #elemento y la vacia en la variable task y en cada iteracion se pregunta si el id 
            #es el que se busca
        this_movie=[peli for peli in pelis if peli['name']==name]
        if this_movie:
            if request.json.get('name'):
                this_movie[0]['name']=request.json['name']

            if request.json.get('status'):
                this_movie[0]['status']=request.json['status']

            return jsonify({'task': this_movie[0]}), 201
        else:
            abort(404)
    else:
        abort(404)

@app.route(uri+'<string:name>', methods=['DELETE'])
def delete_movie(name):
    this_movie=[peli for peli in pelis if peli['name']==name]
    if this_movie:
        pelis.remove(this_movie[0])
        return jsonify({'pelis': pelis})
    else:
        abort(404)

if __name__=='__main__':
    app.run(debug=True)