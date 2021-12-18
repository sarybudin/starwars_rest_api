from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#class User(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  email = db.Column(db.String(120), unique=True, nullable=False)
   # password = db.Column(db.String(80), unique=False, nullable=False)
    #is_active = db.Column(db.Boolean(), unique=False, nullable=False)

   # def __repr__(self):
    #    return '<User %r>' % self.username

    #def serialize(self):
     #   return {
      #      "id": self.id,
       #     "email": self.email,
            # do not serialize the password, its a security breach
#}

    

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False) 
    diametro = db.Column(db.Integer)
    poblacion = db.Column(db.Integer)
    clima = db.Column(db.String(50))
    personajes = db.relationship("Personajes", back_populates="planetas")
    favoritoplanetas = db.relationship("FavoritoPlanetas", back_populates="planetas")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "poblacion": self.poblacion,
            "clima": self.clima,
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    planeta_origen = db.Column(db.Integer,db.ForeignKey('planetas.id'))
    estatura = db.Column(db.Integer)
    colorojos = db.Column(db.String(50))
    planetas = db.relationship("Planetas", back_populates="personajes")
    vehiculos = db.relationship("Vehiculos", back_populates="personajes")
    favoritopersonajes = db.relationship("FavoritoPersonajes", back_populates="personajes")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "planeta_origen": self.planeta_origen,
            "estatura": self.estatura,
            "colorojos": self.colorojos,
        }

class Vehiculos(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False) 
    modelo = db.Column(db.String(50))
    color = db.Column(db.String(50))
    conductor = db.Column(db.String(50))
    id_personaje = db.Column(db.Integer,db.ForeignKey('personajes.id'))
    personajes = db.relationship("Personajes", back_populates="vehiculos")
    favoritovehiculos = db.relationship("FavoritoVehiculos", back_populates="vehiculos")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "color": self.color,
            "conductor": self.conductor,
            "id_personaje": self.id_personaje,
        }

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50))
    favoritopersonajes = db.relationship("FavoritoPersonajes", back_populates="usuario")
    favoritoplanetas = db.relationship("FavoritoPlanetas", back_populates="usuario")
    favoritovehiculos = db.relationship("FavoritoVehiculos", back_populates="usuario")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
        }

    def serializeFavorite(self):
        favoritopersonajes = list(map(lambda x: x.serialize(), self.favoritopersonajes))
        favoritoplanetas = list(map(lambda x: x.serialize(), self.favoritoplanetas))
        favoritovehiculos = list(map(lambda x: x.serialize(), self.favoritovehiculos))
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "favoritopersonajes": favoritopersonajes,
            "favoritoplanetas": favoritoplanetas,
            "favoritovehiculos": favoritovehiculos,
        }

class FavoritoPersonajes(db.Model):
    __tablename__ = 'favoritopersonajes'
    id_favorito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    id_personaje = db.Column(db.Integer,db.ForeignKey('personajes.id'))
    usuario = db.relationship("Usuario", back_populates="favoritopersonajes")
    personajes = db.relationship("Personajes", back_populates="favoritopersonajes")
    
    def serialize(self):
        return {
            "id_favorito": self.id_favorito,
            "id_usuario": self.id_usuario,
            "id_personaje": self.id_personaje,
        }

class FavoritoPlanetas(db.Model):
    __tablename__ = 'favoritoplanetas'
    id_favorito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    id_planeta = db.Column(db.Integer,db.ForeignKey('planetas.id'))
    usuario = db.relationship("Usuario", back_populates="favoritoplanetas")
    planetas = db.relationship("Planetas", back_populates="favoritoplanetas")
    
    def serialize(self):
        return {
            "id_favorito": self.id_favorito,
            "id_usuario": self.id_usuario,
            "id_planeta": self.id_planeta,
        }

class FavoritoVehiculos(db.Model):
    __tablename__ = 'favoritovehiculos'
    id_favorito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    id_vehiculo = db.Column(db.Integer,db.ForeignKey('vehiculos.id'))
    usuario = db.relationship("Usuario", back_populates="favoritovehiculos")
    vehiculos = db.relationship("Vehiculos", back_populates="favoritovehiculos")
    
    def serialize(self):
        return {
            "id_favorito": self.id_favorito,
            "id_usuario": self.id_usuario,
            "id_vehiculo": self.id_vehiculo,
        }

def to_dict(self):
    return {}

## Draw from SQLAlchemy base
