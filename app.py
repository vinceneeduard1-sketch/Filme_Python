from flask import Flask, render_template, request, redirect, url_for
from db_manager import DBManager

app = Flask(__name__)
db = DBManager()


# --- HOME ---
@app.route('/')
def index():
    # Presupunem ca ai un index.html, daca nu, il cream sau redirectionam
    return render_template('layout.html')


# ================= SECȚIUNEA FILME =================

# 1. Tabel Filme
@app.route('/filme')
def filme():
    data = db.select("SELECT * FROM filme")
    return render_template('tabel_filme.html', filme=data)


# 2. Adauga Film
@app.route('/filme/adauga', methods=['GET', 'POST'])
def adauga_film():
    if request.method == 'POST':
        titlu = request.form['titlu']
        an = request.form['an_aparitie']
        durata = request.form['durata']
        regizor = request.form['regizor']

        sql = "INSERT INTO filme (titlu, an_aparitie, durata, regizor) VALUES (%s, %s, %s, %s)"
        db.execute(sql, (titlu, an, durata, regizor))

        # Dupa adaugare, afisam pagina de succes
        return render_template('succes.html', mesaj="Filmul a fost adăugat!", link="/filme")

    return render_template('adauga_filme.html')


# 3. Modifica Film
@app.route('/filme/modifica/<int:id_film>', methods=['GET', 'POST'])
def modifica_film(id_film):
    if request.method == 'POST':
        titlu = request.form['titlu']
        an = request.form['an_aparitie']
        durata = request.form['durata']
        regizor = request.form['regizor']

        sql = "UPDATE filme SET titlu=%s, an_aparitie=%s, durata=%s, regizor=%s WHERE id_film=%s"
        db.execute(sql, (titlu, an, durata, regizor, id_film))

        return render_template('succes.html', mesaj="Filmul a fost modificat!", link="/filme")

    else:
        film = db.select_one("SELECT * FROM filme WHERE id_film = %s", (id_film,))
        return render_template('modifica_filme.html', film=film)


# 4. Sterge Film
@app.route('/filme/sterge/<int:id_film>')
def sterge_film(id_film):
    db.execute("DELETE FROM filme WHERE id_film=%s", (id_film,))
    return redirect(url_for('filme'))


# ================= SECȚIUNEA CATEGORII =================

# 1. Tabel Categorii
@app.route('/categorii')
def categorii():
    data = db.select("SELECT * FROM categorii")
    return render_template('tabel_categorii.html', categorii=data)


# 2. Adauga Categorie
@app.route('/categorii/adauga', methods=['GET', 'POST'])
def adauga_categorie():
    if request.method == 'POST':
        nume = request.form['nume_categorie']
        db.execute("INSERT INTO categorii (nume_categorie) VALUES (%s)", (nume,))
        return render_template('succes.html', mesaj="Categoria a fost adăugată!", link="/categorii")

    return render_template('adauga_categorii.html')


# 3. Modifica Categorie
@app.route('/categorii/modifica/<int:id_cat>', methods=['GET', 'POST'])
def modifica_categorie(id_cat):
    if request.method == 'POST':
        nume = request.form['nume_categorie']
        db.execute("UPDATE categorii SET nume_categorie=%s WHERE id_categorie=%s", (nume, id_cat))
        return render_template('succes.html', mesaj="Categoria a fost modificată!", link="/categorii")

    else:
        cat = db.select_one("SELECT * FROM categorii WHERE id_categorie=%s", (id_cat,))
        return render_template('modifica_categorii.html', cat=cat)


# Sterge Categorie
@app.route('/categorii/sterge/<int:id_cat>')
def sterge_categorie(id_cat):
    db.execute("DELETE FROM categorii WHERE id_categorie=%s", (id_cat,))
    return redirect(url_for('categorii'))


# ================= SECȚIUNEA ÎNCADRĂRI =================

# 1. Tabel Incadrari
@app.route('/incadrari')
def incadrari():
    sql = """
        SELECT i.id_incadrare, f.titlu, f.an_aparitie, c.nume_categorie, i.tip 
        FROM incadrare_filme i
        JOIN filme f ON i.id_film = f.id_film
        JOIN categorii c ON i.id_categorie = c.id_categorie
    """
    data = db.select(sql)
    return render_template('tabel_incadrari.html', incadrari=data)


# 2. Adauga Incadrare
@app.route('/incadrari/adauga', methods=['GET', 'POST'])
def adauga_incadrare():
    if request.method == 'POST':
        id_f = request.form['id_film']
        id_c = request.form['id_categorie']
        tip = request.form['tip']

        db.execute("INSERT INTO incadrare_filme (id_film, id_categorie, tip) VALUES (%s, %s, %s)", (id_f, id_c, tip))
        return render_template('succes.html', mesaj="Încadrarea a fost creată!", link="/incadrari")

    filme = db.select("SELECT * FROM filme")
    categorii = db.select("SELECT * FROM categorii")
    return render_template('adauga_incadrari.html', filme=filme, categorii=categorii)


# 3. Modifica Incadrare
@app.route('/incadrari/modifica/<int:id_inc>', methods=['GET', 'POST'])
def modifica_incadrare(id_inc):
    if request.method == 'POST':
        id_f = request.form['id_film']
        id_c = request.form['id_categorie']
        tip = request.form['tip']

        sql = "UPDATE incadrare_filme SET id_film=%s, id_categorie=%s, tip=%s WHERE id_incadrare=%s"
        db.execute(sql, (id_f, id_c, tip, id_inc))
        return render_template('succes.html', mesaj="Încadrarea a fost actualizată!", link="/incadrari")

    else:
        inc = db.select_one("SELECT * FROM incadrare_filme WHERE id_incadrare=%s", (id_inc,))
        filme = db.select("SELECT * FROM filme")
        categorii = db.select("SELECT * FROM categorii")
        return render_template('modifica_incadrari.html', inc=inc, filme=filme, categorii=categorii)


# Sterge Incadrare
@app.route('/incadrari/sterge/<int:id_inc>')
def sterge_incadrare(id_inc):
    db.execute("DELETE FROM incadrare_filme WHERE id_incadrare=%s", (id_inc,))
    return redirect(url_for('incadrari'))


if __name__ == '__main__':
    app.run(debug=True)