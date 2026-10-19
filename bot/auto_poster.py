#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Income Factory - Automated SEO Blog Post Generator
- Selects unwritten high-CPC topics from bot/topics_pool.json
- Generates structured, SEO-optimized Markdown posts in src/content/blog/
- Uses Gemini API if GEMINI_API_KEY is set, otherwise uses structured SEO generator
- Automatically links to all 6 Micro Web Calculators (/tools/...)
"""

import argparse
import datetime
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = ROOT_DIR / "bot" / "topics_pool.json"
HISTORY_FILE = ROOT_DIR / "bot" / "history.json"
BLOG_DIR = ROOT_DIR / "src" / "content" / "blog"

TOOL_URLS = {
    "customs": ("해외직구 관부가세 자동 계산기", "/tools/customs-calculator/"),
    "salary": ("2026 연봉 실수령액 자동 계산기", "/tools/salary-calculator/"),
    "severance": ("2026 퇴직금 & 평균임금 자동 계산기", "/tools/severance-calculator/"),
    "loan": ("대출 원리금균등 vs 원금균등 이자 계산기", "/tools/loan-calculator/"),
    "dividend": ("배당주 & ETF 복리 시뮬레이터", "/tools/dividend-calculator/"),
    "ai": ("AI 구독료 vs API 가성비 비교 계산기", "/tools/ai-cost-calculator/"),
}


def load_json(path: Path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_with_gemini(topic: dict, api_key: str) -> str:
    """Calls Gemini REST API to write a comprehensive Korean SEO guide."""
    tool_name, tool_url = TOOL_URLS.get(topic["relatedTool"], TOOL_URLS["salary"])
    prompt = f"""당신은 대한민국 최고의 금융·세무·IT 전문 에디터입니다.
다음 주제로 검색엔진(구글, 네이버) 상위 노출에 최적화된 전문 가이드를 마크다운(Markdown) 본문 형식으로 작성하세요.
(YAML frontmatter는 제외하고 본문만 출력하세요.)

- 제목: {topic['title']}
- 설명: {topic['description']}
- 필수 포함 핵심 내용: {', '.join(topic['keyPoints'])}
- 내부 링크 유도: 본문 중간과 결론에 자연스럽게 [{tool_name}]({tool_url}) 링크를 포함하세요.

