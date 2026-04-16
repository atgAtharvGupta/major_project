# Financial Intelligence Platform

A comprehensive Streamlit-based web application for gathering financial news, constructing an ever-growing Neo4j knowledge graph, fetching market data, and performing sentiment analysis using Groq's high-speed cloud LLMs.

## 🚀 Overview
1. **Intelligent Data Collection**: Uses Google Custom Search to scrape relevant financial news.
2. **Knowledge Graph Growth**: Builds and deduplicates a Knowledge Graph (Neo4j) dynamically as you query.
3. **Semantic Analysis**: Utilizes `llama-3.3-70b-versatile` via Groq and `bge-large-en-v1.5` embeddings for deep insights.
4. **Market Data**: Integrates `yfinance` to display relevant historical ticker charts.
5. **Interactive UI**: Clean, dark-mode Streamlit UI that visualizes the growing graph in real-time.
6. **Authentication**: Secured with Google Firebase Auth.

## 🛠️ Tech Stack
* **UI**: Streamlit, Streamlit-Agraph
* **LLM**: Groq (Llama-3.3-70b)
* **Embeddings**: Sentence-Transformers (BGE-Large)
* **Graph DB**: Neo4j
* **Search / Data**: Google Custom Search API, yfinance (Yahoo Finance)
* **Auth**: Firebase REST API

## ⚙️ Prerequisites
You need API Keys for the following services:
1. **Neo4j** (AuraDB or Local)
2. **Groq API**
3. **Google Custom Search & API Key**
4. **Firebase Web App Config**

## 📥 Setup

1. **Clone & Virtual Environment**:
```bash
git clone <repository>
cd <repository>
python -m venv venv
venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure Environment Variables**:
Copy `.env.example` to `.env` and fill in your keys:
```
cp .env.example .env
```
*(Ensure all keys, including Neo4j, Groq, Google, and Firebase are provided).*

## 🏃 Usage
Start the Streamlit application:
```bash
streamlit run app.py
```
Open your browser to the local address provided. Login using the sidebar, and begin asking financial queries.

## 🧪 Testing
The project features a full test suite encompassing LLM pipelines, graph DB integration, and search components.
```bash
pytest tests/ -v
```
