from application import app, db
from flask import jsonify

from application.races import Race

@app.route("/races/<race_id>/")
def get_race(race_id):
	race = Race.query.get(race_id)
	return jsonify(race)
