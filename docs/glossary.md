# Glossary

This page defines project terms as they are used in the pccx public
documentation. It is intentionally conservative: planned work, throughput
targets, and board measurements are labelled as such.

## Project And Release Lines

pccx
: Parallel Compute Core eXecutor. A hardware-software co-design project for
  NPU architectures targeting edge inference workloads.

v001
: Archived experimental pccx architecture line. It remains in the docs as
  historical context and should not be treated as the active RTL target.

v002
: Active KV260 LLM architecture line. In this docs site, `v002` usually means
  the public architecture, ISA, driver, RTL-reference, and verification pages
  for the current `pccx-FPGA-NPU-LLM-kv260` line.

v002.0
: Baseline v002 integration line on KV260. Throughput language for this line is
  measured-only until release evidence is published.

v002.1
: Planned continuation of v002 on the same RTL repository. The roadmap scopes
  sparsity and speculative-decoding work to this line. The 20 tok/s number is a
  target for this line, not a reported board result.

v003.x
: Planned LLM continuation in a separate RTL repository. Public documentation
  treats v003 as a future line until its repository and release branches are
  stabilized.

vision-v001
: Parallel CNN inference track that reuses the KV260 substrate but targets
  vision workloads rather than autoregressive LLM decoding.

pccx-lab
: Companion verification and profiling environment for pccx traces, reports,
  and workflow automation. Public claims derived from lab output still need the
  release evidence gates described in the roadmap.

pccx-llm-launcher
: Companion launcher repository for model preparation, runtime contracts, and
  KV260-facing orchestration. Current public launcher pages describe scaffold,
  mock, and contract surfaces unless they cite board evidence.

## Hardware Target

KV260
: Xilinx Kria KV260 Starter Kit, based on the Zynq UltraScale+ ZU5EV device.
  It is the primary board target for v002 public documentation.

`kv260`
: Lowercase slug used in repository names, branch names, build directories, or
  scripts when a filesystem-safe target identifier is needed.

Zynq UltraScale+
: AMD/Xilinx SoC family that combines a Processing System and Programmable
  Logic fabric. The KV260 target uses a ZU5EV part.

PS
: Processing System. The Arm-based host side of the Zynq device.

PL
: Programmable Logic. The FPGA fabric side where the pccx NPU RTL is
  implemented.

AXI
: Arm AMBA interconnect protocol family used for host, memory, and streaming
  interfaces in the design.

AXI-HP
: High-Performance AXI ports from the PS to PL. In v002 documentation these
  ports are used for high-bandwidth weight traffic into the NPU.

ACP
: Accelerator Coherency Port. In pccx docs, ACP refers to the coherent path
  used for activation/result traffic between host memory and the accelerator.

DSP48E2
: Xilinx DSP slice available in UltraScale+ devices. pccx v002 uses DSP48E2
  packing for the W4A8 GEMM datapath.

BRAM
: Block RAM in the FPGA fabric. pccx uses BRAM for smaller local buffers and
  per-core storage structures.

URAM
: UltraRAM in the FPGA fabric. pccx v002 uses URAM for the shared L2 cache and
  weight buffering structures described in the architecture docs.

CDC
: Clock-domain crossing. Used where data moves between the AXI/control clock
  domain and the core compute clock domain.

Vivado block design
: Xilinx Vivado IP-integrator design graph. In the v002.1 docs, a block-design
  scaffold is build setup material, not proof that implementation or timing has
  completed.

bitstream
: FPGA configuration artifact produced after synthesis and implementation.
  Public pccx docs should call a bitstream deployable only when the matching
  evidence page or release checklist links the build, timing, and board
  artefacts.

SD staging
: Packaging step that prepares files for booting or testing the KV260 from SD
  media. It is a deploy-preparation step and does not by itself establish a
  hardware run.

## Data Types And Numeric Formats

W4A8
: Weight-4, Activation-8 quantization. In pccx v002 this means INT4 weights
  multiplied by INT8 activations on the main integer compute path.

W4A8KV4
: Shorthand used for an evidence-gated Gemma 3N E4B target configuration:
  W4A8 compute with 4-bit KV-cache storage. Treat it as a target configuration
  label unless a page cites measured evidence.

INT4
: Signed 4-bit integer value, used for quantized weights in the W4A8 path.

INT8
: Signed 8-bit integer value, used for quantized activations in the W4A8 path.

BF16
: Brain floating point format with an 8-bit exponent and 7-bit mantissa. pccx
  docs use BF16 for activation, KV-cache, or SFU paths where integer-only
  arithmetic is not the intended representation.

FP32
: IEEE single-precision floating point. Public docs mention FP32 only where the
  operation needs a higher-precision software or SFU-side representation.

