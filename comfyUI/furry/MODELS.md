# comfyUI/furry — required model names (list only)

Weights (`.safetensors` / `.ckpt` binaries) are **not** copied into this Cursor Project.
Install locally under ComfyUI `models/` as usual. Names mined from Jack TF notes, hand-cards, and EARLY Klein/T03 API JSON (2026-11-01).

## Checkpoints (ckpt)

| Name | Role |
|------|------|
| `indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors` | Primary NoobAI V35 stack for Jack TF / EARLY T03 |
| `indigoVoidFurryFusedXL_noobaiV33.safetensors` | Older V33 variant mentioned in notes |

## Style / character LoRAs

| Name | Role |
|------|------|
| `IllustriousBlackRat_Style.safetensors` | ILstyle (`blackrat_style`) — primary style for EARLY mother |
| `Black_Rat_StyleIllustrious.safetensors` | BRIL anthro style — do **not** stack with ILstyle |
| `blackrat_illustrious_v1.safetensors` | BR v1 style alternate |
| `illustriousAnubis.safetensors` | Anubis species (prompts / Anubis modular) |
| `PonyXLBlackRat-KeanonWoods_ArtStyle-000007.safetensors` | Pony style; notes mark as non-TF |

## TF / transformation LoRAs

| Name | Role |
|------|------|
| `LoraBYIL_transformation.safetensors` | BeerYeen Transformation (Furry) IL |
| `Species_Transformation_Concept_Illustrious.safetensors` | Species transformation concept |
| `Mid_transformation.safetensors` | Mid / transfur (Mol_Keun) |
| `transformationv2.safetensors` | Midnightcrawler transfur |
| `Monstrifexv2.safetensors` | Staged monster TF (optional) |

## Detail / enhancer LoRAs (optional stack on single style)

| Name |
|------|
| `Extreme-Sex-v2.0-IllustriousXLNoobAI.safetensors` |
| `Add_Details_Slider_IL_v1.2.safetensors` |
| `AddMicroDetails_Illustrious_v7.safetensors` |
| `AddMicroDetails_NoobAI_v5.safetensors` |
| `BSS_Detail_Enhancer_Slider_v3.safetensors` |
| `Detail_enhancer_IL_v2.safetensors` |
| `Detail_Slider_IL_ShedTheSkin_v1.safetensors` |
| `Detailer_FallenIncursio_v1.safetensors` |
| `detaILeReij_v2.safetensors` |
| `DetailerIL_Jedas_v2.safetensors` |
| `NoobAI_XL_Detailer_EPS1.1_v1.safetensors` |
| `Smooth_Booster_v5.safetensors` |
| `Smooth_Lighting_Enhancer_NoobAI_v2.safetensors` |
| `FluffyFur_Illustrious.safetensors` |
| `TrendCraft_v2.4I_Illustrious.safetensors` |

## ControlNet / adapters (CN)

| Name | Role |
|------|------|
| `noob-sdxl-controlnet-lineart_realistic.fp16.safetensors` | Lineart CN for EARLY T03 (approved_lineart) |
| `noobaiXLControlnet_openposeModel.safetensors` | OpenPose (often OFF in EARLY runs) |
| `ip-adapter-plus_sdxl_vit-h.safetensors` | IP-Adapter SDXL |
| `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | IP-Adapter CLIP vision |

## Klein / FLUX2 edit stack (EARLY nail / local instruction edit)

| Name | Role |
|------|------|
| `flux-2-klein-4b-fp8.safetensors` | Klein 4B UNet (fp8) |
| `qwen_3_4b.safetensors` | FLUX2 text encoder / CLIP |
| `flux2-vae.safetensors` | FLUX2 VAE |

## Notes

- Do **not** load SDXL style LoRAs (e.g. ILstyle) on the Klein/FLUX2 graph.
- Secrets (`civitai_auth.env`, cookies, tokens) are intentionally excluded from this tree.
- Repo layout target: `comfyUI/furry/...` alongside stub `comfyUI/anime/` in the same FelXu/Data project (existing PR #1 only added `comfyUI/README`).
