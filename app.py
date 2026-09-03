from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home.html', methods=['POST','GET'])
def predict():
    if request.method =='GET':
        return render_template('home.html')
    else:
        data = CustomData(
            carat=float(request.form.get('carat')),
            cut=request.form.get('cut'),
            color=request.form.get('color'),
            clarity=request.form.get('clarity'),
            depth=float(request.form.get('depth')),
            table=float(request.form.get('table')),
            x=float(request.form.get('length')),
            y=float(request.form.get('width')),
            z=float(request.form.get('depth'))
        )
        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(pred_df)
        return render_template('home.html', prediction=pred[0])

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)