"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Personajes, Planetas, Usuario, FavoritoPlanetas, FavoritoPersonajes
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# [GET] /people Listar todos los registros de people en la base de datos
@app.route('/people', methods=['GET'])
def personajes():
    personajesTodos= Personajes.query.all()
    personajesTodos= list(map(lambda x: x.serialize(), personajesTodos))

    return jsonify(personajesTodos), 200

#[GET] /people/<int:people_id> Listar la información de una sola people
@app.route('/people/<int:people_id>', methods=['GET'])
def personaje(people_id):
    personaje= Personajes.query.get(people_id)
    if personaje == None:
        return {}
    else:
        return jsonify(personaje.serialize()), 200

# [GET] /planets Listar los registros de planets en la base de datos
@app.route('/planets', methods=['GET'])
def planetas():
    planetasTodos= Planetas.query.all()
    planetasTodos= list(map(lambda x: x.serialize(), planetasTodos))

    return jsonify(planetasTodos), 200

# [GET] /planets/<int:planet_id> Listar la información de un solo planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def planeta(planet_id):
    planeta = Planetas.query.get(planet_id)
    if planeta == None:
        return {}
    else:
        return jsonify(planeta.serialize()), 200

#[GET] /users Listar todos los usuarios del blog
@app.route('/users', methods=['GET'])
def usuario():
    usuarioTodos= Usuario.query.all()
    usuarioTodos= list(map(lambda x: x.serialize(), usuarioTodos))

    return jsonify(usuarioTodos), 200

# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
@app.route('/users/favorites', methods=['GET'])
def usuarioFavorites():
    usuarioTodos= Usuario.query.all()
    usuarioTodos= list(map(lambda x: x.serializeFavorite(), usuarioTodos))

    return jsonify(usuarioTodos), 200

# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planetfavorito al usuario actual con el planet id = planet_id
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def agregarFavoritoPlanetas(planet_id, user_id):
    nuevofavorito = FavoritoPlanetas(
        id_planeta=planet_id,
        id_usuario=user_id
    )
    db.session.add(nuevofavorito)
    db.session.commit()
    return 'ok'

# [POST] /favorite/people/<int:planet_id> Añade una nueva peoplefavorita al usuario actual con el people.id = people_id.
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['POST'])
def agregarFavoritoPersonajes(people_id, user_id):
    nuevofavorito = FavoritoPersonajes(
        id_personaje=people_id,
        id_usuario=user_id
    )
    db.session.add(nuevofavorito)
    db.session.commit()
    return 'ok'

# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def eliminarFavoritoPlanetas(planet_id, user_id):
    #obj = FavoritoPlanetas.query.\
    #filter(FavoritoPlanetas.id_usuario.like(user_id)).\
    #filter(FavoritoPlanetas.id_planeta.like(planet_id)).\
    #one()
    #db.session.delete(obj)
    db.session.query(FavoritoPlanetas).\
    filter(FavoritoPlanetas.id_usuario.like(user_id)).\
    filter(FavoritoPlanetas.id_planeta.like(planet_id)).\
    delete(synchronize_session=False)
    db.session.commit()
    return 'ok'

# [DELETE] /favorite/people/<int:people_id> Elimina una peoplefaorita con el id = people_id.
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def eliminarFavoritoPersonajes(people_id, user_id):
    db.session.query(FavoritoPersonajes).\
    filter(FavoritoPersonajes.id_usuario.like(user_id)).\
    filter(FavoritoPersonajes.id_personaje.like(people_id)).\
    delete(synchronize_session=False)
    db.session.commit()
    return 'ok'




## otros
@app.route('/personajes', methods=['POST'])
def agregarpersonajes():
    body = request.get_json()
    nuevoPersonaje = Personajes(
        nombre=body["nombre"],
        planeta_origen=body["planeta_origen"],
        estatura=body["estatura"],
        colorojos=body["colorojos"]
    )
    db.session.add(nuevoPersonaje)
    db.session.commit()
    return 'personaje'



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
