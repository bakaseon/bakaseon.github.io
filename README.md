# 🚀 Auto Income Factory (웹 계산기 + 자동화 블로그 + 제휴 수익 통합 엔진)

1개월 뒤 월 \$20, 6개월 뒤 월 \$100+ 달성을 위해 설계된 **실용 웹 도구(Micro-Tools) + SEO 자동 포스팅 봇 + 멀티 광고/제휴 수익화 플랫폼**입니다.

---

## 📂 핵심 구조 안내

* **[src/config/site.ts](src/config/site.ts)**: **중앙 수익화 설정 파일** (애드센스 ID, 카카오 애드핏 코드, 쿠팡/제휴 마케팅 링크를 한 곳에서 관리)
* **실용 웹 계산기 4종 (`src/pages/tools/`)**:
  1. `/tools/customs-calculator/` — 해외직구 관부가세 자동 계산기
  2. `/tools/salary-calculator/` — 2026 연봉 실수령액 & 4대보험 계산기
  3. `/tools/dividend-calculator/` — 배당주 & 월배당 ETF 복리 시뮬레이터
  4. `/tools/ai-cost-calculator/` — AI 월 구독료 vs API 종량제 가성비 계산기
* **자동 포스팅 봇 (`bot/auto_poster.py`)**:
  - `bot/topics_pool.json`에서 미발행 주제를 골라 자동으로 웹 계산기 내부 링크가 포함된 SEO 블로그 포스트를 생성합니다.
  - `.github/workflows/daily-auto-post.yml`을 통해 매일 오전 8시(KST) 클라우드에서 무인으로 자동 실행됩니다.

---

## ⚡ 로컬 실행 및 테스트 명령어

```bash
# 1. 개발 서버 실행 (브라우저에서 실시간 확인)
npm run dev

# 2. 자동 블로그 글 생성 봇 즉시 실행 (1회 실행 시 새 글 1편 자동 생성)
npm run post:demo

# 3. 정적 사이트 빌드 (dist/ 폴더 및 sitemap 자동 생성)
npm run build
```

---

## 💰 수익화 연동 3단계 (Cloudflare Pages 무료 배포)

1. **무료 호스팅 배포**:
   - 이 폴더를 내 GitHub 저장소(Repository)에 올린 뒤, **Cloudflare Pages**에서 해당 저장소를 연결하면(Build command: `npm run build`, Output directory: `dist`) 평생 무료로 초고속 웹사이트가 배포됩니다.
2. **1개월 차 즉시 수익화 (승인 대기 없음)**:
   - `src/config/site.ts`의 `affiliates` 항목에 내 **쿠팡 파트너스 / 알리익스프레스 제휴 링크**를 입력합니다.
   - **카카오 애드핏(AdFit)**에 사이트를 등록(약 2~3일 내 승인)한 뒤 발급받은 단위 ID를 `kakaoAdFitUnitTop`에 넣습니다.
3. **장기 고단가 수익화 (구글 애드센스)**:
   - 글이 20~30개 쌓인 후 구글 애드센스 승인을 신청하고, 발급받은 `ca-pub-...` ID를 `googleAdSenseId`에 넣으면 사이트 전체에 고단가 맞춤 광고가 자동 송출됩니다.
