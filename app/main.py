from flask import Flask, jsonify, request
from predictions import Predictor
import ssl
from flask_cors import CORS
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import datetime

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('app/certs/fullchain.pem','app/certs/privkey.pem')

app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prediction_archive/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#### MODELS (no extra file curr due to circular imports with db)

class Text(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.TEXT)
	ron_prediction = db.Column(db.INTEGER)
	ron_prediction_user = db.Column(db.INTEGER)
	rels_christianity = db.Column(db.INTEGER)
	rels_islam = db.Column(db.INTEGER)
	rels_judaism = db.Column(db.INTEGER)
	rels_hindu = db.Column(db.INTEGER)
	rels_buddhism = db.Column(db.INTEGER)
	rels_atheism = db.Column(db.INTEGER)
	rels_unspecific = db.Column(db.INTEGER)
	rels_others = db.Column(db.INTEGER)
	rels_none = db.Column(db.INTEGER)
	sf_religion = db.Column(db.INTEGER)
	sf_politics = db.Column(db.INTEGER)
	sf_economy = db.Column(db.INTEGER)
	sf_education = db.Column(db.INTEGER)
	sf_art = db.Column(db.INTEGER)
	sf_media = db.Column(db.INTEGER)
	sf_ethics = db.Column(db.INTEGER)
	sf_science = db.Column(db.INTEGER)	
	sentiment = db.Column(db.TEXT)
	date = db.Column(db.TEXT)

	def __repr__(self):
		return '<User %r>' % self.text[:25]



# flask API to predict tweets/text via trained DL/ML model

@app.route("/",methods=['GET','POST'])
def index():
<<<<<<< HEAD
    '''
    basic GET API to store annotation + tweet text passed via URL
    '''
    if request.method=='GET':
        # TEXT
        text = request.args.get('text')
        # RON user selection + DL prediction
        ron_selection = request.args.get('ronSelection')
        prediction = predictor.predict(text)
        prediction['user_prediction'] = ron_selection
        # RELIGIONS
        religions = request.args.get('religions')
        if religions:
            religions = religions.split('-')
            religions = [religion for religion in religions if religion != ""]
        prediction['religions'] = religions
        # SOCIAL FIELDS
        social_fields = request.args.get('social_fields')
        if social_fields:
            social_fields = social_fields.split('-')
            social_fields = [field for field in social_fields if field != ""]
        prediction['social_fields'] = social_fields
        # SENTIMENT
        prediction['sentiment'] = request.args.get('sentiment')
=======
	'''
	basic GET API to store annotation + tweet text passed via URL
	'''
	if request.method=='GET':
		# TEXT
		text = request.args.get('text')
		# RON user selection + DL prediction
		ron_selection = request.args.get('ronSelection')
		prediction = predictor.predict(text)
		prediction['user_prediction'] = ron_selection
		# RELIGIONS
		religions = request.args.get('religions')
		if religions:
			religions = religions.split('-')
			religions = [religion for religion in religions if religion != ""]
			prediction['religions'] = religions
		else:
			prediction['religions'] = []
		# SOCIAL FIELDS
		social_fields = request.args.get('social_fields')
		if social_fields:
			social_fields = social_fields.split('-')
			social_fields = [field for field in social_fields if field != ""]
			prediction['social_fields'] = social_fields
		else:
			prediction['social_fields'] = []
		# SENTIMENT
		prediction['sentiment'] = request.args.get('sentiment')
		print(prediction)
		# saving texts and predictions in SQLite DB (needs to be set up first)
		text = Text(
				text = prediction['text'],
				ron_prediction = prediction['ron_prediction'],
				ron_prediction_user = prediction['user_prediction'],
				rels_christianity = 1 if "christianity" in prediction['religions'] else 0,
				rels_islam = 1 if "islam" in prediction['religions'] else 0,
				rels_judaism = 1 if "judaism" in prediction['religions'] else 0,
				rels_hindu = 1 if "hindu" in prediction['religions'] else 0,
				rels_buddhism = 1 if "buddhism" in prediction['religions'] else 0,
				rels_atheism = 1 if "atheism" in prediction['religions'] else 0,
				rels_unspecific = 1 if "unspecific" in prediction['religions'] else 0,
				rels_others = 1 if "others" in prediction['religions'] else 0,
				rels_none = 1 if "none" in prediction['religions'] else 0,
				sf_religion = 1 if "religion" in prediction['social_fields'] else 0,
				sf_politics = 1 if "politics" in prediction['social_fields'] else 0,
				sf_economy = 1 if "economy" in prediction['social_fields'] else 0,
				sf_education = 1 if "education" in prediction['social_fields'] else 0,
				sf_art = 1 if "art" in prediction['social_fields'] else 0,
				sf_media = 1 if "media" in prediction['social_fields'] else 0,
				sf_ethics = 1 if "ethics" in prediction['social_fields'] else 0,
				sf_science = 1 if "science" in prediction['social_fields'] else 0,
				sentiment = prediction['sentiment'],
				date = datetime.date.today().strftime("%B %d, %Y")
		)
		db.session.add(text)
		db.session.commit()

		return jsonify(prediction)
	else:
		return jsonify({'Error':"This is a GET API method, Bruh"})

if __name__ == '__main__':
	predictor = Predictor()
	app.run(debug=False, host='0.0.0.0', port="443", ssl_context=ctx)


