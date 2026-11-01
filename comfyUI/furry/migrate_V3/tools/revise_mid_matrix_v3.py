"""Write a gated sketch/img2img/inpaint specification; never submit image jobs."""
from pathlib import Path
import copy
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
COMFY = Path(r'E:\ComfyUI-aki-v3\ComfyUI')
TARGET = ROOT / 'Jack_男性犬科TF_最小测试矩阵.json'
old = json.loads(TARGET.read_text('utf-8-sig'))
if old.get('schema_version', 1) >= 3:
    raise SystemExit('V3 already exists; edit it directly rather than reset bindings or execution state.')
assert old.get('schema_version') == 2
archive = ROOT / 'verification/matrix_v2_failed_20261101'
archive.mkdir(parents=True, exist_ok=True)
for name in [TARGET.name, 'Jack_男性犬科TF_矩阵V2说明.txt', '阶段规划表_填写用.txt']:
    src = ROOT / name
    dest = archive / name
    if dest.exists() and dest.read_bytes() != src.read_bytes():
        raise RuntimeError(f'Different historical archive exists: {dest}')
    if not dest.exists():
        shutil.copy2(src, dest)

STYLE = copy.deepcopy(old['style'])
STYLE.update(strength_model=0.4, strength_clip=0.4,
             binding_rule='确切文件不变；V3结构诊断固定0.40/0.40，不沿用1.20。此值待测，未证明旧失败由风格权重单独造成。')
MODELS = copy.deepcopy(old['models'])
for model in MODELS.values():
    model['historical_trigger_words_not_used_in_v3'] = model.pop('trigger_selected', '')
    model['previous_v2_settings_not_used'] = {
        key: model.pop(key) for key in ['test_weights_model_equals_clip', 'recommendation_reason', 'recommendation_status'] if key in model
    }
    model['v3_enabled'] = False
    model['v3_strength_model'] = 0.0
    model['v3_strength_clip'] = 0.0
    model['v3_trigger_words'] = ''
    model['v3_decision'] = '本轮停用且不加载；保留文件与历史触发记录，不做任何权重筛选。'

PREFIX = 'blackrat_style, blackrat, clean illustration'
POS = (
    f'{PREFIX}, solo, single character, (adult male human Jack in an incomplete mid-transformation:1.3), '
    'golden-blond shaggy medium-length hair, thick bangs, blue eyes, '
    '(one intact pair of black rectangular glasses worn normally:1.25), '
    '(incomplete muzzle, human cheeks still visible:1.35), '
    'a tiny forward change at the nose tip and front jaw only, human lips and recognizable human facial planes, '
    'one original pair of ears partly lengthening, human-shaped ear bases, '
    '(short fur only on hands and forearms with a clear skin boundary:1.35), '
    'irregular fur fronts stopping below the elbows, bare human skin on the cheeks, neck, upper arms and lower legs, '
    'moderately expanding shoulders, upper back, chest and thighs, '
    '(clothes stretching on both shirt and shorts:1.3), '
    'his original human-sized opaque purple short-sleeved cotton T-shirt pulling tight across the chest, sleeves and underarm seams, '
    'his original khaki shorts pulling tight at the waistband, outer thigh seams and leg hems, '
    'fabric tension, radiating pulling folds and straining seams on BOTH garments, slight seam fraying with coverage maintained, '
    '(startled expression, mid-transformation panic:1.3), widened blue eyes, raised inner eyebrows, mouth slightly open in alarm, '
    'looking down at his changing hands held close in front of his chest, fingers spread, '
    'torso recoiling, shoulders tense, knees bent, staggered planted feet, '
    'closed sneakers, full body, three-quarter view, neutral gray background, no visible tail'
)
NEG = (
    'low quality, blurry, bad anatomy, extra character, duplicate character, extra limbs, extra fingers, fused fingers, '
    '(fully transformed anthro:1.5), (completed canine head:1.5), (long complete canine muzzle:1.5), '
    'full snout, dog head replacing the human face, furry cheeks, facial fur, '
    '(full fur coat:1.5), (fur-covered body:1.5), furry neck, furred upper arms, furry thighs, furry calves, '
    'uniform fur coverage, human face completely lost, completely unchanged human face, '
    '(fully transformed anthro already in fitted clothes:1.4), (ordinary werewolf costume:1.4), '
    '(unchanged slim human proportions:1.3), (intact perfectly fitted clothing:1.4), '
    'loose unstressed shorts, relaxed waistband, oversized shirt, newly tailored outfit, '
    '(calm pose:1.4), relaxed standing pose, greeting wave, hand waving above the head, '
    'calm expression, serene smile, confident grin, snarling wolf face, closed indifferent eyes, '
    'extra ears, two pairs of ears, duplicate glasses, falling glasses, bent glasses, broken glasses, '
    'wrong hair color, waist-length hair, white shirt, blue shirt, different outfit, long trousers, boots, '
    'extreme final-form bulk, missing shirt, missing shorts, disintegrating clothes, transparent clothes, '
    'bare torso, uncovered hips, exposed toes, visible tail, wings, horns, crown, necklace, '
    'cropped head, cropped feet, text, logo, watermark, multiple panels, collage'
)
LOCAL_QUALITY_NEG = 'low quality, blurry, bad anatomy, text, logo, watermark, color mismatch, inconsistent lighting, hard paste edge'

