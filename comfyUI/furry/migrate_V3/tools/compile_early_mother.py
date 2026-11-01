"""Assemble EARLY mother API graphs from the current early-structure spec; never submit."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "本机方法迁移_V3"
SPEC_CANDIDATES = (
    PKG / "A_机器人规格_初期结构准确.json",
    ROOT / "Jack_男性犬科TF_最小测试矩阵.json",
)
EXPECTED_KIND = "robot_early_structure_migration_spec"


def load_spec() -> tuple[dict, Path]:
    for path in SPEC_CANDIDATES:
        if path.is_file():
            spec = json.loads(path.read_text("utf-8-sig"))
            if spec.get("kind") == EXPECTED_KIND:
                return spec, path
    raise SystemExit(
        f"No {EXPECTED_KIND} found. Old compile_local_method.py still expects "
        "robot_local_method_transfer_spec; use this script for EARLY mother."
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_base_graph(spec: dict, output_prefix: str) -> dict:
    p = spec["sampling_defaults"]
    style = spec["style"]
    assert spec["checkpoint"] == "indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors"
    assert style["filename"] == "blackrat_style：IllustriousBlackRat_Style.safetensors"
    assert float(style["strength_model"]) == 0.8
    assert float(style["strength_clip"]) == 0.8
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": spec["checkpoint"]},
            "_meta": {"title": "底模｜V35"},
        },
        "990": {
            "class_type": "CLIPSetLastLayer",
            "inputs": {"clip": ["1", 1], "stop_at_clip_layer": -2},
            "_meta": {"title": "CLIP 最后一层 = -2"},
        },
        "2": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0],
                "clip": ["990", 0],
                "lora_name": style["filename"],
                "strength_model": style["strength_model"],
                "strength_clip": style["strength_clip"],
            },
            "_meta": {"title": "ILstyle｜默认 0.8/0.8"},
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["2", 1], "text": spec["prompts"]["positive_full"]},
            "_meta": {"title": "正面｜初期结构 POS"},
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["2", 1], "text": spec["prompts"]["negative_full"]},
            "_meta": {"title": "负面｜初期结构 NEG"},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": p["width"],
                "height": p["height"],
                "batch_size": p["batch_size"],
            },
            "_meta": {"title": "空 Latent｜832×1216"},
        },
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["2", 0],
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["5", 0],
                "seed": p["seed"],
                "steps": p["steps"],
                "cfg": p["cfg"],
                "sampler_name": p["sampler"],
                "scheduler": p["scheduler"],
                "denoise": 1.0,
            },
            "_meta": {"title": "采样｜固定种子文生图"},
        },
        "7": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["6", 0], "vae": ["1", 2]},
            "_meta": {"title": "解码"},
        },
        "8": {
            "class_type": "SaveImage",
            "inputs": {"images": ["7", 0], "filename_prefix": output_prefix},
            "_meta": {"title": "保存底图"},
        },
    }


def make_klein_graph(spec: dict, instruction_key: str, input_image: str, output_prefix: str) -> dict:
    k = spec["local_klein_option"]
    text = k["instructions"][instruction_key]
    return {
        "76": {
            "class_type": "LoadImage",
            "inputs": {"image": input_image},
            "_meta": {"title": "① 上传原图（点击选择文件）"},
        },
        "70": {
            "class_type": "UNETLoader",
            "inputs": {"unet_name": k["diffusion_model"], "weight_dtype": "default"},
            "_meta": {"title": "模型：Klein 4B FP8（已配好）"},
        },
        "71": {
            "class_type": "CLIPLoader",
            "inputs": {"clip_name": k["text_encoder"], "type": "flux2", "device": "default"},
            "_meta": {"title": "文字编码器：Qwen3 4B（已配好）"},
        },
        "72": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": k["vae"]},
            "_meta": {"title": "图像编码器：FLUX2 VAE（已配好）"},
        },
        "74": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": text, "clip": ["71", 0]},
            "_meta": {"title": "② 在这里填写改图指令（支持中文）"},
        },
        "80": {
            "class_type": "ImageScaleToTotalPixels",
            "inputs": {
                "image": ["76", 0],
                "upscale_method": "nearest-exact",
                "megapixels": 1.0,
                "resolution_steps": 16,
            },
            "_meta": {"title": "自动调整原图尺寸（约100万像素）"},
        },
        "99": {
            "class_type": "GetImageSize",
            "inputs": {"image": ["80", 0]},
            "_meta": {"title": "自动读取原图比例"},
        },
        "122": {
            "class_type": "VAEEncode",
            "inputs": {"pixels": ["80", 0], "vae": ["72", 0]},
            "_meta": {"title": "编码原图作为参考"},
        },
        "82": {
            "class_type": "ConditioningZeroOut",
            "inputs": {"conditioning": ["74", 0]},
            "_meta": {"title": "空负面条件（无需填写）"},
        },
        "121": {
            "class_type": "ReferenceLatent",
            "inputs": {"conditioning": ["82", 0], "latent": ["122", 0]},
            "_meta": {"title": "原图参考（负面分支）"},
        },
        "123": {
            "class_type": "ReferenceLatent",
            "inputs": {"conditioning": ["74", 0], "latent": ["122", 0]},
            "_meta": {"title": "原图参考（指令分支）"},
        },
        "63": {
            "class_type": "CFGGuider",
            "inputs": {
                "model": ["70", 0],
                "positive": ["123", 0],
                "negative": ["121", 0],
                "cfg": k["cfg"],
            },
            "_meta": {"title": "指令引导 CFG=1（保持默认）"},
        },
        "73": {
            "class_type": "RandomNoise",
            "inputs": {"noise_seed": k["seed"]},
            "_meta": {"title": "固定随机种子（可保持默认）"},
        },
        "61": {
            "class_type": "KSamplerSelect",
            "inputs": {"sampler_name": k["sampler"]},
            "_meta": {"title": "采样器 Euler（保持默认）"},
        },
        "62": {
            "class_type": "Flux2Scheduler",
            "inputs": {"steps": k["steps"], "width": ["99", 0], "height": ["99", 1]},
            "_meta": {"title": "Klein蒸馏采样：4步（保持默认）"},
        },
        "66": {
            "class_type": "EmptyFlux2LatentImage",
            "inputs": {"width": ["99", 0], "height": ["99", 1], "batch_size": 1},
            "_meta": {"title": "自动匹配原图比例"},
        },
        "64": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {
                "noise": ["73", 0],
                "guider": ["63", 0],
                "sampler": ["61", 0],
                "sigmas": ["62", 0],
                "latent_image": ["66", 0],
            },
            "_meta": {"title": "执行改图"},
        },
        "65": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["64", 0], "vae": ["72", 0]},
            "_meta": {"title": "解码改图结果"},
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"images": ["65", 0], "filename_prefix": output_prefix},
            "_meta": {"title": "③ 改图结果（自动保存到 output）"},
        },
    }


def write_graph(path: Path, graph: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", "utf-8")
    return sha256_file(path)


def compile_base_then_nail(
    *,
    klein_input: str,
    write_canonical: bool,
) -> dict:
    """Assemble 底图 → 甲尖 Klein from repo materials. Does not POST /prompt."""
    spec, spec_path = load_spec()
    tag = "REVIEW_20261101_EARLY_MOTHER_" + uuid.uuid4().hex[:8]
    out_dir = PKG / "api" / tag
    out_dir.mkdir(parents=True, exist_ok=False)

    base_prefix = f"Jack_Test/{tag}/B01_BASE"
    nail_prefix = f"Jack_Test/{tag}/K01_NAIL"
    base_graph = make_base_graph(spec, base_prefix)
    nail_graph = make_klein_graph(spec, "nail_tip_only", klein_input, nail_prefix)

    base_path = out_dir / "B01_BASE_empty_latent.json"
    nail_path = out_dir / "K01_NAIL_klein.json"
    jobs = [
        {
            "id": "B01_BASE",
            "operation": "empty_latent_txt2img",
            "api_graph_file": str(base_path),
            "api_graph_sha256": write_graph(base_path, base_graph),
            "seed": spec["sampling_defaults"]["seed"],
            "status": "prepared_not_submitted",
            "generates_images": 1,
            "ui_workflow": str(PKG / "EARLY_底图_空Latent文生图.json"),
            "frozen_params_doc": str(PKG / "EARLY_底图冻结参数.md"),
        },
        {
            "id": "K01_NAIL",
            "operation": "klein_nail_tip_only",
            "api_graph_file": str(nail_path),
            "api_graph_sha256": write_graph(nail_path, nail_graph),
            "seed": spec["local_klein_option"]["seed"],
            "input_image": klein_input,
            "status": "prepared_not_submitted",
            "generates_images": 1,
            "depends_on": "B01_BASE",
            "ui_workflow": str(PKG / "EARLY_Klein_甲尖单点编辑.json"),
            "note": "Replace LoadImage with the base output after B01 is reviewed; do not treat mid_color_draft as approved.",
        },
    ]

    manifest = {
        "kind": "early_mother_compile_manifest",
        "spec_kind": EXPECTED_KIND,
        "spec_path": str(spec_path),
        "spec_sha256": sha256_file(spec_path),
        "active_run_tag": tag,
        "submitted": False,
        "path": "base_empty_latent → klein_nail_tip",
        "jobs": jobs,
        "not_passing_mothers": [
            "early_approved/approved_color.png",
            "本机方法迁移_V3/初期母图验收_填写.json (M03 paint)",
        ],
        "local_only_still_required": [
            "model weight hashes",
            "T06/T06b/T06c copy from teaching pack",
            "real ComfyUI generation on 127.0.0.1:8188",
        ],
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )

    if write_canonical:
        # Refresh checked-in canonical API copies (same content, stable prefixes).
        write_graph(PKG / "api" / "EARLY_底图_空Latent文生图_API.json", make_base_graph(spec, "Jack_Test/REVIEW_20261101_EARLY_BASE/B01"))
        for key, name, prefix in (
            ("nail_tip_only", "EARLY_Klein_甲尖单点_API.json", "Jack_Test/REVIEW_20261101_EARLY_KLEIN_NAIL/K01"),
            ("ear_tips_only", "EARLY_Klein_耳尖单点_API.json", "Jack_Test/REVIEW_20261101_EARLY_KLEIN_EAR/K01"),
            ("nose_tip_only", "EARLY_Klein_鼻头单点_API.json", "Jack_Test/REVIEW_20261101_EARLY_KLEIN_NOSE/K01"),
        ):
            # Keep nail API input as-is in checked-in file; ear/nose default to same layout ref.
            write_graph(
                PKG / "api" / name,
                make_klein_graph(spec, key, "Jack_TF_V3/mid_color_draft.png", prefix),
            )

    return {
        "mode": "base_then_nail",
        "api_directory": str(out_dir),
        "jobs": len(jobs),
        "submitted": False,
        "klein_input": klein_input,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=["base_then_nail"],
        default="base_then_nail",
        help="Only base→nail is supported in this minimal compiler.",
    )
    parser.add_argument(
        "--klein-input",
        default="Jack_TF_EARLY/base_color.png",
        help="ComfyUI input-relative path for Klein LoadImage after base is saved.",
    )
    parser.add_argument(
        "--write-canonical",
        action="store_true",
        help="Also refresh checked-in api/EARLY_*_API.json copies.",
    )
    args = parser.parse_args()
    if args.mode != "base_then_nail":
        raise SystemExit(f"Unsupported mode: {args.mode}")
    print(json.dumps(compile_base_then_nail(klein_input=args.klein_input, write_canonical=args.write_canonical), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
