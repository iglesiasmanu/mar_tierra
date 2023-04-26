from flask import render_template, Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from mar_tierra import db
from mar_tierra.models import Visit, Product


main = Blueprint('main', __name__)
consent_yes = Blueprint('consent_yes', __name__)


@main.route("/")
@main.route("/home")
def home():
    ip_address = request.remote_addr
    visit = Visit.query.filter_by(ip_address=ip_address).first()


    if visit:
        visit.visit_count += 1
    else:
        visit = Visit(ip_address=ip_address, visit_count=1, consent_given=False)
        db.session.add(visit)

    return render_template('main/home.html', ip_address=ip_address, consent_given=visit.consent_given)