ASSETS = {
    'human_identity_reference': {
        'input_relative_path': None, 'binding_status': 'needs_selection',
        'required': '当前紫T/卡其短裤/运动鞋版成年男性Jack人类图；不是旧长裤靴子图，也不是V2完整兽人输出。仅用于人工对照与草稿取色，不启用IPAdapter。'
    },
    'mid_lineart': {
        'input_relative_path': 'Jack_TF_V3/mid_lineart.png', 'binding_status': 'needs_creation_and_review',
        'required': '832×1216不透明RGB，白底深线。明确画出极短前颌、人颊、同对过渡耳、惊慌脸与新姿势、增宽肩胸和大腿、上下两件衣料拉力褶。不得从V2全兽图直接提线。'
    },
    'mid_color_draft': {
        'input_relative_path': 'Jack_TF_V3/mid_color_draft.png', 'binding_status': 'needs_creation_and_review',
        'required': '与线稿像素对齐的832×1216不透明RGB色稿，脸/颈/上臂/小腿为人皮，灰黑短毛仅手与部分前臂；紫T、卡其短裤、黄发与正常眼镜已画好。不是在全兽图上简单涂颜色。'
    },
    'stage_edit_mask': {
        'input_relative_path_pattern': 'Jack_TF_V3/masks/{job_id}_edit.png',
        'binding_status': 'create_on_latest_accepted_canvas_before_each_local_job',
        'required': '832×1216不透明灰度PNG，白改黑留；LoadImageMask(channel=red)。不是透明PNG的alpha约定。'
    },
    'stage_protect_mask': {
        'input_relative_path_pattern': 'Jack_TF_V3/masks/{job_id}_protect.png',
        'binding_status': 'create_on_latest_accepted_canvas_before_each_local_job',
        'required': '同尺寸灰度PNG，白色是强制保护区；包含正常眼镜框/镜腿、黄发等与该区不应变化的像素。无保护内容时也须用同尺寸全黑图，不能省略或偷用旧女王mask。'
    }
}
for asset in ASSETS.values():
    rel = asset.get('input_relative_path')
    asset['file_exists_at_spec_write'] = bool(rel and (COMFY / 'input' / rel).exists())

base_job = {
    'id': 'V3_S01', 'operation': 'T03_lineart_plus_color_img2img',
    'source': 'input_assets.mid_color_draft', 'lineart': 'input_assets.mid_lineart',
    'seed': 2026110101, 'denoise': 0.45,
    'transformation_lora': None, 'strength_model': 0.0, 'strength_clip': 0.0,
    'positive_text': POS, 'negative_text': NEG,
    'batch_size': 1, 'images': 1, 'run_if': 'all_structural_inputs_bound_and_visually_passed',
    'acceptance': '必须全部通过base_gates；完整吻、全身毛、仅上衣受力或平静挥手任一出现即整轮停止，不进入局修。',
    'failure_action': 'stop_entire_run_no_retry_no_B', 'status': 'blocked_on_structural_inputs',
    'output_prefix': 'Jack_Test/REVIEW_20261101_TF_MidDiag_V3/V3_S01'
}

