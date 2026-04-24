from fastapi import FastAPI, Request
from prometheus_client import start_http_server, Summary, Counter, Histogram
import logging
import time

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')
SUMMARY = Summary('request_processing_seconds', 'Time spent processing request')

# Start Prometheus metrics server
start_http_server(8000)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    # Log request details
    logger.info(f"Request: {request.method} {request.url} completed in {duration:.4f} seconds")
    
    # Update Prometheus metrics
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(duration)

    return response

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return {"metrics": "Prometheus metrics are available at /metrics endpoint."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)