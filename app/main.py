from flask import Flask, jsonify, request
from predictions import Predictor
import ssl
from flask_cors import CORS

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('app/certs/fullchain.pem','app/certs/privkey.pem')

app=Flask(__name__)
CORS(app)


# flask API to predict tweets/text via trained DL/ML model


@app.route("/",methods=['GET','POST'])
def index():
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

        # saving texts and predictions
        with open('app/prediction_archive/texts_received.txt', "a", encoding="utf-8") as f:
            f.write(jsonify(prediction).get_data(as_text=True))
        return jsonify(prediction)
    else:
        return jsonify({'Error':"This is a GET API method, Bruh"})

if __name__ == '__main__':
    predictor = Predictor()
    app.run(debug=False, host='0.0.0.0', port="443", ssl_context=ctx)