local_defs = [
    ('V3_S02', 'head_muzzle_expression', 'T06b_rebuild', 0.65,
     'nose tip, front jaw, mouth and expression details; protect glasses frames and golden bangs',
     'a recognizable adult human male face, (incomplete very short muzzle:1.35), human cheeks still visible, '
     'human lips, a tiny beginning of forward projection at the nose and front jaw only, bare human facial skin, '
     'startled expression, widened blue eyes behind normally worn black rectangular glasses, raised inner eyebrows, '
     'mouth slightly open in mid-transformation panic, golden-blond thick bangs retained',
     'complete dog head, long snout, full canine muzzle, furry cheeks, animal mask, calm expression, confident grin, '
     'snarling fangs, extra eyes, duplicate glasses, broken glasses, falling glasses, different hair color',
     '只优化极短吻及惊慌表情可读性；不接受整个头换成犬头。原脸必须已在S01通过，不能修救硬失败的全犬头。'),
    ('V3_S03', 'ears', 'T06b_rebuild', 0.60,
     'the same original pair of ears including bases and tips; exclude hair and glasses',
     'the original single pair of human ears partway through lengthening, human-shaped ear bases, '
     'partially tapered ear tips, exposed human skin on the ear bases, incomplete canine ear formation, '
     'coherent attachment to the same human head, surrounding golden hair preserved',
     'extra ears, second pair of ears, fully grown tall canine ears, furred head, headwear, jewelry, horns, changed hair',
     '原有耳根到新耳尖连接连续，数量始终一对；没有独立长出一对兽耳。'),
    ('V3_S04', 'hands_forearms_boundary', 'T06_preserve', 0.40,
     'both hands and distal forearms within one square ROI; exclude upper arms and sleeves',
     'male hands with five fingers each, short charcoal-gray fur only on the hands and distal forearms, '
     'an irregular clear skin-to-fur boundary stopping below the elbows, a visible advancing edge of sparse short fur, '
     'proximal forearms retain bare human skin, coherent finger joints and continuous forearm anatomy',
     'fur beyond elbows, furry upper arms, fur sleeves, uniform complete fur coverage, gloves, furry cuffs, '
     'extra fingers, fused fingers, missing fingers, full character, miniature person, face, eyes, glasses',
     '短毛只占指定手/前臂区域，边界可见，近肘人皮保持；不可把肤色手套当作局部变形。'),
    ('V3_S05', 'chest_shirt', 'T06_preserve', 0.40,
     'purple shirt chest, shoulder/underarm seams and sleeves; exclude hands, face, neck and shorts',
     'the original human-sized opaque purple cotton T-shirt stretched by expanding male shoulders, upper back and chest, '
     'taut sleeves, pulling folds radiating across the chest and underarms, fabric tension, seams straining, '
     'slight seam fraying, purple fabric still covering the torso, the established enlarged torso silhouette preserved',
     'loose shirt, oversized shirt, relaxed unstressed fabric, perfectly fitted new clothing, white shirt, blue shirt, '
     'missing shirt, bare torso, body fur replacing fabric, full character, miniature person, face, eyes, glasses',
     '可指出胸前拉力褶、袖口/腋缝绷紧位置；不是只随机撕一个洞或换成合身背心。'),
    ('V3_S06', 'shorts', 'T06_preserve', 0.40,
     'khaki shorts waistband, outer seams and both leg hems; keep center-front coverage and body pose',
     'the original human-sized opaque khaki shorts stretched by expanding hips and thighs, '
     'taut waistband, diagonal pulling folds, fabric tension along both outer thigh seams and leg hems, '
     'shorts seams straining with tiny superficial outer-seam fraying, continuous khaki fabric maintaining coverage, '
     'the established enlarged thigh silhouette preserved',
     'loose baggy shorts, relaxed waistband, unstressed leg hems, intact perfectly fitted clothing, '
     'newly tailored outfit, long trousers, missing shorts, uncovered hips, exposed skin through large tears, '
     'fur replacing fabric, full character, miniature person, face, eyes, glasses',
     '腰带与至少一侧外缝/裤腿均有明确受力；胸衣与短裤在同一最终画面同时受力，衣物覆盖持续。')
]
JOBS = [base_job]
for jid, region, operation, denoise, mask, pos, neg, check in local_defs:
    JOBS.append({
        'id': jid, 'operation': operation, 'region': region,
        'source': 'latest_accepted_full_canvas', 'lineart': 'input_assets.mid_lineart cropped with same ROI',
        'seed': 2026110101, 'denoise': denoise,
        'transformation_lora': None, 'strength_model': 0.0, 'strength_clip': 0.0,
        'positive_text': f'{PREFIX}, {pos}', 'negative_text': f'{LOCAL_QUALITY_NEG}, {neg}',
        'edit_mask': f'Jack_TF_V3/masks/{jid}_edit.png',
        'protect_mask': f'Jack_TF_V3/masks/{jid}_protect.png',
        'mask_scope': mask,
        'roi': {'x': None, 'y': None, 'side': None, 'working_side': 1024, 'resolve_rule': '按实际mask并集外接框向外留32原图像素，取8倍数正方形，最大832；X/Y夹紧于画布内。若本区目标mask并集不能同框，不自动拆任务，停止并修改草图。'},
        'run_if': 'all_previous_executed_jobs_pass AND only_minor_local_defect_in_this_region AND stage_masks_and_ROI_visually_pass',
        'skip_if': 'this_region_already_passes_at_required_detail; latest accepted canvas remains unchanged',
        'acceptance': check + '；同时重查全部base_gates和mask外保护。',
        'failure_action': 'retain_previous_accepted_image_then_stop_entire_run_no_retry_no_B',
        'batch_size': 1, 'images': 1, 'status': 'conditional_not_run',
        'output_prefix': f'Jack_Test/REVIEW_20261101_TF_MidDiag_V3/{jid}'
    })

