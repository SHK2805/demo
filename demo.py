from atlassian import Confluence
import os
import zipfile
import logging
import re
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def load_config():
    return {
        "CONFLUENCE_SERVER": os.getenv("CONFLUENCE_SERVER"),
        "CONFLUENCE_SPACE": os.getenv("CONFLUENCE_SPACE"),
        "CONFLUENCE_TOKEN": os.getenv("CONFLUENCE_TOKEN"),
        "PARENT_DOC": os.getenv("PARENT_DOC"),
        "ZIP_FILE": os.getenv("ZIP_FILE")
    }

def validate_config(config):
    required_keys = config.keys()
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise ValueError(f"Missing config keys in .env: {', '.join(missing)}")

def setup_logger(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{timestamp}_automation.log"
    log_path = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("Logger initialized.")
    return log_path

def extract_zip(zip_path, extract_to="unzipped_md"):
    if not os.path.isfile(zip_path):
        logging.error(f"ZIP file not found: {zip_path}")
        print(f"[ERROR] ZIP file not found: {zip_path}")
        return None
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to

def get_title_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r"# Use Case Title:\s*

\[(.*?)\]

", line)
            if match:
                return match.group(1)
    return Path(file_path).stem  # fallback to filename

def page_exists(confluence, space_key, title):
    page_id = confluence.get_page_id(space=space_key, title=title)
    return page_id is not None

def publish_to_confluence(confluence, config, title, content):
    try:
        confluence.create_page(
            space=config["CONFLUENCE_SPACE"],
            title=title,
            body=f"<ac:structured-macro ac:name='markdown'><ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body></ac:structured-macro>",
            parent_id=config["PARENT_DOC"],
            representation="storage"
        )
        return True
    except Exception as e:
        logging.error(f"Confluence API error for '{title}': {e}")
        return False

def main():
    config = load_config()
    try:
        validate_config(config)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    setup_logger()
    confluence = Confluence(
        url=config["CONFLUENCE_SERVER"],
        token=config["CONFLUENCE_TOKEN"]
    )

    extracted_folder = extract_zip(config["ZIP_FILE"])
    if not extracted_folder or not os.path.exists(extracted_folder):
        return

    for root, _, files in os.walk(extracted_folder):
        if "__MACOSX" in root:
            continue

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    title = get_title_from_md(file_path)
                    title = os.path.splitext(title)[0]  # Remove .md if present

                    if page_exists(confluence, config["CONFLUENCE_SPACE"], title):
                        logging.info(f"Skipped (already exists): {title}")
                        continue

                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    success = publish_to_confluence(confluence, config, title, content)
                    if success:
                        logging.info(f"Published: {title}")
                    else:
                        logging.error(f"Failed to publish: {title}")
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
