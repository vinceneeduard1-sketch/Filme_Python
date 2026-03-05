# Interfață Web pentru Gestiunea unei Baze de Date (Python & Flask)

Acest proiect a fost realizat de către **Vincene Eduard** din grupa **433A**.

##  Descriere Generală
Proiectul presupune crearea unei aplicații web pentru gestionarea unei baze de date MySQL. Prin această interfață, se realizează accesul la o bază de date ce stochează informații despre filme și categorii, având la bază o asociere de tip M:N.

Logica de backend și comunicarea cu baza de date se realizează exclusiv prin intermediul limbajului Python (utilizând framework-ul Flask), asigurând o structură flexibilă și eficientă.

##  Funcționalități Principale
* **Vizualizare date:** Aplicația preia și afișează datele din tabele sub formă tabelară, inclusiv rezolvarea asocierilor M:N (afișarea datelor referite).
* **Adăugare de la distanță:** Permite introducerea de noi filme, categorii sau încadrări prin intermediul unor formulare web și trimiterea lor către baza de date.
* **Modificare date:** Formularele preiau datele existente pe baza ID-ului selectat și permit actualizarea (UPDATE) acestora în baza de date.
* **Ștergere date:** Utilizatorul poate selecta și șterge (DELETE) rapid una sau mai multe înregistrări direct din interfața web.

##  Structura Codului (Funcții Cheie)

### 1. Gestionarea Bazei de Date (`DBManager`)
Clasa principală care centralizează interacțiunea cu serverul MySQL. Conține metodele `connect()` pentru inițializarea conexiunii și `disconnect()` pentru închiderea securizată a resurselor.

### 2. Manipularea Datelor (`select` & `execute`)
* **`select`**: Execută interogări de tip READ (SELECT) și returnează rezultatele sub formă de dicționar pentru generarea dinamică a paginilor HTML.
* **`execute`**: Gestionează interogările care modifică starea bazei de date (INSERT, UPDATE, DELETE), aplicând automat `commit()` pentru a salva modificările.

### 3. Integrarea Web (`app.py` & rutele)
* **`filme()` / `incadrari()`**: Realizează cererile către baza de date pentru a obține listele complete de date.
* **`adauga_film()` / `modifica_film()`**: Procesează cererile GET (afișare formular) și POST (trimitere date formular) pentru a actualiza informațiile.

##  Structura Bazei de Date (Tabele)
Aplicația gestionează informațiile folosind următoarele tabele:
* **filme** (id_film, titlu, an_aparitie, durata, regizor)
* **categorii** (id_categorie, nume_categorie)
* **incadrare_filme** (tabelă de joncțiune M:N - id_incadrare, id_film, id_categorie, tip)

---
**Tehnologii utilizate:** Python, Flask, MySQL (mysql.connector), HTML, Jinja2.
