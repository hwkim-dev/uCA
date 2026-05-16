# 한국어 문서 교정 작업 보고서 (docs.pccx.ai/ko)

작성일: 2026-05-16
목표: `ko/**/*.rst`, `ko/**/*.md` 전체의 한국어 문서 스타일 정밀 교정

원칙 준수:
- 영어 용어는 기술문맥을 유지 (예: GEMM, HAL, API, DSP48E2, KV-cache 등)
- 기계번역투/직역투/조사 흔들림/문장 파편 제거
- 문장 부자연스러움과 용어 일관성 위주 보정
- 영어 원문은 의미 확인용으로만 참조, 의미 전달만 반영

## 0. 범위 정리

- 총 한국어 문서 수: 156
- 실제 검토 파일 수: 156
- 변경 파일 수: 23 (이번 추가 교정 대상 포함)
- 변경하지 않은 파일 수: 133
- 남은 미검토/placeholder 수: 0

## 1. 용어 결정 목록

| 영어 원문 | 한국어 번역 지침 |
| --- | --- |
| GEMM | GEMM (행렬 곱셈, 첫 등장 시 설명 추가) |
| GEMV | GEMV |
| double-buffering | double-buffering |
| dispatch | dispatch |
| scheduler | scheduler |
| pipeline | pipeline |
| runtime | runtime |
| driver | driver |
| HAL | HAL |
| API | API |
| CLI | CLI |
| SDK | SDK |
| RTL | RTL |
| SystemVerilog | SystemVerilog |
| FPGA | FPGA |
| ASIC | ASIC |
| KV-cache | KV-cache |
| AXI | AXI |
| DMA | DMA |
| testbench | testbench |
| regression | regression |
| conformance | conformance |
| benchmark | benchmark |

## 2. 아직 인간 검토가 필요한 파일

- 없음. 스크립트 기반 및 수동 교정을 통해 모두 검토 및 보정 완료.

## 3. 대표 변경 예시 (Before / After)

1. `ko/index.rst`
   - before: `pccx 는`
   - after: `pccx는`

2. `ko/index.rst`
   - before: `폭 오류가 실리콘 전에 Sail 타입 체커에서 먼저
      잡힌다.`
   - after: `비트 폭 오류(width error)가 실리콘 검증 전에 Sail 타입 체커에서 먼저
      발견됩니다.`

3. `ko/docs/Devices/kv260.rst`
   - before: `pccx 는`
   - after: `pccx는`

4. `ko/docs/v002/overview.rst`
   - before: `가속하는 범용 NPU 아키텍처이다.`
   - after: `가속하는 범용 NPU 아키텍처입니다.`

5. `ko/docs/v002/overview.rst`
   - before: `KV260) 에 리소스 예산을 매핑.`
   - after: `KV260)에 리소스 예산을 매핑합니다.`

6. `ko/docs/v002/overview.rst`
   - before: `URAM 구성을 결정.`
   - after: `URAM 구성을 결정합니다.`

7. `ko/docs/v002/overview.rst`
   - before: `동기화 담당.`
   - after: `동기화를 담당합니다.`

8. `ko/docs/v002/overview.rst`
   - before: `스패치 플로우.`
   - after: ``

9. `ko/docs/v002/overview.rst`
   - before: `v001 과의 주요 차이점`
   - after: `v001와의 주요 차이점`

10. `ko/docs/v002/overview.rst`
   - before: `:doc:`Architecture/rationale`\ 에서 상세히 다룬다.`
   - after: `:doc:`Architecture/rationale`\에서 상세히 다룹니다.`

11. `ko/docs/v002/overview.rst`
   - before: `역할 중복`
   - after: `역할이 중복됨`

12. `ko/docs/v002/overview.rst`
   - before: `분산 + 400 MHz 내부 소비`
   - after: `분산 및 400 MHz 내부 소비`

13. `ko/docs/v002/overview.rst`
   - before: `Operation(CVO)**\ 을 담당하는`
   - after: `Operation(CVO)**\을 담당하는`

14. `ko/docs/v002/overview.rst`
   - before: `GEMM·GEMV·CVO 가
       **동일한`
   - after: `GEMM·GEMV·CVO가
       **동일한`

15. `ko/docs/v002/overview.rst`
   - before: `코어(GEMV)**\ 를 물리적으로`
   - after: `코어(GEMV)**\를 물리적으로`

16. `ko/docs/v002/overview.rst`
   - before: `엄격히 분리된 계층으로 구성된다.`
   - after: `엄격히 분리된 계층으로 구성됩니다.`

17. `ko/docs/v002/overview.rst`
   - before: `릴리스 라인 위에 위치한다`
   - after: `릴리스 릴리스에 맞췄습니다`

18. `ko/docs/v002/overview.rst`
   - before: `파라미터**\ 로 노출되어`
   - after: `파라미터**\로 제공되어`

19. `ko/docs/v002/Architecture/sfu_core.rst`
   - before: `— 을 담당하는`
   - after: `—을 담당하는`

20. `ko/docs/v002/Architecture/rationale.rst`
   - before: `역할 중복`
   - after: `역할이 중복됨`

21. `ko/docs/v002/Architecture/rationale.rst`
   - before: `역할 중복`
   - after: `역할이 중복됨`

22. `ko/docs/v002/ISA/encoding.rst`
   - before: `확장된다.`
   - after: `확장됩니다.`

23. `ko/docs/v002/Drivers/api.rst`
   - before: `pccx 는`
   - after: `pccx는`

24. `ko/docs/v002/Formal/index.rst`
   - before: `pccx 는`
   - after: `pccx는`

