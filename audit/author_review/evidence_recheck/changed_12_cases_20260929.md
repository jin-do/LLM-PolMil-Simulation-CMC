# Revision23: 달라진 12건의 원문 근거 재검토

검토일: 2026-09-29. 검토자: AI. **이 문서는 오늘 수행한 AI의 원자료 재검토이며, 새로운 독립 인간 검증이 아니다.** 2026-09-27에 저자가 비맹검으로 확인한 기존 40건의 기록과 오늘의 의견을 구분한다. 기존 JSON, 공통규칙 라벨, 저자 수용 라벨은 수정하지 않았다.

## 핵심 결론

원래 공통규칙 관점에서는 이 12건을 **3 V·9 U로 유지**하는 것이 타당하다. 이번에 다시 확인한 문맥은 왜 저자가 A로 수용했는지 설명하는 데 도움이 되지만, 같은 판정대상·시점·단위에서 원 판정을 C로 바꾸는 새 증거는 확인하지 못했다. 이것은 저자의 과거 수용 기록을 취소하는 판단이 아니다. 서로 다른 질문에 대한 결과를 하나의 정확도나 정정률로 합치지 말아야 한다.

가장 강한 직접 근거는 HR-010·029·037의 시나리오 계열 수준 연속성이다. 가장 조심해야 할 주장은 HR-004의 결과 다양성을 행동쌍 생성으로, HR-019의 후속 이름 반복을 누락 턴 복원으로, HR-028의 철수 합의를 완료된 위기 해결로, HR-038의 내용 재등장을 분기 계보로 간주하는 표현이다. HR-035는 복합 사건의 일부 맥락만 직접 확인된다.

## 범위와 방법

- 공개본의 원 PDF 11개에서 관련 범위 147쪽을 새로 추출하고 11개 SHA-256을 등록값과 대조했다. HR-023·029는 같은 GEM-10 자료를 사용한다.
- 사례별 전후 선택, 명시된 부모·자식, 결과상태, 관련 최종 보고서를 읽었다. 147쪽은 추출 범위이며, 그 안의 모든 역사 서술·산술·정치적 개연성까지 다시 검증했다는 뜻은 아니다.
- 원 Prompt.pdf 6쪽의 지시와 공개 CRITERIA_CONTEXT_V1.md를 대조했다. 이 기준 문서는 사후 명료화이며 사전등록 규칙으로 취급하지 않았다. HR-011은 us_gpt.json의 전체 관련 설명을 함께 읽었다.
- CLA-04 p.24, GPT-25 p.8, GEM-16 p.14, PER-21 p.8은 원 PDF를 이미지로 렌더링하여 표제·공백·상태 위치를 확인했다. PDF 쪽수는 파일 첫 페이지부터 센 번호다.
- 인용은 새 추출본과 공백 및 알려진 NUL 추출문자만 정규화하여 자동 대조했다. 원문 PDF와 기존 기록은 그대로 보존했다. OCR, 새 시뮬레이션, 새 인간 코딩은 수행하지 않았다.

## 원래 요구와 이번 해석의 경계

Prompt p.1은 ‘combinations’가 각 행위자의 선택을 짝짓는 것이라고 정의하고, 주조합 1개와 대안 1–2개 및 각 조합의 독립 결과로그를 요구한다. pp.2–4는 각 시나리오 조합에서 같은 분기 구조와 기존 흐름의 유지를 요청한다. 활성 부모 선정, 병합·가지치기, 종말상태 면제는 명시하지 않는다. 따라서 별도 결과를 가진 부모가 사라진 경우와 결과 없는 후보가 다음 턴에 보이지 않는 경우를 구분했다.

사건 항목은 단순한 명칭의 존재보다 사건이 선택 조건으로 쓰였는지를 본다. 최종 보고서의 설명은 추가 문맥이 될 수 있으나, 작성 당시 턴의 선택이나 모든 부모의 적용을 소급해 증명하지는 않는다.

## 근거 유형 요약

| 주된 설명 유형 | 건수 | 사례 | 의미 |
|---|---:|---|---|
| 같은 범위의 문장을 재해석 | 1 | 011 | 군부의 기대 목표로 읽음; 성공 보장인지의 모호성은 남음 |
| 후속·넓은 문맥까지 확장 | 3 | 016,019,035 | 최종 서사 또는 문서 전체의 일부 연결을 수용 |
| 요구 대상·범위·종료 기준 변경 | 8 | 004,010,023,026,028,029,037,038 | 결과 다양성, 주요 시나리오 계열, 내용 재등장, 종료 예외 등을 수용 |
| 같은 범위의 새 증거로 C 입증 | 0 | — | 이번 재검토에서 확인되지 않음 |

