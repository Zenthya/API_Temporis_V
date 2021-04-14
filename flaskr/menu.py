from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,request
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json
bp = Blueprint('menu', __name__,url_prefix="/menu")

@bp.route('/')
def index():
    db = get_db()
    counts_cartes = db.execute('SELECT count(*) nb_carte    FROM CARTES as c  ')
    counts_recettes = db.execute('SELECT count(*) nb_recette FROM    RECETTES as r  ')

    return render_template('menu/index.html', counts_cartes=counts_cartes, counts_recettes=counts_recettes)

@bp.route('/Cards',methods=('GET', 'POST'))
@login_required
def cards():
    db = get_db()



    if request.method == 'POST' :

        data = request.form['search']
        if "lvl?" in data :

            Cards = db.execute('SELECT id , name ,color,type,profession,level  FROM CARTES WHERE level == ? ORDER BY level DESC ', ( data[4:] ,))
        elif "mob?" in data :
            Cards = db.execute('SELECT id , name ,color,type,profession,level  FROM CARTES WHERE profession LIKE ? ORDER BY level DESC ', ("%" + data[4:] + "%",))
        elif "rar?" in data :
            Cards = db.execute('SELECT id , name ,color,type,profession,level  FROM CARTES WHERE color LIKE ? ORDER BY level DESC', ("%" + data[4:] + "%",))
        elif "typ?" in data :
            Cards = db.execute('SELECT id , name ,color,type,profession,level  FROM CARTES WHERE type LIKE ? ORDER BY level DESC ', ("%" + data[4:] + "%",))
        else :
            Cards = db.execute('SELECT id , name ,color,type,profession,level FROM CARTES WHERE name LIKE ? ',("%"+data+"%",))

    else :
        Cards = db.execute('SELECT id , name ,color,type,profession,level  FROM CARTES LIMIT 50')
    return render_template('menu/carte.html',Cards =Cards)
@bp.route('/Recipes',methods=('GET','POST'))
@login_required
def recipes():
    db = get_db()

    if request.method == 'POST' :
        data = request.form['search']