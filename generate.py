import os, json, re, requests
from datetime import datetime, timezone, timedelta

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

BRIEF_PROMPT = """오늘 날짜 기준 최신 뉴스를 웹검색해서 HR 담당자용 데일리 브리핑을 만들어라.
대상: 국내 사무직 IT/보안 기업(임직원 약 100명)의 인사·총무 실무자.
비중: 인사·노무 60% / 경제 20% / AI 20%.
관점: 단순 요약이 아니라 "우리 회사가 뭘 확인하거나 바꿔야 하는가" 중심.
- 인사·노무: 노동법·고용노동부 정책·판례·정부지원제도. 각 항목에 [적용일]과 [HR Action]을 붙여라.
- 경제: 채용·인건비·복리후생에 영향 주는 것만.
- AI: HR 자동화·개인정보·보안·생산성 관련만.
- 모든 이슈에 출처와 날짜 표기.
반드시 아래 JSON 형식으로만 답하라. 다른 텍스트 금지.
{
  "digest": "카톡용 요약. 「오늘 HR이 꼭 볼 3가지」를 이모지 포함 3줄로. 공백 포함 190자 이내.",
  "full": "전체 브리핑. 위 구조를 다 담은 일반텍스트."
}
"""

def build_brief():
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ANTHROPIC_API_KEY,
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-5", "max_tokens": 3000,
              "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 8}],
              "messages": [{"role": "user", "content": BRIEF_PROMPT}]},
        timeout=180)
    r.raise_for_status()
    text = "".join(b["text"] for b in r.json()["content"] if b["type"] == "text")
    return json.loads(re.search(r"\{.*\}", text, re.S).group())

if __name__ == "__main__":
    kst = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    obj = build_brief()
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(f"<meta charset='utf-8'><title>HR Daily Brief {kst}</title>"
                f"<pre style='font:16px/1.7 -apple-system,\"Malgun Gothic\",sans-serif;"
                f"white-space:pre-wrap;max-width:720px;margin:2rem auto;padding:0 1rem'>{obj['full']}</pre>")
    with open("digest.txt", "w", encoding="utf-8") as f:
        f.write(obj["digest"][:200])
    print("생성 완료:", kst)
