from .db import engine, SessionLocal
from .models import Base, GameplayFeature, AccessibilityFeature

def seed():
    # Recrée la base de données proprement à chaque exécution
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1️⃣ Création des features de gameplay
    voices = GameplayFeature(name="Il y a des voix qui prononcent des dialogues")
    hold_button = GameplayFeature(name="Il faut maintenir une touche appuyée")

    db.add_all([voices, hold_button])
    db.commit()

    # 2️⃣ Création des features d'accessibilité
    subtitles = AccessibilityFeature(name="Proposer des sous-titres pour les dialogues")
    toggle_option = AccessibilityFeature(name="Proposer une option pour basculer entre maintien / toggle")

    db.add_all([subtitles, toggle_option])
    db.commit()

    # 3️⃣ Association entre les deux
    voices.accessibility_features.append(subtitles)
    hold_button.accessibility_features.append(toggle_option)
    db.commit()

    db.close()
    print("✅ Base de données initialisée avec succès !")

# Permet d'exécuter ce fichier directement depuis le terminal
if __name__ == "__main__":
    seed()
