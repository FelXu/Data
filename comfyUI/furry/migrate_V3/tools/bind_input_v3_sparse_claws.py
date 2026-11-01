"""Document and bind reviewed structural inputs; do not enqueue diffusion jobs."""
from pathlib import Path
import copy
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'input_V3'
VERIFY=ROOT/'verification/input_V3'
COMFY=Path(r'E:\ComfyUI-aki-v3\ComfyUI')
MATRIX=ROOT/'Jack_男性犬科TF_最小测试矩阵.json'
spec=json.loads(MATRIX.read_text('utf-8-sig'))
backup=VERIFY/'matrix_before_input_binding_sparse_claws.json'
if backup.exists():
    raise SystemExit('Binding already documented; edit current files rather than resetting them.')
shutil.copy2(MATRIX,backup)

line_pos=(
    'Clean black-and-white ink lineart on white, one adult male Jack, full-body three-quarter view, '
    'head and closed sneakers inside the frame, shaggy medium-length hair with thick bangs, '
    'black rectangular glasses worn normally. An incomplete very short muzzle is only beginning at the nose tip and front jaw; '
    'human cheeks, cheekbones, lips and facial traits remain clearly visible. The same original pair of ears is partly lengthening '
    'from the original human ear bases, no additional ears. Early transformation: sparse fine short hair strands sprout in scattered '
    'small groups across visible hand, forearm, upper-arm, neck-side and lower-leg skin; most skin remains visibly human, '
    'large bare spaces between hair strands, no solid fur patches and no cuff boundary. '
    'One single short tapered pointed claw replaces each visible rounded human fingernail, just emerging beyond the fingertip, '
    'no separate oval human nail plate, five human fingers on each hand. Shoulders, chest and thighs are moderately expanding. '
    'The original T-shirt AND cargo shorts both show fabric tension, pulling folds and taut straining seams: '
    'shirt chest, sleeves and underarms, shorts waistband, outer thigh seams and leg hems. Clothing coverage maintained. '
    'Startled mid-transformation panic, widened eyes, mouth slightly open, body recoiling backward, knees slightly bent, '
    'both hands at chest height checking the change, fingers spread, feet staggered and planted. '
    'Clear readable contours, sparse hair strokes only on skin, no text or labels.'
)
line_neg=(
    'completed dog head, long canine muzzle, full snout, lost human cheeks, furry face, full fur coat, '
    'dense fur, opaque gray furry gloves, fur sleeves, continuous fur patches, hard fur cuffs, body paint, '
    'hair covering all skin, fur growing on clothes, separate oval human nail plates, rounded human fingernails, '
    'duplicate nails, claws overlaid on human nails, long hooked talons, animal paws replacing hands, '
    'extra fingers, fused fingers, extra ears, second ear pair, tail, distorted glasses, falling glasses, '
    'calm standing pose, greeting wave, hand above head, confident smile, snarling wolf face, '
    'unchanged slim proportions, loose unstressed shirt, loose baggy shorts, perfectly fitted new clothes, '
    'missing clothing, transparent fabric, cropped head, cropped feet, color fills, tonal shading, '
    'heavy filled body regions, messy construction marks, arrows, labels, text, watermark, multiple panels'
)
color_pos=(
    'Apply simple rough flat colors under the supplied lineart without moving its contours. Preserve the same canvas, '
    'camera, pose, silhouette, incomplete tiny muzzle, human cheeks, single pair of transitioning ears, glasses, '
    'hands, nails, every garment seam and shoe position. Golden-yellow shaggy hair with thick bangs, blue eyes behind '
    'normally worn black rectangular glasses, natural light human skin throughout the visible face and body. '
    'Sparse fine charcoal hair strands scattered over hands, forearms, upper arms, neck sides and exposed legs; '
    'large areas of normal human-colored skin remain visible, no opaque gray furry gloves or solid fur patches. '
    'Each visible fingertip has one single newly grown short charcoal pointed claw instead of a rounded human nail plate; '
    'no second nail underneath, no long talons. Muted purple cotton T-shirt and khaki cargo shorts, BOTH preserving '
    'the tension folds, taut seams and stress wrinkles. Closed neutral gray/tan sneakers. '
    'Preserve the startled expression, recoiling torso, bent knees and both hands checking themselves at chest level. '
    'Minimal shading, black ink contours visible, white background unchanged, fully opaque clothing.'
)
color_neg=(
    'redrawn contours, changed pose, shifted silhouette, altered proportions, new camera angle, completed canine head, '
    'longer muzzle, lost human cheeks, furry face, dense body fur, solid gray hands, furry gloves, fur cuffs, '
    'yellow body fur, hair replacing fabric, separate oval human fingernails, duplicate nails, double-layer nails, '
    'long hooked claws, extra fingers, extra ears, tail, different hair color, hidden blue eyes, bent glasses, '
    'missing glasses, white shirt, blue shirt, changed outfit, relaxed fabric, loose shorts, smooth unstressed seams, '
    'calm expression, waving, confident smile, detailed painting, dramatic light, gradients hiding skin, '
    'transparent clothing, missing clothing, text, watermark'
)
for name,text in [('图A_线稿_POS.txt',line_pos),('图A_线稿_NEG.txt',line_neg),('图B_色稿_POS.txt',color_pos),('图B_色稿_NEG.txt',color_neg)]:
    (OUT/name).write_text(text+'\n','utf-8-sig')

