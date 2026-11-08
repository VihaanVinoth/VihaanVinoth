import urllib.request
import json
import re

def fetch_random_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        return data.get('text', 'Coding is awesome!')

def update_readme():
    fact_text = fetch_random_fact()
    formatted_fact = fact_text
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- START_SECTION:fun_fact -->)(.*?)(<!-- END_SECTION:fun_fact -->)"
    replacement = f"\\1\n{formatted_fact}\n\\3"

    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()