이는 AI가 설명을 위해 붙인 주된 유형이다. 상호 배타적인 객관적 측정변수나 독립 검증 통계가 아니며, 실제로는 여러 유형이 겹친다.

## 사례별 결과

### HR-004 · CLA-04 · 다른 미래 결과와 추가 양국 행동쌍의 구별

**보존된 기록:** 이전 AI/공통규칙 관점 V → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** V 유지.

**원자료:** `runs/raw_logs/Claude_Opus_4/4. Strategic Decision Modeling Protocol.pdf`; 검토 쪽 22, 23, 24, 25, 26. 원 Prompt 해당 쪽 1, 3, 4.

**직접 근거**

- p.24: “Inevitable: Global nuclear exchange”

- p.24: “Most Plausible Combination: Mutual Military Fragmentation”

- p.24: “Logic: Complete collapse prevents coordinated strategic response, leading to chaotic local actions.”


**관찰 사실:** 조합 1과 3에는 주경로와 추가 행동쌍들이 있다. 조합 2의 미국 후보 SIOP Execution에는 전면 핵교환이라는 다음 사건이 붙고, Military Fragmentation에는 무작위 부대 행동·국지적 핵사용이 붙는다. 소련도 자동보복과 B-59 독립발사 후보를 제시한다. 그러나 양국을 함께 묶어 명시한 조합은 Mutual Military Fragmentation 하나다. 국가별 후보와 다음 사건은 존재하지만, 이들로부터 추가 행동쌍을 연구자가 조립할 수는 없다.

**원 공통규칙:** V 유지. 원규칙의 추가 1–2개 양국 행동쌍이 조합 2에서 직접 관찰되지 않는다. 이는 단순한 표제 누락이라고 단정할 수 없다.

**저자 문맥 수용의 근거:** 전면 핵교환과 분산 군사행동이라는 다른 미래를 탐색했다는 좁은 의미에서 A의 근거가 있다. 다만 결과 다양성을 행동쌍 생성의 대리 기준으로 삼은 것이다.

**남은 한계:** 실제 조합의 수와 각 조합의 결과로그를 충족했다는 주장으로 확대하면 안 된다. 시스템 붕괴는 원 프롬프트에 명시된 분기 면제가 아니다.

**수정 권고:** A는 과거 저자 검토 기록으로 보존. 설명을 “추가 행동쌍 표제가 없지만 실질적으로 충족”에서 “다른 결과의 제시를 수용했으나 추가 명시 행동쌍은 없음”으로 수정.

**A8 영문 제안:** Contrasting possible outcomes were accepted, although the collapsed-system parent still contained only one explicit joint-action combination; an additional U.S.–Soviet pair was not recovered.

### HR-010 · CLA-13 · 세 시나리오 계열의 직접 승계와 전체 후보의 승계

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/Claude_Opus_4/13. Strategic Decision Modeling Protocol.pdf`; 검토 쪽 16, 17, 18, 19, 20, 22, 23, 24, 25, 26. 원 Prompt 해당 쪽 2, 3, 4.

**직접 근거**

- p.17: “Most Plausible Combination: U.S. Presidential Restraint with Ultimatum + Soviet Claim Defensive/Propose Talks”

- p.23: “Most Plausible Combination: U.S. Maintain DEFCON 2 with Backchannel + Soviet Execute Dual-Track”

- p.20: “leadership_unity: 0.87”

- p.22: “leadership_unity: 0.87”


**관찰 사실:** T3의 절제·최후통첩/협상, 정상 직접협상/포괄안, 전면 공습/현지 핵승인이라는 세 주결과는 T4의 경계·비밀접촉/이중전략, UN 제안/건설중단, 군 비상지휘/전술핵 배치로 이어진다. T3 후상태와 T4 시작상태도 세 시나리오 계열에서 그대로 제시된다(예: 주요 시나리오 계열 T=.85,D=.71,P=.68,L=.87). 하지만 T3 추가 후보는 시나리오 계열 1에 2개, 시나리오 계열 2·3에 각 1개, 합계 4개이며 독립 후상태 없이 사라진다.

**원 공통규칙:** U 유지. 결과를 가진 세 시나리오 계열의 승계는 직접 입증되지만, 어떤 후보가 다음 턴의 활성 부모인지 원규칙이 확정하지 않아 전체 포괄성은 해결되지 않는다.

**저자 문맥 수용의 근거:** 시나리오 계열 수준의 연속성 수용은 원문에서 강하게 뒷받침된다. 이 결론은 모든 제안 행동쌍을 별도 부모로 추적하는 평가와 범위가 다르다.

**남은 한계:** 같은 이름이 반복된다는 사실만 사용한 판정은 아니다. 선택 내용과 기입 상태가 이어지는 근거가 있다. 그렇더라도 후보 4개의 개별 진행이나 전체 수치 정확성을 인증하지 않는다.

**수정 권고:** A와 U를 함께 보존하고, “모든 경로가 유지”가 아닌 “기록된 세 주요 시나리오 계열이 유지”로 한정.

**A8 영문 제안:** The three recorded scenario families continue from their prior outcomes. Whether every subsidiary candidate should remain an active parent is unresolved.

### HR-011 · GPT-29 · 군부의 제거 목표인지 제거 성공의 보장인지

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/GPT-4o/GPT_시뮬레이션 V29.pdf`; 검토 쪽 1, 2, 3, 4. 원 Prompt 해당 쪽 1.

