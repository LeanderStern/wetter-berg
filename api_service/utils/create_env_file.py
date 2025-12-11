from pathlib import Path

from pydantic import validate_call

@validate_call
def create_env_file(env_vars: dict[str, str], file_path: Path) -> None:
    with open(file_path, 'w') as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")