import os
from pathlib import Path
from dotenv import load_dotenv

# .env 는 ko/ 폴더에 있음 (이 파일 기준 상위 폴더)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

key = os.environ.get("OPENAI_API_KEY", "")
print("키 설정 여부:", "설정됨" if key else "비어 있음")
print("키 앞머리:", key[:7] + "..." if key else "-")
