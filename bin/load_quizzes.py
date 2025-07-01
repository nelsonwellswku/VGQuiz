import json
import requests
from pathlib import Path

# Configuration
DIRECTORY = Path("./content_generation/output")
POST_ENDPOINT = "http://localhost:8000/api/quiz"


def post_json_files(directory: Path, endpoint: str):
    if not directory.exists() or not directory.is_dir():
        print(f"[ERROR] Directory does not exist: {directory}")
        return

    for json_file in directory.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
                response = requests.post(endpoint, json=data)
                if response.status_code == 200:
                    print(f"[SUCCESS] Posted {json_file.name}")
                else:
                    print(
                        f"[ERROR] Failed to post {json_file.name}. Status Code: {response.status_code}"
                    )
        except Exception as e:
            print(f"[EXCEPTION] Error with file {json_file.name}: {e}")


if __name__ == "__main__":
    post_json_files(DIRECTORY.resolve(), POST_ENDPOINT)