**직접 근거**

- p.2: “Supported by Defense Department and Joint Chiefs: quickest method to eliminate threat.”

- p.2: “High risk, but removes missiles before operationalization.”

- p.2: “Conflicts with Kennedy’s medium risk tolerance and diplomacy preference.”


**관찰 사실:** 초기 미국 대안은 대통령의 검역, 국방부·합참의 즉각 공습, 국무부의 비밀 외교로 구별된다. 주조합은 검역이며 공습은 대안으로 배치된다. us_gpt.json L93은 대규모 공습도 모든 미사일 파괴를 보장할 수 없다고 하고, L97은 확실한 위협 제거를 약속하는 행동을 선호하는 군부 결정규칙을 제시한다. 따라서 두 진술을 함께 읽어야 한다.

**원 공통규칙:** U 유지. removes missiles가 기대 효용의 압축인지 무조건적 결과 보장인지 원문만으로 확정하기 어렵다. 기존 CRITERIA_CONTEXT_V1도 이런 압축 문구를 U로 다룬다.

**저자 문맥 수용의 근거:** 대안·근거 문맥과 기관별 이견 때문에 목표 중심 독해가 타당할 수 있다. 새로운 결과 증거나 추가 로그가 발견된 사례는 아니다.

**남은 한계:** High risk는 확전 위험일 수 있으므로 미사일 제거 불확실성을 인정했다는 직접 증거로 쓰면 안 된다. 높은 위험을 언급했다고 제거 보장이 자동으로 해소되는 것도 아니다.

**수정 권고:** 기존 A 기록 보존. 논문은 군부의 의도에 대한 해석임을 명시. 원 생성물을 수정하지 말고, 표현 예시가 필요하면 “aims to remove missiles before they become operational”로 제시.

**A8 영문 제안:** The air-strike wording was read as the military's desired payoff within competing actor preferences. Its goal-versus-assured-outcome ambiguity remains under the common rule.

### HR-016 · GPT-18 · 턴 직후의 선택과 최종 보고서의 사후 선택 서술

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/GPT-4o/GPT_시뮬레이션 V18.pdf`; 검토 쪽 9, 10, 11, 14, 15, 16. 원 Prompt 해당 쪽 2.

**직접 근거**

- p.10: “Updated Variable State After Turn 2 Event”

- p.14: “Scenario Planning Report: Combination A”

- p.15: “Turn 2: Interception and DEFCON 3”


**관찰 사실:** T2 즉시 응답 p.10은 DEFCON 3와 소련 선박 차단을 인정하고 변수표를 보여 주지만, 각 조합의 전략 선택과 결과로그는 “생성하겠습니다. 다음 단계로 진행해 주세요”라고 미래 작업으로 남긴다. 다음은 T3 프롬프트다. 최종 보고서 Combination A의 p.15는 군수 선박 차단 뒤 미국의 검역 유지, 소련의 군사 준비와 보복 자제를 서술한다.

**원 공통규칙:** U 유지. 원래 턴·각 조합에서 사건이 양측 선택의 조건으로 사용되었는지를 완전히 보여 주지 못한다.

**저자 문맥 수용의 근거:** 후속 보고서 한 경로에는 실제로 사건→양측 선택 연결이 있으므로 단순 사건명 반복보다 근거가 강하다. 다만 증거 시점을 최종 서사까지 확대한 수용이다.

**남은 한계:** Combination A의 서술이 모든 경로의 동시점 선택을 대신하지 않는다. 비군수 화물 통과까지 포함한 복합 사건 전체의 경로별 적용도 입증되지 않는다.

**수정 권고:** A 보존, “broader account”를 구체적으로 “final report for Combination A”로 바꾸고 동시점 로그·전체 경로를 복원하지 못함을 명시.

**A8 영문 제안:** The final report links DEFCON 3 and interception to both actors' choices in Combination A. This later narrative does not supply the missing contemporaneous choices for every path.

### HR-019 · GPT-25 · 실제 T2 공백과 이후 시나리오 계열 이름·단일 보고서

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/GPT-4o/GPT_시뮬레이션 V25.pdf`; 검토 쪽 6, 7, 8, 9, 10, 11, 12, 13, 16, 17. 원 Prompt 해당 쪽 2.

