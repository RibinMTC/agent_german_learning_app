from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Message:
    sender: str
    content: Any
    message_type: str
    target: Optional[str] = None


@dataclass
class Story:
    title: str
    content: str
    difficulty_level: str
    vocabulary: list[dict[str, str]]
    grammar_points: list[str]


@dataclass
class Scene:
    story_id: str
    dialogue: list[dict[str, str]]
    expected_responses: list[str]
    hints: list[str]


@dataclass
class GrammarFeedback:
    original_text: str
    corrected_text: str
    explanations: list[str]
    suggestions: list[str]