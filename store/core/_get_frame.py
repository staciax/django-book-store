# This file is a part of loguru library
# https://github.com/Delgan/loguru/blob/master/loguru/_get_frame.py

import sys
from collections.abc import Callable
from sys import exc_info
from types import FrameType


def get_frame_fallback(n: int) -> FrameType | None:
    try:
        raise Exception  # noqa: TRY002, TRY301
    except Exception:
        frame = exc_info()[2].tb_frame.f_back  # type: ignore[union-attr]
        for _ in range(n):
            frame = frame.f_back  # type: ignore[union-attr]
        return frame


def load_get_frame_function() -> Callable[[int], FrameType | None]:
    if hasattr(sys, '_getframe'):
        get_frame = sys._getframe
    else:
        get_frame = get_frame_fallback  # type: ignore[assignment]
    return get_frame


get_frame = load_get_frame_function()