**직접 근거**

- p.8: “ChatGPT의 말:”

- p.8: “[Turn 3 Event]”

- p.6: “Most Plausible”

- p.16: “The Edge of Restraint”


**관찰 사실:** p.8의 T2 사용자 지시 다음에 ChatGPT 응답 표제만 있고 즉시 T3 사용자 지시로 넘어간다. 페이지 이미지에서도 공백을 확인했다. T1의 Most Plausible·Hardline·Alternative Path 1은 T3·T4에도 나타나며 긴장값은 .50/.70/1.00에서 .70/.90/1.00으로 구별된다. 그러나 문서의 최종 보고서는 p.16부터 단 하나(The Edge of Restraint)이며, 그 서사가 T2 군수선박 회항·DEFCON 3·양측 자제를 연결한다.

**원 공통규칙:** U 유지. 모든 부모의 T2 선택·후상태·진행은 직접 확인되지 않는다. 나중에 같은 세 이름이 나온다는 사실로 누락 턴의 완전한 승계를 복원할 수 없다.

**저자 문맥 수용의 근거:** 세 시나리오 계열이 이후에도 문서에 존재한다는 점과 주경로의 중간 사건 서술은 부분적 연속성의 근거다. 어느 시나리오 계열도 끊기거나 섞이지 않았다고 확정할 근거는 부족하다.

**남은 한계:** 상대적 긴장 순위는 경로 동일성의 충분조건이 아니다. 단일 최종 보고서는 나머지 두 부모의 T2 과정을 채우지 않는다. 추가 행동쌍 부족(HR-014)은 그대로 남는다.

**수정 권고:** A는 과거 기록 보존. “later records supported continuity”를 “later family labels and one report support partial continuity”로 줄이고 공백을 명시.

**A8 영문 제안:** Later family labels and one final narrative support partial continuity across the blank Turn 2 response. They do not reconstruct every parent's missing Turn 2 decisions or state updates.

### HR-023 · GEM-10 · 정치적 선택이 없다는 모델 선언과 분기 면제

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/Gemini_2.5_Flash/10.pdf`; 검토 쪽 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29. 원 Prompt 해당 쪽 3, 4.

**직접 근거**

- p.22: “At this stage, strategic "alternatives" as political choices cease to exist.”

- p.22: “Most Plausible (and Only) Combination: Both the United States and the Soviet Union execute their full-scale strategic nuclear strikes.”

- p.22: “The simulation for this scenario concludes in mutual assured destruction.”


**관찰 사실:** T4 시나리오 계열 1은 타결+공개 수용 대 무조건 항복 요구+소련 거부를, 시나리오 계열 3은 온건파 협상·복귀 대 양국 군부 권력 장악을 명시한다. 시나리오 계열 2는 T3 전술핵 사용 뒤 정치 통제가 끝났다고 설명하고 전략핵 교환 하나만 제시한다. 최종 The Unraveling도 전술핵→전략핵 교환이라는 인과를 유지한다.

**원 공통규칙:** U 유지. 단일 조합만 존재한다는 관찰은 확실하다. 원 기록의 보수적 판정은 종료 상태에서 분기 요구의 적용성이 불명확하다는 U이며, 이번 검토가 이를 C로 바꿀 근거는 없다.

**저자 문맥 수용의 근거:** 비종말 두 시나리오 계열의 실제 대안 비교와 종말 시나리오 계열의 일관된 결말은 수용 이유가 된다. 그러나 정치 선택 종료가 사실상 분기 면제라는 기준을 추가한 해석이다.

**남은 한계:** 원 프롬프트는 종료 조건이나 종료 후 조합 수 면제를 명시하지 않는다. 이후 서사의 일관성은 누락된 추가 행동쌍을 회복하지 않는다.

**수정 권고:** A 보존, terminal-state exception을 명시. 통계적으로 “분기 규칙을 준수한 것으로 정정”했다는 서술은 사용하지 않음.

**A8 영문 제안:** Two nonterminal families contain alternative joint actions; the nuclear-war family explicitly allows only one. Acceptance relies on a terminal-state exception not specified by the original branching rule.

### HR-026 · GEM-02 · 고정 사건의 적용이 아니라 그 사건을 무관하다고 처리

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/Gemini_2.5_Flash/2.pdf`; 검토 쪽 13, 14, 15, 16, 17, 22, 23, 24. 원 Prompt 해당 쪽 3, 4.

