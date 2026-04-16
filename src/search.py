import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from src.config import GOOGLE_API_KEY, GOOGLE_CSE_ID
from src.llm import extract_entities

# Authorized domains from requirements
ALLOWED_DOMAINS = [
    "moneycontrol.com", "economictimes.indiatimes.com", "livemint.com",
    "business-standard.com", "financialexpress.com", "businesstoday.in",
    "ndtvprofit.com", "nseindia.com", "bseindia.com", "pulse.zerodha.com",
    "screener.in", "trendlyne.com", "bloomberg.com", "reuters.com",
    "cnbc.com", "investing.com", "tradingview.com", "marketwatch.com",
    "thebalancemoney.com", "finance.yahoo.com"
]

def search_financial_news(query: str, num_results: int = 5) -> list:
    """Search Google Custom Search API."""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Missing Google API credentials")
        return []

    url = "https://www.googleapis.com/customsearch/v1"
    try:
        response = requests.get(
            url,
            params={
                "q": query,
                "key": GOOGLE_API_KEY,
                "cx": GOOGLE_CSE_ID,
                "num": min(num_results, 10),
            },
            timeout=15,
        )
        if response.status_code == 200:
            items = response.json().get("items", [])
            filtered_items = []
            for item in items:
                domain = urlparse(item.get("link", "")).netloc.lower()
                if any(allowed in domain for allowed in ALLOWED_DOMAINS):
                    filtered_items.append(item)
            return filtered_items
        print(f"Google API Error: {response.status_code}")
        return []
    except Exception as e:
        print(f"Search error: {e}")
        return []

def fetch_article_content(url: str) -> str:
    """Fetches the full text content of an article."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        )
    }
    
    domain = urlparse(url).netloc.lower()
    is_allowed = any(allowed in domain for allowed in ALLOWED_DOMAINS)
    if not is_allowed:
        print(f"Skipping unauthorized domain: {domain}")
        return ""
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = "\n".join([p.get_text(" ", strip=True) for p in paragraphs if p.get_text(strip=True)])
            return text.strip()
    except Exception as e:
        print(f"Fetch error for {url}: {e}")
    return ""

def search_and_extract(query: str) -> list:
    """Full pipeline: Search -> Fetch -> Extract entities."""
    results = search_financial_news(query)
    extracted_data = []
    seen_urls = set()

    for res in results:
        url = res.get("link")
        title = res.get("title", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        content = fetch_article_content(url)

        if content and len(content) > 200:
            truncated_content = content[:4000]
            entities_rel = extract_entities(truncated_content)
            extracted_data.append({
                "url": url,
                "title": title,
                "content": content,
                "graph_data": entities_rel
            })
            
    return extracted_data
