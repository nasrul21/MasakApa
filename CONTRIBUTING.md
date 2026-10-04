# Contributing to MasakApa

Thanks for helping improve MasakApa.

## Development setup

1. Install Python 3.9 or newer.
2. Install and run Ollama.
3. Pull `gemma3:4b` with `ollama pull gemma3:4b`.
4. Create a virtual environment.
5. Install dependencies from `requirements-dev.txt`.
6. Copy `.env.example` to `.env`.

## Run the app

```bash
streamlit run app.py
```

## Run tests

```bash
python -m unittest discover -s tests -q
```

## Contribution guidelines

- Keep user-facing text available in English and Indonesian where applicable.
- Keep AI response parsing defensive; local models may return imperfect JSON.
- Add or update tests when changing provider behavior or data models.
- Keep result cards concise and preserve the portrait-tablet layout.
- Do not commit `.env`, API keys, or other private data.
