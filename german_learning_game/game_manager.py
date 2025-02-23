from typing import Dict, Optional

from .enhanced_agents import EnhancedStoryWriter, EnhancedSceneDirector, EnhancedGrammarChecker
from .events import EventBus
from .models import Message, Story, Scene, GrammarFeedback


class GameManager:
    def __init__(self):
        self.event_bus = EventBus()
        self.story_writer = EnhancedStoryWriter("story_writer", self.event_bus)
        self.scene_director = EnhancedSceneDirector("scene_director", self.event_bus)
        self.grammar_checker = EnhancedGrammarChecker("grammar_checker", self.event_bus)
        
        self.current_story: Optional[Story] = None
        self.current_scene: Optional[Scene] = None
        self.user_progress: Dict[str, Any] = {}

    async def start_new_game(self, difficulty: str) -> None:
        """Start a new game session with the specified difficulty."""
        await self.event_bus.publish(
            Message(
                sender="game_manager",
                target="story_writer",
                content={"difficulty": difficulty},
                message_type="generate_story"
            )
        )

    async def handle_user_input(self, text: str) -> None:
        """Process user input and provide feedback."""
        await self.event_bus.publish(
            Message(
                sender="game_manager",
                target="grammar_checker",
                content=text,
                message_type="check_grammar"
            )
        )

    async def advance_scene(self) -> None:
        """Progress to the next scene in the current story."""
        if self.current_story:
            await self.event_bus.publish(
                Message(
                    sender="game_manager",
                    target="scene_director",
                    content=self.current_story,
                    message_type="create_scene"
                )
            )

    def update_progress(self, user_response: str, feedback: GrammarFeedback) -> None:
        """Update the user's progress based on their responses and feedback."""
        if not self.current_scene:
            return

        self.user_progress.setdefault("responses", []).append({
            "scene_id": self.current_scene.story_id,
            "user_response": user_response,
            "feedback": feedback
        })