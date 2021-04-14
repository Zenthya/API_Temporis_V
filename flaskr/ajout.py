from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,request
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('ajout', __name__,url_prefix="/ajout")


@bp.route('/card',methods=('GET', 'POST') )
@login_required
def card():
    db = get_db()
    error =None
    if request.method=='POST' :
        name_card= request.form['name_card']
        lvl_card = request.form['lvl_card']
        mob_card = request.form['mob_card']
        if  not name_card :
            error= "nom de la carte requis"
        elif not lvl_card :
            error =" lvl de la carte requis"
        elif not mob_card :
            error =" mob requis "
        elif db.execute('SELECT name FROM CARTES WHERE name= ?',(name_card,)).fetchone() is not None :
            error = "cette carte existe deja"
        else :

            db.execute('INSERT INTO CARTES(name,lv,Drop_mob)VALUES(?,?,?) ',(name_card,lvl_card,mob_card)

            )
            db.commit()
            return redirect(url_for("menu.cards"))
        flash(error)

    return render_template('Ajout/carte.html')