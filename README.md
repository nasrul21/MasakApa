# MasakApa

MasakApa is a local AI meal planner for busy families. It was built for my wife, who works and also cares for our children. After a long day, the app turns the ingredients already available at home into practical meal ideas.

## Why it exists

I made MasakApa for my wife. She works and also cares for our children,
so deciding what to cook after a long day can become another source of stress.
This project is a small, practical tool designed around her real situation:
limited time, limited energy, and the ingredients already available at home.

Choosing what to cook can be difficult when time, energy, and ingredients are limited. MasakApa helps by considering:

- Ingredients already available
- Cooking mood
- Family serving size
- Required missing ingredients and seasonings
- Optional ingredients

## Solution

MasakApa turns a short list of ingredients into practical meal ideas that fit
the user's situation. The user enters what is available at home, chooses a
cooking mood, and selects the number of family servings. The app then uses
local Gemma through Ollama to generate three recipe suggestions.

Each suggestion explains why it fits, separates available ingredients from
required and optional additions, and provides concise cooking steps. Missing
seasonings are called out and included in the relevant cooking instructions.
The selected recipe can be opened in a modal, copied, or downloaded for use
while cooking.

This reduces the mental effort of deciding what to cook without requiring a
large recipe search or sending household ingredient information to a hosted AI
service.

## Demo

[Watch the demo recording](MasakApa_Demo.mov)

## AI architecture

MasakApa uses Gemma 3 4B through a local Ollama server and the OpenAI-compatible Python client. The application can run recipe generation locally, keeping the household's ingredient information on the user's computer.

```text
Streamlit UI
    ↓
Application state and meal services
    ↓
OpenAI-compatible client
    ↓
Ollama → Gemma 3 4B
```

## Requirements

- Python 3.9+
- Ollama
- Gemma 3 4B

Install and prepare the model:

```bash
ollama serve
ollama pull gemma3:4b
```

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the example environment file:

```bash
cp .env.example .env
```

Run the application:

```bash
streamlit run app.py
```

## Configuration

The default local Ollama configuration is:

```env
AI_BASE_URL=http://localhost:11434/v1
AI_API_KEY=ollama
AI_MODEL=gemma3:4b
```

The API key is required by the OpenAI client but is ignored by a local Ollama server. Never commit a real secret in `.env`.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests -q
```

## Project structure

```text
app.py                 Streamlit entry point
config/                Settings, translations, and moods
models/                Typed meal model
providers/             AI prompts, client calls, and response parsing
ui/                    Streamlit components and styling
state.py               Session-state access
tests/                 Automated tests
```

## Hacktoberfest 2026

MasakApa was built for the Hacktoberfest 2026 Weekend Challenge theme, “Build for a Friend”. The project uses open-source AI at its core and explores why local inference can be useful for privacy, cost, and model control.

## License

MIT. See [LICENSE](LICENSE).
