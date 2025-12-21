import logging
from api_service.api_service import ApiService
from base_model import WBBaseModel

def main():
    api_service = ApiService()
    response = api_service.get_snow_forecast()
    print(response.json())


if __name__ == "__main__":
    WBBaseModel.LOGGER.setLevel(logging.DEBUG)
    main()