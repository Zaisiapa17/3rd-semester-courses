# import library third party
from flask import Flask, render_template
from flask_mysqldb import MySQL
# init main app
app = Flask (__name__)
# database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'
# init mysql
mysql = MySQL (app)
# set route default
@app.route('/')
def home ():
    # cursor koneksi mysql
    cur = mysql.connection.cursor()
    # eksekusi kueri
    cur.execute("SELECT * FROM users")
    # fetch hasil kueri masukkan ke var data
    data = cur.fetchall ()
    # tutup koneksi
    cur.close()
    # render array data sebagai users bersama template
    return render_template('home.html', users=data)
    # debug dan auto reload

# debug dan auto reload
if __name__ == '__main__':
    app.run(debug=True)

