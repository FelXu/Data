# comfyUI/furry

Furry / Jack TF ComfyUI 文本与配置（笔记、migrate_V3、prompts、workflows、early_approved、MODELS.md）。

Sibling: `../anime/`（目前仅占位）。同一仓库同时放 furry 与 anime。
TF reference notes (markdown only): [`refs/`](refs/README.md).

## EARLY 母图流水线（现行）

入口在 `migrate_V3/本机方法迁移_V3/`：

1. 读 `开始阅读.txt` 与 `EARLY_底图冻结参数.md`
2. 底图：`EARLY_底图_空Latent文生图.json`（API 在 `api/`）
3. 甲尖 Klein：`EARLY_Klein_甲尖单点编辑.json`；耳/鼻另有单点副本
4. 组装脚本：`migrate_V3/tools/compile_early_mother.py`（`底图→甲尖`，不提交）
5. 蒙版约定：`masks/README.md`（仓库无真实 ROI / 无 T06 本体）

`early_approved/` 与历史 M03 涂改验收 JSON **仅归档**，不作现行通过母图。本轮不跑 T03。
