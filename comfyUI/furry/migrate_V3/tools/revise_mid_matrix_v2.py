"""Revise the diagnostic specification only; never enqueue ComfyUI jobs."""
from pathlib import Path
import copy
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'Jack_男性犬科TF_最小测试矩阵.json'
DATE = '2026-11-01'
old = json.loads(TARGET.read_text('utf-8-sig'))
if old.get('schema_version', 1) > 2:
    raise SystemExit('A newer specification already exists; historical V2 generator must not overwrite it.')
archive = ROOT / 'verification' / 'matrix_v1_failed_20261101'
archive.mkdir(parents=True, exist_ok=True)
if old.get('schema_version', 1) < 2:
    backup = archive / TARGET.name
    if backup.exists() and backup.read_bytes() != TARGET.read_bytes():
        raise RuntimeError('Existing V1 archive differs; preserve it and resolve manually.')
    if not backup.exists():
        shutil.copy2(TARGET, backup)
    shutil.copy2(ROOT / '阶段规划表_填写用.txt', archive / '阶段规划表_填写用.txt')

style = copy.deepcopy(old['style'])
assert style['binding_status'] == 'bound'
assert style['filename'] == 'blackrat_style：IllustriousBlackRat_Style.safetensors'
style['binding_rule'] = '已绑定本机确切文件；本轮保持Model=Clip=1.20。只用已确认的blackrat_style, blackrat；不自动套入BRIL、其他BlackRat变体或旧脚本的额外前缀。'
models = copy.deepcopy(old['models'])
for key, trigger, weights, reason in [
    ('species', 'species_transformation', [0.8, 1.0], '先测0.8/1.0；旧1.3也未显示中期，增大权重不是增加变化过程，本轮不再占用高权重格。'),
    ('mid', 'transformation, mid transformation, transfur', [0.6, 0.8], '0.8沿用建议起点，0.6探索较弱概念注入是否保留更多人类结构；本轮不额外使用泛化主体词furry。'),
    ('byil', 'transformation', [0.6, 0.8, 1.0], '保留0.6/0.8/1.0，分别看弱、中、较强概念注入；不是三个预定变化阶段。'),
]:
    models[key]['trigger_selected'] = trigger
    models[key]['test_weights_model_equals_clip'] = weights
    models[key]['recommendation_reason'] = reason
    models[key]['recommendation_status'] = 'V2待实测的工程候选；不是作者保证的最优参数'

base = (
    'clean illustration, solo, single character, (adult male human Jack undergoing a partial canine transformation:1.25), '
    '(golden-blond shaggy medium-length hair with thick bangs:1.2), blue eyes, '
    '(one intact pair of black rectangular glasses worn normally:1.2), '
    'recognizable human cheekbones and areas of human facial skin, '
    '(only the nose tip and front of the jaw beginning to form a very short canine muzzle:1.25), '
    'one pair of ears in transition, tapered lengthening ear tips with partially human-shaped ear bases, '
    'patches of charcoal-gray short fur on the hands and parts of the forearms, visible skin-to-fur boundaries, '
    'remaining exposed skin still human, five fingers on each hand, '
    '(moderately broadening shoulders and expanding upper back and chest:1.2), '
    'his original human-sized opaque purple cotton short-sleeved T-shirt and khaki shorts becoming undersized, '
    'pulling folds across the chest, taut sleeves and underarm seams, strained outer shorts seams, '
    'slight seam fraying while the shirt and shorts still cover his torso and hips, '
    'closed sneakers covering all toes, one hand raised, balanced standing posture, '
    'full body, three-quarter view, simple neutral gray background, soft even lighting, tail not visible'
)
patch = (
    'An uneven mid-stage transformation is visibly reshaping Jack: his short muzzle is forming while his human face remains recognizable, '
    'patchy fur is spreading, and his growing body is filling the clothes, with clothes stretching, fabric tension and seams straining '
    'across his expanding shoulders, upper back and chest.'
)
negative = (
    'low quality, blurry, bad anatomy, extra person, duplicate character, extra arms, extra legs, '
    'extra fingers, missing fingers, fused fingers, extra ears, duplicate ears, '
    'duplicate glasses, floating eyewear, falling glasses, bent glasses, broken glasses, '
    '(fully transformed anthro already in fitted clothes:1.4), '
    '(ordinary werewolf costume:1.3), (unchanged slim human proportions:1.3), '
    '(intact perfectly fitted clothing:1.3), completed canine head, long fully formed canine muzzle, '
    'uniform completed fur coverage, completely unchanged human appearance, costume head, animal mask, '
    'newly tailored outfit, oversized loose shirt, relaxed unstressed fabric, extreme final-form bulk, '
    'different outfit, white shirt, blue shirt, long trousers, boots, missing shirt, missing shorts, '
    'disintegrating clothes, transparent clothing, bare torso, uncovered hips, bare feet, toes sticking through shoes, '
    'visible tail, horns, wings, crown, necklace, collar, armband, long black hair, '
    'cropped head, cropped feet, text, logo, branding, watermark, multiple panels, collage'
)
style_prefix = ', '.join(style['trained_words'])

