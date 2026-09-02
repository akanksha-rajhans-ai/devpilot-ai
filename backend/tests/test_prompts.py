import pytest

from app.prompts.registry import get_prompt_template


def test_get_chat_general_prompt_template():
    template = get_prompt_template("chat.general")

    assert template.name == "chat.general"
    assert template.version == "v1"
    assert template.prompt_id == "chat.general:v1"


def test_prompt_template_renders_message():
    template = get_prompt_template("chat.general")

    prompt = template.render(message="Explain rate limiting")

    assert "DevPilot AI" in prompt
    assert "Explain rate limiting" in prompt


def test_unknown_prompt_template_raises_error():
    with pytest.raises(ValueError, match="Unsupported prompt template"):
        get_prompt_template("unknown.prompt")