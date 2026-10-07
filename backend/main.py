from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.prediction.predict import predict_grievance

from backend.grievance_repository import (
    save_grievance,
    get_all_grievances,
    find_similar_grievances
)


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI College Grievance Analyzer",
    description="AI-powered student grievance classification API",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class GrievanceRequest(BaseModel):
    complaint: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI College Grievance Analyzer API is running!"
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(request: GrievanceRequest):

    # --------------------------------------------------------
    # STEP 1: Run AI prediction
    # --------------------------------------------------------

    result = predict_grievance(
        request.complaint
    )


    # --------------------------------------------------------
    # STEP 2: Continue only for valid grievances
    # --------------------------------------------------------

    if result["valid"]:

        # ----------------------------------------------------
        # STEP 3: Find similar grievances
        #
        # IMPORTANT:
        # We perform the search BEFORE inserting the new
        # grievance, so the new grievance cannot match itself.
        # ----------------------------------------------------

        similar_grievances = find_similar_grievances(
            new_embedding=result["embedding"],
            threshold=0.60,
            top_k=3
        )


        # ----------------------------------------------------
        # STEP 4: Save the new grievance
        # ----------------------------------------------------

        grievance_id = save_grievance(
            complaint=result["complaint"],
            category=result["category"],
            severity=result["severity"],
            department=result["department"],
            similarity=result["similarity"],
            embedding=result["embedding"]
        )


        # ----------------------------------------------------
        # STEP 5: Add database ID
        # ----------------------------------------------------

        result["grievance_id"] = grievance_id


        # ----------------------------------------------------
        # STEP 6: Add similar grievances
        # ----------------------------------------------------

        result["similar_grievances"] = similar_grievances


        # ----------------------------------------------------
        # STEP 7: Remove embedding from API response
        #
        # The embedding is internal data and should not be
        # sent to the React frontend.
        # ----------------------------------------------------

        result.pop(
            "embedding",
            None
        )


    # --------------------------------------------------------
    # STEP 8: Return result
    # --------------------------------------------------------

    return result


# ============================================================
# GET ALL GRIEVANCES
# ============================================================

@app.get("/grievances")
def get_grievances():

    grievances = get_all_grievances()

    return {
        "count": len(grievances),
        "grievances": grievances
    }