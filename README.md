﻿# text-to-speech-elevenlabs

# 1. Tạo venv
python -m venv venv

venv\Scripts\activate

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Tạo file .env
# Ghi nội dung: ELEVENLABS_API_KEY=sk_xxxxxx

# 6. Chạy server
uvicorn main:app --reload
