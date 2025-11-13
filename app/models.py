from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Table d'association many-to-many entre gameplay et accessibilité
gameplay_accessibility = Table(
    "gameplay_accessibility",
    Base.metadata,
    Column("gameplay_id", Integer, ForeignKey("gameplay_features.id")),
    Column("accessibility_id", Integer, ForeignKey("accessibility_features.id")),
)

class GameplayFeature(Base):
    __tablename__ = "gameplay_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    accessibility_features = relationship(
        "AccessibilityFeature",
        secondary=gameplay_accessibility,
        back_populates="gameplay_features",
    )

class AccessibilityFeature(Base):
    __tablename__ = "accessibility_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    gameplay_features = relationship(
        "GameplayFeature",
        secondary=gameplay_accessibility,
        back_populates="accessibility_features",
    )
