# import library
from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
# init main app
app = Flask (__name__)
# kunci rahasia agar session bisa berjalan
app.secret_key = '!@#$%!'
# database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'
# init mysql
mysql = MySQL (app)

# Set route default dan http method yang dizinkan @app.route('/', methods=['GET', 'POST'))
@app.route('/', methods=['GET', 'POST'])
def login():
    # Cek jika method POST dan ada form data maka proses login
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        # Buat variabel untuk memudahkan pengolahan data
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        
        # Cursor koneksi mysql
        cur = mysql.connection.cursor()

        # Eksekusi kueri
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, passwd))

        # Fetch hasil kueri
        result = cur.fetchone()

        # Cek hasil kueri
        if result:
            # Jika login valid, buat data session
            session['is_logged_in'] = True
            session['username'] = result[1]
            # Redirect ke halaman home
            return redirect(url_for('home'))
        else:
            # Jika login invalid, kembalikan ke login form
            return render_template('login.html')
    else:
        # Jika method selain POST, tampilkan form login
        return render_template('login.html')

# route home
@app.route('/home')
def home():
    # cek session apakah sudah login
    if 'is_logged_in' in session:
        # cursor koneksi mysql
        cur = mysql.connection.cursor()
        # eksekusi kueri
        cur.execute("SELECT * FROM users")
        # fetch hasil kueri
        users_data = cur.fetchall()
        # tutup koneksi
        cur.close()
        # render data bersama template
        return render_template('home.html', users=users_data)
    else:
        return redirect(url_for('login'))

# route logout
@app.route('/logout')
def logout():
    # hapus data session
    session.pop('is_logged_in', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# debug dan auto reload
if __name__ == '__main__':
    app.run(debug=True)
