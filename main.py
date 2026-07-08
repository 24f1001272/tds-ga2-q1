import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Initialize the API
app = FastAPI()

# ---------------------------------------------------------
# 1. THE BOUNCER (CORS Policy)
# This strictly enforces who is allowed to ask for data.
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-d86h7t.example.com"], # The VIP list (No wildcards!)
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, OPTIONS, etc.
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. THE TIMEKEEPER (Middleware)
# This intercepts every request to add custom headers.
# ---------------------------------------------------------
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    # Start the stopwatch
    start_time = time.time()
    
    # Let the API process the request
    response = await call_next(request)
    
    # Stop the stopwatch and calculate the duration
    process_time = time.time() - start_time
    
    # Stamp the custom headers onto the outgoing response
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# ---------------------------------------------------------
# 3. THE CALCULATOR (The /stats Endpoint)
# This does the actual math on the numbers provided.
# ---------------------------------------------------------
@app.get("/stats")
def get_stats(values: str):
    # The 'values' come in as a single string like "1,2,3"
    # We split them by the comma and convert each one to an integer
    number_list = [int(num) for num in values.split(",")]
    
    # Calculate all the required statistics
    count_val = len(number_list)
    sum_val = sum(number_list)
    min_val = min(number_list)
    max_val = max(number_list)
    mean_val = sum_val / count_val
    
    # Return the final JSON exactly as the grader expects
    return {
        "email": "24f1001272@ds.study.iitm.ac.in", # REPLACE THIS!
        "count": count_val,
        "sum": sum_val,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }
