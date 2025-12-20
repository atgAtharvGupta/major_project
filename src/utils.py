import requests
from src.constants import *
import os
from bs4 import BeautifulSoup
import json
import ollama


def search_with_google_api(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api}&cx={search_engine_id}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


def generate_search_queries(user_input):
    """
    Generates keyword-optimized search queries for Indian financial sentiment analysis.
    """
    # Refined prompt for keyword-heavy, Indian-market focused queries
    prompt = f"""
    You are a financial data engineer. Convert the user input into 5-7 HIGH-DENSITY search queries 
    optimized for search engines and news scrapers. 
    
    Context: Indian Financial Market (NSE/BSE).
    Target: {user_input}
    
    Rules for queries:
    1. Use Boolean operators (AND, OR) where helpful.
    2. Include Indian indices/regulators (Nifty, Sensex, SEBI, RBI) if relevant.
    3. Include sentiment-heavy terms (bullish, bearish, brokerage view, target price, outlook).
    4. Focus on performance keywords (Q3 results, EBITDA margins, YoY growth, FII DII activity).
    5. No full sentences. Use keyword strings.

    Output format: Strictly a Python list of strings.
    """

    try:
        response = ollama.chat(
            model=ollama_model,
            messages=[
                {"role": "system", "content": "You generate keyword-optimized search strings for Indian finance."},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.2, "num_predict": 250}
        )
        
        queries_text = response["message"]["content"].strip()
        
        # Clean potential markdown code blocks if the LLM includes them
        if "```python" in queries_text:
            queries_text = queries_text.split("```python")[1].split("```")[0].strip()
        elif "```" in queries_text:
            queries_text = queries_text.split("```")[1].split("```")[0].strip()

        queries = eval(queries_text)
        return queries if isinstance(queries, list) else []
    except Exception as e:
        print(f"Error: {e}")
        return [f"{user_input} Indian market sentiment", f"{user_input} NSE BSE news"]
    
def fetch_full_content(url):
    """
    Fetches the full content of a webpage given its URL.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            full_text = "\n".join([p.get_text() for p in paragraphs])
            return full_text.strip() if full_text else None
        else:
            print(f"Error: Unable to fetch content from {url} (Status Code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return None

from tqdm import tqdm

def create_dataset_from_queries(queries, directory="dataset"):
    """
    Process search queries and save results as text files in the same directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_count = 1  # To ensure unique filenames across all queries

    for query in tqdm(queries, desc="Collecting Data", unit="query"):
        tqdm.write(f"Processing query: {query}")
        valid_count = 0
        page_number = 1

        while valid_count < 10:
            tqdm.write(f"  > Fetching search results, page {page_number}...")
            results = search_with_google_api(query + f"&start={page_number * 10}")

            if not results:
                tqdm.write("  > No more results found. Try refining the query.")
                break

            for result in results:
                if valid_count >= 10:
                    break  # Stop when 10 valid documents are saved

                title = result["title"]
                link = result["link"]
                snippet = result.get("snippet", "No snippet")

                # Fetch full content of the link
                full_content = fetch_full_content(link)
                if full_content:  # Save only if content is valid
                    filename = f"{directory}/doc_{file_count}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"Query: {query}\n")
                        f.write(f"Title: {title}\n")
                        f.write(f"Link: {link}\n")
                        f.write(f"Snippet: {snippet}\n\n")
                        f.write(f"Full Content:\n{full_content}")
                    tqdm.write(f"    Saved: {filename} - {title[:60]}...")
                    valid_count += 1
                    file_count += 1
                else:
                    tqdm.write(f"    Skipped: {link} (No valid content)")

            page_number += 1  # Move to the next page of results

    tqdm.write(f"Finished processing all queries. Total files saved: {file_count - 1}")


def generate_summary_report(context: str, query: str) -> str:
    """
    Generate a detailed summary report for financial sentiment analysis.
    Takes context and query as inputs and returns a comprehensive summary.
    Uses Ollama LLM for report generation.
    """
    prompt = f"""
    You are a financial sentiment analysis assistant. Using the context provided below, generate a detailed summary report:

    Context:
    {context}

    Query:
    {query}

    The report should include:
    1. A high-level summary of the financial trends related to the query.
    2. Key positive, negative, and neutral sentiments detected.
    3. Reasons or factors driving the sentiments.
    4. Suggestions or insights for potential investors or stakeholders.

    Be concise but ensure that the report is actionable and insightful.
    """
    
    # Use Ollama Python library directly
    try:
        response = ollama.chat(
            model=ollama_model,
            messages=[
                {"role": "system", "content": "You are an expert in financial sentiment analysis."},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0.0,
                "num_predict": 500  # max_tokens equivalent in Ollama
            }
        )
        
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Error generating summary report: {e}")
        return f"Error generating report: {str(e)}"


