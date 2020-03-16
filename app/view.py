from app import app
from flask import render_template, request, redirect, url_for
from forms import BuildForm, AddBricks
from models import name_db
import sqlite3


@app.route('/')
def index():
    with sqlite3.connect(name_db) as conn:
        cur = conn.cursor()
        cur.execute("""select * from house order by address """)
        houses = cur.fetchall()
    return render_template('index.html', houses=houses)


@app.route('/building', methods=['GET', 'POST'])
def build_house():
    form = BuildForm()
    errors = []
    if request.method == 'POST':
        if form.validate_on_submit():
            address = request.form['address']
            building_year = int(request.form['build_date'])
            with sqlite3.connect(name_db) as conn:
                cur = conn.cursor()
                cur.execute("""select address from house
                                where address = ?""",
                            (address,)
                            )
                if not cur.fetchone():
                    cur.execute("""insert into house (address , building_year) VALUES (?,?)""",
                                (
                                    address,
                                    building_year
                                )
                                )
                    return redirect(url_for('index'))
                else:
                    errors.append('Дом с таким адресом уже существует')
    return render_template('build.html', form=form, errors=errors)


@app.route('/stats')
def statistic():
    with sqlite3.connect(name_db) as conn:
        cur = conn.cursor()
        cur.execute("""select h.address, task.date, sum(task.count_of_bricks) from house h
                       left join task on task.house_id = h.house_id
                       group by h.address, task.date
                       order by h.address, task.date""")
        statistics = cur.fetchall()
        statistic_with_sum = []
        address = statistics[0][0]
        sum = 0
        for stat in statistics:
            if stat[0] == address:
                try:
                    sum += stat[2]
                except TypeError:
                    sum = stat[2]
            else:
                address = stat[0]
                sum = stat[2]
            statistic_with_sum.append((stat, sum))
    return render_template('statistic.html', statistics=statistic_with_sum)


@app.route('/<id>/add-bricks', methods=['POST', 'GET'])
def add_bricks(id):
    form = AddBricks()
    if request.method == 'POST':
        if form.validate_on_submit():
            count_of_bricks = int(request.form['count_of_bricks'])
            date = request.form['date']
            with sqlite3.connect(name_db) as conn:
                conn.execute(
                    """insert into task (house_id , count_of_bricks, date) VALUES (?,?,?)""",
                    (
                        id,
                        count_of_bricks,
                        date
                    )
                )
            return redirect(url_for('index'))
    return render_template('add_bricks.html', form=form, id=id)
