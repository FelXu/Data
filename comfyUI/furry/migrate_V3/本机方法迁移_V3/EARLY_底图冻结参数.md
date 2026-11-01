# EARLY 本机底图 — 冻结参数

与 `A_机器人规格_初期结构准确.json` 的 `sampling_defaults` / `style` / `prompts` 对齐。
界面图：`EARLY_底图_空Latent文生图.json`　API：`api/EARLY_底图_空Latent文生图_API.json`

| 项 | 冻结值 |
|---|---|
| Checkpoint | `indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors` |
| LoRA | ILstyle `blackrat_style：IllustriousBlackRat_Style.safetensors` **0.8 / 0.8**（母图复现以规格为准，不用 notes 里的 1.2） |
| CLIP last layer | **-2** |
| 画幅 | **832 × 1216**，batch **1** |
| 采样 | steps **28**，CFG **5.0**，`euler_ancestral` / `normal` |
| 种子 | **2026110101**，`control_after_generate=fixed` |
| denoise | **1.0**（空 Latent 文生图） |
| 正面 / 负面 | `POS_方法验证.txt` / `NEG_方法验证.txt` |
| 外形要点 | 中长蓬乱黄发厚刘海、蓝眼、黑框眼镜、紫 T、卡其短裤、运动鞋；E1–E7 初期结构措辞已写进 POS |
| 输出前缀（默认） | `Jack_Test/REVIEW_20261101_EARLY_BASE/B01` |

## 建议本机落盘

1. 跑通底图后，把满意色稿复制到 `E:\ComfyUI-aki-v3\ComfyUI\input\Jack_TF_EARLY\base_color.png`。
2. Klein 甲尖图的 LoadImage 改为该路径（不要继续默认用 `mid_color_draft` 当「已通过」源）。
3. 云端仓库**没有**真实出图；权重哈希仍待本机核验。

## 不做

- 本轮不跑 T03。
- 不把 `early_approved/` 或 M03 涂改母图当作可复现通过样本。
