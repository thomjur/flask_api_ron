from flask import Flask, jsonify, request
from predictions import Predictor
import ssl

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('app/certs/fullchain.pem','app/certs/privkey.pem')

app=Flask(__name__)

#we are importing our function from the colors.py file

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=='GET':
    #getting the url argument       
        text = request.args.get('text')
        prediction = predictor.predict(text)
        # saving texts and predictions
        with open('app/prediction_archive/texts_received.txt', "a", encoding="utf-8") as f:
            f.write(jsonify(prediction).get_data(as_text=True))
        return jsonify(prediction)
    else:
        return jsonify({'Error':"This is a GET API method, Bruh"})

if __name__ == '__main__':
    predictor = Predictor()
    app.run(debug=False, host='0.0.0.0', port="443", ssl_context=ctx)