Precision promotion
: Conversion from the integer compute path to BF16 or FP32 for non-linear or
  numerically sensitive operations such as softmax, RMSNorm, GELU, and RoPE.

Sign recovery
: The correction step used when signed low-bit operands are packed into a
  wider multiply datapath. In pccx docs the term is tied to W4A8 DSP packing,
  not to model-level accuracy claims.

Activation quantization
: Policy for converting activation values into the representation consumed by
  the integer datapath. The v002.1 decision page names the default policy but
  does not claim final model accuracy.

`e_max`
: Maximum-exponent summary used by the v002.1 activation-scale policy. Public
  docs describe it as a scale-selection mechanism, not as measured accuracy or
  throughput evidence.

BFP
: Block floating point. In the v002.1 activation policy, BFP refers to a shared
  power-of-two activation scale for a block of values.

symmetric INT8
: Reviewed activation-scale mode that uses symmetric signed INT8 quantization.
  The design-decision page keeps it as a mode under review rather than the
  v002.1 default.

constant-cache scale
: Driver-provided activation-scale table or constant path. It remains a
  reviewed mode until the hardware/software interface and tests make it the
  chosen default.

`ACT_SCALE_POLICY`
: Public parameter handle for the v002.1 activation scaling policy.

`ACT_SCALE_EMAX_BFP`
: Default v002.1 activation-scale mode named by the design-decision page:
  `e_max` plus BFP power-of-two scaling.

## Compute Blocks

GEMM
: General Matrix-Matrix Multiply. In v002 it is the matrix core used mainly for
  prefill and other matrix-heavy work. The architecture docs describe a 32 x 32
  systolic array for the KV260 configuration.

GEMV
: General Matrix-Vector Multiply. In v002 it is the vector core used for
  decode-dominant work where a new token repeatedly multiplies an activation
  vector by streamed weights.

CVO
: Complex Vector Op. ISA opcode family for non-linear vector operations and
  reductions that execute on the SFU path.

SFU
: Special Function Unit. The backend that executes CVO operations such as exp,
  sqrt, GELU, sin/cos, reduce-sum, scale, and reciprocal.

PE
: Processing Element. A compute cell in the systolic array or related datapath.

Systolic array
: Regular grid of PEs that moves operands through a fixed pattern. In pccx v002
  public docs, this term usually refers to the GEMM array.

Weight Stationary
: GEMM dataflow where a weight tile is loaded into the array and reused across
  many activation steps.

Weight Streaming
: GEMV dataflow where weights stream through the vector datapath because each
  weight is used once for the current token step.

LUT
: Lookup table. In the FPGA sense, LUTs are logic resources. In the algorithmic
  sense, pccx docs also use lookup tables for some dequantization or SFU helper
  paths; read the local context.

CORDIC
: Iterative coordinate-rotation method used for selected transcendental
  functions. pccx docs mention CORDIC as part of the SFU implementation path.

K-split
: Division of the reduction dimension into chunks. v002.1 docs discuss it with
  drain cadence and accumulator bounds, not as a completed scheduler claim.

drain cadence
: Frequency at which partial accumulators are drained from a K-split path.
  The current v002.1 default is parameterized rather than hardwired into a
  public performance claim.

`K_DRAIN_LIMIT`
: Public parameter handle for the v002.1 K-split accumulator drain limit. The
  documented default is `1024`.

DSP accounting baseline
: Convention for reporting intended compute-core DSP usage separately from
  implementation extras. Actual utilization still comes from synthesis reports.

`DSP_BASELINE_GEMM`
: GEMM compute-core DSP baseline parameter. The v002.1 decision page sets it
  to `1024` for the 32 x 32 PE grid.

`DSP_BASELINE_GEMV`
: GEMV compute-core DSP baseline parameter. The v002.1 decision page sets it
  to `64` for four 16-DSP vector lanes.

`DSP_BASELINE_ALPHA`
: Accounting bucket for implementation extras outside the GEMM/GEMV baseline.

## ISA And Runtime Terms

ISA
: Instruction Set Architecture. pccx v002 uses a custom fixed-width 64-bit ISA
  for compute, memory, and CVO instructions.

VLIW
: Very Long Instruction Word. In pccx docs this describes the fixed-width
  instruction format and explicit fields used by the NPU dispatcher.

opcode
: Operation-code field in an instruction. The v002 ISA pages are the source of
  truth for opcode values and instruction field layouts.

GEMM instruction
: v002 ISA compute instruction that dispatches matrix-matrix work to the GEMM
  backend.

GEMV instruction
: v002 ISA compute instruction that dispatches matrix-vector work to the GEMV
  backend.

MEMCPY instruction
: v002 ISA memory movement instruction. See the ISA reference for supported
  source and destination paths.

