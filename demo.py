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


import csv
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# 📊 REPORT WRITER MODULE
# ─────────────────────────────────────────────────────────────

class ReportWriter:
    def __init__(self, zip_path, output_dir="reports"):
        os.makedirs(output_dir, exist_ok=True)
        zip_name = Path(zip_path).name
        self.report_path = os.path.join(output_dir, f"{Path(zip_name).stem}_report.csv")
        self.rows = []

    def add_row(self, file_name, confluence_url, status, zip_name):
        self.rows.append({
            "File Name": file_name,
            "Confluence URL": confluence_url,
            "Status": status,
            "Zip File": zip_name
        })

    def write(self):
        with open(self.report_path, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["File Name", "Confluence URL", "Status", "Zip File"])
            writer.writeheader()
            writer.writerows(self.rows)
        return self.report_path


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
    try:
        extracted_folder = self.extractor.extract()
        md_files = self.extractor.get_md_files()

        for file_path in md_files:
            file_name = Path(file_path).name
            title = self.extractor.get_title(file_path)
            zip_name = Path(self.config.ZIP_FILE).name

            exists, page_id = self.publisher.page_exists(title)
            if exists:
                url = f"{self.config.CONFLUENCE_SERVER}/pages/viewpage.action?pageId={page_id}"
                self.report.add_row(file_name, url, "Already Exists", zip_name)
                logging.info(f"Skipped (already exists): {title} [Page ID: {page_id}]")
                continue

            try:
                content = self.extractor.read_file(file_path)

                # Wrap raw markdown using Confluence macro
                markdown_macro = (
                    "<ac:structured-macro ac:name='markdown'>"
                    "<ac:plain-text-body><![CDATA["
                    f"{content}"
                    "]]></ac:plain-text-body></ac:structured-macro>"
                )

                success = self.publisher.publish(title, markdown_macro)
                if success:
                    page_id = self.publisher.client.get_page_id(self.config.CONFLUENCE_SPACE, title)
                    url = f"{self.config.CONFLUENCE_SERVER}/pages/viewpage.action?pageId={page_id}"
                    self.report.add_row(file_name, url, "Published", zip_name)
                else:
                    self.report.add_row(file_name, "", "Error", zip_name)
            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")
                self.report.add_row(file_name, "", f"Error: {str(e)}", zip_name)

        report_path = self.report.write()
        logging.info(f"Report saved to: {report_path}")
        print(f"CSV report generated: {report_path}")

    except Exception as e:
        logging.error(f"Fatal error in run(): {e}")
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    try:
        automation = ConfluenceAutomation()
        automation.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"[ERROR] {e}")
