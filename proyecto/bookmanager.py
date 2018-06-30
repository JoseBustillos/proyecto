import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "proyecto.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Estudiantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=True)
    apellido = db.Column(db.String(30), unique=True, nullable=True)

    def __repr__(self):
        return "<Estudiante: {}>".format(self.id,self.nombre,self.apellido)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        estudiante = Estudiantes(id=request.form.get("id"),
                           nombre=request.form.get("nombre"),
                           apellido=request.form.get("apellido"))
        db.session.add(estudiante)
        db.session.commit()

    estudiantes = Estudiantes.query.all()
    num = len(estudiantes)
    return render_template("home.html", estudiantes=estudiantes,numero=num)
    # return render_template("home.html")

@app.route("/update", methods=["POST"])
def update():
    newId = request.form.get("newId")
    oldId = request.form.get("oldId")
    newNombre = request.form.get("newNombre")
    oldNombre = request.form.get('oldNombre')
    newApellido = request.form.get('newApellido')
    oldApellido  = request.form.get('oldApellido')
    estudiante = Estudiantes.query.filter_by(id=oldId).first()
    estudiante.id = newId
    estudiante.nombre = newNombre
    estudiante.apellido = newApellido
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    idEstudiante = request.form.get("id")
    print(idEstudiante)
    print("hola")
    estudiante = Estudiantes.query.filter_by(id=idEstudiante).first()
    db.session.delete(estudiante)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
