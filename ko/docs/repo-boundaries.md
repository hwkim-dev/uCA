# 저장소 경계

모델과 보드는 IP 코어를 소비한다. IP 코어는 `rtl/` 또는
`compatibility/` 안에서 특정 모델 이름이나 보드 이름을 절대 참조하지
않는다.

## 저장소 역할

| 저장소 | 역할 |
| --- | --- |
| `pccx` | 정본 사양, 문서, 프로젝트 인덱스. |
| `pccx-v002` | v002 IP 코어 패키지 — LLM, Vision, Voice, 공용 재사용 소스. |
| `pccx-v003` | 향후 v003 IP 코어 패키지. |
| `pccx-FPGA-NPU-LLM-kv260` | KV260 + LLM 애플리케이션 통합. `pccx-v002`를 소비한다. |

## 배치 규칙

| 내용 | 소유자 |
| --- | --- |
| 아키텍처 계약, 레지스터 맵, 메모리 맵, 최상위 인터페이스 | 버전화된 IP 코어 패키지. 여기에는 문서화 목적으로 미러링한다. |
| 재사용 가능한 RTL, 패키지, 인터페이스, 래퍼, 테스트벤치, formal 하니스 | `pccx-v00N` IP 코어 패키지. |
| 보드 제약, Vivado 프로젝트 파일, 보드 최상위 래퍼, PS/PL 연결 | 보드 통합 저장소. |
| 모델 매니페스트, 애플리케이션 런타임 코드, 드라이버 HAL, 보드 동작 증거 | 애플리케이션 통합 저장소. |

## 네이밍 레드 플래그

다음 이름들은 IP 코어의 `rtl/` 또는 `compatibility/` 경로 안에서
허용되지 않는다. 단, 소비자(consumer)를 명확히 설명하는 README 또는
compatibility 문서는 예외다.

```text
gemma  gemma3n  gemma4  llama  qwen  mistral  e4b
kv260  kria  zcu104  alveo  versal
```
