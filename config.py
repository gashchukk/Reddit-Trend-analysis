#!/usr/bin/env python3

import json
import os
import time
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from weasyprint import HTML
import argparse

load_dotenv()

BASE_URL = "https://old.reddit.com"
HEADERS = {"User-Agent": "trend-research-bot"}
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

JSON_DIR = "./json"
PDF_DIR = "./reports"

MAX_POSTS_PER_SUBREDDIT = 100
MAX_COMMENTS_PER_POST = 5
MAX_WORKERS = 5              # Parallel threads

# LLM settings
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.3

