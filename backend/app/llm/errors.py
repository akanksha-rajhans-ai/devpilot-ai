class LLMProviderError(Exception):
    def __init__(
        self,
        message: str,
        provider: str,
        model: str,
    ):
        super().__init__(message)
        self.provider = provider
        self.model = model