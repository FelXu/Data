# Jack × NoobAI V35 — LoRA 搭配与效果笔记

> 路径：`E:\ComfyUI-aki-v3\ComfyUI\models\loras\_notes_Jack_V35\Jack_V35_LoRA_搭配与效果.md`  
> 更新：2026-11-01 Asia/Hong_Kong（Fel 目视 QC：T6 / T7b / T8a / T8b / T9 / T9b）  
> 用途：上下文满了先读本文件，再出图。通用 Civitai 说明见同级目录旁 `_LoRA使用说明_目录.txt`。

---

## 硬规则（反复踩坑）

1. **出图目录**：只写 `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\`（子文件夹 OK）。**禁止 Desktop**。
2. **底模生产默认**：Indigo Void Furry Fused XL NoobAI **V35 fp32**。
3. **画风 LoRA 不要互叠**：ILstyle 与 BRIL / v1 / BRI **不要**叠在同一张里。细节类（XS / BSS / Noob Detailer 等）可以叠在**单一**画风上。
4. **触发词互斥**（别混用）：
   - **ILstyle**（`blackrat_style：IllustriousBlackRat_Style.safetensors`）：`blackrat_style, blackrat`
   - **BRIL**（`Black-rat-furry,anthro,tranform,human：Black_Rat_StyleIllustrious.safetensors`）：只要 `black-rat-anthro`（anthro 模式）。不要加 `blackrat_style` / `black-rat-furry` / tranform / human
5. **QC 命名**：需 Fel 目视的放 `Jack_Test\REVIEW_YYYYMMDD_<topic>\`，文件名带权重/种子/采样；默认 **FULL only**（不要 HEAD 裁切）。
6. **质量优先**：不在打游戏时再抠 VRAM；游戏中勿重载出图（曾 OOM）。
7. **珠宝 NEG 仍有用**；耳朵偏大时用 smaller/normal ears，别堆过重 ear-rim/hair-tuck。
8. **白眼球 prompt 单独试过失败**（变成实心蓝/光团）——先别靠 `(white of the eyes)` 硬锁。

---

## 常用文件名（models/loras）

| 简称 | 文件 |
|------|------|
| ILstyle | `blackrat_style：IllustriousBlackRat_Style.safetensors` |
| BRIL | `Black-rat-furry,anthro,tranform,human：Black_Rat_StyleIllustrious.safetensors` |
| XS / Extreme-Sex | `extreme sex：Extreme-Sex-v2.0-IllustriousXLNoobAI.safetensors`（触发 `extreme sex`） |
| BSS | `BSS_Detail_Enhancer_Slider_v3.safetensors` |
| Noob Detailer | `NoobAI_XL_Detailer_EPS1.1_v1.safetensors` |

新细节 LoRA 已在本机：`Detail_Slider_IL_ShedTheSkin_v1`、`Detail_enhancer_IL_v2`、`Smooth_Lighting_Enhancer_NoobAI_v2`（见 T9/T9b）。Extreme-Sex 仍为当前 **v2.0**。

---

## 默认采样（近期 Jack 全身体）

- 采样：`euler_ancestral` / `normal`
- steps **35**，CFG **5**（部分历史配方 CFG6）
- 尺寸 **1024×1536**
- txt2img denoise 1.0

---

## 已验证搭配（Fel QC）

### ★ 主力推荐 — T6：ILstyle@1.1 + Extreme-Sex@1.0

- **状态：基本稳定可用，可记为后续出图优先尝试组合**
- 栈：V35 + ILstyle@**1.1** + XS@**1.0** + 触发 `blackrat_style, blackrat` + `extreme sex`
- 档位试验：XS 0.4→1.2 ×3 种子 → `REVIEW_20261031_ILstyle11_XS_T6`
- 观感：
  - **XS@1.0** 较平衡，定为 keeper 权重
  - XS@**0.8 起**偶尔画框外伸多余肢体
  - 高 XS 未见明显压黑/珠宝爆增；耳朵仍偏大；手指偶发不稳

### T7 → T7b：BRIL 单画风 + XS

- T7：BRIL@1.1 + XS 0.4→1.2 → `REVIEW_20261101_BRIL11_XS_T7`（青色/赛璐璐 anthro 偏移符合预期）
- **T7b（Fel 更认）**：BRIL@**1.0** + XS@**0.8 / 1.0** 各 6 张 → `REVIEW_20261101_BRIL10_XS_T7b`
  - **XS@1.0 最好**，但**不太稳定 → 实战要多抽卡**
  - 触发仅 `black-rat-anthro`

### T8a：ILstyle@1.1 + BSS（无 XS）

- `REVIEW_20261101_ILstyle11_BSS_T8a`
- 权重大约 **0.8–1.0** 可用
- **稳定性一般**；偶尔耳朵饰品
- 未叠 Extreme-Sex / BRIL

### T8b：ILstyle@1.1 + Noob Detailer — **PASS / 先不用**

- `REVIEW_20261101_ILstyle11_Noob_T8b`
- **耳朵颜色基本控制不住** → 当前栈直接 pass，不要当默认细节 LoRA

---

## 过程结论速查（T1–T5 等）

| 轮次 | 结论摘要 |
|------|----------|
| 历史 hist | V33 ILstyle@0.85 + hires dn0.25 曾是喜欢的参考方向；V35 上改走更高 ILstyle |
| T2–T3 | ILstyle~0.75–1.0；珠宝/耳缘问题靠 NEG + ear lock；0.75 珠宝最干净 |
| T4/T4b | ILstyle~1.1 方向锁定；耳朵易过大；减轻 ear 约束 + smaller ears；FULL only |
| T5 | **不要** ILstyle + BRIL 叠细节试验里的 BR 画风互叠；用户纠正后拆成 T6/T7 |
| Phase A | keepers 曾 C1 BRIL@0.9、C3 BRIL@1.0+XS@0.5；眼白方案失败；REF LAB/i2i 路径已弃 |
| 权重扫（更早） | 单画风高权重观感大致 ILstyle@1.2 > v1@1.0 > BRIL@0.8 > BRI@0.7–0.8（不同目标时可回查 Jack_Test/lora_weight） |

---

## 出图时优先试的配方（短列表）

1. **主推**：`ILstyle@1.1 + Extreme-Sex@1.0`，euler_a 35 CFG5 1024×1536，触发 blackrat_style/blackrat + extreme sex  
2. **备选画风**：`BRIL@1.0 + Extreme-Sex@1.0`，触发 black-rat-anthro；**多抽**  
3. **仅细节替换试**：ILstyle@1.1 + BSS@0.8–1.0（知会饰品风险）；**不要**默认上 Noob Detailer  

---

## REVIEW 文件夹索引（本轮）

- `Jack_Test\REVIEW_20261031_ILstyle11_XS_T6`
- `Jack_Test\REVIEW_20261101_BRIL11_XS_T7`
- `Jack_Test\REVIEW_20261101_BRIL10_XS_T7b`
- `Jack_Test\REVIEW_20261101_ILstyle11_BSS_T8a`
- `Jack_Test\REVIEW_20261101_ILstyle11_Noob_T8b`
- `Jack_Test\REVIEW_20261101_BRIL09_NewDetail_T9`
- `Jack_Test\REVIEW_20261101_ILstyle11_NewDetail_T9b`
- `Jack_Test\REVIEW_20261101_ILstyle12_NewDetail_T9b2`（ILstyle@1.2 T9b2 — ok=27）

脚本：`E:\ComfyUI-aki-v3\scripts\comfy_ilstyle11_xs_t6.py`、`comfy_bril11_xs_t7.py`、`comfy_bril10_xs_t7b.py`、`comfy_ilstyle11_bss_t8a.py`、`comfy_ilstyle11_noob_t8b.py`、`comfy_bril09_newdetail_t9.py`、`comfy_ilstyle11_newdetail_t9b.py`、`comfy_ilstyle12_newdetail_t9b2.py`

---

## 待办备忘

- T9/T9b Fel QC 已记；T9b2 ILstyle@1.2 矩阵 **已出齐 27/27**（REVIEW_20261101_ILstyle12_NewDetail_T9b2）— 待 Fel 目视
- DE（Detail_enhancer_IL_v2）对 TF/LEWD **不适合**，后续配方默认跳过
- 耳朵尺寸、手指、眼白、IP-Adapter 锁脸：等 Fel 点头再开  
- T8b Noob：除非换耳色策略，否则保持 pass  
- Extreme-Sex 仍为当前 **v2.0**

（完）

---

## T9 / T9b — 新细节 LoRA 单测（完成）

- **LoRA 文件**（`models\loras\`）:
  - `Detail_Slider_IL_ShedTheSkin_v1.safetensors` — 8789076
  - `Detail_enhancer_IL_v2.safetensors` — 228492876
  - `Smooth_Lighting_Enhancer_NoobAI_v2.safetensors` — 197084608
- **设定**：V35 / euler_a 35 CFG5 1024×1536 / FULL only；种子 20261031–033；DE 0.5/0.8/1.0；SLE 0.3/0.5/0.7；Slider 2/3/4；各轨 27 张，**不混叠 BRIL 与 ILstyle**
- **T9** BRIL@**0.9**（触发 black-rat-anthro）→ `REVIEW_20261101_BRIL09_NewDetail_T9` — **ok=27 fail=0**
- **T9b** ILstyle@**1.1**（触发 blackrat_style）→ `REVIEW_20261101_ILstyle11_NewDetail_T9b` — **ok=27 fail=0**
- 脚本：`scripts\comfy_bril09_newdetail_t9.py`、`scripts\comfy_ilstyle11_newdetail_t9b.py`
- raw：`BlackRat_NoobAI_NoXS\BRIL09_NewDetail_T9\raw`、`…\ILstyle11_NewDetail_T9b\raw`
- **视觉 QC**：见下方 **「2026-11-01 Fel QC — T9 / T9b」**（DE 不适合 TF/LEWD；DS4 + SLE0.5–0.7 可用；ILstyle 耳色优于 BRIL）


---

## 2026-11-01 Fel QC — T9 / T9b（新细节 LoRA）

> 用户口令摘录（Fel）：T9 里 DE 从 0.5 起有奇怪背景，不适合 TF/LEWD；DS4 FULL 与 SLE0.5–0.7 可以；BRIL 耳朵颜色一直不好控会跟头发走。T9b 结果和 T9 差不多，风格模型对耳朵颜色控制较好；**ILstyle 权重提到 1.2 再跑一遍 T9b**。

### T9 — BRIL@0.9 + 新细节 LoRA
- 目录：`Jack_Test\REVIEW_20261101_BRIL09_NewDetail_T9`
- **Detail_enhancer_IL_v2（DE）**：权重从 **0.5 起**会出现奇怪/怪异背景 → **不适合 TF / LEWD 内容** → **pass / 本项目避免使用**（矩阵 A/B 可比仍可出同权单元格，但笔记标记不可用）
- **Detail Slider ShedTheSkin（DS）@4 FULL**：可用 / OK
- **Smooth_Lighting_Enhancer_NoobAI_v2（SLE）@0.5–0.7**：可用 / OK
- **BRIL 耳色**：仍难控，耳朵易跟头发颜色 bleed → **画风侧持续问题**（非细节 LoRA 单独造成）

### T9b — ILstyle@1.1 + 同细节档位
- 目录：`Jack_Test\REVIEW_20261101_ILstyle11_NewDetail_T9b`
- 细节 LoRA 表现与 T9 **大致相同**（DE 背景怪；DS4 + SLE0.5–0.7 可用）
- **耳色**：ILstyle 画风对耳朵颜色控制 **优于 BRIL**
- **下一步（已完成）**：ILstyle@**1.2** 同矩阵重跑 → `REVIEW_20261101_ILstyle12_NewDetail_T9b2` — **ok=27 fail=0**；脚本 `comfy_ilstyle12_newdetail_t9b2.py`；视觉 QC 待 Fel

### 配方侧短结论（2026-11-01）
- 细节 keeper 候选：**DS@4**、**SLE@0.5–0.7**（叠在单一画风上；勿 BRIL+ILstyle 互叠）
- 细节 pass：**DE**（TF/LEWD 背景污染）
- 画风耳色优先试 **ILstyle**（现升 1.2 验证）；BRIL 耳色 bleed 记为已知限制
- Extreme-Sex 仍为当前 **v2.0**（可选叠，本轮 T9/T9b 未叠 XS）


---

## ILstyle 现为默认风格 LoRA（2026-11-01）

- **默认画风**：`ILstyle`（`blackrat_style：IllustriousBlackRat_Style.safetensors`）
- **相对 BRIL**：耳色更稳（T9/T9b Fel QC）；BRIL 耳色易跟头发 bleed
- **权重**：常用 **~1.1–1.2**；T9b2（ILstyle@1.2）≈ T9b（@1.1）观感同档，可作生产默认
- **硬互斥**：ILstyle **永不与 BRIL 同栈**（画风互叠禁止）
- **细节叠法**：细节类（XS / DS / SLE / 下文新 Detail）只叠在**单一**画风上

### Keepers（截至 2026-11-01）

- **XS / Extreme-Sex**：仍为当前 **v2.0**；常用叠 **@1.0**（T6 keeper）
- **DS（ShedTheSkin Slider）@4**：OK
- **SLE（Smooth Lighting Enhancer NoobAI v2）@0.5–0.7**：OK
- **DE（Detail_enhancer_IL_v2）**：pass（怪异背景，不适合 TF/LEWD）

---

## 2026-11-01 新装 Detail LoRA 清单

路径：`E:\ComfyUI-aki-v3\ComfyUI\models\loras\`

| 文件 | 大小 (bytes) | 状态 |
|------|-------------:|------|
| `Smooth_Booster_v5.safetensors` | 197,086,960 | OK |
| `AddMicroDetails_Illustrious_v7.safetensors` | 228,470,764 | OK |
| `AddMicroDetails_NoobAI_v5.safetensors` | 228,470,676 | OK |
| `TrendCraft_v2.4I_Illustrious.safetensors` | 114,431,360 | OK |
| `DetailerIL_Jedas_v2.safetensors` | 228,465,628 | OK |
| `Add_Details_Slider_IL_v1.2.safetensors` | 5,448,608 | OK |
| `detaILeReij_v2.safetensors` | 228,450,340 | OK |
| `Detailer_FallenIncursio_v1.safetensors` | 228,472,436 | OK |
| `FluffyFur_Illustrious.safetensors` | 228,463,924 | OK |

已装摘要：
- `Smooth_Booster_v5.safetensors` — 197,086,960
- `AddMicroDetails_Illustrious_v7.safetensors` — 228,470,764
- `AddMicroDetails_NoobAI_v5.safetensors` — 228,470,676
- `TrendCraft_v2.4I_Illustrious.safetensors` — 114,431,360
- `DetailerIL_Jedas_v2.safetensors` — 228,465,628
- `Add_Details_Slider_IL_v1.2.safetensors` — 5,448,608
- `detaILeReij_v2.safetensors` — 228,450,340
- `Detailer_FallenIncursio_v1.safetensors` — 228,472,436
- `FluffyFur_Illustrious.safetensors` — 228,463,924 — **OK**

> 说明：本批**未做生成 QC**；下列权重为 Civitai 角色 + Jack/ILstyle/XS 栈风险推估，供首测。

---

## 分析与建议首测权重（无 QC，仅分析）

基线栈假设：**ILstyle@1.2 + XS@1.0**（单一画风；不叠 BRIL）。新 Detail **一次只加一个**做 A/B。

1. **Smooth Booster v5**（`Smooth_Booster_v5`）
   - 角色：lighting / detail booster（与 SLE 同族方向）
   - 建议首测：**0.3–0.7**，叠在 ILstyle@1.2+XS@1.0 下
   - 风险：**不要与 SLE 双高同栈**（同族 lighting booster 互抢）

2. **Add Micro Details**
   - 触发：`addmicrodetails`
   - Indigo V35 优先：**NoobAI v5**；备选 **Illustrious v7**
   - 建议：**0.4–0.8**
   - 风险：耳缘 / 珠宝 **过细碎**；叠 XS 时更要盯耳饰爆炸

3. **TrendCraft v2.4I**（`TrendCraft_v2.4I_Illustrious`）
   - 角色：style-detail
   - 建议：**0.4–0.6（偏低）**
   - 风险：**与 ILstyle 风格打架** → 只低权试；勿当主画风

4. **Detailer IL Jedas v2**（`DetailerIL_Jedas_v2`）
   - 触发：`Jeddtl02`
   - 建议：中低权起步（约 0.4–0.7），**仔细 A/B**
   - 风险：耳色 / 珠宝影响未知

5. **detaILeReij v2**（`detaILeReij_v2`）
   - 建议：**≤0.8**
   - 风险：**≥0.9 易艺术 bleed**（风格偏移）

6. **Add Details Slider IL v1.2**（`Add_Details_Slider_IL_v1.2`）
   - 体积极小；当 dial / slider 用
   - 风险：**不要与 ShedTheSkin DS 双高同栈**

7. **FallenIncursio Detailer**（`Detailer_FallenIncursio_v1`）
   - 触发：`detailed`
   - 角色：灵活细节 dial；首测可扫中档

8. **Fluffy Fur IL**（`FluffyFur_Illustrious`） — **已装**
   - 毛发专项实验；**与 Extreme-Sex 打架风险单独测**，勿和 XS 高权首轮硬叠

---

## Future solo A/B order（只记顺序，本轮不跑图）

1. baseline：**ILstyle@1.2 + XS@1.0**
2. + **Smooth Booster**（0.3–0.7；勿双高 SLE）
3. + **Add Micro Details NoobAI v5**（`addmicrodetails`，0.4–0.8）
4. + **TrendCraft** 低权（0.4–0.6；防 style fight）
5. + **Jedas / detaILeReij / Fallen**（各单独扫；触发各自词）
6. + **Add Details Slider IL**（勿双高 DS）
7. + **Fluffy Fur**（毛发专项；与 XS 分测）

零生成确认：本笔记更新轮次 **未跑任何 Comfy 出图**。

---

---

## 2026-11-01 归档 — Jack_Test 历史搭配可用/不可用（删图前）

> 目的：Fel 清理旧 PNG 前固化可用/不可用搭配。**可用/不可用以 Fel 既有 QC（对话+本笔记+日志）为准**，不以文件夹名猜测。Jack_Test 图片仅用于 **清理索引**（下列 Folders index）。本段 **不发明** 未给过的 QC；仅有文件、未见 QC 的标「awaiting QC / unknown」。**本轮未删除任何 Jack_Test 图片。**

### Keep / usable

| 项 | 证据 / 备注 |
|----|-------------|
| **默认画风 ILstyle ~1.1–1.2** | 耳色比 BRIL 稳（T9/T9b Fel QC）；T9b2@1.2 可作生产默认；**永不与 BRIL 同栈** |
| **Extreme-Sex / Lewd Details v2.0** | 仍为当前文件；高 XS（~1.0）有用；T7b 多抽不稳定 |
| **T6 keeper**：ILstyle@1.1 + XS@1.0 | REVIEW_20261031_ILstyle11_XS_T6；Fel 定为后续优先尝试 |
| **Detail Slider ShedTheSkin DS@4 FULL** | T9/T9b Fel QC OK |
| **Smooth_Lighting_Enhancer SLE@0.5–0.7** | T9/T9b Fel QC OK |
| **BSS Detail ~0.8–1.0** | T8a ok-ish；偶发耳朵饰品；稳定性一般 |

### Pass / avoid

| 项 | 证据 / 备注 |
|----|-------------|
| **Detail_enhancer_IL_v2 DE ≥0.5** | 怪异背景 → **不适合 TF/LEWD**（T9/T9b） |
| **NoobAI_XL_Detailer** | 耳色失控 → pass（T8b） |
| **BRIL 耳色跟头发 / 难控** | 持续问题（T7/T7b/T9） |
| **重珠宝 endemic** | 历史多轮；**jewelry NEG 仍有用** |
| **双 ILstyle 叠 / BRIL+ILstyle 混** | 硬规则禁止；T5 已纠正 |
| **白眼球 prompt 单独硬锁** | 早期失败（实心蓝/光团） |

### Folders index（删图对照 — Jack_Test）

| 文件夹 | 张数(约) | 一轮是什么 |
|--------|---------:|------------|
| REVIEW_20261031_ILstyle085_V35 | 11 | T1/hist：ILstyle@0.85 早期 V35 对照（含 REF + FULL/HEAD） |
| REVIEW_20261031_ILstyle085_V35_T2 | 8 | T2：ILstyle@0.85 eulerA35 CFG5 |
| REVIEW_20261031_ILstyle085_V35_T3 | 12 | T3：ILstyle 0.75/0.85 权重试 |
| REVIEW_20261031_ILstyle_V35_T4 | 12 | T4：ILstyle 1.1/1.2 FULL+HEAD |
| REVIEW_20261031_ILstyle_V35_T4b | 6 | T4b：ILstyle 1.1–1.3 FULL only |
| REVIEW_20261031_ILstyle11_Detail_BRIL_T5 | 6 | T5：ILstyle±BSS/Noob/XS/BRIL 混试（**互叠已废弃**） |
| REVIEW_20261031_ILstyle11_XS_T6 | 15 | **T6 keeper 方向**：ILstyle@1.1 + XS 0.4→1.2 |
| REVIEW_20261031_PhaseA_Eye | 0 | Phase A 眼白路径（空 / 已弃） |
| REVIEW_20261101_BRIL11_XS_T7 | 15 | T7：BRIL@1.1 + XS 扫 |
| REVIEW_20261101_BRIL10_XS_T7b | 12 | T7b：BRIL@1.0 + XS@0.8/1.0（Fel 更认但要多抽） |
| REVIEW_20261101_ILstyle11_BSS_T8a | 15 | T8a：ILstyle@1.1 + BSS（无 XS） |
| REVIEW_20261101_ILstyle11_Noob_T8b | 15 | T8b：Noob Detailer — **pass** |
| REVIEW_20261101_BRIL09_NewDetail_T9 | 27 | T9：BRIL@0.9 + DE/SLE/DS |
| REVIEW_20261101_ILstyle11_NewDetail_T9b | 27 | T9b：ILstyle@1.1 + 同细节矩阵 |
| REVIEW_20261101_ILstyle12_NewDetail_T9b2 | 27 | T9b2：ILstyle@1.2 同矩阵 — **ok=27**；目视 QC 待 Fel（细节结论已从 T9/T9b 继承） |
| REVIEW_20261101_ILstyle12_NewDetail6_T10 | 75 | **T10 新 Detail×6** — ok=75 fail=0；待 Fel 目视 |
| BlackRat_FullX / BlackRat_NoobAI_* | 0 PNG 于顶层 | 旧研究/raw 路径；多数 REVIEW 的 raw 子目录；**awaiting QC / unknown**（勿当 Fel 已 QC 的 keeper 证据） |
| _refs / _xfer | — | 参考/中转；非 QC 批次 |

### 删图前最短口令

1. 先留笔记本节 + 既有 Fel QC 段；**不要只靠文件夹名回忆**。  
2. 可删候选：T1–T5 探索、T8b pass、T9/T9b 里已判定 DE 废片、空 BlackRat_* 顶层、PhaseA_Eye。  
3. 建议暂留到 T10 QC 完：T6 keeper、T7b、T8a、T9/T9b 的 DS/SLE 对照、T9b2、T10。  
4. **代理未执行删除** — Fel 自行清理。

---

## 2026-11-01 拟定 — T10 新 Detail×6 测试策略（待 Fel 确认后开跑）

**状态：已完成（2026-11-01 Asia/Hong_Kong）。** Fel 确认策略后跑完 — **ok=75 fail=0** FULL；文件夹 Jack_Test\\REVIEW_20261101_ILstyle12_NewDetail6_T10；脚本 scripts\\comfy_ilstyle12_newdetail6_t10.py；**无** TrendCraft 额外 w0.6；视觉 QC 待 Fel。

### Scope（6 LoRA，baseline 上一次只加一个）

1. `Smooth_Booster_v5`
2. `AddMicroDetails_NoobAI_v5`（trigger：`addmicrodetails`；IL v7 本轮延后）
3. `TrendCraft_v2.4I_Illustrious`
4. `DetailerIL_Jedas_v2`（trigger：`Jeddtl02`）
5. `detaILeReij_v2`
6. `Detailer_FallenIncursio_v1`（trigger：`detailed`）

**本轮延后：** `Add_Details_Slider_IL_v1.2`、`FluffyFur_Illustrious`、`AddMicroDetails_Illustrious_v7`。

### Baseline（每个 cell 共用）

- 栈：**ILstyle@1.2 + Extreme-Sex@1.0**
- 模型 / 分辨率：V35 fp32 **1024×1536**
- 采样：**euler_a** 35 / **CFG 5**
- **无 BRIL**；本轮 **不加 SLE / DS / DE**

### Weights（天花板扫）

- 每个 LoRA 试：**0.4 / 0.7 / 1.0 / 1.2**
- **例外 — TrendCraft**：额外加 **0.6**（即 0.4 / 0.6 / 0.7 / 1.0 / 1.2）；若 1.2 风格打架严重，Fel 可事后砍高权 cell
- Smooth Booster 作者偏好叠用 **≤0.7** — 仍单跑 **1.0 / 1.2** 一次看天花板

### Seeds（抗随机）

- 全体 cell 共用 3 个固定种子：**20261101 / 20261102 / 20261103**
- 另出 **baseline-only** 同 3 种子各 1 张（对照）

### Count

- 4 权网格：baseline 3 + 6×4×3 = **3+72 = 75 FULL**
- 若纳入 TrendCraft 额外 **w0.6×3** → **78 FULL**

### Output folder

`Jack_Test\REVIEW_20261101_ILstyle12_NewDetail6_T10`

### Filename rules（Fel）

- LoRA 名可读、少/不缩写；含 **weight + seed + FULL**
- **不要**把 CFG / sampler / steps 塞进文件名

示例：

- `T10_BASE_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`
- `T10_Smooth_Booster_v5_w0.7_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`
- `T10_AddMicroDetails_NoobAI_v5_w1.0_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png`
- `T10_TrendCraft_v2.4I_w0.6_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`
- `T10_DetailerIL_Jedas_v2_w1.2_ILstyle1.2_ExtremeSex1.0_FULL_s20261103.png`
- `T10_detaILeReij_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`（权重仅 0.4/0.7/1.0/1.2，无 0.8）
- `T10_Detailer_FallenIncursio_v1_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`


### T10 出图结果（2026-11-01）

- **REVIEW**：Jack_Test\\REVIEW_20261101_ILstyle12_NewDetail6_T10 — **75/75 FULL**，fail=0
- Baseline：ILstyle@1.2 + Extreme-Sex@1.0 ×3 seeds
- Detail×6 @ 0.4/0.7/1.0/1.2 ×3 seeds（无 BRIL/SLE/DS/DE；无 TrendCraft 额外 0.6）
- 脚本：E:\\ComfyUI-aki-v3\\scripts\\comfy_ilstyle12_newdetail6_t10.py
- **视觉 QC：待 Fel**（本轮代理未自评可用/不可用）
- **未删除**任何既有 Jack_Test 图片

## 2026-11-01 Fel 优选图参数拆解（T10 七张）

> 用户说明：这几张**不是**只让 keep 标签，要**分析并记录完整参数组合**。来源文件夹：`Jack_Test\REVIEW_20261101_ILstyle12_NewDetail6_T10`。脚本：`scripts\comfy_ilstyle12_newdetail6_t10.py`。

### 共用底参（七张相同）
- Checkpoint：Indigo NoobAI **V35 fp32**
- 风格：`ILstyle@1.2`（默认风格 LoRA；不与 BRIL 混用）
- 细节增强（当时开启）：`Extreme-Sex-v2.0`（Lewd Details）**@1.0** + 触发相关词按 T10 脚本
- 采样：`euler_ancestral` · steps **35** · CFG **5** · 尺寸 **1024×1536** · FULL
- 提示：沿用 T10 Jack POS/NEG（含 jewelry NEG、小号耳锁等；以脚本为准）

### 七张各自变量（Fel 评为较好）
| # | 文件名 | 额外 Detail LoRA | 权重 | Seed | 触发词 |
|---|--------|------------------|------|------|--------|
| 1 | `T10_detaILeReij_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png` | `detaILeReij_v2` | **0.4** | 20261101 | （脚本可选 detailed；本胞以文件名为准） |
| 2 | `T10_DetailerIL_Jedas_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png` | `DetailerIL_Jedas_v2` | **0.4** | 20261101 | **Jeddtl02** |
| 3 | `T10_DetailerIL_Jedas_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png` | `DetailerIL_Jedas_v2` | **0.4** | 20261102 | **Jeddtl02** |
| 4 | `T10_Detailer_FallenIncursio_v1_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png` | `Detailer_FallenIncursio_v1` | **0.4** | 20261102 | **detailed** |
| 5 | `T10_Detailer_FallenIncursio_v1_w0.7_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png` | `Detailer_FallenIncursio_v1` | **0.7** | 20261102 | **detailed** |
| 6 | `T10_Detailer_FallenIncursio_v1_w1.2_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png` | `Detailer_FallenIncursio_v1` | **1.2** | 20261102 | **detailed** |
| 7 | `T10_Smooth_Booster_v5_w1.0_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png` | `Smooth_Booster_v5` | **1.0** | 20261101 | 无强制触发 |

### 组合解读（分析，非新 QC）
- 七张都是 **ILstyle@1.2 + ExtremeSex@1.0 + 单一新 Detail**；没有 Smooth/Jedas/Fallen 互叠。
- **FallenIncursio** 在同一种子 `20261102` 上 0.4 / 0.7 / **1.2** 都被点名 → 该 Detailer 在此栈容错宽，高权重仍可能入眼（仍要防过锐/首饰）。
- **Jedas@0.4** 两个种子都入选 → 低权重较稳，优先当轻量细节层。
- **detaILeReij 只见 0.4** 入选 → 先当低压；更高档未在这批评选里。
- **Smooth_Booster@1.0** 入选（高于作者叠层常说的 0.3–0.7）→ 在本栈可试到 1.0，但别默认再叠 SLE。
- 用户下一步已要求：**去掉 Extreme-Sex** 用同七组变量做 T11 对照（见 T11 节）。


---

## 2026-11-01 — Fel T10 keepers（完整参数 combo）+ T11 NoExtremeSex A/B

**状态：** Fel 从 T10 挑了 7 张 keeper（`pt139u`：去掉 extreme love / Extreme-Sex 再比）；本轮 **记录完整 combo**，并开跑 **T11 = 同 cell 去掉 Extreme-Sex**。T10 原图 **未删**。

### 共用设定（T10 脚本 `comfy_ilstyle12_newdetail6_t10.py`）

| 项 | 值 |
|---|---|
| ckpt | `indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors` (V35 fp32) |
| Style LoRA | `blackrat_style：IllustriousBlackRat_Style.safetensors` **@ 1.2** |
| Extreme-Sex | `extreme sex：Extreme-Sex-v2.0-IllustriousXLNoobAI.safetensors` **@ 1.0** + POS trigger **`extreme sex`** |
| 分辨率 | **1024×1536** |
| Sampler / Scheduler | **euler_ancestral** / **normal** |
| Steps / CFG / denoise | **35** / **5.0** / **1.0** |
| POS/NEG | 与 T10 相同（见 `prompt_t10.json`）；detail 有 trigger 时额外塞入 POS |
| 禁止 | NO BRIL / SLE / ShedTheSkin DS / DE；一次只叠一个 detail LoRA |
| T10 REVIEW 文件夹 | `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_ILstyle12_NewDetail6_T10` |

### Fel 选定的 7 张 T10 keepers（完整 combo + 精确文件名）

1. **detaILeReij_v2 @ 0.4 · seed 20261101**
   - 栈：ckpt V35 + ILstyle@1.2 + ExtremeSex@1.0 + **`detaILeReij_v2.safetensors` @ 0.4**（无专用 trigger）
   - 文件：`T10_detaILeReij_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`
   - 路径：`...\REVIEW_20261101_ILstyle12_NewDetail6_T10\T10_detaILeReij_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`

2. **DetailerIL_Jedas_v2 @ 0.4 · seed 20261101**
   - 栈：ckpt V35 + ILstyle@1.2 + ExtremeSex@1.0 + **`DetailerIL_Jedas_v2.safetensors` @ 0.4**；POS trigger **`Jeddtl02`**
   - 文件：`T10_DetailerIL_Jedas_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`

3. **DetailerIL_Jedas_v2 @ 0.4 · seed 20261102**
   - 栈：同上（Jedas@0.4 + `Jeddtl02`）；仅 seed 不同
   - 文件：`T10_DetailerIL_Jedas_v2_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png`

4. **Detailer_FallenIncursio_v1 @ 0.4 · seed 20261102**
   - 栈：ckpt V35 + ILstyle@1.2 + ExtremeSex@1.0 + **`Detailer_FallenIncursio_v1.safetensors` @ 0.4**；POS trigger **`detailed`**
   - 文件：`T10_Detailer_FallenIncursio_v1_w0.4_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png`

5. **Detailer_FallenIncursio_v1 @ 0.7 · seed 20261102**
   - 栈：同上但 Fallen@**0.7** + `detailed`
   - 文件：`T10_Detailer_FallenIncursio_v1_w0.7_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png`

6. **Detailer_FallenIncursio_v1 @ 1.2 · seed 20261102**
   - 栈：同上但 Fallen@**1.2** + `detailed`
   - 文件：`T10_Detailer_FallenIncursio_v1_w1.2_ILstyle1.2_ExtremeSex1.0_FULL_s20261102.png`

7. **Smooth_Booster_v5 @ 1.0 · seed 20261101**
   - 栈：ckpt V35 + ILstyle@1.2 + ExtremeSex@1.0 + **`Smooth_Booster_v5.safetensors` @ 1.0**（无专用 trigger）
   - 文件：`T10_Smooth_Booster_v5_w1.0_ILstyle1.2_ExtremeSex1.0_FULL_s20261101.png`

### T11 — 同 cell 去掉 Extreme-Sex（A/B，待 QC）

- **目的：** 与上述 7 keepers 一对一对比（去掉 Lewd Details / “extreme love” / ExtremeSex LoRA + 去掉 POS `extreme sex`）
- **栈：** ILstyle@1.2 +（可选）同一 detail LoRA@同一 weight；**无** Extreme-Sex 文件、**无** extreme sex trigger overweight
- **另加 1 张 BASE：** ILstyle@1.2 only，seed **20261101**（无 detail、无 XS）→ 共 **8** 张
- 分辨率 / sampler / CFG / steps / POS·NEG（除 XS trigger）：与 T10 相同
- **脚本：** `E:\ComfyUI-aki-v3\scripts\comfy_ilstyle12_noxs_t11.py`
- **REVIEW：** `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_ILstyle12_NoExtremeSex_T11`
- **文件名示例：**
  - `T11_BASE_ILstyle1.2_NoExtremeSex_FULL_s20261101.png`
  - `T11_Smooth_Booster_v5_w1.0_ILstyle1.2_NoExtremeSex_FULL_s20261101.png`
  - `T11_Detailer_FallenIncursio_v1_w1.2_ILstyle1.2_NoExtremeSex_FULL_s20261102.png`
- **视觉 QC：待 Fel**（T11 跑完后对照 T10 keepers）
- **未删除**任何既有 Jack_Test / T10 图片

### T11 出图结果（2026-11-01 Asia/Hong_Kong）

- **REVIEW**：`Jack_Test\REVIEW_20261101_ILstyle12_NoExtremeSex_T11` — **8/8 FULL**，fail=0
- 栈：ILstyle@1.2 only（+ detail when keeper）；**无 Extreme-Sex / 无 `extreme sex` trigger**
- 清单：
  1. `T11_BASE_ILstyle1.2_NoExtremeSex_FULL_s20261101.png`
  2. `T11_detaILeReij_v2_w0.4_ILstyle1.2_NoExtremeSex_FULL_s20261101.png`
  3. `T11_DetailerIL_Jedas_v2_w0.4_ILstyle1.2_NoExtremeSex_FULL_s20261101.png`
  4. `T11_DetailerIL_Jedas_v2_w0.4_ILstyle1.2_NoExtremeSex_FULL_s20261102.png`
  5. `T11_Detailer_FallenIncursio_v1_w0.4_ILstyle1.2_NoExtremeSex_FULL_s20261102.png`
  6. `T11_Detailer_FallenIncursio_v1_w0.7_ILstyle1.2_NoExtremeSex_FULL_s20261102.png`
  7. `T11_Detailer_FallenIncursio_v1_w1.2_ILstyle1.2_NoExtremeSex_FULL_s20261102.png`
  8. `T11_Smooth_Booster_v5_w1.0_ILstyle1.2_NoExtremeSex_FULL_s20261101.png`
- 脚本：`E:\ComfyUI-aki-v3\scripts\comfy_ilstyle12_noxs_t11.py`
- **视觉 QC：待 Fel**（对照 T10 keepers；本轮代理未自评）
- **未删除**任何既有 T10 / Jack_Test 图片

## 2026-11-01 Fel 指定对照 — T11 NoExtremeSex vs T10（三张）

Fel 点名用来比「去掉 Extreme-Sex」效果的三张（皆 T11）：
1. `T11_Smooth_Booster_v5_w1.0_ILstyle1.2_NoExtremeSex_FULL_s20261101.png` ↔ T10 同参有 XS
2. `T11_Detailer_FallenIncursio_v1_w0.7_ILstyle1.2_NoExtremeSex_FULL_s20261102.png` ↔ T10 同参有 XS
3. `T11_Detailer_FallenIncursio_v1_w1.2_ILstyle1.2_NoExtremeSex_FULL_s20261102.png` ↔ T10 同参有 XS

### 观感差（分析）
- **身材/黑毛剪影/ILstyle 线面**：去掉 XS 后大体仍在；肌肉体量主要不靠 XS 单独支撑。
- **Extreme-Sex 更像在加**：局部清晰度/微细节、表情与叙事感（有 XS 的 Smooth@1.0 带 ?! 与颤线等「愣住/TF」感；无 XS 更偏中性摆拍目录图）。
- **FallenIncursio 0.7 / 1.2**：无 XS 后仍能站住；差异更多在「活力度/口型微表情/体表微纹理」而非整套崩掉。
- **结论倾向**：若目标是干净全身造型抽卡，可无 XS；若要 LEWD/TF 清晰与情绪钩子，XS@1.0 仍有价值。细节器（Smooth Booster / Fallen）与 ILstyle 可独立于 XS 工作。

