# Follow-up rehearsal and selection methods

Read2026-09-14 while yielding the shared GPU. These are additional primary methods
for interpreting the observed source tradeoff; no author implementation was reused.
The exact versions are the **NeurIPS2019 proceedings PDFs**, identified by URLs and
SHA256 in retrieval.json. Text files are convenience extractions with pypdf; CLEAR's
mathematical symbol extraction is imperfect, so the PDF is authoritative.

- [CLEAR / Experience Replay for Continual Learning](https://papers.nips.cc/paper_files/paper/2019/file/fa7cdfad1a5aaf8370ebeda47a1ff1c3-Paper.pdf), §3 and §4.1–4.2.
  CLEAR combines novel and replayed experience in actor-critic training, with
  V-trace correction and behavioral cloning losses on replay. Its usual mixture
  is50:50. Separate, simultaneous and sequential task training distinguish task
  compatibility from loss of old performance during later learning. Our comparison
  uses hard supervised labels and no actor-critic or cloning loss; the balanced
  source is simple rehearsal, not CLEAR. Its base-mixture diagnostic similarly
  asks whether the rules are jointly learnable.
- [Online Continual Learning with Maximally Interfered Retrieval](https://papers.nips.cc/paper_files/paper/2019/file/15825aee15eb335cc13f9b559f166ee8-Paper.pdf), §3.1 and Algorithm1.
  MIR estimates a candidate parameter update, ranks stored examples by the
  resulting increase in loss, and rehearses high-interference examples with incoming
  data. This differs from prioritizing current prediction errors. Our gap policy
  measures current errors and makes one source choice; it does not test virtual
  updates, select replay examples by predicted damage, or implement MIR. A failure
  of gap-only selection does not establish a limitation of MIR or all selection.

The arXiv metadata endpoint for1811.11682 returned HTTP429 on one request. Its
failed attempt is recorded in retrieval-error.txt; no retry was made. The official
conference copies were then obtained directly and cached. No arXiv version is
claimed for these proceedings artifacts.