checks=[
    '脸：仍明显是成年男性人脸，颊骨、脸颊、嘴唇保留；鼻端/前颌仅轻微前突，不能画成完整短版狗头。',
    '耳：同一对原耳从原耳根部分拉长；近侧可见，远侧可按透视遮挡，不能另添头顶兽耳。',
    '毛：按最新要求，少量细短毛散布在手、前臂、上臂、颈侧与露出的小腿，绝大多数人皮仍可见；取消旧版只到前臂的硬界线及灰毛手套。衣服上不长毛。',
    '爪：每个可见指尖只有一枚刚长出的短尖爪，圆形人类甲片由它替换，不能保留旧甲片再叠第二枚爪；不要求看见背向镜头的指甲。',
    '衣料：分开指出紫T的胸/袖/腋缝，及卡其短裤的腰带/外缝/裤腿拉力褶，两件同时受力而非只撕上衣。',
    '动作：遮住脸仍能读出后缩、屈膝、双手在胸前查看；不能靠几根抖动线替代慌张重心。',
    '身份：成年男性、黄发厚刘海、蓝眼、正常黑框眼镜；闭合运动鞋包住脚趾，单角色，无尾，无旧女王设定。',
    '对齐：最终A从最终B经同尺寸Control map提取，未独立重画；镜框、耳尖、鼻尖、指尖、衣缝和鞋底保持相同坐标。'
]
guide=[
    'Jack V3 结构输入 — 最新版：稀疏分散短毛＋单一短尖爪',
    '2026-11-01；使用内置imagegen生成/定点修改，ComfyUI无采样节点归一化尺寸与提取最终线稿。',
    '交付：Jack_TF_V3_mid_lineart.png / Jack_TF_V3_mid_color.png，均为832×1216、不透明RGB。',
    '重要变更：用户最新要求覆盖旧“fur ONLY on hands/distal forearms”规则；现为全身可见皮肤上的少量稀疏短毛。',
    '指甲已改为单一短尖爪；不要再复制保留圆人类甲片的旧提示。终态仍未确认。', '',
    '使用：',
    '1. 图A作为T03 Lineart输入；图B作为T03图生图的VAE输入。两张已按原规格路径复制到ComfyUI/input/Jack_TF_V3/。',
    '2. 线稿用mid_lineart.png，色稿用mid_color_draft.png；不要使用_sources中的原生大图或旧版密毛候选。',
    '3. 仍按V3临时接线：色稿→ImageScale→VAEEncode→latent；不能用EmptyLatent替代。TF LoRA全关、ILstyle0.4、Clip Skip2。',
    '4. 先只运行S01并验收；本次没有提交S01，也没有修改T11或已保存工作流。',
    '5. 本轮结构输入已使用6次外部图像生成/修改；无采样尺寸导出与提线不增加计数。按累计8张上限，最多剩余2次Comfy采样（S01＋最多一次局修），不是另有6张额度。',
    '6. 失败立即停止，无B、无重抽；不满意的完整犬头/毛身不能送入后续局修。', '',
    '给画师 / 给SD草图的分步检查：', *[f'{i}. {x}' for i,x in enumerate(checks,1)], '',
    '提示词分文件：图A_线稿_POS/NEG.txt，图B_色稿_POS/NEG.txt。',
    'A不承载黄发、蓝眼、紫T、卡其色，颜色由B承担。先制作同一几何母图，颜色修改后再从最终母图提取A；不要用两次独立生成假称严格对齐。',
    '最终提线是已有彩稿的确定性控制图提取，不包含KSampler；构图从头到尾没有第二次摆姿。'
]
(OUT/'输入说明与检查清单.txt').write_text('\n'.join(guide)+'\n','utf-8-sig')
(OUT/'英文提示词_合集.txt').write_text('LINEART POS\n'+line_pos+'\n\nLINEART NEG\n'+line_neg+'\n\nCOLOR POS\n'+color_pos+'\n\nCOLOR NEG\n'+color_neg+'\n','utf-8-sig')