작성 규칙:
1. H2(##), H3(###) 소제목을 명확히 구분하세요.
2. 반드시 비교 표(Markdown Table)를 1개 이상 포함하세요.
3. 독자가 바로 실행할 수 있는 체크리스트와 구체적인 수치 예시를 포함하세요.
4. 분량은 공백 포함 1,800자 이상으로 깊이 있게 작성하세요.
"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.65}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()


def generate_structured_article(topic: dict) -> str:
    """Generates a rich, structured SEO article without external API dependency."""
    tool_name, tool_url = TOOL_URLS.get(topic["relatedTool"], TOOL_URLS["salary"])
    points = topic.get("keyPoints", [])

    body = f"""{topic['description']}

실제 데이터를 기반으로 가장 많이 헷갈려 하시는 핵심 기준과 손해를 보지 않기 위한 실전 계산 방법을 단계별로 정리해 드립니다.

## 1. 핵심 요약 및 반드시 알아야 할 3가지 포인트

바쁜 분들을 위해 가장 중요한 핵심 기준 3가지를 먼저 요약합니다.

1. **{points[0] if len(points) > 0 else '최신 기준 확인'}**
2. **{points[1] if len(points) > 1 else '실전 수치 비교'}**
3. **{points[2] if len(points) > 2 else '비용 절감 체크리스트'}**

> **실전 팁:** 복잡한 수식을 직접 계산할 필요 없이 본 사이트의 **[{tool_name}]({tool_url})**를 활용하시면 내 조건에 맞는 정확한 금액을 1초 만에 시뮬레이션할 수 있습니다.

## 2. 조건별 상세 비교표 (한눈에 보는 손익 분석)

선택하는 방식에 따라 실제 발생하는 비용과 절감 효과를 비교한 표입니다.

| 구분 | 일반 기준 (미적용 시) | 최적화 전략 적용 시 | 예상 차이 및 효과 |
| :--- | :--- | :--- | :--- |
| **초기 세팅 난이도** | 매우 쉬움 (기본값 유지) | 5분 내외 확인 및 설정 | **즉시 적용 가능** |
| **세금 및 수수료 부담** | 기본 세율 100% 부담 | 비과세·면세·우대 한도 극대화 | **연간 15% ~ 70% 비용 절감** |
| **장기 복리 효과 (3~5년)** | 고정 지출 누적 | 절감된 금액 재투자 가능 | **수십만 ~ 수백만 원 자산 격차** |

## 3. 단계별 실전 체크리스트

실수 없이 혜택을 챙기기 위해 아래 순서대로 점검해 보세요.

### Step 1: 내 현재 기준 금액 및 한도 확인하기
가장 먼저 내가 지출하거나 투자하려는 금액이 면세·비과세 또는 우대 구간 내에 있는지 확인해야 합니다. 기준 한도를 단 조금이라도 초과할 경우 전체 금액에 대해 과세되거나 상위 구간 요율이 적용될 수 있습니다.

### Step 2: 웹 계산기로 시나리오별 모의 계산 실행
어림짐작으로 판단하기보다 **[{tool_name}]({tool_url})**에 내 실제 수치를 입력해 A안과 B안의 차이를 비교해 보세요. 눈으로 정확한 원화(₩) 및 달러($) 차액을 확인하면 의사결정이 훨씬 명확해집니다.

### Step 3: 절감한 금액으로 현금흐름 파이프라인 강화
아낀 세금이나 구독료, 대출 이자는 그냥 소비하지 말고 별도의 파킹통장이나 월배당 ETF 계좌로 모아두면 또 다른 현금흐름을 만드는 씨앗이 됩니다.
"""
    return body.strip()


def create_markdown_file(topic: dict, body_content: str) -> Path:
    today_str = datetime.date.today().isoformat()
    tags_json = json.dumps(topic.get("tags", []), ensure_ascii=False)
    tool_name, _ = TOOL_URLS.get(topic["relatedTool"], TOOL_URLS["salary"])

    frontmatter = f"""---
title: "{topic['title']}"
description: "{topic['description']}"
pubDate: {today_str}
category: "{topic['category']}"
tags: {tags_json}
relatedTool: "{topic['relatedTool']}"
faq:
  - q: "가장 빠르고 정확하게 내 조건에 맞는 금액을 계산하려면 어떻게 하나요?"
    a: "본문 상단과 하단에 연결된 '{tool_name}'에 수치를 입력하시면 2026년 최신 기준이 반영된 결과를 별도 회원가입 없이 즉시 확인하실 수 있습니다."
  - q: "입력한 개인 금융·직구 금액 정보가 서버에 저장되나요?"
    a: "아니요, 본 사이트의 모든 계산기는 사용자의 웹 브라우저 내부에서만 동작하며 어떠한 수치도 외부 서버로 전송하거나 저장하지 않으므로 안심하고 이용하실 수 있습니다."
---

{body_content}
"""
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    file_path = BLOG_DIR / f"{topic['slug']}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter)
    return file_path


def main():
    parser = argparse.ArgumentParser(description="Auto Income Factory Blog Generator")
    parser.add_argument("--demo", action="store_true", help="Force structured template mode without API call")
    parser.add_argument("--count", type=int, default=1, help="Number of posts to generate in this run")
    args = parser.parse_args()

    topics = load_json(TOPICS_FILE, [])
    history = load_json(HISTORY_FILE, {"published_slugs": []})
    published = set(history.get("published_slugs", []))

    for md_file in BLOG_DIR.glob("*.md"):
        published.add(md_file.stem)

    pending_topics = [t for t in topics if t["slug"] not in published]
    if not pending_topics:
        print("[INFO] 모든 예약 토픽이 이미 발행되었습니다.")
        return 0

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    generated_count = 0

    for next_topic in pending_topics[: args.count]:
        if api_key and not args.demo:
            try:
                body = generate_with_gemini(next_topic, api_key)
            except Exception:
                body = generate_structured_article(next_topic)
        else:
            body = generate_structured_article(next_topic)

        out_path = create_markdown_file(next_topic, body)
        published.add(next_topic["slug"])
        generated_count += 1
        print(f"[SUCCESS] Generated: {out_path.name}")

    history["published_slugs"] = sorted(list(published))
    history["last_run"] = datetime.datetime.now().isoformat()
    save_json(HISTORY_FILE, history)

    print(f"[DONE] Total newly generated posts: {generated_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
