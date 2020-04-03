from application import app, db

from application.sheet.models import CharacterSheet

@app.route("/sheet/<char_id>/", methods=["GET"])
def character_view(char_id):
	return render_template("sheet.html", sheet = CharacterSheet(char_id))