SPEC = {
    'kind': 'robot_staged_control_spec_not_comfy_workflow', 'schema_version': 3,
    'revision': 'V3_explicit_mid_sketch_color_then_masked_regions', 'date': '2026-11-01',
    'status': 'needs_structural_inputs', 'maximum_total_images': 6, 'user_budget_cap': 8,
    'planned_base_images': 1, 'maximum_conditional_local_images': 5, 'B_enabled': False,
    'purpose': '先验证明确中期轮廓/材质边界/全身衣料应力/慌张姿势能否被遵从，再按需精修；不是LoRA权重矩阵或六格序列。',
    'formal_endpoint': None,
    'previous_round': {
        'user_report': 'V2_A全部失败：完整犬吻、全身毛、短裤应力不足、平静挥手。',
        'inspected_images': ['V2_A01', 'V2_A05', 'V2_A08'],
        'observation': '无TF LoRA对照也偏完整兽头/毛身/大尾；不是仅提高负向权重即可确认修复。',
        'archive': 'verification/matrix_v2_failed_20261101',
        'preserve': '旧A和V2_A的全部PNG/graph/results原样保留，V3独立输出目录。'
    },
    'checkpoint': old['checkpoint'], 'style': STYLE, 'models': MODELS,
    'why_change_route': [
        '旧T02从空latent/denoise1生成；同一身体骨架没有编码人颊与极短前颌的轮廓、皮毛区域分布、衣褶或惊慌脸。关键词写进行中也无法指定每一处形状。',
        'Lineart把明确中期轮廓作为空间约束；它不携带可靠颜色/材质分区，所以同时用对齐色稿作为低降噪latent输入。',
        '局修只在指定像素区域采样及回贴；区域外保持已接受的人皮/衣物/身份，不让毛发由全局文本重新蔓延。',
        '全身慌张姿态与上下衣应力必须在草图及S01解决；不靠低降噪T06把平静完整兽人重新改姿。'
    ],
    'input_assets': ASSETS,
    'asset_preparation_without_sampling': [
        '选符合当前衣装的男性人类Jack作人工身份对照；本轮无IPAdapter输入。记录源文件和SHA256。',
        '画新姿势：双手在胸前近处张开查看、身体后缩、肩紧张、膝弯、双脚错步踩稳；不是手举到头顶挥手。脸睁大眼、抬内眉、嘴微张。',
        '草图脸保留人类颊骨与嘴唇，只有鼻端/前颌极短前突；同一对耳半拉长，不能画完整犬头后再靠NEG缩回。',
        '画出比起点宽的肩胸及大腿；紫T胸袖腋缝、短裤腰带两侧缝和裤口均有受力线，微开线只在外缝且不改变覆盖。',
        '色稿用人皮色填脸/颈/上臂/小腿，炭灰短毛仅手与前臂局部，界线停在肘下；黄发、紫T、卡其短裤和眼镜均按当前参考。',
        '线稿与色稿同尺寸同坐标逐像素对齐；线稿不画分区标签、箭头、文字、条纹占位线，以免生成成皮肤花纹。',
        '必须先实际打开两图检查，记录审核结果及hash；没有文件、未审核或画成全兽就保持needs_structural_inputs，禁止提交S01。',
        '每次局修前在最新已接受画布上制作edit/protect灰度mask并通过T06c同裁框预览；预览不含KSampler，不消耗采样预算。'
    ],
    'sampling_defaults': {'width': 832, 'height': 1216, 'batch_size': 1, 'steps': 28, 'cfg': 5.0,
                          'sampler': 'euler_ancestral', 'scheduler': 'normal',
                          'clip_skip': 2, 'comfy_clip_last_layer': -2,
                          'OpenPose_enabled': False, 'IPAdapter_enabled': False,
                          'lineart_model': 'noob-sdxl-controlnet-lineart_realistic.fp16.safetensors',
                          'lineart_strength': 0.8, 'lineart_start': 0.0, 'lineart_end': 0.9},
    'parameter_reason': '改为结构保持任务：CFG5/28步是待测起点，非作者最优；首张denoise0.45让色稿参与而非空latent。各区噪声按保留/重建职责明确区分，不在同一骨架上扫权重。',
    'global_mid_only_positive': POS, 'global_mid_only_negative': NEG,
    'local_prompt_rule': '只有S01使用全身全文；S02–S06使用各自短POS/NEG，不把全身、眼镜、五官等不属于当前裁区的描述塞入手/衣裤裁图。身份由当前画布和保护回贴维持。',
    'jobs': JOBS,
    'base_gates': {
        'G1_incomplete_face': '缩略图放大可辨同一人脸与人类颊部；仅鼻端/前颌小幅前突，绝不是完整犬吻/犬头。',
        'G2_limited_fur': '毛只在手和部分前臂，界线清楚且肘上/脸/颈/小腿仍人皮；多出的毛身/尾立即失败。',
        'G3_growth_and_both_garments': '肩胸大腿比瘦弱起点扩大；紫T和卡其短裤同时有明确绷紧缝线/拉力褶；只有上衣裂口不通过。',
        'G4_panic_pose_expression': '脸惊讶慌张，身体后缩紧张，双手在身前查看而非挥手；仅加几根抖动线不通过。',
        'G5_identity': '单人、成年男性Jack、黄发厚刘海、蓝眼、同一副正常黑框眼镜、原紫T/卡其短裤/闭合运动鞋，全身在画面内。',
        'G6_integrity': '同一对耳、无多肢/重复五官，衣物覆盖保持，无旧女王形态/饰品/可见尾。'
    },
    'execution_policy': [
        '这是自适应顺序流程，不是可并行发出的六行网格；同时最多一个待验收采样，验收前不能排后续任务。',
        'S01任何base_gate失败就立即结束，零局修、零B、零重抽。不能把全犬头或全身毛当作局修起点。',
        'S01通过才按S02→S06检查；该区已合格就跳过，不为了凑6张采样。skip是无缺陷，不是允许忽略硬失败。',
        '局修只从latest_accepted_full_canvas取源；未执行/跳过的步骤不改变该指针。验收后才更新指针，失败图绝不成为后续源。',
        '局修一旦当前局部或任何全局条件失败，保留上一个已接受版本并立即停止整轮；不自动回滚重试、不花剩余额度试LoRA。',
        '最大6次KSampler执行（1底图+5按需局部），小于用户8张上限；两个未使用名额不安排任何输出。每次实际采样含失败均计数，只有缓存命中且没有新采样才不增加。',
        '节点预览/线稿色稿与mask制作不包含扩散采样；若另用生成模型做草图，也必须计入同一预算，不能暗中追加，因此本规格要求手绘或确定性编辑准备。'
    ],
    'temporary_api_contract': {
        'saved_workflows_unchanged': True,
        'templates': {'T03': str(ROOT.parent/'场景实操模板/api/T03_草图定稿_角色参考加线稿.json'),
                      'T06': str(ROOT.parent/'场景实操模板/api/T06_已有图局部微调_统一裁框回贴.json'),
                      'T06b': str(ROOT.parent/'场景实操模板/api/T06b_已有图局部重建_统一裁框回贴.json'),
                      'T06c': str(ROOT.parent/'场景实操模板/api/T06c_裁框与蒙版检查_不采样.json')},
        'shared_patch': [
            '仅复制成临时API；1.ckpt_name=本规格V35；2仅开启已绑定ILstyle0.40/0.40，TF及其他行关闭；增加990 CLIPSetLastLayer(-2)接1.CLIP到2.clip。',
            '3.text直接用job.positive_text，4.text直接用job.negative_text；删除未使用的20–24/30–33旧字符串链，彻底移除旧角色POS/NEG。',
            '6使用28步/CFG5/Euler a/normal/单batch及job.denoise；8.SaveImage采用本行独立V3前缀。'
        ],
        'T03_patch': [
            '50.image=mid_lineart，51=832×1216；53.image直接接51.IMAGE，52用所列Lineart模型；53强度0.80/起0/止0.90。',
            '删除旧60–64 IP支路，6.model直接接2.MODEL；不加载旧参考图。删除空latent5及不用的190/191反相支路，199.images改接51.IMAGE。',
            '新增900 LoadImage(mid_color_draft)→901 ImageScale(832×1216,crop=disabled)→902 VAEEncode(vae=1.VAE)；6.latent_image接902.LATENT。S01 denoise=0.45。'
        ],
        'T06_patch': [
            '50.image读最新已接受RGB全图副本，不用旧alpha。新增900 LoadImageMask(edit,channel=red)；52.mask改接900.MASK。70/71/72同步写本行ROI，73=1024。',
            '57.expand由24改8工作像素；64.blur_radius=4、sigma=1为原图像素；仅T06b的58.grow_mask_by保持0，避免双重外扩；普通T06的58没有此输入。',
            '新增901 LoadImageMask(protect,red)→902 CropMask(同X/Y/side)→903 MaskToImage→904 ImageScale(1024²,bilinear)→905 ImageToMask(red)。',
            '906 MaskComposite(destination=57.MASK,source=905.MASK,operation=subtract,x0,y0)作为采样mask；T06b接58.mask，T06接59.mask。',
            '907 MaskComposite(destination=65.MASK,source=902.MASK,operation=subtract,x0,y0)；908 MaskComposite(destination=907.MASK,source=52.MASK,operation=multiply,x0,y0)；67.mask=908.MASK。最终羽化后扣保护，再夹回原edit域，禁止毛色越界回贴。',
            '新增910 LoadImage(mid_lineart)→911 ImageCrop(同X/Y/side)→912 ImageScale(1024²)→913 ControlNetLoader(同Lineart模型)→914 ControlNetApplyAdvanced(positive=3,negative=4,image=912,strength=.80,start0,end.90,vae=1.VAE)；6.positive/negative改接914。',
            'T06b白区内容会被重建编码处理，不把预画在白区里的短吻线当成天然锁；必须使用上述局部Lineart条件。',
            '输出仍是832×1216完整画布；67按原坐标回贴，resize_source=false。保留原图与中间版本，不覆盖V1/V2结果。'
        ],
        'T06c_patch': '同源RGB、相同70–72与edit灰度mask输入；增加采样mask/最终回贴mask/保护mask预览，不带KSampler。',
        'no_auto_enqueue': '本轮只交付规格；没有绑定与审核实际结构图、stage mask及ROI时不得执行。'
    },
    'field_contract': {
        'schema_version': '3；旧run_matrix_A及V2执行器均不兼容，禁止直接重用。',
        'status': 'needs_structural_inputs表示规格已写好，但草图/色稿/身份参考未实际绑定审核；不能冒称可立即运行。',
        'jobs[].positive_text/negative_text': '该步骤最终完整文本，整体替换实际CLIP文本，不自动拼旧公共提示/LoRA触发词。',
        'jobs[].roi': '局修前根据最新接受图和mask解析，null未解析就不能运行；X/Y/side在图、mask、lineart与回贴全路径一致。',
        'jobs[].operation': 'T03为新姿势及全幅结构，T06b为局部重建，T06为保留原像素的小修；不互换职责。',
        'latest_accepted_full_canvas': '运行指针，只有验收通过才更新；跳过保持原值，失败停止，不按前一ID盲取文件。',
        'maximum_total_images': '本规格硬上限6，用户允许上限8；不把剩余2张当作重试额度。'
    },
    'output_record_fields': ['job_id','prompt_id','full_api_graph_file','actual_positive_text','actual_negative_text','actual_model_and_lora_weights','seed','denoise','source_canvas_file_and_hash','lineart_and_color_draft_hash','edit_protect_mask_hash','resolved_roi','base_gates_pass','local_acceptance','outside_edit_and_protect_pixel_check','output_file','accepted_canvas_pointer','stop_reason'],
    'sources': [
        {'url':'https://blog.comfy.org/p/preprocessor-and-frame-interpolation','supports':'Pose是关节/骨架，Lineart是轮廓；线稿不保留颜色材质。'},
        {'url':'https://docs.comfy.org/tutorials/basic/image-to-image','supports':'色稿经VAE latent参与img2img；denoise小于1保留更多原图条件。'},
        {'url':'https://docs.comfy.org/tutorials/basic/inpaint','supports':'mask指定局部重绘区域。'},
        {'local':'场景实操模板/api/T03、T06、T06b、T06c及本机nodes.py/nodes_mask.py','supports':'节点映射、alpha反相、MaskComposite扣保护等按本机代码核查。'}
    ],
    'notes': ['正式终态仍未确认；局部犬科结构不确认耳长、最终毛色、尾或指趾设定。', '这轮三种TF LoRA全部0且不加载，也不写它们的触发词；先用结构输入验证mid-only，不承诺提示词必然成功。', '若S01失败，停止并回到草图/色稿审查；新的绘制或采样方案须另立规格，不在本轮偷偷扩张。']
}
TARGET.write_text(json.dumps(SPEC, ensure_ascii=False, indent=2)+'\n','utf-8')

