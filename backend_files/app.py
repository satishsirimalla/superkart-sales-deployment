import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained model pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'superkart_model.joblib')
model = joblib.load(MODEL_PATH)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "SuperKart Sales Forecasting API is running!"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        # Ensure input data is converted to a DataFrame
        if isinstance(data, dict):
            input_df = pd.DataFrame([data])
        else:
            input_df = pd.DataFrame(data)
            
        # Standardize sugar content if needed
        if 'Product_Sugar_Content' in input_df.columns:
            input_df['Product_Sugar_Content'] = input_df['Product_Sugar_Content'].replace({'reg': 'Regular'})
            
        # Generate predictions
        predictions = model.predict(input_df)
        
        return jsonify({
            "status": "success",
            "predictions": [round(float(p), 2) for p in predictions]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
