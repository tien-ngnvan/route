import os
from dotenv import load_dotenv
from typing import Optional, Any, Union
from pydantic import SecretStr


def get_from_dict_or_env(
    data: dict[str, Any],
    key: Union[str, list[str]],
    env_key: str,
    default: Optional[str] = None,
) -> str:
    """Get a value from a dictionary or an environment variable.

    Args:
        data: The dictionary to look up the key in.
        key: The key to look up in the dictionary. This can be a list of keys to try
            in order.
        env_key: The environment variable to look up if the key is not
            in the dictionary.
        default: The default value to return if the key is not in the dictionary
            or the environment. Defaults to None.
    """
    if isinstance(key, (list, tuple)):
        for k in key:
            if k in data and data[k]:
                return data[k]

    if isinstance(key, str) and key in data and data[key]:
        return data[key]

    key_for_err = key[0] if isinstance(key, (list, tuple)) else key

    return get_from_env(key_for_err, env_key, default=default)



def get_from_env(key: str, env_key: str, default: Optional[str] = None) -> str:
    """Get a value from a dictionary or an environment variable.

    Args:
        key: The key to look up in the dictionary.
        env_key: The environment variable to look up if the key is not
            in the dictionary.
        default: The default value to return if the key is not in the dictionary
            or the environment. Defaults to None.

    Returns:
        str: The value of the key.

    Raises:
        ValueError: If the key is not in the dictionary and no default value is
            provided or if the environment variable is not set.
    """
    load_dotenv()
    
    if env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif env_key in os.getenv(env_key):
        return os.getenv[env_key]
    if default is not None:
        return default
    msg = (
        f"Did not find {key}, please add an environment variable"
        f" `{env_key}` which contains it, or pass"
        f" `{key}` as a named parameter."
    )
    raise ValueError(msg)

def convert_to_secret_str(value: Union[SecretStr, str]) -> SecretStr:
    """Convert a string to a SecretStr if needed.

    Args:
        value (Union[SecretStr, str]): The value to convert.

    Returns:
        SecretStr: The SecretStr value.
    """
    if isinstance(value, SecretStr):
        return value
    return SecretStr(value)