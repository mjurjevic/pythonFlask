
from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", 
    
	database="kolokvijum2" # napraviti bazu i importovati
    # korisnik.sql u nju 
    )


def pretvori(zer):
	zer = list(zer)
	n = len(zer)

	for i in range(n):
		if isinstance(zer[i],bytearray):
			zer[i] = zer[i].decode()

	return zer

@app.route('/')
def index():
    return 'Hello world'

@app.route('/register',methods=['POST','GET'])
def register():
	if request.method == 'GET':
		return render_template(
			'register.html'
		)
	
	broj_indeksa = request.form['broj_indeksa']
	ime_prezime = request.form['ime_prezime']
	godina = request.form['godina']
	password = request.form['password']
	confirm = request.form['confirm']
	prosek = request.form['prosek']
	broj_polozenih = request.form['broj_polozenih']

	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM korisnik WHERE broj_indeksa=?'
	vrednost = (broj_indeksa, )
	cursor.execute(sql,vrednost)

	rez = cursor.fetchone()

	if rez != None:
		return render_template(
			'register.html',
			index_greska= 'Korisnik sa ovim indeksom vec postoji u bazi'
		)
	
	if confirm != password:
		return render_template(
			'register.html',
			conf_greska = 'Ne poklapaju se'
		)
	
	ispiti = int(broj_polozenih)

	if ispiti < 0:
		return render_template(
			'register.html',
			broj_polozenih_greska ='Broj je negativan'
		)

	prosek1 = float(prosek)

	if (prosek1 < 6 or prosek1 > 10):
		return render_template(
			'register.html',
			prosek_greska = 'Prosek nije izmedju 6 i 10'
		)

	cursor = mydb.cursor(prepared=True)
	sql = 'INSERT INTO korisnik VALUES(null,?,?,?,?,?,?)'
	vrednosti=(broj_indeksa,ime_prezime,godina,password,prosek,broj_polozenih)
	cursor.execute(sql,vrednosti)
	mydb.commit()

	return redirect(url_for('show_all'))

@app.route('/show_all')

def show_all():
	cursor=mydb.cursor(prepared=True)
	sql = 'SELECT * FROM korisnik'
	cursor.execute(sql)
	rez = cursor.fetchall()

	n= len(rez)
	for i in range(n):
		rez[i] = pretvori(rez[i])

	return render_template(
		'show_all.html',
		podaci = rez
	)

@app.route('/login',methods=['POST','GET'])

def login():
	if request.method == 'GET':
		return render_template(
			'login.html'
		)
	
	broj_indeksa = request.form['broj_indeksa']
	password = request.form['password']

	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM korisnik WHERE broj_indeksa=?'
	vrednost=(broj_indeksa, )

	cursor.execute(sql,vrednost)
	rez = cursor.fetchone()

	if rez == None:
		return render_template(
			'login.html',
			index_greska= 'Korisnik ne postoji sa ovim indeksom  u bazi'
		)
	
	rez = pretvori(rez)

	if rez[4] != password:
		return render_template(
			'login.html',
			pass_greska = 'Losa sifra'
		)

	session['broj_indeksa'] = broj_indeksa

	return redirect(url_for('show_all'))


@app.route('/logout')

def logout():
	if 'broj_indeksa' in session:
		session.pop('broj_indeksa')
		return redirect(url_for('login'))
	else:
		return redirect(url_for('show_all'))

@app.route('/delete/<broj_indeksa>', methods=['POST'])

def delete(broj_indeksa):
	if 'broj_indeksa' not in session:
		return redirect(url_for('login'))

	cursor = mydb.cursor(prepared=True)
	sql = 'DELETE FROM korisnik WHERE broj_indeksa=?'
	vrednost =(broj_indeksa,)

	cursor.execute(sql,vrednost)

	mydb.commit()

	return redirect(url_for('show_all'))

@app.route('/update/<broj_indeksa>',methods=['POST','GET'])

def update(broj_indeksa):
	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM korisnik WHERE broj_indeksa=?'
	vrednost = (broj_indeksa, )
	cursor.execute(sql,vrednost)
	rez = cursor.fetchone()
	rez= pretvori(rez)

	if request.method == 'GET':
		return render_template(
			'update.html',
			korisnik = rez
		)

	broj_indeksa = request.form['broj_indeksa']
	ime_prezime = request.form['ime_prezime']
	godina = request.form['godina']
	password = request.form['password']
	confirm = request.form['confirm']
	prosek = request.form['prosek']
	broj_polozenih = request.form['broj_polozenih']

	rez= pretvori(rez)

	if confirm != password:
		return render_template(
			'update.html',
			conf_greska = 'Ne poklapaju se',
			korisnik = rez
		)

	ispiti = int(broj_polozenih)

	if ispiti < 0:
		return render_template(
			'update.html',
			broj_polozenih_greska ='Broj je negativan',
			korisnik = rez
		)

	prosek1 = float(prosek)

	if (prosek1 < 6 or prosek1 > 10):
		return render_template(
			'update.html',
			prosek_greska = 'Prosek nije izmedju 6 i 10',
			korisnik = rez
		)

	cursor= mydb.cursor(prepared=True)
	sql = 'UPDATE korisnik SET ime_prezime=?,godina_rodjenja=?,sifra=?,prosek=?,polozeni_ispiti=? WHERE broj_indeksa=?'
	vrednost = (ime_prezime,godina,password,prosek,broj_polozenih,broj_indeksa)
	cursor.execute(sql,vrednost)
	mydb.commit()
	
	return redirect(url_for('show_all'))

# @app.route('/better_than_average/<average>', methods=['POST','GET'])
# def better_than_average(average):
# 	cursor = mydb.cursor(prepared=True)
# 	sql = 'SELECT * FROM korisnik WHERE prosek=?'
# 	cursor.execute(average,)
# 	rez = cursor.fetchall()
# 	n=len(rez)
# 	for i in range(n):
# 		rez[i] = pretvori(rez[i])

# 	return render_template(
# 		'better_than_average.html',
# 		covek=rez
# 	)

app.run(debug=True)
