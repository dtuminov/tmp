from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import bentoml

class RepoData(BaseModel):
    repo_id: str
    snapshot_date: datetime
    
    # 30-day metrics
    stars_30d: int
    forks_30d: int
    commits_30d: int
    contributors_30d: int
    
    # 90-day metrics
    stars_90d: int
    forks_90d: int
    commits_90d: int
    contributors_90d: int
    
    # 365-day metrics
    stars_365d: int
    forks_365d: int
    commits_365d: int
    contributors_365d: int
    
    # Repository metadata
    repo_age: int
    primary_language: Optional[str] = None
    license: Optional[str] = None
    has_ci: bool
    has_wiki: bool
    
    # Labels (for training/prediction)
    viral_label: Optional[bool] = None
    abandoned_label: Optional[bool] = None

# Load the model
model = bentoml.picklable_model.get("virality_lama:latest")

@bentoml.service
class ViralityPredictionService:
    
    @bentoml.api
    def predict(self, repo_data: RepoData) -> dict:
        # Convert to format expected by model
        features = [
            repo_data.stars_30d,
            repo_data.forks_30d,
            repo_data.commits_30d,
            repo_data.contributors_30d,
            repo_data.stars_90d,
            repo_data.forks_90d,
            repo_data.commits_90d,
            repo_data.contributors_90d,
            repo_data.stars_365d,
            repo_data.forks_365d,
            repo_data.commits_365d,
            repo_data.contributors_365d,
            repo_data.repo_age,
            1 if repo_data.has_ci else 0,
            1 if repo_data.has_wiki else 0
        ]
        
        prediction = model.predict_proba([features])[0]
        
        return {
            "viral_probability": float(prediction[1]) if len(prediction) > 1 else float(prediction[0]),
            "abandoned_probability": 0.0  # Placeholder - adjust based on your model
        }