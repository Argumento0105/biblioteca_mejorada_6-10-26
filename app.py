from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "bd_biblioteca.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def crear_bd():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            categoria TEXT NOT NULL,
            anio INTEGER NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            estudiante TEXT NOT NULL,
            libro_id INTEGER NOT NULL,
            FOREIGN KEY (libro_id) REFERENCES libros(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            duracion INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def inicio():
    return redirect(url_for("listar_libros"))


@app.route("/libros")
def listar_libros():
    conn = get_db_connection()
    libros = conn.execute(
        "SELECT * FROM libros ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("libros.html", libros=libros)


@app.route("/libro/nuevo", methods=("GET", "POST"))
def nuevo_libro():

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        categoria = request.form["categoria"]
        anio = request.form["anio"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO libros (titulo, autor, categoria, anio)
            VALUES (?, ?, ?, ?)
        """, (titulo, autor, categoria, anio))

        conn.commit()
        conn.close()

        return redirect(url_for("listar_libros"))

    return render_template("form_libro.html")


@app.route("/libro/eliminar/<int:id>")
def eliminar_libro(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM libros WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("listar_libros"))


@app.route("/prestamos")
def listar_prestamos():

    conn = get_db_connection()

    prestamos = conn.execute("""
        SELECT
            prestamos.id,
            prestamos.fecha,
            prestamos.estudiante,
            libros.titulo
        FROM prestamos
        INNER JOIN libros
        ON prestamos.libro_id = libros.id
        ORDER BY prestamos.id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "prestamos.html",
        prestamos=prestamos
    )


@app.route("/prestamo/nuevo", methods=("GET", "POST"))
def nuevo_prestamo():

    conn = get_db_connection()

    libros = conn.execute(
        "SELECT * FROM libros ORDER BY titulo"
    ).fetchall()

    if request.method == "POST":

        fecha = request.form["fecha"]
        estudiante = request.form["estudiante"]
        libro_id = request.form["libro_id"]

        conn.execute("""
            INSERT INTO prestamos
            (fecha, estudiante, libro_id)
            VALUES (?, ?, ?)
        """, (fecha, estudiante, libro_id))

        conn.commit()
        conn.close()

        return redirect(url_for("listar_prestamos"))

    conn.close()

    return render_template(
        "form_prestamo.html",
        libros=libros
    )


@app.route("/prestamo/eliminar/<int:id>")
def eliminar_prestamo(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM prestamos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("listar_prestamos"))



@app.route("/estudiantes")
def listar_estudiantes():

    conn = get_db_connection()

    estudiantes = conn.execute("""
        SELECT * FROM estudiantes
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "estudiantes.html",
        estudiantes=estudiantes
    )


@app.route("/estudiante/nuevo", methods=("GET", "POST"))
def nuevo_estudiante():

    if request.method == "POST":

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        correo = request.form["correo"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO estudiantes
            (nombre, apellido, correo)
            VALUES (?, ?, ?)
        """, (
            nombre,
            apellido,
            correo
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("listar_estudiantes"))

    return render_template("form_estudiante.html")


@app.route("/estudiante/eliminar/<int:id>")
def eliminar_estudiante(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM estudiantes WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("listar_estudiantes"))


@app.route("/cursos")
def listar_cursos():

    conn = get_db_connection()

    cursos = conn.execute("""
        SELECT * FROM cursos
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "cursos.html",
        cursos=cursos
    )


@app.route("/curso/nuevo", methods=("GET", "POST"))
def nuevo_curso():

    if request.method == "POST":

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        duracion = request.form["duracion"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO cursos
            (nombre, descripcion, duracion)
            VALUES (?, ?, ?)
        """, (
            nombre,
            descripcion,
            duracion
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("listar_cursos"))

    return render_template("form_curso.html")


@app.route("/curso/eliminar/<int:id>")
def eliminar_curso(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM cursos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("listar_cursos"))

if __name__ == "__main__":
    crear_bd()
    app.run(debug=True)
