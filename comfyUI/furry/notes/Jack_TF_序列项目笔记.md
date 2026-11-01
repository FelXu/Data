# Jack TF 序列项目笔记

> 路径：`E:\ComfyUI-aki-v3\ComfyUI\models\loras\_notes_Jack_TF\Jack_TF_序列项目笔记.md`  
> 指针：同目录 `_Jack_TF_笔记_看这里.txt`  
> 更新：2026-11-01 Asia/Hong_Kong（HumanForm v2 keepers + v3 hair lock + Species/Mid LoRA 已落盘）  
> 记忆约定：profile / memory **只放本路径**；配方、调研、QC 一律写进本文件。

---

## 1. 项目目标

- 角色：**Jack**（Anubis / 黑毛兽人）**TF 序列**创作。
- 近期 anthro Jack 设定（来自 V35 生产线）：**女性**、肌肉型、黑肤/黑毛、蓝眼、肩长黑发、无毛身体倾向；珠宝 NEG。（anthro 终点仍按既有女性线，待 Fel 再确认）
- **人形（HumanForm）已纠正**：Fel 指定为 **完全人类男性**（非肌肉女）。以 §7.1 POS 为准。
- 流程优先级：
  1. **先锁定人形外观参考（male human Jack — HumanForm v2）**
  2. 再做 progressive TF / mid-TF / 终点 anthro 序列分镜
- 本笔记长期吸收：Civitai 调研、选定 LoRA、人形 ref 参数、序列分镜、QC。

---

## 2. 与旧项目关系（Jack×V35）

- 风格默认仍倾向：**ILstyle @ ~1.2** on **Indigo Void Furry Fused XL NoobAI V35 fp32**。
- **不要**与 BRIL / v1 / BRI 画风互叠。
- 细节搭配、Fel QC、禁区见旧笔记（**勿整份复制**）：  
  `E:\ComfyUI-aki-v3\ComfyUI\models\loras\_notes_Jack_V35\Jack_V35_LoRA_搭配与效果.md`
- Extreme-Sex：T11 显示更偏 lewd micro/叙事；**干净外观 ref 优先不上 XS**（HumanForm v2 male = No Extreme-Sex）。

---

## 3. 输出目录约定

