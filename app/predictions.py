from fastai.text.all import *
import re

class Predictor():
	def __init__(self):
		self.ron_predictor = load_learner('app/classifier/ron_classifier.pkl')

	def clean_tweet(self, tweet):
		'''
		helpfer function to clean tweets
		'''
		pattern = re.compile(r'@\w+|http[s]*\://[\w\./]+|[\.,:;\n\t\"\'-\?“”#&]+')
		clean_tweet = re.sub(pattern, ' ', tweet)
		clean_tweet = re.sub(r'\s{2,}', ' ', clean_tweet)
		clean_tweet = clean_tweet.strip().lower()
		return clean_tweet

	def predict(self, text):
		'''
		main function to predict a text
		'''
		clean_text = self.clean_tweet(text)
		ron_prediction = self.ron_predictor.predict(clean_text)[0]
		return {'text': text, 'ron_prediction': ron_prediction }