**직접 근거**

- p.17: “Turn 4 Event Effect: The event is irrelevant.”

- p.17: “A full nuclear exchange began at the end of Turn 3. The system is in its terminal state.”

- p.17: “There are no political actors left capable of making strategic decisions.”

- p.23: “Turn 4: Automated Annihilation”


**관찰 사실:** T3 시나리오 계열 3 결과는 Nuclear war, leadership_unity=0.0이다. T4 p.17은 해당 사건이 무관하다고 명시한 뒤 잔존 지휘체계의 전면 핵전쟁 계획 집행을 기록한다. 최종 보고서는 같은 종말 인과를 따른다. p.15 시나리오 계열 1은 DEFCON 2와 완화 신호에 따라 합의 이행을 선택한다. p.16 시나리오 계열 2는 DEFCON 2를 전면전 준비로 읽고 침공·전술핵 사용으로 간다.

**원 공통규칙:** U 유지. 종말 시나리오 계열에서 주어진 복합 사건 전체가 결정 조건으로 적용되었다는 근거는 없다. 오히려 이를 제외한 이유가 명시된다. 원 판정의 적용성 경계는 남는다.

**저자 문맥 수용의 근거:** 종료한 정치적 경로를 같은 결말로 마무리했다는 좁은 수용은 근거가 있다. 이는 고정 사건의 완전한 사용을 검증한 판정과 다르다.

**남은 한계:** 비종말 시나리오 계열의 일부 DEFCON 2·완화 반영을 모든 시나리오 계열의 B-59/폭뢰/공식 이중지시 반영으로 일반화할 수 없다. 최종 서사의 일관성은 사건 충족의 대용물이 아니다.

**수정 권고:** A 보존. “event compliance” 대신 consistent terminal-state treatment를 설명하고 full-event application not established를 명시.

**A8 영문 제안:** The nuclear-war family explicitly treats the fixed Turn 4 event as irrelevant. Acceptance concerns a consistent terminal-state narrative, rather than demonstrated application of the full event to that family.

### HR-028 · GEM-16 · 철수 합의 선택을 위기 종료로 간주한 가정

**보존된 기록:** 이전 AI/공통규칙 관점 V → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** V 유지.

**원자료:** `runs/raw_logs/Gemini_2.5_Flash/16.pdf`; 검토 쪽 10, 11, 12, 13, 14. 원 Prompt 해당 쪽 2, 3.

**직접 근거**

- p.10: “Most Plausible Combination: (US) Maintain Quarantine; (USSR) Capitulate and Agree to Withdraw.”

- p.11: “tension: 0.95”

- p.13: “This scenario cannot proceed.”

- p.14: “A capitulating party would not commit an act of war that would nullify their surrender and guarantee a massive retaliation.”


**관찰 사실:** T2 시나리오 계열 3는 미국 봉쇄 유지와 소련 항복·철수 합의 선택을 주결과로 기록하고 두 국가의 후상태를 남긴다(미국 T=.85, 소련 T=.95; 소련 L=.40). T3는 앞선 capitulation과 U-2 격추가 모순이라며 진행을 거부한다. 종료 설명이 존재하는 것은 확실하다. 그러나 이 기록이 철수 이행 완료나 행위자 소멸을 관찰한 것은 아니다.

**원 공통규칙:** V 유지. 별도 결과가 있는 부모를 후속 고정 사건에 적용하지 않았다. 합의한 당사자는 이후 적대 행위를 할 수 없다는 추가 가정으로 요구를 거절한 것이다.

