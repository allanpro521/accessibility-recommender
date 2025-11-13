from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import SessionLocal
from .models import GameplayFeature

app = FastAPI(title="Accessibility Recommender")

# Autoriser le front à communiquer avec le backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre plus tard si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API d'accessibilité 🎮"}

@app.get("/gameplay-features")
def get_gameplay_features():
    """Renvoie la liste de toutes les features de gameplay disponibles."""
    db = SessionLocal()
    features = db.query(GameplayFeature).all()
    db.close()
    return [{"id": f.id, "name": f.name} for f in features]

@app.post("/recommendations")
def get_recommendations(selected_ids: list[int]):
    """Renvoie les features d'accessibilité associées aux gameplay sélectionnés."""
    db = SessionLocal()
    if not selected_ids:
        raise HTTPException(status_code=400, detail="Aucune feature de gameplay sélectionnée.")
    
    features = db.query(GameplayFeature).filter(GameplayFeature.id.in_(selected_ids)).all()

    # Construire la liste unique des accessibilités associées
    recommendations = set()
    for f in features:
        for acc in f.accessibility_features:
            recommendations.add(acc.name)
    
    db.close()
    return {"recommendations": sorted(list(recommendations))}
