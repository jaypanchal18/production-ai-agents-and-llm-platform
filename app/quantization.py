import tensorflow as tf
from fastapi import APIRouter, HTTPException
import numpy as np

router = APIRouter()

@router.post("/quantize_model")
async def quantize_model(model_path: str, quantization_type: str):
    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)
        
        # Check the quantization type
        if quantization_type not in ['dynamic', 'full']:
            raise HTTPException(status_code=400, detail="Invalid quantization type. Use 'dynamic' or 'full'.")

        # Apply quantization
        if quantization_type == 'dynamic':
            quantized_model = tf.quantization.quantize_dynamic(model, tf.int8)
        else:
            # Full quantization
            quantized_model = tf.quantization.quantize(model, tf.int8, tf.int8)

        # Save the quantized model
        quantized_model_path = model_path.replace('.h5', '_quantized.h5')
        tf.keras.models.save_model(quantized_model, quantized_model_path)

        return {"message": "Model quantized successfully", "quantized_model_path": quantized_model_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))