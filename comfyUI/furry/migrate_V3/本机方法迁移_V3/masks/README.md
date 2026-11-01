# 蒙版约定（仓库无真实 ROI PNG）

仓库**没有**蒙版 PNG，也**没有** T06 / T06b / T06c 工作流本体。这些只在本机教学总手册：

- `E:\CODEX\ComfyUI\教学总手册\场景实操模板\workflows\T06_已有图局部微调_统一裁框回贴.json`
- `E:\CODEX\ComfyUI\教学总手册\场景实操模板\workflows\T06b_已有图局部重建_统一裁框回贴.json`
- `E:\CODEX\ComfyUI\教学总手册\场景实操模板\workflows\T06c_裁框与蒙版检查_不采样.json`
- API 同目录 `api\T06_*.json` / `T06b_*.json`（见规格 `T06_node_contract.templates`）

本目录**不伪造**蒙版图冒充真 ROI。云端也未从本机拷贝 T06。

## 本机应拷贝的路径与命名

按规格与历史脚本约定，建议放在 ComfyUI 输入树：

```
E:\ComfyUI-aki-v3\ComfyUI\input\Jack_TF_V3\masks\
  {job_id}_edit.png      # 白=允许改，黑=保留（与图同尺寸）
  {job_id}_protect.png   # 保护区（眼镜、黄发、未改甲根等）；外扩羽化后再扣回
```

通过母图相关输入另见：

```
E:\ComfyUI-aki-v3\ComfyUI\input\Jack_TF_EARLY\
  base_color.png           # 本机底图（文生）
  source_after_review.png  # 修完待验源
  approved_color.png       # 七项通过后
  approved_lineart.png     # 从最终色稿零采样重提
```

若仍用中期布局参考（仅构图，非通过）：`input\Jack_TF_V3\mid_color_draft.png`。

## 空模板尺寸约定（手绘灰度时）

| 约定 | 值 |
|---|---|
| 全图画幅 | **832 × 1216**（与色稿同尺寸；禁止沿用别图坐标） |
| 色彩 | 灰度；**白=改，黑=留**（LoadImageMask 选 red 时同语义） |
| T06 推荐 | denoise **0.30**（0.25–0.40），关线稿，ILstyle 0.60/0.60；只遮甲尖小块 |
| T06b 推荐 | denoise **0.60**（0.55–0.65）；蒙版包住旧突出、新轮廓与中间背景 |
| 节点外扩 | 57 expand=8（工作像素）；64 blur_radius=4 / sigma=1（原图像素）；外扩后再扣保护区 |
| 工作边长 | 节点 73 通常 **1024**；ROI 70/71/72 必须从当张图与蒙版实测 |

可在本机用纯黑 832×1216 PNG 作「空白 edit 画布」再手绘白区；**不要**把空白文件提交进仓库冒充已画 ROI。
