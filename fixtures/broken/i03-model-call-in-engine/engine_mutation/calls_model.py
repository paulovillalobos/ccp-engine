"""A module that would call a model from inside the engine. verify must refuse it."""
import openai  # noqa: F401


def read(text):
    return openai.chat(text)
