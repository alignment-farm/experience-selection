# Primary methods and implementation provenance

Read 14 September 2026; versioned HTML cached locally with SHA256 in retrieval.json.
No novelty claim and no author code from these four papers reused.

- [aTTT 2607.03441v1](https://arxiv.org/html/2607.03441v1), §3.1–3.3 and §4.5: Self/Env/Summary supply different next-token update data; repetition filtering requires an update-count control. Here labels and self answers use a matched answer-only CE objective; this is not a reproduction of trajectory-token aTTT.
- [Self-Guided TTT 2607.09415v1](https://arxiv.org/html/2607.09415v1), §2 and Algorithm 1: question-conditioned span selection; generation retains full context. Our checked-example context reference likewise retains the accessible teaching evidence. No question-guided span selection tested.
- [VANE 2608.09448v2](https://arxiv.org/html/2608.09448v2), §3.3–3.4: shadow proposal followed by later proxy validation; live parameters and optimizer are restored before deployment. This motivates separating candidate fitting from useful behavior, but our checked labels are stronger information than VANE's future visual proxy.
- [SEAL 2506.10943v2](https://arxiv.org/html/2506.10943v2), §3.1 and Algorithm 1: self-edit generation is learned using post-update task reward, and update value depends on current parameters. We measure that dependence without training a generator or outer RL loop.

Copied scripts/runtime.py, pyproject.toml, uv.lock and sources/model-reference.json
from procedure-transfer at checkout dcdc0d6f54dde235549f8abfba407598b6635667;
runtime's last-change revision 0be899d8cb23bc35d330bcb7f72043d38f3475a0.
The diagnosis read is pinned at c183674bcecf9346d84e233aa5c084b1a9acb3ac.
The runtime transitively adapts procedure-acquisition-and-reuse revision
08d8ec1b0b757e8a537a14d708bd895e8829ac68. No source-study cases or adapters reused.
Model Qwen/Qwen3-4B-Instruct-2507 revision cdbee75f17c01a7cc42f958dc650907174af0554.
MLX-LM 86b48c461feebf87c58788655b7e57b5574b9e6d, MLX0.32.2; lock pins dependencies.
Model files accessed through a read-only-use symlink; checked against copied hashes.
Native MLX chosen because chat serving does not provide gradients or adapter resets.
