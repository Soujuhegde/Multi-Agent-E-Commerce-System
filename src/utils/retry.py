"""
Retry Utility
"""

import time

from functools import wraps


def retry(
    retries: int = 3,
    delay: int = 2
):

    def decorator(func):

        @wraps(func)
        def wrapper(
            *args,
            **kwargs
        ):

            last_exception = None

            for attempt in range(
                retries
            ):

                try:

                    return func(
                        *args,
                        **kwargs
                    )

                except Exception as exc:

                    last_exception = exc

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator