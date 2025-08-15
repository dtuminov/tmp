# save_model.py
import pickle, bentoml

with open("models/virality_model.pkl", "rb") as f:
    virality_model = pickle.load(f)

# store as a “picklable_model” — Bento just keeps the bytes & metadata
bentoml.picklable_model.save_model(
    name        = "virality_model",
    model       = virality_model,
    signatures  = {
        "predict_proba": {"batchable": True},
        # LightAutoML ensembles expose .predict_proba
    },
)
