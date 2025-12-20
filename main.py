import logging
from api_service.api_service import ApiService
from api_service.utils.create_env_file import create_env_file
from base_model import WBBaseModel

def main():
    create_env_file(
        {"SYNOPTIC_API_KEY": "your_api_key_here"},
        file_path= __file__.parent / ".env")


if __name__ == "__main__":
    WBBaseModel.LOGGER.setLevel(logging.INFO)
    main()