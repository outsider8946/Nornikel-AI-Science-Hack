from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum

class EntityType(str, Enum):
    MATERIAL = "Material"
    PROCESS = "Process"
    EQUIPMENT = "Equipment"
    EXPERIMENT = "Experiment"
    EXPERT = "Expert"
    FACILITY = "Facility"
    METHOD = "Method"

class ExtractedEntity(BaseModel):
    """Извлечённая сущность"""
    type: EntityType = Field(description="Тип сущности")
    name: str = Field(description="Каноническое имя")
    synonyms: list[str] = Field(default_factory=list, description="Синонимы")
    attributes: dict = Field(default_factory=dict, description="Дополнительные свойства")

class ExtractedFact(BaseModel):
    """Числовой факт"""
    parameter: str = Field(description="Что измеряется")
    value: float = Field(description="Числовое значение")
    unit: str = Field(description="Единица измерения")
    condition: Optional[str] = Field(default=None, description="Условие")
    confidence: float = Field(default=0.7, ge=0.0, le=1.0, description="Уверенность")

class ExtractedRelation(BaseModel):
    """Связь между сущностями"""
    source: str = Field(description="Имя источника")
    source_type: EntityType = Field(description="Тип источника")
    target: str = Field(description="Имя цели")
    target_type: EntityType = Field(description="Тип цели")
    relation_type: str = Field(description="Тип связи")
    properties: dict = Field(default_factory=dict, description="Свойства связи")

class ExtractedClaim(BaseModel):
    """Утверждение"""
    statement: str = Field(description="Текст утверждения")
    evidence_level: Literal["strong", "moderate", "weak", "contradicted"] = Field(description="Уровень доказательности")
    supporting_entities: list[str] = Field(default_factory=list, description="Подтверждающие сущности")

class ExtractionResult(BaseModel):
    """Полный результат извлечения"""
    entities: list[ExtractedEntity] = Field(default_factory=list)
    facts: list[ExtractedFact] = Field(default_factory=list)
    relations: list[ExtractedRelation] = Field(default_factory=list)
    claims: list[ExtractedClaim] = Field(default_factory=list)