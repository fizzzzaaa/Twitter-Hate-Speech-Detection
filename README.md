# 🛡️ Twitter Hate Speech Detection

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A machine learning-powered tool that detects hate speech and offensive content in Twitter (X) tweets in real-time. Built for research, content moderation, and social media analytics.

## ✨ Features

- 🔍 Fetch tweets by keyword, hashtag, or user timeline (Twitter API v2)
- 🧠 Hate speech classification using fine-tuned transformers (e.g., RoBERTa, BERT)
- 📊 Confidence score for each prediction (hate / offensive / neutral)
- 🚀 REST API endpoint for batch or single tweet analysis
- 📁 Export results to CSV / JSON

## 🛠️ Tech Stack

- **Python** 3.9+
- **Tweepy** – Twitter API wrapper
- **Transformers** (Hugging Face) – hate speech model
- **Flask** / **FastAPI** – API server (optional)
- **Pandas** – data handling

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/twitter-hate-detection.git
cd twitter-hate-detection

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
