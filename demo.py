import os
import zipfile
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from atlassian import Confluence
import markdown

# ─────────────────────────────────────────────────────────────
# 🔧 CONFIGURATION
# ─────────────────────────────────────────────────────────────

class Config:
    def __init__(self):
        load_dotenv()
        self.CONFLUENCE_SERVER = os.getenv("CONFLUENCE_SERVER")
        self.CONFLUENCE_SPACE = os.getenv("CONFLUENCE_SPACE")
        self.CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")
        self.PARENT_DOC = os.getenv("PARENT_DOC")
        self.ZIP_FILE = os.getenv("ZIP_FILE")
        self.EXTRACT_FOLDER = "unzipped_md"
        self.validate()

    def validate(self):
        missing = [k for k, v in self.__dict__.items() if not v]
        if missing:
            raise ValueError(f"Missing config keys: {', '.join(missing)}")

# ─────────────────────────────────────────────────────────────
# 📋 LOGGING
# ─────────────────────────────────────────────────────────────

class Logger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{timestamp}_publish.log")
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        logging.info("Logger initialized.")
        self.log_file = log_file

# ─────────────────────────────────────────────────────────────
# 📦 FILE HANDLING
# ─────────────────────────────────────────────────────────────

class MarkdownExtractor:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.extract_to = self._get_extract_folder()

    def _get_extract_folder(self):
        base_name = Path(self.zip_path).stem  # e.g., "usecases"
        extract_folder = os.path.join(os.getcwd(), base_name)
        return extract_folder

    def extract(self):
        if not os.path.isfile(self.zip_path):
            logging.error(f"ZIP file not found: {self.zip_path}")
            return None
        os.makedirs(self.extract_to, exist_ok=True)
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_to)
        logging.info(f"Extracted ZIP to: {self.extract_to}")
        return self.extract_to

    def get_md_files(self):
        if not os.path.exists(self.extract_to):
            logging.error(f"Folder not found: {self.extract_to}")
            return []
        md_files = []
        for root, _, files in os.walk(self.extract_to):
            if "__MACOSX" in root:
                continue
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
        return md_files

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def get_title(file_path):
        return Path(file_path).stem

# ─────────────────────────────────────────────────────────────
# 🌐 CONFLUENCE INTEGRATION
# ─────────────────────────────────────────────────────────────

class ConfluencePublisher:
    def __init__(self, config: Config):
        self.config = config
        self.client = Confluence(
            url=config.CONFLUENCE_SERVER,
            token=config.CONFLUENCE_TOKEN
        )

    def page_exists(self, title):
        page_id = self.client.get_page_id(space=self.config.CONFLUENCE_SPACE, title=title)
        return page_id is not None, page_id

    def publish(self, title, markdown_content):
        try:
            html_content = markdown.markdown(markdown_content)
            self.client.create_page(
                space=self.config.CONFLUENCE_SPACE,
                title=title,
                body=html_content,
                parent_id=self.config.PARENT_DOC,
                representation="storage"
            )
            logging.info(f"Published: {title}")
            return True
        except Exception as e:
            logging.error(f"Failed to publish '{title}': {e}")
            return False

# ─────────────────────────────────────────────────────────────
# 🚀 MAIN EXECUTION
# ─────────────────────────────────────────────────────────────

class ConfluenceAutomation:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.extractor = MarkdownExtractor(self.config.ZIP_FILE, self.config.EXTRACT_FOLDER)
        self.publisher = ConfluencePublisher(self.config)

    def run(self):
        self.extractor.extract()
        md_files = self.extractor.get_md_files()

        for file_path in md_files:
            title = self.extractor.get_title(file_path)
            exists, page_id = self.publisher.page_exists(title)
            if exists:
                logging.info(f"Skipped (already exists): {title} [Page ID: {page_id}]")
                continue

            content = self.extractor.read_file(file_path)
            self.publisher.publish(title, content)

if __name__ == "__main__":
    try:
        automation = ConfluenceAutomation()
        automation.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"[ERROR] {e}")
