"""Validate a proposed run against the early-structure contract; never submit it.

Reads A_机器人规格_初期结构准确.json (or the same-content matrix). Numerical / hash
gates only — does not look at pixels. M03 paint + early_approved are archival and
are NOT treated as a currently passing mother unless a new review file says so.
"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "本机方法迁移_V3"
SPEC_CANDIDATES = (
    PKG / "A_机器人规格_初期结构准确.json",
    ROOT / "Jack_男性犬科TF_最小测试矩阵.json",
)
EXPECTED_KIND = "robot_early_structure_migration_spec"
# Archival only — Fel decided these are not reproducible Klein/empty-latent mothers.
ARCHIVAL_NOT_PASSING = (
    "early_approved/approved_color.png",
    "early_approved/approved_lineart.png",
    "本机方法迁移_V3/初期母图验收_填写.json (M03 paint path)",
)


def load_spec() -> dict:
    for path in SPEC_CANDIDATES:
        if path.is_file():
            spec = json.loads(path.read_text("utf-8-sig"))
            if spec.get("kind") == EXPECTED_KIND:
                return spec
    raise SystemExit(f"No {EXPECTED_KIND} found under {ROOT}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--operation", choices=["source_edit", "T03", "T06", "T06b", "base_txt2img"], required=True)
parser.add_argument("--generated-count", type=int, required=True)
parser.add_argument("--denoise", type=float, default=0.65)
parser.add_argument("--lineart-strength", type=float, default=0.0)
parser.add_argument("--review-file", type=Path)
args = parser.parse_args()
spec = load_spec()
errors = []
if not 0 <= args.generated_count < spec["maximum_total_images"]:
    errors.append("Selected run budget exhausted or invalid; maximum two images.")
if not 0 < args.denoise <= 1 or not 0 <= args.lineart_strength <= 1:
    errors.append("Invalid parameter range.")
if args.denoise <= 0.5 and args.lineart_strength >= 0.75:
    errors.append("Forbidden denoise<=0.5 AND effective Lineart>=0.75.")
if args.operation == "T03":
    if not args.review_file or not args.review_file.exists():
        errors.append("Approved source review file is required before T03.")
    else:
        review = json.loads(args.review_file.read_text("utf-8-sig"))
        if review.get("superseded_as_passing_mother") is True:
            errors.append(
                "Review file is marked superseded_as_passing_mother; do not treat M03/early_approved as current pass."
            )
        if review.get("source_semantic_pass") is not True:
            errors.append("Source semantic review has not passed.")
        checks = review.get("E1_to_E7", {})
        if any(checks.get(key) is not True for key in spec["early_stage_contract"]):
            errors.append("Every E1-E7 check must explicitly pass.")
        src = Path(review.get("source_file") or "__missing_source__")
        if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest() != review.get("source_sha256"):
            errors.append("Reviewed source file/hash does not match.")
if args.operation in ["T06", "T06b"]:
    errors.append(
        "Local ROI and mask/protection validation must be supplied to the region executor; "
        "this general checker does not authorize a local job. See 本机方法迁移_V3/masks/README.md."
    )
if args.operation == "base_txt2img" and args.denoise != 1.0:
    errors.append("Empty-latent EARLY base expects denoise=1.0.")
result = {
    "ready": not errors,
    "operation": args.operation,
    "errors": errors,
    "submitted": False,
    "spec_kind": spec.get("kind"),
    "archival_not_passing_mothers": list(ARCHIVAL_NOT_PASSING),
    "note": (
        "Passing numerical checks is not proof of semantic stability; "
        "source_edit / base_txt2img still require output review. "
        "Do not use early_approved or M03 paint as the reproducible mother."
    ),
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(2 if errors else 0)
