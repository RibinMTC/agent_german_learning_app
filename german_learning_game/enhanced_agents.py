from typing import Any, Dict, List, Optional
from smol_dev.agents import Agent, AgentState
from litellm import completion

from .events import EventBus
from .models import Message, Story, Scene, GrammarFeedback


class SmolAgent(Agent):
    def __init__(
        self,
        name: str,
        event_bus: EventBus,
        system_prompt: str,
        model: str = "gpt-4-turbo",
        temperature: float = 0.7
    ):
        super().__init__(name=name)
        self.event_bus = event_bus
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature
        self.state = AgentState()
        self.event_bus.subscribe(self.handle_message)

    async def _get_completion(self, prompt: str) -> str:
        """Get completion from LiteLLM."""
        response = await completion(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content

    async def handle_message(self, message: Message) -> None:
        """Handle incoming messages from the event bus."""
        if hasattr(self, f"_handle_{message.message_type}"):
            handler = getattr(self, f"_handle_{message.message_type}")
            await handler(message)

    async def send_message(self, content: Any, message_type: str, target: Optional[str] = None) -> None:
        """Send a message through the event bus."""
        message = Message(
            sender=self.name,
            target=target,
            content=content,
            message_type=message_type
        )
        await self.event_bus.publish(message)


class EnhancedStoryWriter(SmolAgent):
    def __init__(self, name: str, event_bus: EventBus):
        system_prompt = """You are a creative German language learning story writer.
        Create engaging stories that help learners practice German while being entertained.
        Include everyday situations, natural dialogue, and appropriate grammar structures."""
        super().__init__(name=name, event_bus=event_bus, system_prompt=system_prompt)

    async def _handle_generate_story(self, message: Message):
        difficulty = message.content["difficulty"]
        prompt = f"""Generate a German learning story for {difficulty} level learners.
        Include:
        1. A title in both German and English
        2. A story in German with natural dialogue
        3. Key vocabulary with translations
        4. Grammar points used in the story
        
        Format the response as a structured story object."""

        story_content = await self._get_completion(prompt)
        # Parse the completion into a Story object
        # This is a simplified version - you'd want more robust parsing
        story = Story(
            title="Sample Story",  # Replace with parsed title
            content=story_content,
            difficulty_level=difficulty,
            vocabulary=[],  # Parse vocabulary from response
            grammar_points=[]  # Parse grammar points from response
        )
        await self.send_message(story, "story_generated", message.sender)


class EnhancedSceneDirector(SmolAgent):
    def __init__(self, name: str, event_bus: EventBus):
        system_prompt = """You are a scene director for an interactive German learning game.
        Create engaging scenes with natural dialogue and appropriate learning challenges."""
        super().__init__(name=name, event_bus=event_bus, system_prompt=system_prompt)

    async def _handle_create_scene(self, message: Message):
        story = message.content
        prompt = f"""Create an interactive scene based on this story:
        {story.content}
        
        Include:
        1. Natural dialogue exchanges
        2. Expected user responses
        3. Helpful hints
        4. Progressive difficulty
        
        Format the response as a structured scene object."""

        scene_content = await self._get_completion(prompt)
        # Parse the completion into a Scene object
        scene = Scene(
            story_id=story.title,  # Use a proper ID in production
            dialogue=[],  # Parse dialogue from response
            expected_responses=[],  # Parse expected responses
            hints=[]  # Parse hints from response
        )
        await self.send_message(scene, "scene_created", message.sender)


class EnhancedGrammarChecker(SmolAgent):
    def __init__(self, name: str, event_bus: EventBus):
        system_prompt = """You are a German language grammar checker.
        Analyze text for grammatical correctness and provide helpful feedback."""
        super().__init__(name=name, event_bus=event_bus, system_prompt=system_prompt)

    async def _handle_check_grammar(self, message: Message):
        text = message.content
        prompt = f"""Analyze this German text for grammatical correctness:
        {text}
        
        Provide:
        1. Corrections if needed
        2. Explanations of errors
        3. Suggestions for improvement
        4. Alternative phrasings
        
        Format the response as a structured feedback object."""

        feedback_content = await self._get_completion(prompt)
        # Parse the completion into a GrammarFeedback object
        feedback = GrammarFeedback(
            original_text=text,
            corrected_text="",  # Parse from response
            explanations=[],  # Parse from response
            suggestions=[]  # Parse from response
        )
        await self.send_message(feedback, "grammar_feedback", message.sender)