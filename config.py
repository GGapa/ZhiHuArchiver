import os
import dotenv

dotenv.load_dotenv()

GITHUB_USER = os.getenv("GITHUB_USER", "")
REPO_NAME = os.getenv("REPO_NAME", "ZhiHuArchive")
BASE_URL = f"https://{GITHUB_USER}.github.io/{REPO_NAME}"
SITE_TITLE = os.getenv("SITE_TITLE", "知乎备份")
SITE_DESCRIPTION = os.getenv("SITE_DESCRIPTION", "知乎文章和回答备份目录")