def job(jid, family, weight, seed, source=None):
    trigger = models[family]['trigger_selected'] if family else ''
    positive = ', '.join(x for x in [style_prefix, trigger, base, patch] if x)
    result = {
        'id': jid, 'phase': 'A_screen' if '_A' in jid else 'B_seed_check',
        'seed': seed, 'transformation_lora': family,
        'strength_model': weight, 'strength_clip': weight,
        'trigger_words': trigger, 'pos_patch': patch,
        'positive_text': positive, 'negative_text': negative,
        'batch_size': 1, 'images': 1,
        'output_prefix': f'Jack_Test/REVIEW_20261101_TF_MidDiag_V2/{jid}_s{seed}',
        'status': 'pending_selection' if source else 'not_run'
    }
    if source:
        result.update(copy_best_passing_from=source, skip_if_none_pass=True,
                      resolve_before_enqueue=['strength_model', 'strength_clip'],
                      inheritance_rule='仅复制同族A组通过硬验收的赢家权重；POS/NEG/触发词与赢家必须逐字相同。未决null不得提交，禁止猜成0或默认1。')
    return result

jobs = [job(f'V2_A{n:02d}', f, w, 2026110101) for n, f, w in [
    (1, None, 0), (2, 'species', 0.8), (3, 'species', 1.0),
    (4, 'mid', 0.6), (5, 'mid', 0.8),
    (6, 'byil', 0.6), (7, 'byil', 0.8), (8, 'byil', 1.0)
]]
jobs.extend([
    job('V2_B01', None, 0, 2026110102),
    job('V2_B02', 'species', None, 2026110102, ['V2_A02', 'V2_A03']),
    job('V2_B03', 'mid', None, 2026110102, ['V2_A04', 'V2_A05']),
    job('V2_B04', 'byil', None, 2026110102, ['V2_A06', 'V2_A07', 'V2_A08']),
])

