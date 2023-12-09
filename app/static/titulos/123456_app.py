from flask import Flask, send_from_directory, request, render_template
import sqlite3
from datetime import datetime

import traceback
import sys

app = Flask(__name__, static_folder='static', template_folder='templates')




@app.route("/")
def entry_form():
    return send_from_directory(app.static_folder, "form.html")

@app.route("/intro", methods=['POST'])
def intro_form():
    # VALIDAR LA INFO RECIBIDA
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    dni = request.form["dni"]
    cp = request.form["cp"]
    nacimiento = request.form["nacimiento"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    gender = request.form.get("gender")
    servicio_activo = request.form["servicio_activo"]
    grado = request.form["grado"]
    equivalencia = request.form["equivalencia"]

    print(request.form)
    print(servicio_activo)
    categoria = request.form["categoria"]

    # TODO validar variables
    # edad < 60
    try:
        limit = datetime.now()
        n = datetime.strptime(nacimiento, "%Y-%m-%d")
        edad = limit.year - n.year
        #añadir aqui el motivo concreto por el que no se puede matricular y citar la norma
        #cambiar la nueva página de error por un pop-up
        if edad > 60:
            return "DEMASIADO MAYOR"
        if edad == 60:
            if limit.month < n.month:
                return "DEMASIADO MAYOR"
            elif limit.month == n.month and limit.day >= n.day:
                return "DEMASIADO MAYOR"
        
    except:
        return "La fecha de nacimiento no se ha recibido con el formato esperado. Consulte con la administración"

    # categoria == oficial
    if categoria != "oficial":
        return "Necesita ser oficial para poder acceder"

    # Elegir Género
    if gender not in ['Hombre', 'Mujer']:
        error = 'Invalid gender'
        return "Tiene que seleccionar un género"

    # equivalencia == si

    # grado  == no
    if grado != "no":
        return "Si ya tiene un grado no puede matricularse."

    # servicio activo != otro
    if servicio_activo == "otro":
        return "Su situación administrativa no es válida"

    # titulo = request.form["titulo"]
    # fotografia

    # ESCRIBIRLO EN LA BD
    try:
        with sqlite3.connect("/var/admision/admision.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO admision_2023 (nombre,apellidos,DNI,gender,CP,fecha_nacimiento,telefono,email,escalafon,situacion_servicio,grado,categoria_profesional,equivalencia_titulo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(nombre,apellidos,dni,cp,nacimiento,telefono,email,10,servicio_activo,grado,categoria,equivalencia) )
            con.commit()
    except Exception as e:
        print(e)
        con.rollback()
        return "Error del servidor, pruebe más tarde."
    finally:
        con.close()

    # REPORTAR OK
    return "Datos insertados correctamente"


@app.route("/consulta")
def dump_db():
    try:
        with sqlite3.connect("/var/admision/admision.db") as con:
            cur = con.cursor()
            
            cur.execute("SELECT * FROM admision_2023 ORDER BY escalafon ASC LIMIT 0,1 ;")
            result = cur.fetchall()


            print(result)
            return render_template("datos.html", result=result)

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        # or
        print(sys.exc_info()[2])
        print("except")
        return "Error"
    finally:
        con.close()