guide = [
    'Jack男性犬科TF V3 — 先定中期结构，再按区修；2026-11-01',
    '状态：needs_structural_inputs。未出图，草图/色稿/当前人类参考尚未绑定审核。正式终点留空。',
    '同名JSON是机器人执行规格，不是可Load的ComfyUI workflow。旧执行器不兼容。', '',
    '路线：T03中期线稿＋色稿图生图 → 通过才按需T06b头/耳 → T06手前臂/胸衣/短裤。',
    '最大6次采样=1张结构底图+最多5次局修，少于8张；没有B，失败立即停止，没有重抽。合格区域跳过。',
    '为什么换：骨架不画吻长、人颊、毛发区域或衣褶；线稿定这些形状，色稿限制材质/配色，mask控制局部写入。',
    '不能直接运行旧T03：其中仍有旧女王提示、V33与女王IP参考；JSON temporary_api_contract列出需整体替换与临时接线。原工作流不改。', '',
    '准备输入（不使用扩散采样）：', *[f'{i}. {line}' for i,line in enumerate(SPEC['asset_preparation_without_sampling'],1)], '',
    '采样：V35 fp32；ILstyle确切文件不变但降至Model=Clip=0.40；Species/Mid/BYIL整轮全部关闭且无触发前缀。',
    '832×1216；28步；CFG5；Euler a/normal；Clip Skip2。OpenPose和IP均关闭。',
    'Lineart强度0.80、截止0.90。首张色稿img2img denoise0.45，不能再接EmptyLatent或denoise1。以上均为待测起点。', '',
    '步骤（不是并行网格，前一张验收后才能下一张）：'
]
for j in JOBS:
    guide += [f"{j['id']} | {j['operation']} | denoise={j['denoise']} | 最多1次", f"运行条件：{j['run_if']}", f"验收：{j['acceptance']}", 'POS：'+j['positive_text'], 'NEG：'+j['negative_text'], '']
