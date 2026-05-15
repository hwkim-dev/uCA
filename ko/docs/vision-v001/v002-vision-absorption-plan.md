---
orphan: true
---

# Absorption plan — vision-v001 → `pccx-v002/Vision/`

> Draft / planning / evidence-gated.
> 현재 vision RTL이 아직 커밋되지 않아 계획 템플릿이 중심이다.

## 선조건

흡수는 아래 조건이 모두 충족될 때만 정당화된다.

1. `pccx-vision-v001`(또는 private staging workspace)에 vision RTL이 존재하고
   v002 LLM substrate 수준의 성숙도를 보일 것.
2. vision RTL이 `pccx-v002/common/rtl/packages/`,
   `pccx-v002/common/rtl/interfaces/`,
   `pccx-v002/common/rtl/wrappers/`와 충돌 없이 공존할 것.
3. vision 쪽 ISA, register ABI, control bus가 v002 contract와 호환되거나,
   한 contract에서 처리 가능한 수준으로만 divergence 할 것.
4. to-be-absorbed RTL 경로에 `kv260`, `kria`, `gemma` 등 model/board 모델명이 노출되지 않을 것.

조건이 하나라도 깨지면 standalone로 유지하고 대상은 `pccx-v003/Vision/`
또는 `pccx-vision-vNNN`로 이동한다.

## 전환 절차(조건 충족 시)

1. **Inventory**: `pccx-vision-v001`의 파일을 전부 수집해 IP-core / spec / model-specific로 분류.
2. **Dependency audit**: `common/rtl`에서 공유 모듈과 vision-only 모듈을 분리.
3. **Boundary review**: RTL 경로 내 모델·보드 토큰 유입 여부를 최종 점검.
4. **Branching**: `pccx-v002`에 `Vision/rtl`, `Vision/sim`, `Vision/tb`, `Vision/formal` 생성 및 반영.
5. **Source manifest 갱신**: `pccx-v002/SOURCE_MANIFEST.md`에 경로 mapping 추가.
6. **Contract 확장**: `compatibility/v002-contract.yaml`에 vision 관련 필드
   (입력 포맷, 가중치 형식 차등 여부, control bus revision 등) 반영.
7. **검증**: 기존 Sail typecheck, 시뮬레이션 wrapper(vision testbench 확장), fresh-clone reachability 검증 실행.
8. **pin 갱신**: 흡수된 SHA를 소비자 저장소로 배포.

## 이 계획이 아닌 것

- 구현 일정표가 아니다.
- 미리 흡수 결정이 확정된 문서는 아니다.
- vision RTL이 오늘 존재한다는 뜻은 아니다.

## tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)
