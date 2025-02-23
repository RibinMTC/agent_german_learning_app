from typing import Callable, List, Optional
from .models import Message


class EventBus:
    def __init__(self):
        self._subscribers: List[Callable[[Message], None]] = []

    def subscribe(self, callback: Callable[[Message], None]) -> None:
        """Subscribe to events on the bus."""
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Message], None]) -> None:
        """Unsubscribe from events on the bus."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    async def publish(self, message: Message) -> None:
        """Publish a message to all subscribers."""
        for subscriber in self._subscribers:
            if not message.target or subscriber.__self__.name == message.target:
                await subscriber(message)