MEMSET instruction
: v002 ISA instruction used to write shape or constant-table state rather than
  to run arithmetic.

CVO instruction
: v002 ISA instruction that dispatches an SFU function over a vector or
  reduction operand.

HAL
: Hardware Abstraction Layer. The C/C++ driver layer that wraps register,
  memory, and instruction-dispatch details for host software.

Sail
: ISA-specification language used by the pccx formal model. In pccx docs, Sail
  models are used to check instruction semantics and field widths against the
  intended ISA structure.

launcher contract
: Data-only interface between the planned KV260 runtime path and launcher
  software. A contract page describes shapes and guardrails; it is not board
  execution evidence.

readiness scaffold
: Typed placeholder or adapter surface that makes a future hardware path
  reviewable before device access is implemented.

AXI command/status shapes
: Launcher-side data structures for command and status exchange over the
  future KV260 boundary. Shape validation is contract evidence, not a live
  MMIO run.

result streaming
: Runtime path for returning generated tokens or accelerator results. Public
  docs should distinguish mock streams, serial test framing, and captured board
  streams.

serial TTY
: Character-device path used by launcher or lab tooling to exchange framed
  records with a connected target. Tests that skip without a device are not
  board evidence.

TraceStream
: pccx-lab iterator contract for trace records. File replay and serial TTY
  sources can share this surface while still having different evidence status.

`KVFPGA_TTY`
: Environment or configuration path naming the serial device used by the KV260
  trace source.

newline JSON framing
: Trace framing style where one JSON payload is carried per line between
  begin/end markers.

CRC
: Cyclic redundancy check. In pccx-lab trace framing docs it is used to detect
  corrupted payloads; skipped bad frames should not be counted as valid
  hardware evidence.

sequence gap
: Missing trace-frame sequence number reported by the lab pipeline. It is a
  diagnostic signal that the captured stream may be incomplete.

## Memory And Model Terms

L1
: Local per-core memory or buffer close to a compute backend.

L2
: Shared on-chip cache in the v002 architecture. It is backed by URAM and is
  shared by GEMM, GEMV, SFU, and memory-dispatch paths.

Weight Buffer
: On-chip FIFO/buffer path for model weights arriving from external memory.
  GEMM uses it for weight preload/reuse; GEMV uses it for streaming.

KV cache
: Attention key/value storage retained across autoregressive decoding steps.
  pccx docs distinguish KV-cache design targets from measured board capacity
  or throughput claims.

Attention Sink
: KV-cache policy term for retaining the first tokens of a prompt while using a
  sliding local window for recent tokens.

Local Window
: KV-cache policy term for the recent-token region retained during long-context
  decoding.

RoPE
: Rotary Position Embedding. pccx maps RoPE-related sine and cosine work to CVO
  operations in the SFU path.

RMSNorm
: Root Mean Square Layer Normalization. In pccx docs this is one of the
  non-linear or reduction-heavy operations associated with the SFU path.

Softmax
: Normalization used in attention. pccx docs map its exponential, reduction,
  reciprocal, and scale steps to CVO/SFU operations.

GELU
: Gaussian Error Linear Unit activation. pccx docs map GELU to the CVO/SFU
  path.

Gemma 3N E4B
: Target LLM family named in the v002 public docs. Claims about token rate or
  board execution remain evidence-gated unless the page cites published
  verification data.

GemmaArchSpec
: Launcher-side configuration object for Gemma shape metadata and packed-size
  checks. It is a spec-validation surface, not a model execution claim.

W4 prep
: Launcher-side preparation of signed W4 packed weights and related metadata.
  Current docs treat it as a software contract until hardware handoff evidence
  lands.

manifest metadata
: Structured metadata that records prepared weight shapes, scales, packed
  sizes, or related handoff fields for the launcher path.

tokenizer contract
: Offline tokenizer interface used by the launcher scaffold. Placeholder
  fixtures do not claim real Gemma tokenizer assets.

token streaming
: Movement of prompt or generated-token data across a runtime boundary. In the
  current software-path docs, serial and mock streaming are scaffold evidence
  until board captures are published.

marker-wrapped chunks
: Token-transport records delimited by explicit markers, sometimes with length
  prefixes. They define framing behavior rather than hardware throughput.

mock orchestration
: End-to-end software path that joins prompt encode, W4 prep, mock command
  polling, output receive, and decode without a real board run.

AltUp
: Gemma-specific multi-stream state item named in v002.1 FAQ material. Its
  effect on throughput or memory pressure still needs measured evidence before
  public claims.

LAuReL
: Gemma-specific mechanism named in model and FAQ pages. Public docs may
  describe the mapping, but speedup or accuracy claims need evidence.