spec = {
    'kind': 'robot_test_matrix_spec_not_comfy_workflow', 'schema_version': 2,
    'revision': 'V2_mid_structure_growth_fabric_stress', 'date': DATE, 'status': 'not_run',
    'maximum_total_images': 12, 'planned_A_images': 8, 'maximum_B_images': 4,
    'purpose': '诊断同一个男性Jack中期：可见人兽结构混合＋肩背胸扩张＋原人类尺寸衣料受力。不是六格分镜，不据此确认终态。',
    'formal_endpoint': None,
    'previous_round': {
        'user_report': 'A01–A08全部不合格：普通穿衣狼人，过程感、服装应力、体型扩张不足。',
        'images_inspected_this_revision': ['A01', 'A04', 'A05', 'A08'],
        'observation': '抽查包含无转化LoRA的A01也偏完整犬头；未把失败全部归因于转化LoRA。旧POS/NEG含当前瘦型、服装不变、禁止撕裂等冲突。',
        'spec_backup': str((archive / TARGET.name).relative_to(ROOT)).replace('\\', '/'),
        'execution_records_preserved': '_ops/graph_A01.json … graph_A08.json；_ops/matrixA_results.json；原PNG不动',
        'comparison_limit': 'V2同时修正提示词结构及各族触发配置；不能把V1→V2差异归因于某个单独词或权重。'
    },
    'checkpoint': old['checkpoint'], 'style': style, 'models': models,
    'input_profile': copy.deepcopy(old['input_profile']),
    'prompt_blocks': {'style_prefix': style_prefix, 'identity_structure_clothing_base': base,
                      'mid_stage_patch': patch, 'negative_full': negative},
    'field_contract': {
        'jobs[].positive_text': '实际提交CLIP正向编码器的完整文本；整体替换旧POS，不追加旧触发合集、score_9/source_artwork或旧角色文本。',
        'jobs[].negative_text': '实际提交CLIP负向编码器的完整文本；整体替换旧NEG，移除对体型增大及轻度衣缝损坏的旧禁令。',
        'jobs[].pos_patch': '每格一条中期方向句，已经包含在positive_text中；不可在positive_text后重复追加。所有行刻意相同。',
        'jobs[].trigger_words': '只属于当前一种转化LoRA；基线为空。已经包含在positive_text中，不再拼接其他族触发词。',
        'jobs[].strength_model/strength_clip': 'Model=Clip=w；B02–B04的null必须从同族通过项解析，未解析不运行。',
        'jobs[].output_prefix': '使用独立V2目录及V2编号，禁止删除或覆盖原A01–A08结果。',
        'prompt_blocks': '便于人类编辑核对；运行只读取逐行完整文本。编辑公共块后必须重建并核查全部逐行文本，不能只改一处留下不一致。'
    },
    'legacy_runner_compatible': False,
    'runner_contract': [
        '这是机器执行规格，不是ComfyUI workflow；不能直接拖入ComfyUI当工作流。',
        '旧_ops/run_matrix_A.py只读旧common字段、过滤A开头编号，并硬编码前缀/参数，还会回写状态；禁止原样运行它执行V2。',
        '执行器须要求schema_version=2，读jobs[].positive_text/negative_text和input_profile，识别V2_A/V2_B；本规格故意不提供旧common键，避免静默丢弃补丁。',
        '每行载入固定ILstyle1.2/1.2；有family时再载入该模型字典中的唯一一种转化LoRA；基线跳过转化LoRA。BRIL和其他LoRA关闭。',
        '提交前从实际API graph反读CLIP文本、CLIPSetLastLayer、权重、种子及采样/骨架参数，与规格逐项比对。',
        '只运行单输出临时API，不保存覆盖T02/T11等本机工作流；本次修订不提交出图。'
    ],
    'trigger_rule': '风格词＋当前族触发词＋公共身份/混合结构/衣料块＋同一句pos_patch。族内不同权重和复验保持全文一致；跨族比较的是模型＋触发词方案。',
    'parameter_decision': {
        'change_resolution_steps_cfg': False,
        'reason': '保留832×1216、22步、CFG7、Euler a/normal、denoise1，先解决语义冲突。更高步数或CFG不等于更多变形过程。',
        'keep_T02_OpenPose': True,
        'pose_role': '沿用同一骨架0.70/截止0.85，仅约束姿态关节；不保证肌肉宽度、衣褶应力或变化阶段。IP=0，没有自动选用未获确认的人类母图。',
        'clip_skip': '全行2（CLIPSetLastLayer=-2）；既有记录中Mid/BYIL训练元数据为2，Species为1，本轮统一2是比较设置，不宣称Species最优。'
    },
    'mid_target': '保留人类面颊的短吻形成中、同一对耳部分拉长、手/前臂局部短毛与人皮边界；肩背胸比瘦弱起点更宽；原紫T/卡其短裤被撑紧、缝线受力。黄发厚刘海、蓝眼、黑框眼镜正常佩戴，姿势固定，无可见尾。',
    'jobs': jobs,
    'preflight': [
        '确认使用V2规格和支持逐行完整文本的执行器；不把旧脚本或V1图当成V2测试。',
        'ILstyle已绑定确切文件；核对当前文件与模型记录，三个转化LoRA需匹配所列SHA256。',
        '确认input/OC_advanced/pose_wave.png存在，记录其SHA256，全部任务使用同一文件。',
        '完整替换POS/NEG；没有旧女王设定、旧六格眼镜掉落事件、旧瘦型限制或旧触发词合集。',
        'CLIPSetLastLayer=-2连接所有文本路径；IP=0；单一转化LoRA；单分支、batch=1。',
        '先跑8张A再人工验收，B为有条件第二种子复验；状态、prompt_id、完整graph与PNG逐一保存。',
        '检查队列空闲；提交状态未知时先查prompt_id，不盲目重投；总数包含实际已采样的失败/重试图。'
    ],
    'hard_gates_all_required': {
        'G1_partial_structure': '短吻正在形成且人类面颊/脸结构仍可辨认；另至少能看到耳形过渡或皮肤—毛发推进边界之一。完整犬头加黄发不通过。',
        'G2_body_growth': '肩、上背、胸明显宽于瘦弱起点且处于中等扩张；只加兽头、不变体型不通过，终态巨兽也不通过。',
        'G3_clothes_stress': '仍是原紫T/卡其短裤/运动鞋；胸肩/袖口或腋下有拉力褶和绷紧缝线，短裤外缝受力。仅合身紧衣不通过；轻度线缝开裂可通过。',
        'G4_identity_pose': '成年男性Jack，黄发厚刘海、蓝眼、黑框眼镜正常完整佩戴；同一站姿与抬手、完整全身画面。',
        'G5_integrity': '单角色、同一对耳、手指和肢体连接正确；衣物仍覆盖躯干腰臀，鞋包住脚趾；不出现面具/兽装/终态/新尾巴。'
    },
    'hard_fail': ['任一G1–G5不通过即失败；不得用画质或总分抵消。', '不能仅凭提示词已写了mid-stage判定通过；必须在图中指出混合结构与布料拉力位置。'],
    'score_0_to_2_each_after_hard_gates': ['混合结构可读性', '体型扩张可读性', '衣料受力可读性', 'Jack身份与姿势', '线条结构与画风'],
    'selection_rule': '先全部硬条件通过，再按五项总分选同族赢家；同分选更低权重。同族A全失败就跳过该族B，绝不选最好看的失败图。',
    'B_execution_gate': 'A全部未通过（含基线）则B01–B04全部跳过；只要有A通过才运行B01对照，B02–B04各自还必须有同族赢家。',
    'replication_rule': 'B只换到2026110102种子，继承同族通过项的权重、全文、骨架和参数；复验仍需全部硬条件通过。两种子仅是初步敏感性检查，不保证统计稳定。',
    'budget_rule': 'A固定8张，B最多4张，总计≤12；单任务单输出batch=1，无四格整套、无补抽、无自动权重网格扩张。',
    'if_all_fail': '停止当前矩阵，不用剩余额度堆权重/CFG；下一轮另做T03明确中间态草图，或从确认的人类母图用T06分区域局修，直接控制短吻/耳根/肩衣轮廓。本轮不新增该分支。',
    'output_record_fields': ['job_id', 'prompt_id', 'full_api_graph_file', 'actual_positive_text', 'actual_negative_text', 'checkpoint_filename', 'style_filename', 'lora_filename', 'lora_sha256', 'seed', 'strength_model', 'strength_clip', 'pose_input_hash', 'output_file', 'G1_G5_pass', 'hard_fail_reasons', 'scores', 'review_notes'],
    'notes': ['正式终点、耳形/最终毛色/尾/指趾数仍未确认，本轮局部犬科特征不构成终态定稿。', '原衣服保留指款式与颜色延续，不等于剪裁永远合身；本轮明确允许受力与小范围缝线损伤。', '静态中期图用同一身体上的混合结构和衣料应力表达过程，单写时间词并不能保证模型画出过程。', '没有复制作者默认的1girl/female/breasts等NEG；不引入旧女王、旧饰品、性别转化或成人露骨内容。']
}
TARGET.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', 'utf-8')

