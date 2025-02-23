from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .events import EventBus
from .models import Message


class BaseAgent(ABC):
    def __init__(self, name: str, event_bus: EventBus):
        self.name = name
        self.event_bus = event_bus
        self.event_bus.subscribe(self.handle_message)

    @abstractmethod
    async def handle_message(self, message: Message) -> None:
        """Handle incoming messages from the event bus."""
        pass

    async def send_message(self, content: Any, message_type: str, target: Optional[str] = None) -> None:
        """Send a message to the event bus."""
        message = Message(
            sender=self.name,
            target=target,
            content=content,
            message_type=message_type
        )
        await self.event_bus.publish(message)


class StoryWriterAgent(BaseAgent):
    async def handle_message(self, message: Message) -> None:
        if message.message_type == "generate_story":
            # Generate a German language learning story
            story = await self._generate_story(message.content)
            await self.send_message(story, "story_generated", message.sender)

    async def _generate_story(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation will use LLM to generate stories
        pass


class SceneDirectorAgent(BaseAgent):
    async def handle_message(self, message: Message) -> None:
        if message.message_type == "create_scene":
            # Create an interactive scene based on the story
            scene = await self._create_scene(message.content)
            await self.send_message(scene, "scene_created", message.sender)

    async def _create_scene(self, story: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation will create interactive scenes
        pass


class GrammarCheckerAgent(BaseAgent):
    async def handle_message(self, message: Message) -> None:
        if message.message_type == "check_grammar":
            # Check grammar of user input
            feedback = await self._check_grammar(message.content)
            await self.send_message(feedback, "grammar_feedback", message.sender)

    async def _check_grammar(self, text: str) -> Dict[str, Any]:
        # Implementation will check German grammar
        pass