guide += ['停止条件：', *[f'{k}：{v}' for k,v in SPEC['base_gates'].items()],
          'S01任一条失败即停止；局修若破坏任一条也停止。失败图不能进入下一步。', '',
          '蒙版与文本要点：',
          '白改黑留的灰度edit/protect图用LoadImageMask red读取；protect白是保护，和edit含义相反。不要混用LoadImage透明alpha反相语义。',
          '眼镜框与镜腿、黄发在保护区；要画惊慌眼神时可改镜片内眼睛，但不遮噪正常镜框。不能保护错误几何后强贴成正常眼镜。',
          '耳mask同时包含同一对原耳根与目标耳尖；手mask不越过肘部人皮边界；上衣mask与短裤mask分别处理。',
          '图/蒙版/线稿使用完全相同裁框；最终外扩/羽化后再扣保护且夹回原edit域。57外扩8是工作图像素，64羽化4是原图像素，单位不要混。',
          '手/衣/裤局部POS不放full body、五官、眼镜等全身身份词，防止局部生出小人或脸。全局身份通过源图、未改区域与保护回贴维持。',
          '若完整犬头、全身毛或全局姿势错误，停止回草图，不能用低噪T06逐处补救。', '',
          '机器人字段：jobs[].positive_text/negative_text为最终全文；roi null需解析；临时接线参照temporary_api_contract；记录完整graph和全部hash。',
          '旧V2失败规格/说明/填表已备份至verification/matrix_v2_failed_20261101；V1/V2原图及_ops记录均保留。']