- QC / REVIEW **只**放：`E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\` 下  
  `REVIEW_YYYYMMDD_TF_*`
- **禁止 Desktop**（含中转）。
- 脚本：`E:\ComfyUI-aki-v3\scripts\comfy_tf_*.py` + 对应 `*_logs\`。

---

## 4. 本机已有疑似 TF 相关 LoRA（已核盘）

| 文件 | 大小 | 备注 |
|------|------|------|
| `transformation：LoraBYIL_transformation.safetensors` | **217.89 MB** (228,475,572 B) | SHA256 `6631A2A95804A26FB0E5277BA51D28407810A44D098A63FCAB58122FF4BC3535` = **BeerYeen Transformation (Furry) IL**（CivArchive/Civitai 系 `LoraBYIL_transformation`）；触发偏 `transformation`；V2 说明更擅 anthro↔human / anthro↔feral；评论：抬权重可稳住 snout/fur 但易吞角色辨识；有人反馈 **序列一致性一般**。序列阶段先试 **0.6 / 0.8 / 1.0** |
| `Species_Transformation_Concept_Illustrious.safetensors` | **218.13 MB** (228,551,828 B) | Civitai #1 versionId **2349624**；触发 `species_transformation`；权重试 **0.8–1.3**；作者 NEG 含女体词 → male Jack **必须清理** |
| `Mid_transformation.safetensors` | **217.88 MB** (228,470,212 B) | Mol_Keun v2 versionId **1043354**；SHA256 `B263135F303A7D154959578F0617579775CA09E6240D09621B4F8FC7BF311010`；触发 `transformation, mid transformation, transfur…`；作者 Strength **~0.8** Clip Skip **2**；Civitai Bearer 对本账号 401/download-auth，改从 HF mirror `75dhsx/MolKeun` 校验哈希落盘 |
| `Black-rat-furry,anthro,tranform,human：Black_Rat_StyleIllustrious.safetensors` | **217.88 MB** | **BRIL** 画风；名含 tranform/human，但 V35 笔记：anthro 模式触发只要 `black-rat-anthro`；**不当作通用 TF 概念 LoRA**；勿与 ILstyle 互叠 |
| `Blackratf：PonyXLBlackRat-KeanonWoods_ArtStyle-000007.safetensors` | **217.88 MB** | Pony 画风误命中；**非 TF** |
| `anubis, anthro, female：illustriousAnubis.safetensors` | **217.88 MB** | Anubis 物种向，非 TF 序列概念 |

**结论：** 本机已有可用 TF 概念底牌 **BeerYeen BYIL transformation**；序列仍建议补 shortlist 的 sequence/mid 专用款。

---

## 5. Civitai 调研（Illustrious / NoobAI 兼容 TF）

检索时间：2026-11-01；API + 作者页 + CivArchive 评论。评论 API 多无正文，坑点综合自 Usage Tips / 邻近 TF 帖。

### 5.1 Shortlist（下载优先级，**尚未批量下载**）

| # | 名称 | URL | model id / best version | 大小 | 触发词 | 权重 / 设置（作者+社区） | Jack TF 利弊 | 本机？ |
|---|------|-----|-------------------------|------|--------|---------------------------|--------------|--------|
| 1 | **Species Transformation (Concept) [IL]** | https://civitai.com/models/2076546 | **2076546 / 2349624** (`Species_Transformation_Concept_Illustrious.safetensors`) | ~218 MB | `species_transformation`；序列示例：transformation sequence / multiple views / human to anthro / mid transformation / cutaway | **0.8–1.3**；Clip Skip 1 | **最贴合序列分镜**；⚠ 作者示例 NEG 含 `1girl, female, breasts…`——女性 Jack **必须删**；可能与 ILstyle 抢风格 | 否 |
| 2 | **Transfur / Mid transformation** (Mol_Keun) | https://civitai.com/models/913269 | **913269 / 1043354 v2.0** (`Mid_transformation.safetensors`) | **217.88 MB** (228,470,212 B) | `transformation, mid transformation, transfur, furry, anthro [Species]` | Usage Tips **Strength 0.8**；Clip Skip **2** | 下载量最高；专攻 mid；过高易 melt/吞身份 | **是**（2026-11-01；Civitai token `/me` 401 → HF mirror 哈希校验） |
| 3 | **Transfur - Transformation** (Midnightcrawler) | https://civitai.com/models/1263452 | **1263452 / 1428109 v1.0** (`transformationv2.safetensors`) | 217.88 MB bf16 | `mid transformation, transfur, transformation, female, human` | Steps 30；CFG **5–7** | 触发含 **female, human**，对 Jack 过渡友好 | 否 |
| 4 | **Transformation (Furry) IL** BeerYeen / BYIL | CivArchive mirrors / Civitai BeerYeen 系 | 本地文件即此系；另有 *Trans Thru Sex* 变体 SHA≠本地 | 217.89 MB | `transformation`（及 e621 TF 标签变体） | 社区：抬权重↑覆盖更稳但角色糊；标签加权优于盲目加 LoRA；有人说序列不一致 | **已在盘**；先做权重扫再决定是否另下 Thru-Sex 变体 | **是** |
| 5 | **Monstrifex** IL | https://civitai.com/models/2525768 | **2525768 / 2838883** (`Monstrifexv2.safetensors`)（勿下 Anima） | ~189 MB | `monstrifex` + `pre-transformation` / `early` / `mid-transformation` / `post transformation` | **勿同帧堆冲突阶段词**；pre 偏人类需 prompt 辅助 | 内建 4 阶段利于分镜；偏 monster/尖刺，需压 | 否 |
| 6 | **Gender Transition Slider - IL** | https://civitai.com/models/466010 | **466010 / 1981172** | **8.38 MB** | 无强触发 | IL：**数值越高越男性**；要男可加 `beard` | Jack 主线 female，默认不需要；可随时下 | 否 |
| 7 | **Gender transformation** | https://civitai.com/models/1947555 | **1947555 / 2207370** | 217.88 MB | `gender_transformation` | 竖构图差；推荐 mirror / potion / partition | 偏 TG 叙事，非物种 TF | 否 |
| 8 | **transformación.** | https://civitai.com/models/2210338 | **2210338 / 2488535** | 217.87 MB | `transformation` / `gender change` / `tf` / `tg` / `mid transformation` | 作者自训补 TF 不稳 | 通用备选，下载量低 | 否 |

**明确不进默认下载：** Transfurs (Changed Special) goo/latex（https://civitai.com/models/2012796）— 除非 Fel 要 Changed 线。

### 5.2 人形 / humanization 结论

- 通用 IL “anthro→human humanization” LoRA **稀缺**（多为角色特化 humanization）。
- Pony 的 Human–Anthro Slider（365856）**不进 IL 默认栈**。
- 人形 ref 阶段：靠 **Fel 锁定的 1boy human male POS + 强 NEG anthro/fur/snout/female/muscular** + ILstyle 画风；不必为 ref 阻塞下载。

### 5.3 常见坑检查表

1. 权重过高 → melt / 身份丢失；mid 类先 ~0.8。  
2. 阶段词互斥（pre/mid/post）。  
3. POS：TF 触发靠前 → 物种/身份 → 姿态；ILstyle 触发勿与 BRIL 混。  
4. Species Transformation 作者 NEG 反女 → 复制必清理。  
5. ILstyle × TF 概念会互相拉扯 → 序列阶段单独做权重矩阵。  
6. 珠宝 NEG 继续。  
7. NSFW mid-TF 手部/破衣易炸 → 先锁干净外观。

---

## 6. 空白区（持续填充）

### 6.1 选定 LoRA（待 Fel 确认）

- **已下载：** #1 Species Transformation + #2 Mid transformation v2（#3 Midnightcrawler **暂跳过**）。  
- 本地扫：`LoraBYIL_transformation` @0.6/0.8/1.0；Species @0.8–1.3；Mid @~0.8 CS2。  
- Gender slider / Changed goo：默认不下。

### 6.2 人形 ref 参数

见 §7。

### 6.3 序列分镜

- 待人形锁定（v2 male）：Human 100% → early → mid → late → Anubis 终点（性别待 Fel 确认）。  
- 分镜表 / 种子锁 / i2i：空白。

---

## 7. HumanForm refs v1（2026-11-01）— **WRONG / DISCARDED**

> **作废。** Fel 纠正：人类形态 **不是** muscular female。v1 文件夹保留不删，仅作废参考；后续一律用 **v2 male**。

- 目标（错误）：female human Jack / muscular athletic woman
- 文件夹（保留不删）：E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_HumanForm_refs_v1
- 脚本：E:\ComfyUI-aki-v3\scripts\comfy_tf_human_refs_v1.py
- 栈：V35 + ILstyle@1.2；无 Extreme-Sex；BASE / Smooth@0.7 / Fallen@0.4；euler_a 35 CFG5 1024×1536
- 结果：12 ok / 0 fail @ 2026-11-01 13:30:57 Asia/Hong_Kong — **外观方向错误，勿再引用为身份锁**

### 7.1 锁定人形外观（Fel POS，权威）

以下为 Fel 纠正后的 **HumanForm 外观 POS 正文**（完整保存；生成时身份/衣着/发型以此为准）：

`
1boy, solo, completely human male, no tail,
175cm tall, slim lean build, skinny weak physique,
ordinary medium short male hairstyle, typical short men's haircut, back and sides, yellow hair, prominent thick bangs covering forehead, slightly messy short yellow hair, hair not long at the back, short hair overall,
blue eyes, wearing black-framed glasses, black glasses frames, black rimmed glasses,
purple t-shirt, casual purple tee,
(casual khaki shorts:1.65), regular knee-length khaki shorts, simple plain khaki shorts, normal casual shorts, straight leg khaki shorts, no bib, no suspenders, no straps, no harness, no overalls,
sneakers, athletic shoes,
detailed human face, handsome young man, soft expression, light skin tone, completely human appearance,
`

> **发型注（2026-11-01）：** §7.1 短发措辞已被 Fel 自绘参考覆盖。衣着/眼镜/体型仍以本节为准；**头发以 §8.1 + §10 v3 hair POS 为准**（中长蓬乱黄发）。

**NEG 要点（对齐 T10 珠宝习惯 + 人形纠偏）：** 杀 anthro / furry / snout / animal ears / tail；muscular / hyper；female / breasts；long hair；bib / overalls / suspenders / harness；(jewelry:1.55) 及 ear jewelry / metal accessories / earrings / piercings / chains 等（同 T10）；**不要**把衣服整体塞进 NEG（需要 purple tee / khaki shorts / sneakers）。

---

## 8. HumanForm refs v2 male（2026-11-01）

- 目标：**completely human male Jack**（Fel POS 锁定；slim/weak，非肌肉；黄短发+厚刘海；蓝眼；黑框眼镜；紫T；卡其短裤；运动鞋）。
- 文件夹：E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_HumanForm_refs_v2_male
- 脚本：E:\ComfyUI-aki-v3\scripts\comfy_tf_human_refs_v2_male.py
- 栈：V35 fp32 + **ILstyle@1.2**；**无 Extreme-Sex**；无 anthro LoRA；多数 BASE，可选 Smooth_Booster@0.7 / Fallen@0.4 轻细节子集
- 采样：euler_a / normal，35，CFG5，1024×1536，FULL
- seeds：20261101–04；poses：front stand + 3/4 stand
- 目标约 12 张（BASE×8 + Smooth×2 + Fallen×2）
- 文件名例：TF_Human_v2_male_BASE_ILstyle1.2_front_s20261101.png（无 CFG 噪音）
- 结果计数 / 观感：12 ok / 0 fail — 跑完于 2026-11-01 13:46:41 Asia/Hong_Kong（human-lock reinforced rerun）

- 文件示例：TF_Human_v2_male_BASE_ILstyle1.2_front_s20261101.png, TF_Human_v2_male_BASE_ILstyle1.2_front_s20261102.png, TF_Human_v2_male_BASE_ILstyle1.2_front_s20261103.png, TF_Human_v2_male_BASE_ILstyle1.2_front_s20261104.png, TF_Human_v2_male_BASE_ILstyle1.2_q3_s20261101.png, TF_Human_v2_male_BASE_ILstyle1.2_q3_s20261102.png…
- 栈实跑：V35 + ILstyle@1.2；**无 Extreme-Sex**；BASE×8 + Smooth@0.7×2 + Fallen@0.4×2；poses front/q3；seeds 20261101–04；Fel male POS + 强化 human/anti-anthro
- 抽检（reinforced）：BASE front/q3 + Smooth front + Fallen q3 + front/q3 s20261103 — **完全人类男性**（无吻部/兽耳/毛皮/尾巴）；黄短发+厚刘海、蓝眼、黑框眼镜、紫T、卡其短裤、运动鞋、slim/weak 可读。
- 备注：首轮同栈曾泄漏白肤 anthro（吻部/兽耳）；已强化 human/anti-anthro 权重并重跑；首轮泄漏图归档于同目录 _pass1_anthro_leak_archive\（勿当身份锁）。

---


## 8.1 Fel keepers — HumanForm v2 male（2026-11-01）

- Fel 批准 **2** 张 v2 male keepers（chat）：正面站立 / 紫T / 卡其短裤 / 偏短黄发 / 眼镜。
- 文件夹：`E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_HumanForm_refs_v2_male`
- 用途：人形身份 + **衣着锁**（紫T + 卡其短裤 + 运动鞋）基准；后续 TF 序列起点外观。
- **发型升级：** Fel 另提供自绘人设参考（2026-11-01）→ 衣服 **保持**（勿改成参考图的工装裤/登山靴）；头发改为 **中长蓬乱黄发**（过耳、及颈/后颈、厚刘海盖额、分层凌乱尖刺）。**不是** back-and-sides / buzz。见 §10 v3 hair。

## 9. 下一步建议

1. ~~Fel 目视 HumanForm v2 male~~ → **2 keepers 已批**；衣着锁保留。  
2. ~~下载 #1+#2~~ → **已落盘**；#3 暂跳过。  
3. Fel 目视 **v3 hair** 小批 → 锁中长黄发。  
4. 把 ChatGPT 分镜 brief 跑出的 4–6 阶段 POS + LoRA 权重 → 写分镜表；起点 = v3 hair human lock（物种终点仍 TBD / 可按 charcoal anthro dog·Anubis-like）。  
5. 最小矩阵 ≤12 gens 验证 Species/Mid/BYIL 权重后再拉长序列。

---


## 10. HumanForm refs v3 hair (2026-11-01 14:17:16 Asia/Hong_Kong)

- 目标：衣服不变（紫T+卡其短裤+运动鞋）；发型改为 Fel 自绘参考的 **中长蓬乱黄发**（过耳/及颈、厚刘海盖额、分层凌乱）。
- 文件夹：E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_HumanForm_refs_v3_hair
- 脚本：E:\ComfyUI-aki-v3\scripts\comfy_tf_human_refs_v3_hair.py
- 栈：V35 fp32 + ILstyle@1.2；**无 Extreme-Sex**；**无 detail LoRA**；BASE only
- 采样：euler_a / normal，35，CFG5，1024×1536；poses front×3 + q3×3；seeds 20261111–13
- 结果：6 ok / 0 fail — 2026-11-01 14:17:16 Asia/Hong_Kong
- 文件：TF_Human_v3_hair_BASE_ILstyle1.2_front_s20261111.png, TF_Human_v3_hair_BASE_ILstyle1.2_front_s20261112.png, TF_Human_v3_hair_BASE_ILstyle1.2_front_s20261113.png, TF_Human_v3_hair_BASE_ILstyle1.2_q3_s20261111.png, TF_Human_v3_hair_BASE_ILstyle1.2_q3_s20261112.png, TF_Human_v3_hair_BASE_ILstyle1.2_q3_s20261113.png


## 11. Fel ChatGPT / 教学包指针（只读，勿改写包内文件）

- 路径：E:\CODEX\ComfyUI\教学总手册\Furry_TF序列资料\
- 内容：Furry_TF序列参考资料.html + 资料来源.json（R01–R12）+ 空白 阶段规划表_填写用.txt + 核查记录.json + 开始阅读.txt
- 阅读顺序：先 **R01 / R02 / R04**（anthro/hybrid 造型、werewolf TF 分镜、i2i 序列方法），再按部位与工具查其余条目。
- 与本机关系：六行规划表是分镜规划，**不是**把现有 T11 四阶段工作流扩成六格；额外格可单独制作。映射到既有 **T11 四阶段** workflow。
- **不要改写**该资料包；配方与 Jack 实操只写本笔记。填表产出贴回本笔记 §分镜。
- 录入：2026-11-01 14:18:43 Asia/Hong_Kong


## 变更日志

- 2026-11-01：笔记增加 §11 指针 → Fel ChatGPT 包 Furry_TF序列资料（R01–R12 / 阶段规划表；不改写包）。
- 2026-11-01：Fel 批 v2 male **2 keepers**；自绘参考锁 **更长蓬乱黄发**（衣着不变）；下载 Species(2349624) + Mid(1043354/HF)；启动 HumanForm **v3 hair** 小批。
- 2026-11-01：创建笔记 + 指针；核盘本地 TF（确认为 BeerYeen BYIL）；Civitai shortlist；启动 HumanForm refs v1；出图完成 12/12。
- 2026-11-01：Fel 纠正人类形态为 **1boy slim male**（非肌肉女）；**标记 HumanForm v1 WRONG/discarded**；锁定 §7.1 POS；启动 HumanForm refs v2 male；首轮 anthro 泄漏后 **human-lock reinforced 重跑** 12/12 ok；泄漏图归档 _pass1_anthro_leak_archive。

## 2026-11-01 ILstyle bind + MidDiag Matrix A (ops)
- ILstyle bound: `blackrat_style：IllustriousBlackRat_Style.safetensors`
- Triggers: `blackrat_style, blackrat` (often also with score_9 / source_artwork in POS)
- Stage sheet filled/overwritten by ChatGPT: `E:\CODEX\ComfyUI\教学总手册\Furry_TF序列资料\阶段规划表_填写用.txt`
- Endpoint draft: male jackal / Anubis-inspired charcoal short fur (NOT Queen / old female endpoint)
- Spec: `Jack_男性犬科TF_最小测试矩阵.json`; run A01-A08 only this pass; B deferred
- Stamp: 2026-11-01 14:43 (Asia/Hong_Kong)


## V2 MidDiag MatrixA run — 2026-11-01 (Asia/Hong_Kong)
- Ran V2_A01–V2_A08 only (B skipped). Folder: `Jack_Test/REVIEW_20261101_TF_MidDiag_MatrixV2A`.
- Runner: `E:\ComfyUI-aki-v3\scripts\run_matrix_V2A.py` (schema_version=2; POS/NEG full REPLACE).
- Params: V35 fp32, ILstyle 1.2/1.2, T02 OpenPose pose_wave str0.7 end0.85 IP off, 832x1216 euler_a 22 CFG7 clip-2, seed 2026110101.
- Spec status set to `V2_A_group_done`. T11 untouched.
- Files: V2_A01_BASE_w0_s2026110101.png, V2_A02_Species_w0.8_s2026110101.png, V2_A03_Species_w1.0_s2026110101.png, V2_A04_Mid_w0.6_s2026110101.png, V2_A05_Mid_w0.8_s2026110101.png, V2_A06_BYIL_w0.6_s2026110101.png, V2_A07_BYIL_w0.8_s2026110101.png, V2_A08_BYIL_w1.0_s2026110101.png

---

## Matrix V3 S01 (2026-11-01 Asia/Hong_Kong)

- **Status:** S01_done — **STOP** for Fel QC; S02–S06 not run; **T11 untouched**.
- **Script:** `E:\ComfyUI-aki-v3\scripts\run_matrix_V3_S01_T03.py`
- **Output:** `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_MidDiag_MatrixV3\S01_00001_.png`
- **prompt_id:** `b8544764-c610-4014-a5cd-00f580dd265f`
- **Params:** ckpt=indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors; ILstyle=blackrat_style：IllustriousBlackRat_Style.safetensors@0.40/0.40; TF_LoRA=OFF; 832x1216; steps=28; CFG=5; euler_ancestral/normal; clip=-2; denoise=0.45; seed=2026110101; lineart_CN=noob-sdxl-controlnet-lineart_realistic.fp16.safetensors@0.80/0-0.90; OpenPose=OFF; IP=OFF
- **TF LoRAs:** OFF; ILstyle 0.40/0.40; V35 fp32; 832×1216; 28/CFG5/euler_a/clip-2; OpenPose OFF; IP OFF; denoise 0.45; lineart CN 0.80/0–0.90.

---

## Matrix V3 S01 redraw retest R01/R02 (2026-11-01 Asia/Hong_Kong)

- **Status:** R01+R02 done — **STOP**; no chain; **T11 untouched**.
- **Script:** `E:\ComfyUI-aki-v3\scripts\run_matrix_V3_S01_T03.py`
- **Outputs:** `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_MidDiag_MatrixV3\S01_R01_d065.png` ; `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_TF_MidDiag_MatrixV3\S01_R02_d075.png`
- **Params:** ILstyle 0.8/0.8; Lineart CN 0.5 end 0.75; denoise R01=0.65 R02=0.75; steps28 CFG5 euler_a; seed 2026110101; TF LoRAs OFF; OpenPose/IP OFF; 832x1216 V35.
- **Source:** each job independent from mid_color_draft (no R01→R02 chain).

---

## EARLY Klein nail-tip K01 (2026-11-01 Asia/Hong_Kong) — migrate_V3 localization

- **Migrate pack:** `E:\CODEX\ComfyUI\教学总手册\Furry_TF序列资料\本机方法迁移_V3\`
- **Mother QC form:** `初期母图验收_填写.json` — inspected `input\Jack_TF_V3\mid_color_draft.png` sha256 `71878694…ECE2`; **E1=false E6=false** (long pointed ears + solid black claws); E2–E5/E7 true; **source_semantic_pass=false** → no T03.
- **Klein:** 1/2 budget. API `api\EARLY_Klein_甲尖单点_API.json`; input mid_color_draft; seed 2026110101; 4step CFG1 euler; ILstyle OFF. prompt_id `120bcac1-24b7-43de-95bc-98aab116faee`.
- **Output:** `E:\ComfyUI-aki-v3\ComfyUI\output\Jack_Test\REVIEW_20261101_EARLY_KLEIN_NAIL\K01_00001_.png` (sha256 `BFBE4366…14EB`).
- **E6 after Klein:** still **fail** — nails shortened/mostly pale but claw/talon silhouette remains + ≥1 solid black plate; E1 ears unchanged fail. Do not auto-approve; no second seed this turn.
- **Next:** wait **Fel visual QC**; decide second Klein (ears) vs mask+paint tips. T03 blocked until source_semantic_pass.


---

## Fel QC revise E1/E6 (t166u) — 2026-11-01 17:24:53 +08:00 Asia/Hong_Kong

- **E1 = PASS**: pointed ears already match early TF; do **not** treat elongated tip-ears as fail (Fel).
- **E6 criteria revise**: nails should show **root-deep → tip-light charcoal gradient**; current fail mainly **RIGHT INDEX** finger entirely solid black (other nails better).
- Updated form: `初期母图验收_填写.json` — mother+K01 E1=true; E6=false with notes; **source_semantic_pass=false** until E6 fixed. Reviewer cite Fel t166u.
- No Comfy gens this turn. T03 still blocked.

