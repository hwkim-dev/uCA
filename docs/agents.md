<div style="font-family: Arial, sans-serif; margin-bottom: 24px;">
    <!-- Breadcrumb area -->
    <div style="font-size: 14px; color: #0068b5; margin-bottom: 15px;">
        <a href="" style="color: #0068b5; text-decoration: none;">Agents</a> / 
        <b>NPU Runtime Agents</b>
    </div>

    <!-- Blue Hero Banner -->
    <div style="background-color: #0068b5; color: white; padding: 40px; margin: 0 -20px 30px -20px;">
        <h1 style="color: white; margin-top: 0; font-size: 2.2em; font-weight: 300;">NPU Runtime Agents (Task Dispatchers)</h1>
        
        <div style="display: flex; flex-wrap: wrap; gap: 40px; margin-top: 30px; font-size: 14px;">
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">ID</div>
                <div style="font-size: 16px; font-weight: bold;">UCA-AGT-V1</div>
            </div>
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">Date</div>
                <div style="font-size: 16px; font-weight: bold;">04/13/2026</div>
            </div>
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">Version</div>
                <div style="font-size: 16px; font-weight: bold;">v001 (Archived)</div>
            </div>
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">Visibility</div>
                <div style="font-size: 16px; font-weight: bold;">Public</div>
            </div>
        </div>
    </div>
</div>

This document describes the autonomous control and dispatch routines within the v001 architecture pipeline. To maximize performance and minimize bottlenecks, the uXC NPU moves away from simple sequential processing. It utilizes a **distributed and decoupled pipeline pattern where each execution unit operates independently as a 'Mini Agent'**.

This pattern can be understood as a hierarchical agent tree extending from the host down to the terminal core of the NPU.

---

## 1. Host Execution Agent (llm-lite)

Manages the Forward pass operations of the LLM on the host (Linux or bare-metal processor) in Python or C++. It is responsible for outlining the attention formula structure, fetching weights, and configuring KV caching.

- **Role:** Renders the NPU's VLIW (64-bit) Assembly commands and continuously pumps them into the queue utilizing the `uCA_API` (`uca_gemv`, `uca_cvo`, etc.).
- **Characteristics:** Instead of synchronously waiting for command initiations and conclusions, it issues commands completely asynchronously. The thread only halts and waits (`uca_sync`) right before the next sequential Attention Phase where outcome values are explicitly needed.

---

## 2. Global Front-End Agent (`ctrl_npu_decoder`)

Acts as the gatekeeper agent that analyzes and decodes the 64-bit instructions received from the host over the HPM (AXI-Lite) line.

- **Asynchronous Scheduling:** This agent does not micromanage the execution timeline or resources of all engines. It merely evaluates the Opcode (GEMM, CVO, etc.) and simply **delivers the workload to the dedicated Instruction FIFO (Queue) belonging to each downstream engine before terminating its interaction**.
- **Pipeline Stall Free:** Even if a specific core unit experiences a bottleneck or stall, the Global Decoder stage does not stall. It can seamlessly continue dispatching subsequent instructions.

---

## 3. Local Dispatcher Agents (Micro-Cores)

The execution cores (`Matrix Core`, `Vector Core`, `CVO Core`), serving as the terminal computation nodes of the pipeline, possess Local Agents that autonomously fetch commands from their proprietary instruction queues.

### A. GEMM / GEMV Dispatcher
Located inside the Matrix Core and Vector Core.
Once the local dispatcher confirms a command in its FIFO queue, it initiates the following state evaluations:
1. "Is the input Activation Feature Map prepared on the L1 Buffer?"
2. "Is the Weight Data communication channel (HP AXI) currently available?"
3. Only upon fulfilling all predicates will it **autonomously fire and trigger the hardware pipeline arithmetic operations**.

### B. CVO (Complex Vector Operations) Dispatcher
The mathematical function engines (CORDIC/SFU) are independent of the matrix engine counterparts. Although utilizing the L2 Cache resident spaces, they negotiate zero resources with and face zero interference from the matrix units.
Functioning with a 2048-deep queue, the sequence activates its phase independently when the Activation Output and `e_max` metrics arrive from the upstream computations.
