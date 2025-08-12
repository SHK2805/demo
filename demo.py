import os
import zipfile
import logging
import re
from pathlib import Path
from atlassian import Confluence

# Configuration
config = {
    "CONFLUENCE_SERVER": "https://myconfluence",
    "CONFLUENCE_SPACE": "my_confluence_space",
    "CONFLUENCE_TOKEN": "my_dummy_token",
    "PARENT_DOC": "123456789",
    "ZIP_FILE": "path_to_zip/file.zip"
}

# Setup logging
logging.basicConfig(
    filename="publish_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Confluence client
confluence = Confluence(
    url=config["CONFLUENCE_SERVER"],
    token=config["CONFLUENCE_TOKEN"]
)

def extract_zip(zip_path, extract_to="unzipped_md"):
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

def publish_to_confluence(title, content):
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
    extracted_folder = extract_zip(config["ZIP_FILE"])
    for root, _, files in os.walk(extracted_folder):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    title = get_title_from_md(file_path)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    success = publish_to_confluence(title, content)
                    if success:
                        logging.info(f"Published: {title}")
                    else:
                        logging.error(f"Failed to publish: {title}")
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
