import enum
from enum import Enum
from typing import List, Dict
from pydantic import BaseModel


# Enums for LSAS anxiety levels
class AnxietyLevel(str, enum.Enum):
    NONE = "No social anxiety"
    MILD = "Mild social anxiety"
    MODERATE = "Moderate social anxiety"
    MARKED = "Marked social anxiety"
    SEVERE = "Severe social anxiety"
    VERY_SEVERE = "Very severe social anxiety"


def get_anxiety_level(score: int) -> AnxietyLevel:
    if score < 30:
        return AnxietyLevel.NONE
    elif score < 50:
        return AnxietyLevel.MILD
    elif score < 65:
        return AnxietyLevel.MODERATE
    elif score < 80:
        return AnxietyLevel.MARKED
    elif score < 95:
        return AnxietyLevel.SEVERE
    else:
        return AnxietyLevel.VERY_SEVERE


class FearLevel(str, Enum):
    NONE = "0 - None"
    MILD = "1 - Mild"
    MODERATE = "2 - Moderate"
    SEVERE = "3 - Severe"


class AvoidanceLevel(str, Enum):
    NEVER = "0 - Never"
    OCCASIONALLY = "1 - Occasionally"
    OFTEN = "2 - Often"
    USUALLY = "3 - Usually"


class Question(BaseModel):
    id: int
    situation: str
    fear_options: List[str]
    avoidance_options: List[str]


class LSASQuestions(BaseModel):
    questions: List[Question]
    fear_scale: Dict[str, str]
    avoidance_scale: Dict[str, str]