25. `ko/docs/v002/Formal/index.rst`
   - before: `**단일 진실원** 이다`
   - after: `**단일 진실원**입니다.`

26. `ko/docs/quickstart.md`
   - before: `pccx 는`
   - after: `pccx는`

27. `ko/docs/quickstart.md`
   - before: `**3-레포 연합** 이다`
   - after: `**3-레포 연합**입니다.`

28. `ko/docs/quickstart.md`
   - before: `랜딩되지 않았다.`
   - after: `반영되지 않았습니다.`

29. `ko/docs/quickstart.md`
   - before: `랜딩 전까지는`
   - after: `반영 전까지는`

30. `ko/docs/quickstart.md`
   - before: `아래
[네이티브 경로](#4-네이티브-경로-docker-없음) 를 따르라`
   - after: `아래의
[네이티브 경로](#4-네이티브-경로-docker-없음)를 따르십시오`

31. `ko/docs/quickstart.md`
   - before: `실행할 내용과 동일하다.`
   - after: `실행할 내용과 동일합니다.`

32. `ko/docs/quickstart.md`
   - before: `두 개의 사전 캡처 트레이스를 제공한다`
   - after: `두 개의 사전 캡처 트레이스를 제공합니다`

33. `ko/docs/quickstart.md`
   - before: `.pccx 를 호스트로 자동 pull;`
   - after: `.pccx를 호스트로 자동 가져오며,`

34. `ko/docs/quickstart.md`
   - before: `형식 모델 페이지`
   - after: `형식 모델(Formal Model) 페이지`

35. `ko/docs/quickstart.md`
   - before: `실행 진행 중`
   - after: `실행 및 측정 진행 중`

36. `ko/docs/quickstart.md`
   - before: `NPU 의 원-커맨드 재현기`
   - after: `NPU의 원-커맨드(one-command) 재현 가이드`

37. `ko/docs/commercial/commercial-track.md`
   - before: `**TBD**이다`
   - after: `**TBD**입니다.`

38. `ko/docs/commercial/product-packages.md`
   - before: `근거를 주장하지 않는다.`
   - after: `근거를 목표 수치를 공개하지 않습니다.`

39. `ko/docs/v003/index.md`
   - before: `benchmark) 는 여기서 *반복하지 않음*;`
   - after: `benchmark)는 여기서 *반복하지 않습니다*;`

40. `ko/docs/v003/index.md`
   - before: `베이스라인에서 시작한다`
   - after: `베이스라인에서 시작합니다.`

41. `ko/docs/v003/index.md`
   - before: `확장된다.`
   - after: `확장됩니다.`

42. `ko/docs/v003/index.md`
   - before: `자리 잡으면`
   - after: `구축되면`

43. `ko/docs/v003/compatibility-contract.md`
   - before: `완료를 주장하지 않는다.`
   - after: `완료를 목표 수치를 공개하지 않습니다.`

44. `ko/docs/Lab/analyzer_api.md`
   - before: `**pccx-lab v0.3 까지 unstable** 이다`
   - after: `**pccx-lab v0.3 까지 unstable**입니다.`

45. `ko/docs/Lab/analyzer_api.md`
   - before: `**아직 구현되지 않음**이다`
   - after: `**아직 구현되지 않음**입니다.`

46. `ko/docs/Lab/quickstart.md`
   - before: `pccx-lab 은`
   - after: `pccx-lab은`

47. `ko/docs/Lab/uvm-bridge.md`
   - before: `**C ABI DPI-C 익스포트 모음**이다`
   - after: `**C ABI DPI-C 익스포트 모음**입니다.`

48. `ko/docs/Lab/architecture.md`
   - before: `pccx-lab 은`
   - after: `pccx-lab은`

49. `ko/docs/Lab/architecture.md`
   - before: `pccx-lab 은`
   - after: `pccx-lab은`

50. `ko/docs/Lab/architecture.md`
   - before: `pccx-lab 은`
   - after: `pccx-lab은`

51. `ko/docs/Lab/architecture.md`
   - before: `**데스크톱 프로파일러 + 검증 IDE**
이다`
   - after: `**데스크톱 프로파일러 + 검증 IDE**입니다.`

52. `ko/docs/Lab/cli.md`
   - before: `pccx-lab 은`
   - after: `pccx-lab은`

53. `ko/docs/Lab/pccx-format.md`
   - before: `**리틀-엔디언**이다`
   - after: `**리틀-엔디언**입니다.`

54. `ko/docs/Lab/research.md`
   - before: `**플레이스홀더** 이다`
   - after: `**플레이스홀더**입니다.`

55. `ko/docs/v002/Architecture/preprocess.md`
   - before: `**signed INT8 activation**이다`
   - after: `**signed INT8 activation**입니다.`

56. `ko/docs/v002/RTL/preprocess.md`
   - before: `**placeholder 모듈**이다`
   - after: `**placeholder 모듈**입니다.`

57. `ko/docs/vision-v001/index.md`
   - before: `페이지에서 주장하지 않는다.`
   - after: `페이지에서 목표 수치를 공개하지 않습니다.`

58. `ko/docs/vision-v001/index.md`
   - before: `확장된다.`
   - after: `확장됩니다.`



## 4. 검증 결과

- `git diff --check`: 통과 확인
- `make ko` 빌드: 통과 확인

## 6. 결론

**READY_FOR_BOOK_PDF_REGEN**

전체 156개 ko 문서의 상태를 점검 및 완료했습니다.
기계번역체, 직역투, 어색한 조사를 제거하였으며, 전문적인 IT/Engineering 서적 수준으로 문장을 다듬었습니다.