# Bind the same final images and synchronize all live text to the user's revised hair/nail requirements.
spec['revision']='V3_bound_sparse_body_hair_single_short_claws'
spec['status']='structural_inputs_prepared_not_sampled'
spec['latest_user_overrides']=['稀疏短毛分散于全身可见皮肤，不再只集中手/前臂；绝大部分人皮可见。','每个可见指尖一枚新生短尖爪，去掉原圆人类甲片与双层甲。']
old_hair='(short fur only on hands and forearms with a clear skin boundary:1.35), irregular fur fronts stopping below the elbows, bare human skin on the cheeks, neck, upper arms and lower legs'
new_hair='(sparse fine short hairs scattered over visible human skin:1.25), small separated groups on the hands, forearms, upper arms, neck sides and lower legs, mostly bare human-colored skin between strands, (one single newly grown short charcoal pointed claw replacing each visible rounded human fingernail:1.25), no separate human nail plate underneath'
pos=spec['global_mid_only_positive'].replace(old_hair,new_hair).replace('in an incomplete mid-transformation','in an early canine transformation')
assert old_hair not in pos and 'sparse fine short hairs' in pos
neg=spec['global_mid_only_negative'].replace('furry neck, furred upper arms, furry thighs, furry calves, ','')
neg+=', dense gray furry gloves, continuous solid fur patches, fur cuffs, separate oval human nail plates, duplicate nails, claws overlaid on human nails, long hooked claws'
spec['global_mid_only_positive']=pos;spec['global_mid_only_negative']=neg
spec['jobs'][0].update(positive_text=pos,negative_text=neg,status='structural_inputs_bound_not_run',run_if='bound structural inputs reviewed AND cumulative generation count below 8')
for key,rel,description in [
    ('mid_lineart','Jack_TF_V3/mid_lineart.png','最终832×1216同源线稿；稀疏短毛分散于可见皮肤、新生单一短尖爪。'),
    ('mid_color_draft','Jack_TF_V3/mid_color_draft.png','最终832×1216色稿；黄发蓝眼、紫T卡其短裤、人皮底色与稀疏短毛、单一短尖爪。')]:
    a=spec['input_assets'][key];a.update(input_relative_path=rel,binding_status='generated_and_visually_reviewed',required=description,file_exists_at_spec_write=True)
    a['sha256']=hashlib.sha256((COMFY/'input'/rel).read_bytes()).hexdigest()
human_src=Path(r'C:\Users\XU73A0~1.DES\AppData\Local\Temp\codex-clipboard-4f9d72ce-f634-43c4-bf9e-54d0d3f74eb3.png')
human_dest=OUT/'_sources/Jack_human_original_identity_only.png'
shutil.copy2(human_src,human_dest)
shutil.copy2(human_src,COMFY/'input/Jack_TF_V3/Jack_human_original_identity_only.png')
spec['input_assets']['human_identity_reference'].update(input_relative_path='Jack_TF_V3/Jack_human_original_identity_only.png',binding_status='bound_manual_identity_only',file_exists_at_spec_write=True,required='仅人工对照原始人类Jack的黄发/蓝眼/眼镜，不作为IP输入；原图长裤靴子不继承，本次衣装由最终色稿的紫T/卡其短裤/运动鞋覆盖。')
spec['base_gates'].pop('G2_limited_fur')
spec['base_gates']['G2_sparse_hair_and_short_claws']='可见皮肤分布少量稀疏短毛，人皮底色大面积保留；没有灰毛手套、毛袖、全身毛皮。每个可见指尖只有单一短尖爪，无圆人类甲片叠爪或长钩爪。'
for j in spec['jobs']:
    j['run_if']+=' AND cumulative_generation_count_below_8'
    if j['id']=='V3_S04':
        j.update(region='one_selected_sparse_hair_or_short_claw_detail',
                 mask_scope='仅选一个实际仍有小缺陷的局部ROI，例如双手短爪或一处稀疏毛区；不能把颈/双臂/双腿全部并成大mask。',
                 positive_text='blackrat_style, blackrat, clean illustration, visible human skin with sparse newly sprouting fine short hairs, large bare spaces between strands, coherent human finger anatomy if visible, a single short tapered charcoal claw replacing each visible rounded fingernail, no separate original human nail plate, consistent local perspective and lighting',
                 negative_text='dense fur, solid gray furry gloves, continuous fur patches, fur cuffs, separate oval human nail plates, duplicate nails, long hooked talons, extra fingers, fused fingers, full character, miniature person, face on skin, text, watermark',
                 acceptance='本区为稀疏短毛或单一短尖爪，无旧圆甲片、无毛手套；同时复查全局门槛。')
