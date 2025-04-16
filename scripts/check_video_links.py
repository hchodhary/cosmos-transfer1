# check_video_links.py

import os
import re
import requests

def find_md_files(root="."):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".md"):
                yield os.path.join(dirpath, f)

def extract_video_urls(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'<video\s+src="([^"]+)"', content)

def check_video_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        content_type = response.headers.get('Content-Type', '')
        if response.status_code == 200 and 'video' in content_type:
            print(f"✅ Video OK: {url}")
            return True
        else:
            print(f"❌ Invalid video: {url} (Status: {response.status_code}, Type: {content_type})")
            return False
    except Exception as e:
        print(f"❌ Error checking {url}: {e}")
        return False

def main():
    all_passed = True
    for md_file in find_md_files():
        video_urls = extract_video_urls(md_file)
        for url in video_urls:
            if not check_video_url(url):
                all_passed = False
    if not all_passed:
        exit(1)

if __name__ == "__main__":
    main()
