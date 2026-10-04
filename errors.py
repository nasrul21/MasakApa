"""Application-specific exceptions."""


class MasakApaError(Exception):
    """Base class for expected application errors."""


class AIConfigurationError(MasakApaError):
    """Raised when AI configuration is missing or invalid."""


class AIRequestError(MasakApaError):
    """Raised when the AI provider request fails."""


class AIResponseError(MasakApaError):
    """Raised when the AI response cannot become valid meal data."""
