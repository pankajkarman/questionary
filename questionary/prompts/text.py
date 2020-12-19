from typing import Any, Optional, List, Tuple

from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.lexers import Lexer, SimpleLexer

from questionary.constants import (
    DEFAULT_QUESTION_PREFIX,
    DEFAULT_STYLE,
    INSTRUCTION_MULTILINE,
)
from questionary.prompts.common import build_validator
from questionary.question import Question


def text(
    message: str,
    default: str = "",
    validate: Any = None,
    qmark: str = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    multiline: bool = False,
    instruction: Optional[str] = None,
    lexer: Optional[Lexer] = None,
    **kwargs: Any,
) -> Question:
    """Prompt the user to enter a free text message.

    This question type can be used to prompt the user for some text input.

    Args:
        message: Question text.

        default: Default value will be returned if the user just hits
                 enter.

        validate: Require the entered value to pass a validation. The
                  value can not be submitted until the validator accepts
                  it (e.g. to check minimum password length).

                  This can either be a function accepting the input and
                  returning a boolean, or an class reference to a
                  subclass of the prompt toolkit Validator class.

        qmark: Question prefix displayed in front of the question.
               By default this is a :code:`?`.

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

        multiline: If :code:`True`, multiline input will be enabled.

        instruction: Write instructions for the user if needed. If :code:`None`
                     and :code:`multiline=True`, some instructions will appear.

        lexer: Supply a valid lexer to style the answer. Leave empty to
               use a simple one by default.

    Returns:
        :class:`Question`: Question instance, ready to be prompted (using :code:`.ask()`).
    """

    merged_style = merge_styles([DEFAULT_STYLE, style])
    lexer = lexer or SimpleLexer("class:answer")
    validator = build_validator(validate)

    if instruction is None and multiline:
        instruction = INSTRUCTION_MULTILINE

    def get_prompt_tokens() -> List[Tuple[str, str]]:
        result = [("class:qmark", qmark), ("class:question", " {} ".format(message))]
        if instruction:
            result.append(("class:instruction", " {} ".format(instruction)))
        return result

    p = PromptSession(
        get_prompt_tokens,
        style=merged_style,
        validator=validator,
        lexer=lexer,
        multiline=multiline,
        **kwargs,
    )
    p.default_buffer.reset(Document(default))

    return Question(p.app)