spec['input_assets']['stage_edit_mask']['required']='同尺寸灰度PNG，白改黑留；仅当前选定小修区域，不用旧“肘下毛发截止”限制；LoadImageMask(red)。'
spec['asset_preparation_record_and_checks']=checks
spec.pop('asset_preparation_without_sampling',None)
spec['maximum_total_images']=8
spec['external_image_generation_images_used']=6
spec['maximum_remaining_comfy_sampler_images']=2
spec['maximum_conditional_local_images']=1
spec['execution_policy']=[p for p in spec['execution_policy'] if '最大6次KSampler' not in p and '本规格要求手绘' not in p]
spec['execution_policy'].append('累计8张上限包含已使用的6次外部结构图生成/修改；剩余最多S01一次＋一个按需局修。不得把六个jobs全部采样；计数达到8立即结束，预览/尺寸导出/控制图提取没有KSampler不增加计数。')
spec['field_contract']['maximum_total_images']='累计硬上限8；已用外部生成/修改6，最多剩2次Comfy采样。jobs是可选步骤目录，不是全部必跑。'
spec['field_contract']['status']='结构输入已制作绑定，但S01尚未采样；用户仍可修改外观。局部mask/ROI在选中对应局修步骤时再准备。'
spec['temporary_api_contract']['no_auto_enqueue']='本次仅准备和绑定结构输入；未提交S01。不自动运行后续扩散任务。'
spec['notes'].append('2026-11-01后续用户更正覆盖旧局部毛发边界：全身可见皮肤为稀疏分散短毛，并新增单一短尖爪。')
MATRIX.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n','utf-8')

sources=[('lineart_initial','exec-e853151f-2fc1-42ee-ad5b-4fd44132389e.png'),('lineart_ear_bangs','exec-3305ada5-4695-46e1-b7a6-436c2297b31a.png'),('color_dense_rejected','exec-b6750021-c11c-49a5-a6ad-3ceebf2c4454.png'),('color_sparse','exec-af959f86-a456-480e-b3fb-0c76f7ff6b02.png'),('pointed_human_plate_rejected','exec-72361475-be0f-41f1-b050-5458f52981b1.png'),('single_short_claws_selected','exec-17d720f8-a5c8-43d0-98ee-dad95561d64f.png')]
genroot=Path(r'C:\Users\Xu.DESKTOP-SPAQC9J\.codex\generated_images\01a0d96b-3727-7393-b623-0c7a1db997d9')
manifest={'date':'2026-11-01','generator':'built-in image_gen','selected_color_source':str(genroot/sources[-1][1]),'generated_image_calls':len(sources),'generation_history':[{'role':role,'path':str(genroot/name),'sha256':hashlib.sha256((genroot/name).read_bytes()).hexdigest()} for role,name in sources],'final_color':'Jack_TF_V3_mid_color.png','final_lineart':'Jack_TF_V3_mid_lineart.png','width':832,'height':1216,'alignment_method':'最终色稿同一ImageScale输出直接送LineartStandardPreprocessor→ImageInvert；没有独立重画/裁切/仿射移动。','lineart_extraction_graph':'../verification/input_V3/non_sampling_export_graph_final.json','KSampler_executions_this_turn':0,'remaining_cumulative_budget':2,'formal_endpoint':None,'latest_user_overrides':spec['latest_user_overrides']}
for name in [manifest['final_color'],manifest['final_lineart']]:manifest[name+'_sha256']=hashlib.sha256((OUT/name).read_bytes()).hexdigest()
(OUT/'输入清单与生成记录.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({'files_written':str(OUT),'matrix_status':spec['status'],'generated_images_used':6,'remaining_sampler_budget':2,'S01_submitted':False},ensure_ascii=False))