rows = []
for j in jobs:
    w = '继承同族合格赢家' if j['strength_model'] is None else str(j['strength_model'])
    rows.append(f"{j['id']} | seed={j['seed']} | {j['transformation_lora'] or '无转化LoRA'} | Model=Clip={w}\nPOS补丁：{j['pos_patch']}")
doc = f'''Jack 男性犬科TF — 中期诊断矩阵 V2
更新：{DATE}；未提交图片；正式终点继续留空。

一、使用哪个文件
覆盖更新同名 Jack_男性犬科TF_最小测试矩阵.json；schema_version=2。
这是机器人执行规格，不能直接Load到ComfyUI当workflow。T02/T11节点与连线未修改。
旧矩阵备份：verification/matrix_v1_failed_20261101/；原A图与_ops执行记录保留。
旧_ops/run_matrix_A.py不支持新字段，也硬编码旧前缀与参数，不能原样运行V2。

二、为什么改
抽看A01/A04/A05/A08（用户报告全部8张失败）；连无转化LoRA的A01也偏完整拟兽。
移除旧POS的slim slender build、unchanged clothing、upper arms and torso retain the human stage。
移除旧NEG的torn clothing、huge muscles。只限制终态巨兽与完全缺衣，不禁止本轮必需的增壮和局部缝线损伤。
不再把furry/anthro jackal作为全局主体，转而描述同一人类脸上的短吻、同一对耳的过渡、皮肤到短毛的边界。

三、执行字段（必须整体替换旧文本）
jobs[].positive_text：该行完整POS，直接写入CLIP正向；不要再加旧前缀或额外补丁。
jobs[].negative_text：该行完整NEG，直接写入CLIP负向。
jobs[].trigger_words：当前唯一转化LoRA的触发配置，已经含在该行全文中。
jobs[].pos_patch：本行一句方向，已经含在全文；12行刻意相同，不能按权重分配不同阶段。
jobs[].transformation_lora：null表示无转化LoRA；其余从models读取本机文件。
jobs[].strength_model/strength_clip：同一权重；B02–B04的null须从copy_best_passing_from通过项解析，否则跳过。
prompt_blocks：给人阅读和修改的公共块；运行权威是逐行全文，改公共块时要同步重建所有行。
input_profile：固定采样与骨架参数；执行器须读字段，不可沿用硬编码值。
jobs[].output_prefix：独立V2目录与编号；禁止删改上一轮原图。

四、固定参数和LoRA
V35 fp32；ILstyle={style['filename']}；Model=Clip=1.20。
画风只用已绑定的blackrat_style, blackrat；不混BRIL或其他BlackRat变体。
Species：species_transformation；0.80/1.00。暂不再测1.30，权重不等于变化百分比。
Mid v2：transformation, mid transformation, transfur；0.60/0.80。0.60是探索值，0.80为原建议起点。
BYIL：transformation；0.60/0.80/1.00。
同族内仅变权重；跨族因专用触发不同，称为“模型+触发方案比较”。基线没有转化LoRA触发前缀。
保留T02+OpenPose，同一pose_wave.png，强度0.70、截止0.85，IP=0；骨架只管姿态，不保证肌肉与衣料形状。
832×1216，22步，CFG7，Euler a/normal，denoise1，batch1；全行Clip Skip2=-2。
不提高步数/CFG作为过程感修复；Species训练记录clip_skip1，本轮统一2是固定比较设置，非最优宣称。

五、共同POS（风格词+当前族触发词+以下主体块+补丁；各行全文已生成）
主体块：
{base}

每行POS补丁P：
{patch}

六、完整NEG
{negative}

七、矩阵（A共8张；B最多4张；不执行完整六格）
{chr(10).join(rows)}

八、验收与停机规则
G1：短吻形成+人类脸仍可辨；同时至少可见耳过渡或皮肤—毛发边界。
G2：肩背胸较瘦弱起点明显扩大，但不是终态巨兽。
G3：原紫T/卡其短裤明显受力，有拉力褶/绷紧缝线；轻度局部开线允许，完全合身兽人衣服失败。
G4：男性、黄发厚刘海、蓝眼、正常佩戴的黑框眼镜、同姿势和全身画面。
G5：单人、同一对耳、解剖连接无硬错；衣鞋覆盖保持，无尾/面具/兽装。
所有硬条件先通过，再打分。漂亮但没有中期不算通过。
A全失败则整组B跳过；有通过才运行B01，每族B仍须本族有通过赢家。B与赢家全文/参数一致，只换种子。
两种子仅是初筛，不证明长期稳定。最多12张，不能偷偷补抽。
V2若仍全失败，下一步改为T03明确中期草图或T06从确认的人类母图分区重建结构；本轮不追加新测试。
'''
(ROOT / 'Jack_男性犬科TF_矩阵V2说明.txt').write_text(doc, 'utf-8-sig')