PLE
: Per-Layer Embedding mechanism referenced by Gemma model docs. Treat
  PLE-related scheduling text as design mapping unless an evidence page links a
  measurement.

grouped-query attention
: Attention variant that shares key/value projections across query groups.
  pccx docs discuss it as part of the Gemma mapping and KV-cache traffic
  budget.

cross-layer KV sharing
: Gemma-specific KV reuse pattern that affects cache residency and traffic.
  Public docs should keep it separate from measured throughput claims.

EAGLE-3
: Speculative-decoding technique named in the v002.1 roadmap scope. In this
  repo it is planned work, not a completed v002.0 feature.

SSD
: Speculative-decoding roadmap item in the v002.1 scope. Expand or redefine
  the acronym at the point of use when adding detailed public documentation.

J Tree
: Roadmap shorthand associated with the v002.1 speculative-decoding stack.
  Treat it as planned scope until a design page defines and verifies it.

G sparsity
: Roadmap lane for v002.1 sparsity work. It should be described as ramp scope
  until implementation and evidence pages say more.

H/H+
: Roadmap shorthand for EAGLE-3 speculative-decoding phases in the v002.1
  ramp.

I SSD
: Roadmap shorthand for the SSD phase in the v002.1 ramp.

K benchmark
: Roadmap shorthand for benchmark/evidence work after the v002.1 mechanism
  lanes. Benchmarks become public claims only through the evidence gates.

## Metrics And Evidence

tok/s
: Tokens per second. pccx uses this as the primary user-visible decoding
  throughput unit.

TT
: Throughput target. This is planning shorthand for a target token rate, not a
  measurement. Public pages should prefer spelling out "throughput target" on
  first use.

measured-only
: Documentation posture for the v002.0 release line: do not quote throughput,
  timing closure, or board-run claims until the evidence checklist admits those
  measurements.

bring-up
: Hardware integration phase where the bitstream, board setup, host driver,
  and smoke tests are made to run together. Bring-up logs are evidence inputs,
  not automatically release claims.

release evidence
: Checklist-gated artifacts used to decide whether timing, throughput, or
  board-execution statements are allowed in public docs.

evidence inventory
: Public list of measured, reproducible artefacts and pending gates. It is the
  place to check whether a value is measured, pending, or only a target.

claim guard
: Review rule or scan that prevents public docs from turning targets,
  scaffolds, mocks, or pending gates into completed hardware claims.

pre-flight
: Preparatory state for build, launcher, or deploy work before the full command
  sequence has been run and evidence has been captured.

smoke capture
: Small board or tool run used to collect initial logs. It can support bring-up
  evidence, but it does not replace release evidence for timing or throughput.

timing report
: Vivado report used to justify timing wording. A docs page should not claim
  timing closure without a linked report or release evidence entry.

utilization report
: Vivado report used to justify FPGA resource wording such as DSP, LUT, BRAM,
  or URAM counts.

throughput target
: Planned token-rate goal. It must remain distinct from measured throughput in
  public wording.

board run
: Execution against a connected KV260 or other named target board. Mock tests,
  type checks, and local software orchestration are not board runs.

trace replay
: Analysis of an existing `.pccx` trace file through pccx-lab tooling. Replay
  can validate analysis paths without proving new hardware execution.

## Documentation And Release Terms

spec resolution
: Reader step that separates architecture intent, model mapping, ISA source of
  truth, and measured evidence before quoting a claim.

runbook
: Step-by-step command record for a build, local docs check, deploy, or
  hardware procedure. A runbook is procedure evidence only after the commands
  and results are captured.

deploy runbook
: Documentation path for publishing the Sphinx site through GitHub Pages. A
  deploy check proves publication, not hardware performance.

release status
: Label such as draft, prerelease, latest release, or archived release used by
  release notes. It should not be overloaded with hardware readiness.

pre-release
: GitHub Release state for work that is published before being treated as a
  final release.

validation status
: Release-note field that records which checks passed, failed, or were not run.
  It should name commands or CI runs where useful.

known limitations
: Release-note section for caveats, missing evidence, or deferred capability.

release checklist
: Maintainer checklist for release hygiene. For pccx ISA PDF changes, the
  checklist includes rebuilding the PDF from `main.tex`.

GitHub Pages deploy
: Publication workflow for the documentation site. Passing deploy does not
  convert a target, mock, or pending gate into measured evidence.

contributors acknowledgement
: Public recognition of people who contribute documentation, reviews, bug
  reports, diagrams, examples, or related code after maintainers accept the
  entry for publication.

news section
: Placeholder area for future project updates, release announcements, and
  community news. It should not carry release claims without the same evidence
  gates as the rest of the docs.
