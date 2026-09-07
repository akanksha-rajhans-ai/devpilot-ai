from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    version: str
    template: str

    @property
    def prompt_id(self) -> str:
        return f"{self.name}:{self.version}"

    def render(self, **values: str) -> str:
        return self.template.format(**values)


CHAT_GENERAL_V1 = PromptTemplate(
    name="chat.general",
    version="v1",
    template=(
        "You are DevPilot AI, an enterprise AI developer productivity assistant.\n"
        "Answer clearly and practically.\n\n"
        "User message:\n{message}"
    ),
)

AGENT_ANSWER_V1 = PromptTemplate(
    name="agent.answer",
    version="v1",
    template=(
        "You are DevPilot AI, an enterprise AI developer productivity assistant.\n"
        "Use the plan to answer the user clearly.\n\n"
        "Plan:\n{plan}\n\n"
        "User message:\n{message}"
    ),
)

def get_prompt_template(name: str, version: str = "v1") -> PromptTemplate:
    if name == "chat.general" and version == "v1":
        return CHAT_GENERAL_V1

    if name == "agent.answer" and version == "v1":
        return AGENT_ANSWER_V1

    raise ValueError(f"Unsupported prompt template: {name}:{version}")