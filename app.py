import os
import openai
import time
import random
from transformers import pipeline
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
from flask import Flask, jsonify,render_template,request
from app import create_app
from flask_cors import CORS
from chatbot import get_chatbot_response
load_dotenv()

os.environ["HUGGING_FACE_HUB_TOKEN"]=os.getenv("HUGGING_FACE_HUB_TOKEN")
alpha_vantage_api_key=os.getenv("ALPHA_VANTAGE_API_KEY")



app=create_app()

CORS(app)
if __name__ == "__main__":
    app.run()