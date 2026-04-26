from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import os
import psycopg2

app = FastAPI()

class ModelCustomizationRequest(BaseModel):
    model_name: str
    parameters: dict

class ModelComparisonRequest(BaseModel):
    model_names: list

def load_model(model_name):
    try:
        model = tf.keras.models.load_model(f'models/{model_name}')
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

def customize_model(model, parameters):
    # Apply customizations to the model based on parameters
    for key, value in parameters.items():
        if hasattr(model, key):
            setattr(model, key, value)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid parameter: {key}")
    return model

def compare_models(models):
    # Placeholder for model comparison logic
    results = {}
    for model_name in models:
        model = load_model(model_name)
        # Example: Evaluate model performance on a dataset
        results[model_name] = model.evaluate(np.random.rand(100, 10), np.random.rand(100, 1))
    return results

@app.post("/customize_model/")
async def customize_model_endpoint(request: ModelCustomizationRequest):
    model = load_model(request.model_name)
    customized_model = customize_model(model, request.parameters)
    return {"message": "Model customized successfully", "model_name": request.model_name}

@app.post("/compare_models/")
async def compare_models_endpoint(request: ModelComparisonRequest):
    if not request.model_names:
        raise HTTPException(status_code=400, detail="Model names list cannot be empty")
    results = compare_models(request.model_names)
    return {"comparison_results": results}