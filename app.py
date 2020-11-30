from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "mndkfjkdsfj"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mycountry'
app.config['MYSQL_DB'] = 'darts'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        name = request.form['nm']

        session['name'] = name

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dart VALUES (%s, %s)", (name, 501))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('game'))

    return render_template('home.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    final_value = 501
    if request.method == 'POST':
        number = request.form['num']

        if 'name' in session:
            name = session['name']

        cur = mysql.connection.cursor()

        cur.execute("SELECT score FROM dart WHERE name = %s", (name,))

        value = cur.fetchall()
        final_value = value[0][0]
        final_value -= int(number)

        if final_value == 0:
            cur.execute("DELETE FROM dart WHERE name = %s", (name,))
            mysql.connection.commit()

            session.pop('name', None)

            flash('You have done your rounds and completed 501 points!!!', 'info')
            return render_template('home.html')

        cur.execute("UPDATE dart SET score = %s where name = %s", (final_value, name))
        mysql.connection.commit()
        cur.close()

        return render_template('calc.html', final_value=final_value)

    return render_template('calc.html', final_value=final_value)


if __name__ == '__main__':
    app.run()
