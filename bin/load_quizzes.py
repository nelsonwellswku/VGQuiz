import json
import requests
import logging
from pathlib import Path

# configuration
output_directory = Path("./content_generation/output").resolve()
post_endpoint = "http://localhost:8000/api/quiz"

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s: %(asctime)s %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


def post_json_files(directory: Path, endpoint: str):
    if not directory.exists() or not directory.is_dir():
        logger.error(f"Directory does not exist: {directory}")
        return

    for json_file in directory.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
                response = requests.post(endpoint, json=data)
                if response.status_code == 200:
                    logger.info(f"Posted {json_file.name}")
                elif response.status_code == 409:
                    logger.info(f"Posted {json_file.name} but quiz already exists.")
                else:
                    logger.error(
                        f"Failed to post {json_file.name}. Status Code: {response.status_code}"
                    )

        except Exception as e:
            logger.exception(f"Error with file {json_file.name}: {e}")


if __name__ == "__main__":
    platforms = [f for f in output_directory.iterdir() if f.is_dir()]
    for platform in platforms:
        platform_directory = output_directory.joinpath(platform)
        post_json_files(platform_directory.resolve(), post_endpoint)
