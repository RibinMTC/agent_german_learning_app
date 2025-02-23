# German Learning Game

An interactive German language learning game powered by AI agents that create personalized learning experiences.

## Features

- Interactive story-based learning
- Real-time speech recognition
- Intelligent grammar checking
- Adaptive difficulty levels
- Multi-agent system for dynamic content generation

## Architecture

The system uses an event-driven architecture with multiple specialized agents:

- StoryWriterAgent: Generates German language learning stories
- SceneDirectorAgent: Creates interactive scenes
- GrammarCheckerAgent: Provides feedback on user input
- EventBus: Handles inter-agent communication

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Install dependencies:
   ```bash
   pip install .
   ```

## Configuration

The system can be configured using:
- `config/llm_config.yaml`: LLM provider settings
- `config/prompts.yaml`: Agent prompts and templates
- `.env`: Environment variables

## Usage

Start the web server:
```bash
python -m german_learning_game.web_app
```

Connect to the WebSocket endpoint:
```
ws://localhost:53685/ws/{session_id}
```

## Development

Install development dependencies:
```bash
pip install ".[dev]"
```

Run tests:
```bash
pytest
```

## License

MIT License