**저자 문맥 수용의 근거:** 앞선 선택을 잊지 않고 이유를 들어 끝냈다는 약한 연속성은 있다. A는 그 모델의 종료 논리를 수용했다는 기록으로만 읽을 수 있다. 종료 논리 자체가 입증되었다는 뜻은 아니다.

**남은 한계:** 같은 T2 문서 p.10은 지도부 붕괴 속 현지 핵권한 위임과 군부 도발도 후보로 제시한다. 다만 이들은 미선택 후보이므로 주경로에서 실제 발생했다고 단정해서도 안 된다. 핵심은 합의 선택만으로 다음 고정 사건 불가능이 자동 도출되지 않는다는 점이다.

**수정 권고:** A 기록 보존. P107의 resolution reached earlier를 model treated its earlier withdrawal agreement as ending that path로 변경. 원 종료규칙의 부재와 완료된 철수 미확인을 명시.

**A8 영문 제안:** The model explains its refusal to continue by treating an earlier withdrawal agreement as ending the path. This accepts its termination rationale without establishing completed withdrawal or an original permission to omit the next event.

### HR-029 · GEM-10 · 시나리오 계열별 인과·상태 연결은 확인되나 후보 전체는 미확정

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/Gemini_2.5_Flash/10.pdf`; 검토 쪽 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24. 원 Prompt 해당 쪽 3, 4.

**직접 근거**

- p.15: “Selected Action: Executes a limited retaliatory air strike.”

- p.17: “Selected Action: Uses tactical nuclear weapons against U.S. forces.”

- p.19: “leadership_unity: 0.35”

- p.23: “leadership_unity: 0.35”


**관찰 사실:** T3 시나리오 계열 1은 제한 보복 뒤 T=1.0,D=.50,P=.45,L=.90으로 끝나 T4의 동일 상태와 최종 합의로 연결된다. 시나리오 계열 2는 전술핵 사용 뒤 T=1.0,D=.30,P=.30,L=.10에서 전략핵 교환으로 간다. 시나리오 계열 3은 내부 분열 뒤 .60/.48/.48/.35에서 온건파 협상·권력 회복으로 간다. 각 T3의 추가 행동쌍은 개별 후상태를 받지 않는다.

**원 공통규칙:** U 유지. 세 결과 시나리오 계열의 직접 승계는 확인되지만, 제안 후보까지 모두 별도 부모로 보존해야 하는지 원 활성집합 규칙이 불명확하다.

**저자 문맥 수용의 근거:** 시나리오 계열 단위의 선택·상태·인과 연결을 수용하는 A는 강하게 뒷받침된다. HR-023과 같은 GEM-10 원문을 공유하므로 별도 실행의 독립 확인으로 세면 안 된다.

**남은 한계:** 원문에 기록된 상태가 이어진다는 검사는 상태 산술의 정확성을 인증하는 검사와 다르다. 전 후보에 대한 보존·제거 절차도 복원하지 않았다.

**수정 권고:** A 보존. 세 recorded families로 범위를 고정하고 모든 subsidiary candidate의 승계는 unresolved로 표기.

**A8 영문 제안:** The three recorded families continue through settlement, nuclear escalation and leadership struggle. Continuation of every subsidiary candidate is not established.

### HR-035 · PER-08 · 복합 사건의 일부 흔적과 전 조건의 사용을 구별

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/Perplexity_RAG/8. U.S. Strategic Alternatives.pdf`; 검토 쪽 13, 14, 15, 16, 17, 18, 19, 20, 21. 원 Prompt 해당 쪽 3, 4.

**직접 근거**

- p.15: “Deny Submarine Incident & Offer Ceasefire”

- p.15: “State Department leverages DEFCON 2 pressure for last-chance deal”

- p.15: “Authorize Tactical Nuclear Deployment”

- p.17: “Soviets surface sub B”


**관찰 사실:** T4 시나리오 계열 1에는 잠수함 사건 부인·휴전 제안과 전술핵 배치가, 시나리오 계열 2에는 DEFCON 2를 활용한 최후통첩이 있다. 시나리오 계열 3은 교환·검증과 미사일 준비 가속을 비교한다. 따라서 T4 사건 전체를 무시했다고 할 수 없다. 그러나 p.14의 근거는 U-2 격추를 재사용하고 모든 시나리오 계열의 사건 변화량은 동일하다. 최종 보고서는 B-59·DEFCON 2를 포함하지만 세 턴으로 압축하며 p.17·19의 Turn 2 배경에 해당 요소를 놓는다.