(ROOT/'Jack_男性犬科TF_矩阵V3说明.txt').write_text('\n'.join(guide)+'\n','utf-8-sig')
v2note = ROOT/'Jack_男性犬科TF_矩阵V2说明.txt'
v2note.write_text('历史V2说明：已由矩阵V3取代，请看Jack_男性犬科TF_矩阵V3说明.txt。以下保留旧稿供失败诊断。\n\n'+v2note.read_text('utf-8-sig'),'utf-8-sig')
plan = ROOT/'阶段规划表_填写用.txt'
head = plan.read_text('utf-8-sig').split('最小测试矩阵：',1)[0]
plan.write_text(head+'最小测试矩阵：已改V3；见同名JSON与Jack_男性犬科TF_矩阵V3说明.txt。\n以上六格仍是历史草案、正式终点未确认；不作为V3参数或衣物/体型限制。\nV3仅一张新中期线稿+色稿结构底图，后续最多五次按区修，合计≤6次采样；三种TF LoRA全关，ILstyle0.4；失败立即停，无B。\n输入草图/色稿尚未制作绑定，当前只交付规格，未采样。\n','utf-8-sig')
print(json.dumps({'updated':str(TARGET),'schema_version':3,'status':SPEC['status'],'maximum_total_images':6,'submitted_images':0},ensure_ascii=False))
