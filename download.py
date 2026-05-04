import requests  # type: ignore
import json
import re
from tqdm import tqdm  # type: ignore
from pathlib import Path
import random
import time
import dotenv
import os
from functools import wraps


def retry_with_exponential_backoff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wait_times = [60 * 2**i for i in range(1, 7)] + [
            64 for _ in range(10)
        ]  # 2min, 4min, 8min, 16min, 32min, 64min
        last_exception = None

        for wait in wait_times:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                print(f"Attempt failed. Waiting {wait} seconds before retry...")
                last_exception = e
                time.sleep(wait)

        raise last_exception

    return wrapper


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
}


def download_article(path: str, cookie: str) -> dict:
    article_id = path.split("/")[-1]
    url = f"https://zhuanlan.zhihu.com{path}"
    response = requests.get(
        url,
        headers={**HEADERS, "Cookie": cookie, "Referer": "https://www.zhihu.com"},
        timeout=10,
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    match = re.search(
        r'<script id="js-initialData" type="text/json">(.*?)</script>', response.text
    )
    if not match:
        raise Exception(f"Cannot find initialData in {path}")
    data = json.loads(match.group(1))
    articles = data.get("initialState", {}).get("entities", {}).get("articles", {})
    if article_id not in articles:
        raise Exception(f"Article {article_id} not found in page data")
    return normalize_article(articles[article_id])


def download_answer(path: str, api_base: str, cookie: str) -> dict:
    api_path = path.replace("/answer/", "/answers/")
    response = requests.get(
        api_base + api_path,
        params={"include": "content,comment_count,voteup_count"},
        headers={**HEADERS, "Cookie": cookie, "Referer": "https://www.zhihu.com"},
        timeout=10,
    )
    if response.status_code == 403:
        raise Exception(f"Failed to download {path}: 403 Forbidden")
    if response.status_code == 404:
        return None
    if "error" in response.json():
        raise Exception(f"Error: {response.json()['error']}")
    return response.json()


def download_content() -> None:
    dotenv.load_dotenv()
    cookie = os.getenv("COOKIE_A")
    api_base = os.getenv("API")

    answer_path = Path("answer")
    answer_path.mkdir(exist_ok=True)
    article_path = Path("article")
    article_path.mkdir(exist_ok=True)

    with open("paths.json", "r", encoding="utf-8") as file:
        paths = json.load(file)

    processed_links = set(answer_path.glob("*.json")) | set(article_path.glob("*.json"))
    processed_ids = set([file.stem for file in processed_links])

    Path("not_found_paths.txt").touch(exist_ok=True)
    with open("not_found_paths.txt", "r", encoding="utf-8") as file:
        not_found_paths = set(file.read().splitlines())

    paths = [p for p in paths if p not in not_found_paths]
    paths = [p for p in paths if p.split("/")[-1] not in processed_ids]

    censorship_path = Path("censorship.json")
    if censorship_path.exists():
        with open(censorship_path, "r", encoding="utf-8") as f:
            censorship = json.load(f)
    else:
        censorship = {}

    for path in tqdm(paths):
        is_article = "/p/" in path
        content_type = "article" if is_article else "answer"
        content_id = path.split("/")[-1]

        if is_article:
            data = download_article(path, cookie)
        else:
            data = download_answer(path, api_base, cookie)

        if data is None:
            print(f"Skipping {path} because it does not exist")
            with open("not_found_paths.txt", "a", encoding="utf-8") as file:
                file.write(path + "\n")
            continue

        with open(f"{content_type}/{content_id}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        censorship[path] = False
        with open(censorship_path, "w", encoding="utf-8") as f:
            json.dump(censorship, f, ensure_ascii=False, indent=4)

        sleep_time = random.random() * 4 + 1
        time.sleep(sleep_time)

def normalize_article(data: dict) -> dict:
    """把文章 JSON 的駝峰命名統一轉換成蛇形命名，與 render.py 和 summary.py 保持一致"""
    data["image_url"] = data.get("imageUrl", "")
    data["voteup_count"] = data.get("voteupCount", 0)
    data["comment_count"] = data.get("commentCount", 0)

    author = data.get("author", {})
    author["avatar_url"] = author.get("avatarUrl", "")
    if author.get("url", "").startswith("/people/"):
        author["url"] = "https://www.zhihu.com" + author["url"]

    return data

download_content_with_retry = retry_with_exponential_backoff(download_content)
download_content_with_retry()