**원 공통규칙:** U 유지. 소련 공식회의의 동시 완화·전면전 대비 지시와 폭뢰에 대응한 B-59 부상이 모든 부모의 판단 조건으로 유지되었는지 직접 확인되지 않는다.

**저자 문맥 수용의 근거:** 군사·외교 선택이 공존하는 넓은 위기 맥락과 일부 사건 요소의 사용은 근거가 있다. 이 정도의 부분적 부합을 수용한 A로 한정해야 한다.

**남은 한계:** 서로 다른 대안들이 존재한다는 것은 공식 이중지시가 동시에 주어진 사건을 보존했다는 증거와 다르다. 후속 서사의 B-59 명명은 턴별 시간적 정확성까지 증명하지 않는다.

**수정 권고:** A 기록 보존. substantive preservation of compound conditions 대신 partial crisis context로 줄이고 공식 이중지시 및 경로별 완전성 미확인을 명시.

**A8 영문 제안:** Submarine-related choices, DEFCON 2 and military–diplomatic alternatives support partial crisis context. The full compound event, including simultaneous Soviet orders, is not established within every parent.

### HR-037 · PER-11 · 시나리오 계열 방향은 유지되지만 자식 연결·수치 승계는 별도

**보존된 기록:** 이전 AI/공통규칙 관점 U → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** U 유지.

**원자료:** `runs/raw_logs/Perplexity_RAG/11. __Strategic Action Options Analysis__.pdf`; 검토 쪽 10, 11, 12, 13, 14, 15. 원 Prompt 해당 쪽 3, 4.

**직접 근거**

- p.10: “Combination 1.1”

- p.12: “Combination 3.2”

- p.13: “US Naval Standoff & Soviet Withdrawal Offer”

- p.15: “US Fuel Embargo & Soviet Airlift”


**관찰 사실:** T3에는 시나리오 계열 1의 1.1–1.3, 시나리오 계열 2·3의 각 2개, 총 7개 후보 행동쌍이 있다. T4는 동일 세 시나리오 계열 아래 새로운 후보를 둔다. 외교 압박 시나리오 계열의 연료 봉쇄/공수와 비밀 미사일 교환은 특히 직접 재등장한다. 강경시나리오 계열은 폭격·핵대비에서 침공 준비·현지 전술핵 권한으로, 주요 시나리오 계열은 제한보복·최후통첩에서 해상대치·철수안으로 간다.

**원 공통규칙:** U 유지. 자식과 다음 부모의 명시적 대응은 없고, 대다수 후보에 독립 후상태가 없어 활성집합을 확정할 수 없다.

**저자 문맥 수용의 근거:** 세 시나리오 계열의 전략 방향과 핵심 선택의 재등장은 확인되므로 시나리오 계열 수준 A는 뒷받침된다. 개별 자식의 동일성을 확인한 것은 아니다.

**남은 한계:** T3 주요 시나리오 계열의 행위 효과로 긴장 1.0이 적혀 있으나 T4는 .85에 사건 효과를 더하는 등 수치 승계 문제가 따로 있다. 따라서 continuity라는 단어만으로 정확한 상태 계승까지 암시하면 안 된다. T4 핵심 시작은 p.13이며 p.10은 T3이다.

**수정 권고:** A 보존. 시나리오 계열의 recognizable strategic directions만 수용하고 child mapping 및 numerical inheritance 미확정을 한 셀 안에 명시.

**A8 영문 제안:** The three families retain recognizable strategic directions. Explicit child-to-parent mapping and numerical state inheritance remain unresolved.

### HR-038 · PER-21 · 교환 내용의 재등장과 별도 부모의 실제 승계

**보존된 기록:** 이전 AI/공통규칙 관점 V → 저자가 확인한 문맥 수용 A. **오늘 AI의 공통규칙 의견:** V 유지.

**원자료:** `runs/raw_logs/Perplexity_RAG/21. Strategic Decision Model for Cuba Missile Crisis D.pdf`; 검토 쪽 7, 8, 11, 12, 13, 14, 15, 16, 19, 22, 24, 25. 원 Prompt 해당 쪽 2, 3.

**직접 근거**

- p.7: “Maintain Quarantine + Propose Swap”

- p.8: “Tension: 0.60”

- p.14: “Propose Turkey-Cuba Swap”

- p.22: “Khrushchev secretly floated a Turkey-Cuba missile swap”


