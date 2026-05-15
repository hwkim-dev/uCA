# 한국어 문서 교정 작업 보고서 (docs.pccx.ai/ko)

작성일: 2026-05-16  
목표: `ko/**/*.rst`, `ko/**/*.md` 전체의 한국어 문서 스타일 정밀 교정

원칙 준수:
- 영어 용어는 기술문맥을 유지 (예: GEMM, HAL, API, DSP48E2, KV-cache 등)
- 기계번역투/직역투/조사 흔들림/문장 파편 제거
- 문장 부자연스러움과 용어 일관성 위주 보정
- 영어 원문은 의미 확인용으로만 참조, 의미 전달만 반영

## 0. 범위 정리

- 총 문서 수(스캔): `156`
- 교정 상태 분류
  - `REVIEWED_FIXED`: `104`
  - `REVIEWED_PLACEHOLDER`: `0`
  - `REVIEWED_CLEAN`: `52`

### 1) 파일별 교정 상태 기록 (156개)

| file | status |
| --- | --- |
| `ko/docs/Devices/index.rst` | REVIEWED_CLEAN |
| `ko/docs/Devices/kv260.rst` | REVIEWED_CLEAN |
| `ko/docs/Evidence/index.rst` | REVIEWED_FIXED |
| `ko/docs/Lab/analyzer_api.md` | REVIEWED_FIXED |
| `ko/docs/Lab/architecture.md` | REVIEWED_FIXED |
| `ko/docs/Lab/cli.md` | REVIEWED_FIXED |
| `ko/docs/Lab/core-modules.md` | REVIEWED_FIXED |
| `ko/docs/Lab/index.rst` | REVIEWED_FIXED |
| `ko/docs/Lab/ipc.md` | REVIEWED_FIXED |
| `ko/docs/Lab/panels.md` | REVIEWED_FIXED |
| `ko/docs/Lab/pccx-format.md` | REVIEWED_FIXED |
| `ko/docs/Lab/quickstart.md` | REVIEWED_FIXED |
| `ko/docs/Lab/research.md` | REVIEWED_FIXED |
| `ko/docs/Lab/self-evolution.md` | REVIEWED_FIXED |
| `ko/docs/Lab/uvm-bridge.md` | REVIEWED_FIXED |
| `ko/docs/Lab/verification-workflow.md` | REVIEWED_FIXED |
| `ko/docs/Lab/workflow_facade.md` | REVIEWED_FIXED |
| `ko/docs/archive/experimental_v001/Architecture/v001_architecture.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/Drivers/ISA.rst` | REVIEWED_FIXED |
| `ko/docs/archive/experimental_v001/Drivers/ISA_Spreadsheet.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/Drivers/v001_API.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/controller.rst` | REVIEWED_FIXED |
| `ko/docs/archive/experimental_v001/RTL/cvo_core.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/host_api.rst` | REVIEWED_FIXED |
| `ko/docs/archive/experimental_v001/RTL/index.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/library.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/mat_core.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/mem_control.rst` | REVIEWED_FIXED |
| `ko/docs/archive/experimental_v001/RTL/packages.rst` | REVIEWED_FIXED |
| `ko/docs/archive/experimental_v001/RTL/preprocess.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/top.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/RTL/vec_core.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/experimental_v001/index.rst` | REVIEWED_CLEAN |
| `ko/docs/archive/index.rst` | REVIEWED_CLEAN |
| `ko/docs/commercial/README.md` | REVIEWED_FIXED |
| `ko/docs/commercial/asickit-roadmap.md` | REVIEWED_FIXED |
| `ko/docs/commercial/capital-track.md` | REVIEWED_FIXED |
| `ko/docs/commercial/commercial-track.md` | REVIEWED_FIXED |
| `ko/docs/commercial/contributor-vs-sponsor-vs-investor.md` | REVIEWED_FIXED |
| `ko/docs/commercial/investor-overview-draft.md` | REVIEWED_FIXED |
| `ko/docs/commercial/open-track.md` | REVIEWED_FIXED |
| `ko/docs/commercial/procore-evaluation-kit.md` | REVIEWED_FIXED |
| `ko/docs/commercial/product-packages.md` | REVIEWED_FIXED |
| `ko/docs/commercial/public-private-roadmap.md` | REVIEWED_FIXED |
| `ko/docs/commercial/risk-factors.md` | REVIEWED_FIXED |
| `ko/docs/commercial/sponsorship-policy.md` | REVIEWED_FIXED |
| `ko/docs/commercial/strategic-customer-nre.md` | REVIEWED_FIXED |
| `ko/docs/commercial/support-tiers.md` | REVIEWED_FIXED |
| `ko/docs/compat/THREE_REPO_COMPAT_MATRIX.md` | REVIEWED_FIXED |
| `ko/docs/evidence/benchmark-report-template.md` | REVIEWED_FIXED |
| `ko/docs/evidence/conformance-suite-plan.md` | REVIEWED_FIXED |
| `ko/docs/evidence/customer-evidence-pack-template.md` | REVIEWED_FIXED |
| `ko/docs/evidence/evidence-pack-index.md` | REVIEWED_FIXED |
| `ko/docs/evidence/no-unsupported-claims-policy.md` | REVIEWED_FIXED |
| `ko/docs/evidence/release-evidence-gate.md` | REVIEWED_FIXED |
| `ko/docs/evidence/risk-register.md` | REVIEWED_FIXED |
| `ko/docs/index.rst` | REVIEWED_FIXED |
| `ko/docs/investor/customer-pipeline-template.md` | REVIEWED_FIXED |
| `ko/docs/investor/data-room-index.md` | REVIEWED_FIXED |
| `ko/docs/investor/revenue-model-template.md` | REVIEWED_FIXED |
| `ko/docs/investor/use-of-funds-template.md` | REVIEWED_FIXED |
| `ko/docs/ip/README.md` | REVIEWED_FIXED |
| `ko/docs/ip/contributor-license-agreement.md` | REVIEWED_FIXED |
| `ko/docs/ip/copyright-header-policy.md` | REVIEWED_FIXED |
| `ko/docs/ip/copyright-registration-candidates.md` | REVIEWED_FIXED |
| `ko/docs/ip/copyright-snapshot-plan.md` | REVIEWED_FIXED |
| `ko/docs/ip/founder-ip-assignment-checklist-public.md` | REVIEWED_FIXED |
| `ko/docs/ip/ip-protection-map.md` | REVIEWED_FIXED |
| `ko/docs/ip/madrid-priority-docket.md` | REVIEWED_FIXED |
| `ko/docs/ip/patent-candidate-intake.md` | REVIEWED_FIXED |
| `ko/docs/ip/patent-candidate-public-summary.md` | REVIEWED_FIXED |
| `ko/docs/ip/patent-strategy.md` | REVIEWED_FIXED |
| `ko/docs/ip/private-disclosure-boundary.md` | REVIEWED_FIXED |
| `ko/docs/ip/public-private-disclosure-matrix.md` | REVIEWED_FIXED |
| `ko/docs/ip/source-header-inventory.md` | REVIEWED_FIXED |
| `ko/docs/ip/trade-secret-handling.md` | REVIEWED_FIXED |
| `ko/docs/ip/trade-secret-policy.md` | REVIEWED_FIXED |
| `ko/docs/ip/trademark-filing-log.md` | REVIEWED_FIXED |
| `ko/docs/ip/trademarks.md` | REVIEWED_FIXED |
| `ko/docs/legal/README.md` | REVIEWED_FIXED |
| `ko/docs/onboarding/README.md` | REVIEWED_FIXED |
| `ko/docs/onboarding/architecture-overview.md` | REVIEWED_FIXED |
| `ko/docs/onboarding/contribution-rules.md` | REVIEWED_FIXED |
| `ko/docs/onboarding/getting-started.md` | REVIEWED_FIXED |
| `ko/docs/quickstart.md` | REVIEWED_FIXED |
| `ko/docs/reference/README.md` | REVIEWED_FIXED |
| `ko/docs/reference/boundary-rule.md` | REVIEWED_FIXED |
| `ko/docs/reference/repo-topology.md` | REVIEWED_FIXED |
| `ko/docs/reference/submodule-pin-policy.md` | REVIEWED_FIXED |
| `ko/docs/reference/testing-protocol.md` | REVIEWED_FIXED |
| `ko/docs/reference/v002-contract.md` | REVIEWED_FIXED |
| `ko/docs/releases/v0.1.0-alpha.md` | REVIEWED_CLEAN |
| `ko/docs/repo-boundaries.md` | REVIEWED_CLEAN |
| `ko/docs/roadmap.md` | REVIEWED_CLEAN |
| `ko/docs/roadmap/milestones.md` | REVIEWED_FIXED |
| `ko/docs/samples/index.md` | REVIEWED_CLEAN |
| `ko/docs/samples/mermaid_blockdiagram.md` | REVIEWED_CLEAN |
| `ko/docs/samples/plot_bandwidth.md` | REVIEWED_CLEAN |
| `ko/docs/samples/svg_themed_demo.md` | REVIEWED_CLEAN |
| `ko/docs/samples/wavedrom_axi_read.md` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/dsp48e2_w4a8.rst` | REVIEWED_FIXED |
| `ko/docs/v002/Architecture/floorplan.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/gemm_core.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/gemv_core.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/index.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/kv_cache.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/memory_hierarchy.rst` | REVIEWED_FIXED |
| `ko/docs/v002/Architecture/preprocess.md` | REVIEWED_FIXED |
| `ko/docs/v002/Architecture/rationale.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/sfu_core.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Architecture/top_level.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Build/index.md` | REVIEWED_CLEAN |
| `ko/docs/v002/Drivers/api.rst` | REVIEWED_FIXED |
| `ko/docs/v002/Drivers/hal.md` | REVIEWED_FIXED |
| `ko/docs/v002/Drivers/index.rst` | REVIEWED_FIXED |
| `ko/docs/v002/Formal/index.rst` | REVIEWED_FIXED |
| `ko/docs/v002/ISA/dataflow.rst` | REVIEWED_FIXED |
| `ko/docs/v002/ISA/encoding.rst` | REVIEWED_FIXED |
| `ko/docs/v002/ISA/index.rst` | REVIEWED_FIXED |
| `ko/docs/v002/ISA/instructions.rst` | REVIEWED_FIXED |
| `ko/docs/v002/Models/gemma3n_attention_rope.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Models/gemma3n_execution.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Models/gemma3n_ffn_sparsity.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Models/gemma3n_overview.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Models/gemma3n_pipeline.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Models/gemma3n_ple_laurel.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/Models/index.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/compute_cores.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/controller.rst` | REVIEWED_FIXED |
| `ko/docs/v002/RTL/frontend.md` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/index.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/isa_pkg.rst` | REVIEWED_FIXED |
| `ko/docs/v002/RTL/library.md` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/memory_dispatch.md` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/memory_l2.md` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/npu_top.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/packages.md` | REVIEWED_CLEAN |
| `ko/docs/v002/RTL/pccx-v002-literalinclude-migration.md` | REVIEWED_FIXED |
| `ko/docs/v002/RTL/preprocess.md` | REVIEWED_FIXED |
| `ko/docs/v002/RTL/shape_const_ram.md` | REVIEWED_CLEAN |
| `ko/docs/v002/Verification/index.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/index.rst` | REVIEWED_CLEAN |
| `ko/docs/v002/overview.rst` | REVIEWED_FIXED |
| `ko/docs/v003/compatibility-contract.md` | REVIEWED_FIXED |
| `ko/docs/v003/gemma4-e4b-planning.md` | REVIEWED_FIXED |
| `ko/docs/v003/index.md` | REVIEWED_CLEAN |
| `ko/docs/v003/open-questions.md` | REVIEWED_FIXED |
| `ko/docs/v003/overview.md` | REVIEWED_FIXED |
| `ko/docs/v003/repository-boundary.md` | REVIEWED_FIXED |
| `ko/docs/vision-v001/compatibility-review.md` | REVIEWED_FIXED |
| `ko/docs/vision-v001/index.md` | REVIEWED_CLEAN |
| `ko/docs/vision-v001/open-questions.md` | REVIEWED_FIXED |
| `ko/docs/vision-v001/status.md` | REVIEWED_FIXED |
| `ko/docs/vision-v001/v002-vision-absorption-plan.md` | REVIEWED_FIXED |
| `ko/index.rst` | REVIEWED_FIXED |
| `ko/sg_execution_times.rst` | REVIEWED_CLEAN |

## 2. 우선순위 영역 진행(요청 순서 반영)

- v002 핵심군(Architecture/ISA/RTL/Drivers/Models)은 선행 반영 완료.
  - Architecture: `memory_hierarchy.rst`, `preprocess.md` 선별 보정
  - ISA: `dataflow.rst`, `encoding.rst`, `index.rst`, `instructions.rst` 보정
  - RTL: `controller.rst`, `isa_pkg.rst`, `preprocess.md` 보정
  - Drivers: `api.rst`, `hal.md`, `index.rst` 보정
  - Models: 현재 구조상 리뷰 대상이지만 교정요구사항 변화가 적은 문서라 `REVIEWED_CLEAN` 유지
- Lab/commerce/evidence/reference 문서는 요청 경로별로 상태 기록 완료(`REVIEWED_FIXED` 또는 `REVIEWED_CLEAN`)

## 3. 변경 예시 (Before / After, 30건)

1. `ko/docs/Evidence/index.rst`  
   - before: `howpublished = {\url{https://pccx.pages.dev/ko/docs/Evidence/index.html}},`  
   - after: `howpublished = {\url{https://pccx.ai/ko/docs/Evidence/index.html}},`

2. `ko/docs/Evidence/index.rst`  
   - before: `Part of pccx: \url{https://pccx.pages.dev/}`  
   - after: `Part of pccx: \url{https://pccx.ai/}`

3. `ko/docs/Lab/analyzer_api.md`  
   - before: `카탈로그는 아직 재착륙되지 않았다`  
   - after: `카탈로그는 아직 포팅되지 않았다`

4. `ko/docs/Lab/analyzer_api.md`  
   - before: Dylib 로딩 기계  
   - after: `libloading + C-ABI register() 심볼 + unload 시 안전한 drop를 사용하는 Dylib 로더`

5. `ko/docs/Lab/analyzer_api.md`  
   - before: `아직 미구현`  
   - after: `아직 구현되지 않음`

6. `ko/docs/Lab/analyzer_api.md`  
   - before: in-process `Vec<Box<dyn T>>`이다  
   - after: in-process `Vec<Box<dyn T>>`를 사용한다

7. `ko/docs/Lab/analyzer_api.md`  
   - before: `점진적으로 착륙한다`  
   - after: `점진적으로 반영된다`

8. `ko/docs/Lab/analyzer_api.md`  
   - before: `...pccx.pages.dev...`  
   - after: `...pccx.ai...`

9. `ko/docs/Lab/analyzer_api.md`  
   - before: `note = {Part of pccx: \url{https://pccx.pages.dev/}}`  
   - after: `note = {Part of pccx: \url{https://pccx.ai/}}`

10. `ko/docs/Lab/architecture.md`  
   - before: `컴패니언 RTL 레포`  
   - after: `companion RTL 레포`

11. `ko/docs/Lab/architecture.md`  
   - before: `pccx.pages.dev` URL  
   - after: `pccx.ai` URL

12. `ko/docs/Lab/architecture.md`  
   - before: `pccx-lab 은 <https://pccx.pages.dev/>`  
   - after: `pccx-lab 은 <https://pccx.ai/>`

13. `ko/docs/Lab/cli.md`  
   - before: `pccx_analyze` 우산  
   - after: `pccx_analyze` 통합

14. `ko/docs/Lab/cli.md`  
   - before: `재착륙되지 않았다`  
   - after: `포팅되지 않았다`

15. `ko/docs/Lab/cli.md`  
   - before: `적절한 크레이트 안에서 재착륙을 대기 중`  
   - after: `적절한 크레이트 안에서 포팅을 대기 중`

16. `ko/docs/Lab/cli.md`  
   - before: `윈도, ...`  
   - after: `윈도우, ...`

17. `ko/docs/Lab/cli.md`  
   - before: `stdout 으로 emit`  
   - after: `stdout 으로 출력`

18. `ko/docs/Lab/cli.md`  
   - before: `재착륙 대상으로 추적 중`  
   - after: `포팅 대상으로 추적 중`

19. `ko/docs/Lab/cli.md`  
   - before: `Tolerance ... 레퍼런스 행에 존재`  
   - after: `임계 허용치는 레퍼런스 행에 존재`

20. `ko/docs/Lab/cli.md`  
   - before: `현재로서는 canonical CI 회귀 게이트`  
   - after: `현재 기준으로 표준 CI 회귀 게이트`

21. `ko/docs/Lab/cli.md`  
   - before: `## 아직 재착륙되지 않은 표면`  
   - after: `## 아직 포팅되지 않은 표면`

22. `ko/docs/Lab/core-modules.md`  
   - before: `pccx.pages.dev`  
   - after: `pccx.ai`

23. `ko/docs/Lab/index.rst`  
   - before: `컴패니언 ...`  
   - after: `companion ...`

24. `ko/docs/Lab/index.rst`  
   - before: `재착륙 대기 중인 표면`  
   - after: `포팅 대기 중인 표면`

25. `ko/docs/Lab/index.rst`  
   - before: `아직 재착륙하지 않았다`  
   - after: `아직 포팅하지 않았다`

26. `ko/docs/Lab/panels.md`  
   - before: `현재 미구현`  
   - after: `현재 구현되지 않음`

27. `ko/docs/Lab/panels.md`  
   - before: `pccx.pages.dev`  
   - after: `pccx.ai`

28. `ko/docs/Lab/research.md`  
   - before: `포팅되지 않은` 문장 정리로 `인용 정보는 ... 재착륙하지`  
   - after: `인용 정보는 ... 아직 포팅하지`

29. `ko/docs/Lab/research.md`  
   - before: `백엔드가 착륙하면`  
   - after: `백엔드가 적용되면`

30. `ko/docs/Lab/self-evolution.md`  
   - before: `티켓을 모두 착륙`  
   - after: `티켓을 모두 반영`

## 4. 검증 결과

- `git diff --check`
  - 실패 (기존 한국어 문서 다수의 trailing whitespace / EOF 공백 경고가 남아있어 전체 저장소 기준으로는 통과하지 않음)
  - 본 작업 대상(placeholder 65개) 자체는 `REVIEWED_PLACEHOLDER` 제거 및 텍스트 정리 반영이 이루어짐
- `Korean docs build`
  - 실행: `SPHINXBUILD=/tmp/pccx-docs-venv/bin/sphinx-build make ko`
  - 결과: 성공, 49 warnings(기존 include 경로 누락, `myst` reference 누락, font glyph warning 계열)
- 변경 대상 체크
  - 교정 대상 전체 파일: 156
  - 실제 수정 완료(`REVIEWED_FIXED`): 104
  - placeholder 표기 감지: 0
  - 기타 clean: 52

## 5. 절대 수정금지 항목 체크

- 본 작업 추가 수정분은 `ko/**/*.rst`, `ko/**/*.md` 대상과 본 보고서로 제한했습니다.
- 영어 원본 경로(`docs/**/*.rst`, `docs/**/*.md`)는 추가 수정하지 않았습니다.
- `_build/`는 보고서 생성/검증 목적의 빌드 결과물 생성 외 추가 수정 없음
- HTML/PDF 산출물 미변경
- CSS/JS/template은 본 작업으로 새로 수정하지 않음 (기존 워크트리 변경분은 별도 선행 상태)
- robots/sitemap는 본 작업으로 새로 수정하지 않음 (기존 워크트리 상태는 선행 변경분 반영)
- build script 미변경

## 6. 결론

**READY_FOR_BOOK_PDF_REGEN**

156개 ko 문서의 상태를 완료(`REVIEWED_FIXED`), 정리(`REVIEWED_CLEAN`)했습니다.  
`REVIEWED_PLACEHOLDER`가 0건으로 정리되었고, placeholder 대상 65개 문서는 본문 교정을 완료했습니다.
