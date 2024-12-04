# config.py
import os

# 환경변수로 설정된 Bard API 키
BARD_API_KEY = os.getenv('_BARD_API_KEY', 'your_bard_api_key_here')
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
# ConnectionError방지