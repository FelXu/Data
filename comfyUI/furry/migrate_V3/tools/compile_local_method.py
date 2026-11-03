"""Legacy compiler for robot_local_method_transfer_spec.

Current EARLY mother specs use kind=robot_early_structure_migration_spec.
Use compile_early_mother.py for 底图→甲尖 Klein assembly. This file never submits jobs.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import uuid
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "Jack_男性犬科TF_最小测试矩阵.json"
EARLY_KIND = "robot_early_structure_migration_spec"
LEGACY_KIND = "robot_local_method_transfer_spec"


def make_graph(spec, job):
    p = spec["sampling_defaults"]
    style = spec["style"]
    cn = spec["lineart"]
    effective_cn = job["lineart_strength"] if job["lineart_enabled"] else 0.0
    if job["denoise"] <= 0.5 and effective_cn >= 0.75:
        raise ValueError("Forbidden: denoise<=0.5 AND effective Lineart>=0.75")
    assert spec["checkpoint"] == "indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors"
    assert style["filename"] == "blackrat_style：IllustriousBlackRat_Style.safetensors"
    assert all(not m["enabled"] for m in spec["transformation_loras"].values())
    graph = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": spec["checkpoint"]}},
        "990": {"class_type": "CLIPSetLastLayer", "inputs": {"clip": ["1", 1], "stop_at_clip_layer": -2}},
        "2": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0],
                "clip": ["990", 0],
                "lora_name": style["filename"],
                "strength_model": style["strength_model"],
                "strength_clip": style["strength_clip"],
            },
        },
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": spec["prompts"]["positive_full"]}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": spec["prompts"]["negative_full"]}},
        "900": {"class_type": "LoadImage", "inputs": {"image": spec["inputs"]["color"]["comfy_input_relative"]}},
        "901": {
            "class_type": "ImageScale",
            "inputs": {
                "image": ["900", 0],
                "upscale_method": "lanczos",
                "width": 832,
                "height": 1216,
                "crop": "disabled",
            },
        },
        "902": {"class_type": "VAEEncode", "inputs": {"pixels": ["901", 0], "vae": ["1", 2]}},
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["2", 0],
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["902", 0],
                "seed": p["seed"],
                "steps": p["steps"],
                "cfg": p["cfg"],
                "sampler_name": p["sampler"],
                "scheduler": p["scheduler"],
                "denoise": job["denoise"],
            },
        },
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": job["output_prefix"]}},
    }
    if job["lineart_enabled"]:
        graph.update(
            {
                "50": {"class_type": "LoadImage", "inputs": {"image": spec["inputs"]["lineart"]["comfy_input_relative"]}},
                "51": {
                    "class_type": "ImageScale",
                    "inputs": {
                        "image": ["50", 0],
                        "upscale_method": "lanczos",
                        "width": 832,
                        "height": 1216,
                        "crop": "disabled",
                    },
                },
                "52": {"class_type": "ControlNetLoader", "inputs": {"control_net_name": cn["model"]}},
                "53": {
                    "class_type": "ControlNetApplyAdvanced",
                    "inputs": {
                        "positive": ["3", 0],
                        "negative": ["4", 0],
                        "control_net": ["52", 0],
                        "image": ["51", 0],
                        "strength": job["lineart_strength"],
                        "start_percent": cn["start"],
                        "end_percent": cn["end"],
                        "vae": ["1", 2],
                    },
                },
            }
        )
        graph["6"]["inputs"].update(positive=["53", 0], negative=["53", 1])
    for node in graph.values():
        for value in node["inputs"].values():
            if isinstance(value, list):
                assert len(value) == 2 and value[0] in graph and isinstance(value[1], int)
    assert graph["8"]["inputs"]["images"] == ["7", 0]
    assert graph["7"]["inputs"]["samples"] == ["6", 0]
    return graph


def compile_mode(mode=None):
    spec = json.loads(SPEC_PATH.read_text("utf-8-sig"))
    kind = spec.get("kind")
    if kind == EARLY_KIND:
        raise SystemExit(
            "Current matrix/spec kind is robot_early_structure_migration_spec. "
            "This legacy compiler requires robot_local_method_transfer_spec. "
            "Use: python tools/compile_early_mother.py --mode base_then_nail"
        )
    assert kind == LEGACY_KIND, f"Unexpected kind={kind!r}"
    mode = mode or spec["selected_mode"]
    if mode not in spec["modes"]:
        raise ValueError(f"Unknown mode {mode}")
    selected = spec["modes"][mode]["jobs"]
    assert 1 <= len(selected) <= spec["maximum_total_images"] == 2
    tag = "REVIEW_20261101_Jack_METHOD_" + uuid.uuid4().hex[:8]
    out = ROOT / "本机方法迁移_V3" / "api" / tag
    out.mkdir(parents=True, exist_ok=False)
    spec["selected_mode"] = mode
    spec["jobs"] = []
    for recipe in selected:
        job = copy.deepcopy(recipe)
        job.update(
            status="prepared_not_submitted",
            batch_size=1,
            images=1,
            seed=spec["sampling_defaults"]["seed"],
            source="inputs.color",
            transformation_lora=None,
            output_prefix=f"Jack_Test/{tag}/{recipe['id']}",
            positive_text=spec["prompts"]["positive_full"],
            negative_text=spec["prompts"]["negative_full"],
        )
        path = out / (job["id"] + ".json")
        graph = make_graph(spec, job)
        path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", "utf-8")
        job["api_graph_file"] = str(path)
        job["api_graph_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        spec["jobs"].append(job)
    spec["status"] = "method_prepared_not_submitted"
    spec["active_run_tag"] = tag
    SPEC_PATH.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", "utf-8")
    return {"mode": mode, "jobs": len(spec["jobs"]), "api_directory": str(out), "submitted": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["lineart_ablation", "denoise_pair"])
    args = parser.parse_args()
    print(json.dumps(compile_mode(args.mode), ensure_ascii=False, indent=2))
