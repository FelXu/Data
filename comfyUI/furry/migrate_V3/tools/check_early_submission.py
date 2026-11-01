"""Validate a proposed run against the early-stage contract; never submit it."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--operation',choices=['source_edit','T03','T06','T06b'],required=True)
parser.add_argument('--generated-count',type=int,required=True)
parser.add_argument('--denoise',type=float,default=0.65)
parser.add_argument('--lineart-strength',type=float,default=0.0)
parser.add_argument('--review-file',type=Path)
args=parser.parse_args()
spec=json.loads((ROOT/'Jack_男性犬科TF_最小测试矩阵.json').read_text('utf-8-sig'))
errors=[]
if not 0<=args.generated_count<spec['maximum_total_images']:
    errors.append('Selected run budget exhausted or invalid; maximum two images.')
if not 0<args.denoise<=1 or not 0<=args.lineart_strength<=1:
    errors.append('Invalid parameter range.')
if args.denoise<=0.5 and args.lineart_strength>=0.75:
    errors.append('Forbidden denoise<=0.5 AND effective Lineart>=0.75.')
if args.operation=='T03':
    if not args.review_file or not args.review_file.exists():
        errors.append('Approved source review file is required before T03.')
    else:
        review=json.loads(args.review_file.read_text('utf-8-sig'))
        if review.get('source_semantic_pass') is not True:
            errors.append('Source semantic review has not passed.')
        checks=review.get('E1_to_E7',{})
        if any(checks.get(key) is not True for key in spec['early_stage_contract']):
            errors.append('Every E1-E7 check must explicitly pass.')
        src=Path(review.get('source_file') or '__missing_source__')
        if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest()!=review.get('source_sha256'):
            errors.append('Reviewed source file/hash does not match.')
if args.operation in ['T06','T06b']:
    errors.append('Local ROI and mask/protection validation must be supplied to the region executor; this general checker does not authorize a local job.')
result={'ready':not errors,'operation':args.operation,'errors':errors,'submitted':False,
        'note':'Passing numerical checks is not proof of semantic stability; source_edit still requires output review.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(2 if errors else 0)
