from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String)
    file_path = Column(String)
    dataset_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LatentVector(Base):
    __tablename__ = "latent_vectors"
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    vector_data = Column(Text)
    labels = Column(Text)
    sigma = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelResult(Base):
    __tablename__ = "model_results"
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    model_type = Column(String)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    sigma = Column(Float)
    result_data = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PrivacyAttackResult(Base):
    __tablename__ = "privacy_attack_results"
    id = Column(Integer, primary_key=True, index=True)
    model_result_id = Column(Integer, ForeignKey("model_results.id"))
    attack_type = Column(String)
    success_rate = Column(Float)
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
