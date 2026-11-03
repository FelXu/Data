# TF notes — Jack EARLY mother

## 2026-11-01 17:33 Asia/Hong_Kong — EARLY mother M03 PASS (Fel t167u / pt167u)

- Goal: one qualified early-TF mother (E1–E7 Fel-corrected). Budget override: new mother-production goal after prior K01 used 1/2.
- Method order: Klein K01 (prior) → Klein K02 right-index-only (fail E6) → paint/paste ROI on K01 right INDEX nail (PASS).
- Working method: **paint/paste nail ROI** (not Klein; not T03; forbid denoise<=0.5 && lineart>=0.75 honored).
- Best: `output\Jack_Test\REVIEW_20261101_EARLY_MOTHER\M03_00001_.png`
  SHA256 E2CF37753429EED48A2FA4DFFAECC1F2DED67D003EE6D633E32FADE97CAE0A1A
- Bound: `input\Jack_TF_EARLY\approved_color.png` + `source_after_review.png` + `approved_lineart.png` (export prompt_id 9bd3a81b-ab38-4b72-87bb-3e8c7546aacf)
- E1 tip-pointed ears PASS (not shrunk). E2 canine nose tip. E3 no muzzle. E4 sparse short hair gaps. E5 purple tee+khaki shorts taut. E6 right INDEX root-deep→tip-light charcoal gradient (was solid black). E7 Jack identity OK.
- QC: `本机方法迁移_V3\初期母图验收_填写.json` source_semantic_pass=true approved_bound=true
- Next: T03 allowed now that mother passes. Do not reopen nail Klein unless E6 regresses.

## 2026-11-01 — 可复现路径改判（仓库补齐，未出图）

- Fel：不再沿用 M03 涂改 / `early_approved` 作为可复现通过母图（文件留档；`初期母图验收_填写.json` 标 `superseded_as_passing_mother=true`）。
- 仓库新增：`EARLY_底图_空Latent文生图.json` + API、耳/鼻 Klein UI+API、`tools/compile_early_mother.py`、`masks/README.md`。
- 规格 `source_semantic_pass` 仍为 false。本轮不跑 T03；真实出图、权重哈希、T06 拷贝仍须本机。