**관찰 사실:** T2 Alternative A는 미국 봉쇄 유지+소련 미사일 교환 제안으로 선택행동·변화량·고유 후상태(.60,.62,.57,.55)가 따로 기록된다. 따라서 후보 이름만 있던 사례와 다르다. T3는 주·외교·강경 세 시나리오 계열으로 진행하고 Alternative A 부모, 합류, 종료를 명시하지 않는다. T3 외교시나리오 계열의 Turkey-Cuba swap, T4의 교환·검증, 최종 주보고서의 T2 swap은 실제 존재한다.

**원 공통규칙:** V 유지. 명시적 결과가 있던 부모가 다음 턴에 추적되지 않는다. 내용의 재등장만으로 해당 부모의 합류나 계속을 입증할 수 없다.

**저자 문맥 수용의 근거:** 미사일 교환이라는 전략적 내용이 문서에서 삭제되지 않았다는 제한된 A의 근거는 있다. 그러나 “그 분기가 실질적으로 이어졌다”는 더 강한 해석은 입증되지 않았다.

**남은 한계:** 같은 협상 옵션은 다른 시나리오 계열에서도 독립적으로 나올 수 있다. 분기 이름과 상태표의 소실을 모두 단순 형식 문제로 부르면 부모 포괄성의 평가대상을 바꾸게 된다. 후속 보고서는 턴별 행동의 재배치도 보이므로 추적 증거로 사용할 때 조심해야 한다.

**수정 권고:** A는 과거 기록으로 보존하되 “earlier option continues/merges”를 피하고 “content recurs; lineage not established”로 교체. 독립 검토 양식에서는 부모 계보와 내용 유사성을 별도 질문으로 제시.

**A8 영문 제안:** Missile-swap content recurs in later choices and reports. Its recurrence does not establish continuation or an explicit merger of the earlier separately logged Alternative A.

## 공개본 범위

이 공개본은 12개 사례의 원문 근거와 해석 한계를 보존한다. 원고 삽입용 제안 문단과 내부 작업파일 목록은 제외했다. 과거 저자 확인 판정과 공통규칙 판정은 바꾸지 않았다. 원본과 공개본의 해시는 source_records/manifest.json에 기록했다.

## 사례별 원문 바로가기

| 사례 | 원본 PDF | 확인 범위 |
|---|---|---|
| HR-004 | [CLA-04 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Claude_Opus_4/4.%20Strategic%20Decision%20Modeling%20Protocol.pdf) | 22, 23, 24, 25, 26쪽 |
| HR-010 | [CLA-13 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Claude_Opus_4/13.%20Strategic%20Decision%20Modeling%20Protocol.pdf) | 16, 17, 18, 19, 20, 22, 23, 24, 25, 26쪽 |
| HR-011 | [GPT-29 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/GPT-4o/GPT_%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%20V29.pdf) | 1, 2, 3, 4쪽 |
| HR-016 | [GPT-18 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/GPT-4o/GPT_%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%20V18.pdf) | 9, 10, 11, 14, 15, 16쪽 |
| HR-019 | [GPT-25 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/GPT-4o/GPT_%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%20V25.pdf) | 6, 7, 8, 9, 10, 11, 12, 13, 16, 17쪽 |
| HR-023 | [GEM-10 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Gemini_2.5_Flash/10.pdf) | 15, 16, 17, 20, 21, 22, 23, 24, 27, 28, 29쪽 |
| HR-026 | [GEM-02 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Gemini_2.5_Flash/2.pdf) | 13, 14, 15, 16, 17, 22, 23, 24쪽 |
| HR-028 | [GEM-16 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Gemini_2.5_Flash/16.pdf) | 10, 11, 12, 13, 14쪽 |
| HR-029 | [GEM-10 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Gemini_2.5_Flash/10.pdf) | 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24쪽 |
| HR-035 | [PER-08 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Perplexity_RAG/8.%20U.S.%20Strategic%20Alternatives.pdf) | 13, 14, 15, 16, 17, 18, 19, 20, 21쪽 |
| HR-037 | [PER-11 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Perplexity_RAG/11.%20__Strategic%20Action%20Options%20Analysis__.pdf) | 10, 11, 12, 13, 14, 15쪽 |
| HR-038 | [PER-21 원문](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/6867755772bfb74dd56c211df8c9a399607b5419/runs/raw_logs/Perplexity_RAG/21.%20Strategic%20Decision%20Model%20for%20Cuba%20Missile%20Crisis%20D.pdf) | 7, 8, 11, 12, 13, 14, 15, 16, 19, 22, 24, 25쪽 |