# Update only the matrix appendix; keep the six-frame storyboard and endpoint untouched.
plan_path = ROOT / '阶段规划表_填写用.txt'
plan = plan_path.read_text('utf-8-sig')
head = plan.split('最小测试矩阵：', 1)[0]
head = head.replace('ILstyle确切文件名与其触发词尚待绑定，不能由别名猜选。', f'ILstyle现已绑定{style["filename"]}，触发词blackrat_style, blackrat。')
appendix = '''最小测试矩阵：V2已替换旧版；完整规格见Jack_男性犬科TF_最小测试矩阵.json，字段说明见Jack_男性犬科TF_矩阵V2说明.txt。
本次仅修订中期诊断；以上六格仍是未批准终态的历史草案，不据此执行。旧草案的瘦型/完整衣物限制不得覆盖V2新增的体型扩张、衣料应力和局部开线目标。
V2为8张A+最多4张B：无转化；Species0.8/1.0；Mid0.6/0.8；BYIL0.6/0.8/1.0。各族独立触发，不再用触发词合集。
同一固定姿势，眼镜始终正常佩戴；正式终点仍留空。全行V35 fp32、已绑定ILstyle1.2/1.2、832×1216、22步、CFG7、Euler a、Clip Skip2、OpenPose0.7/截止0.85、IP0。
本轮未生成图片。原A01–A08与旧规格已保留；全部硬条件失败就停止，不以最好看的失败图选赢家。
'''
plan_path.write_text(head + appendix, 'utf-8-sig')
print(json.dumps({'updated': str(TARGET), 'revision': spec['revision'], 'jobs': len(jobs), 'submitted_images': 0}, ensure_ascii=False))
