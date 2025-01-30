from flask import Flask, request, redirect, render_template, send_file
from models import db, Nota, Tag, TagNota
from datetime import datetime, timedelta
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_tables():
    db.create_all()

def add_tags_to_nota(nota, tags):
    for tag_id in tags:
        tag = Tag.query.get(tag_id) or Tag(nome=f'Tag {tag_id}')
        db.session.add(tag)
        db.session.add(TagNota(nota=nota, tag=tag))

@app.get("/")
def index():
    return render_template("formulario.html", tags=Tag.query.all())

@app.post("/criar")
def criar_nota():
    titulo = request.form.get("titulo")
    citacao = request.form.get("citacao")
    autor = request.form.get("autor")
    tags = request.form.getlist("tags")
    nota = Nota(titulo=titulo, citacao=citacao, autor=autor)
    db.session.add(nota)
    add_tags_to_nota(nota, tags)
    db.session.commit()
    return redirect("/")

@app.get("/tags")
def tags():
    return render_template("tags.html", tags=Tag.query.all())

@app.post("/tags/criar")
def criar_tag():
    nome = request.form.get("nome")
    if nome:
        nova_tag = Tag(nome=nome)
        db.session.add(nova_tag)
        db.session.commit()
    return redirect("/tags")

@app.post("/tags/apagar/<int:tag_id>")
def apagar_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return redirect("/tags")

@app.get("/notas")
def notas():
    return render_template("notas.html", notas=Nota.query.all())

@app.get("/notas/filtrar")
def filtro_notas():
    tags = Tag.query.all()
    return render_template("filtro_notas.html", tags=tags)


@app.post("/notas/filtrar")
def filtrar_notas():
    data_minima = request.form.get("data_minima")
    data_maxima = request.form.get("data_maxima")
    data_exata = request.form.get("data_exata")
    tags = request.form.getlist("tags")
    autor = request.form.get("autor")
    citacao = request.form.get("citacao")

    query = Nota.query

    # Converter strings de data em objetos datetime
    if data_minima:
        data_minima = datetime.strptime(data_minima, '%Y-%m-%d')
        # Adiciona um dia para incluir todo o dia
        query = query.filter(Nota.data_criacao >= data_minima)

    if data_maxima:
        data_maxima = datetime.strptime(data_maxima, '%Y-%m-%d')
        # Adiciona um dia para incluir todo o dia
        query = query.filter(Nota.data_criacao < data_maxima + timedelta(days=1))

    if data_exata:
        data_exata = datetime.strptime(data_exata, '%Y-%m-%d')
        # Comparar apenas a data
        query = query.filter(db.func.date(Nota.data_criacao) == data_exata.date())

    if tags:
        query = query.join(TagNota).filter(TagNota.tag_id.in_(tags))

    if autor:
        query = query.filter(Nota.autor.ilike(f"%{autor}%"))

    if citacao:
        query = query.filter(Nota.citacao.ilike(f"%{citacao}%"))

    notas_filtradas = query.all()
    return render_template("notas.html", notas=notas_filtradas)

@app.post("/notas/apagar/<int:nota_id>")
def apagar_nota(nota_id):
    nota = Nota.query.get(nota_id)
    if nota:
        db.session.delete(nota)
        db.session.commit()
    return redirect("/notas")

@app.route('/exportar')
def exportar_db():
    db_path = './instance/data.db'
    return send_file(db_path, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)