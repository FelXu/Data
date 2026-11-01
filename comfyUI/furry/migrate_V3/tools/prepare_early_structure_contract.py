"""Prepare early-stage semantic contract, local edit recipes and manual; no sampling."""
from pathlib import Path
import copy
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
COMFY=Path(r'E:\ComfyUI-aki-v3\ComfyUI')
TARGET=ROOT/'Jack_男性犬科TF_最小测试矩阵.json'
OUT=ROOT/'本机方法迁移_V3'
VERIFY=ROOT/'verification/early_structure_20261101'
VERIFY.mkdir(exist_ok=True)
old=json.loads(TARGET.read_text('utf-8-sig'))
if old.get('revision')=='V3_early_structure_semantic_contract_20261101':
    raise SystemExit('Already prepared; preserve current state.')
backup=VERIFY/'matrix_before_early_structure_contract.json'
assert not backup.exists();shutil.copy2(TARGET,backup)

POS=(
    'blackrat_style, blackrat, a freshly redrawn clean ink and cel-shaded illustration, solo adult male Jack, '
    'shaggy golden-yellow hair with thick bangs, blue eyes, black rectangular glasses worn normally, '
    '(only the tips of the same human ears are becoming slightly pointed:1.25), normal human ear length and bases, '
    '(a subtly canine-shaped nose tip retaining natural skin color:1.25), '
    'human nasal bridge, cheeks, upper lip, chin and jaw remain in their original human positions and proportions, '
    'flat human facial profile without a projecting muzzle, '
    'sparse fine short hairs sprouting separately over visible human skin, large bare spaces between strands, '
    '(mostly natural human fingernails with only a small distal tip area beginning to darken charcoal:1.25), '
    'normal short human nail length and fingertip silhouettes, natural proximal nail plates retained, '
    'moderately enlarging shoulder and chest muscles filling the original opaque purple cotton T-shirt, '
    'original khaki shorts also pulled taut over expanding thighs, visible fabric tension and pulling folds on BOTH garments, '
    'continuous unbroken fabric, intact seams, startled worried expression, mouth slightly open, '
    'body leaning back, knees slightly bent, both hands held near the chest checking the change, closed sneakers, '
    'full-body three-quarter view, readable new ink contours, developed cel-shaded form, simple light background'
)
NEG=(
    'complete canine head, projecting muzzle, protruding jaw, elongated facial bones, elongated canine ears, '
    'black dog nose, dark nose leather, furry face, full fur coat, dense fur patches, opaque furry gloves, fur cuffs, '
    'solid black nail plates, complete claws, hooked talons, long pointed nails, loss of natural human nail plates, '
    'torn fabric, holes, ripped seams, fraying, missing clothing, transparent fabric, '
    'fully transformed female Anubis, extra ears, extra limbs, extra fingers, fused fingers, '
    'different hair color, missing glasses, distorted glasses, calm greeting wave, confident smile, '
    'neon outlines, rainbow contour lines, fluorescent skin, false colors, unrequested handheld object, '
    'near-identical tracing, copied rough sketch strokes, unfinished underpainting, text, watermark, collage'
)
EARLY={
    'E1_ears':'同一对人耳，仅上缘耳尖刚变尖，耳长与耳根基本仍人类；明显尖长兽耳失败。',
    'E2_nose':'仅鼻头形状轻微犬形化，颜色仍接近周围人皮；黑色鼻皮失败。',
    'E3_face_bones':'鼻梁、颊骨、上唇、下颌与下巴保持人类比例，无吻突、无面骨前伸。',
    'E4_hair':'可见皮肤有稀疏、分散的细短毛，大面积人皮清楚；连续毛片/灰毛手套失败。',
    'E5_clothes':'肩胸大腿开始增大，紫T和卡其短裤同时受力，但面料与缝线完整，无破洞开线。',
    'E6_nails':'自然人甲整体与短长度保留，只有远端一小部分甲尖开始发黑；整枚黑甲、突出尖爪失败。',
    'E7_identity_emotion':'成年男性Jack、黄发厚刘海、蓝眼、正常黑框眼镜、原衣鞋；慌张查看双手，非平静挥手。'
}
edit_prompts={
    'nail_tip_only': 'Edit only the nails and tiny fingertip silhouettes. Restore normal SHORT human fingernails, natural proximal nail plates and normal finger pads. Remove the existing protruding pointed claws and restore the original short human fingertip outline. Darken ONLY a small distal tip area of each visible nail to charcoal, keeping most of every nail natural. No whole black nail, no new claw projection. Keep all fingers, pose, sparse body hair, ears, face, glasses, hair, clothing, colors and background unchanged.',
    'nose_tip_only': 'Edit ONLY the nose tip. Give the nasal tip a very subtle canine-like shape while retaining its natural human skin color. Keep the nasal bridge, cheeks, upper lip, jaw, chin and facial-bone proportions unchanged. No forward muzzle, no jaw projection, no black dog nose. Keep the glasses, eyes, hair, expression and every other part unchanged.',
    'ear_tips_only': 'Edit ONLY the tips of the existing human ears. Restore nearly normal human ear length and human ear bases; only the upper ear rims begin to form small points. Remove the overly long pointed ear silhouette. Keep the same original pair, no second ear pair, no upright dog ears. Preserve hair, glasses, face, pose and everything else.'
}
steps={
    'T03':{'operation':'whole_image_redraw_from_approved_structure','steps':28,'cfg':5.0,'sampler':'euler_ancestral','scheduler':'normal','denoise_candidates':[0.65,0.75],'ILstyle_model':0.8,'ILstyle_clip':0.8,'lineart_default_enabled':False,'lineart_when_enabled':{'strength':0.5,'range':[0.45,0.55],'start':0.0,'end':0.75},'source_gate':'all E1–E7 must pass before T03; current cached source does not pass'},
    'T06':{'operation':'preserve_structure_local_texture_or_tip_color','denoise_range':[0.25,0.40],'recommended':0.30,'lineart_enabled':False,'steps':28,'cfg':5.0,'ILstyle_model':0.6,'ILstyle_clip':0.6,'mask_rule':'只遮需要变化的甲尖小范围/一处毛发等；不遮整张人甲，不改变已正确轮廓。'},
    'T06b':{'operation':'local_structure_rebuild_only_if_needed','denoise_range':[0.55,0.65],'recommended':0.60,'lineart_strength_range':[0.45,0.55],'lineart_start':0.0,'lineart_end':0.75,'steps':28,'cfg':5.0,'ILstyle_model':0.6,'ILstyle_clip':0.6,'mask_rule':'若去旧尖爪或缩耳，mask必须包住旧突出形状、目标新轮廓与两者间背景；局部正确线稿须独立接CN，不能只在mask内预画线。'}
}
spec={
    'kind':'robot_early_structure_migration_spec','schema_version':5,'workflow_family':'Jack V3',
    'revision':'V3_early_structure_semantic_contract_20261101','date':'2026-11-01',
    'status':'source_reference_requires_latest_early_stage_revision',
    'semantic_transfer_validated':False,'source_semantic_pass':False,
    'formal_endpoint':{'character':'Jack','sequence_type':'TGTF','target':'adult female anthropomorphic Anubis','appearance_details':'not finalized','inherit_old_queen_design':False},
    'current_subject':'adult male Jack at the exact early stage E1–E7; terminal TGTF design is metadata only',
    'checkpoint':'indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors',
    'style':{'alias':'ILstyle','filename':'blackrat_style：IllustriousBlackRat_Style.safetensors','strength_model':0.8,'strength_clip':0.8,'trigger_words':['blackrat_style','blackrat'],'BRIL_enabled':False},
    'inputs':{
        'layout_color':{'file':str(ROOT/'input_V3/Jack_TF_V3_mid_color.png'),'comfy_input':'Jack_TF_V3/mid_color_draft.png','origin':'cached image_gen color construction image','allowed_role':'composition/color/layout reference only; NOT approved current early anatomy'},
        'layout_lineart':{'file':str(ROOT/'input_V3/Jack_TF_V3_mid_lineart.png'),'comfy_input':'Jack_TF_V3/mid_lineart.png','origin':'deterministically extracted from cached color image','allowed_role':'layout reference only; old full claws and elongated ears are not ground truth'},
        'approved_color':None,'approved_lineart':None,
        'current_reference_failures':['full dark pointed claws conflict with only a small dark distal nail tip','visible ear is more elongated/pointed than just-sharpened human ear tips'],
        'policy':'Runtime can be entirely local; do not call image_gen by default. Reuse cached image_gen art only after E1–E7 are corrected and reviewed. Local Klein edit or manual drawing can replace image_gen source preparation.',
        'approval_record_required':['source_sha256','E1_to_E7_boolean_results','reviewer','review_notes'],
        'abort_before_T03_if_source_not_passed':True,
        'pair_alignment':'After changing source silhouette, regenerate same-coordinate lineart from final approved color; never keep the old mismatching claw/ear lineart.'
    },
    'early_stage_contract':EARLY,
    'sampling_defaults':{'width':832,'height':1216,'steps':28,'cfg':5.0,'sampler':'euler_ancestral','scheduler':'normal','seed':2026110101,'batch_size':1,'ui_seed_control':'fixed','clip_last_layer':-2,'OpenPose_enabled':False,'IPAdapter_enabled':False},
    'lineart':{'model':'noob-sdxl-controlnet-lineart_realistic.fp16.safetensors','default_strength':0.5,'recommended_range':[0.45,0.55],'start':0.0,'end':0.75,'initial_diagnostic_enabled':False,'reason':'historical CN runs showed false-color/neon artifacts; root cause not established'},
    'numerical_guards':{'forbidden':'denoise <= 0.5 AND effective_lineart_strength >= 0.75','applies_to':['T03','T06','T06b'],'action':'abort_before_submission','ILstyle_test_range':[0.6,1.0],'ILstyle_default':0.8,'ILstyle_range_is_guarantee':False},
    'steps':steps,'prompts':{'positive_full':POS,'negative_full':NEG,'replace_old_prompt_entirely':True},
    'local_prompt_cards':{
        'nail_tip_POS':'natural short human fingernails, proximal nail plates retain their natural color, only a small distal nail-tip area beginning to darken charcoal, normal human fingertip silhouette',
        'nail_tip_NEG':'whole black nail plate, protruding claw, hooked talon, loss of human nail plate, extra nail',
        'nose_POS':'slightly canine-shaped nose tip in natural skin color, unchanged human bridge, cheeks, upper lip and jaw, human facial profile',
        'nose_NEG':'black dog nose, dark nose leather, projecting muzzle, elongated jaw, changed facial bones',
        'ear_POS':'the same human ears, normal human ear bases and length, only tiny points beginning at the upper rims',
        'ear_NEG':'long upright dog ears, elongated elf ears, second ear pair, changed hair or glasses',
        'fabric_POS':'continuous intact opaque purple cotton or khaki fabric as appropriate to this crop, tension folds over enlarging muscles, pulled taut intact seams',
        'fabric_NEG':'holes, torn cloth, ripped seams, fraying, new outfit, face or miniature person on clothing'
    },
    'local_klein_option':{'installed':True,'new_download_required':False,'role':'optional local semantic source editor; not a replacement for V35 render model','diffusion_model':'flux-2-klein-4b-fp8.safetensors','text_encoder':'qwen_3_4b.safetensors','vae':'flux2-vae.safetensors','steps':4,'cfg':1.0,'sampler':'euler','seed':2026110101,'ILstyle_enabled':False,'one_detail_per_job':True,'instructions':edit_prompts,'negative_prompt_policy':'do not copy SDXL NEG recipe; the existing distilled CFG1 workflow uses its reference-conditioning path'},
    'transformation_loras':{'Species':{'enabled':False},'Mid':{'enabled':False},'BYIL':{'enabled':False}},
    'when_to_enable_TF_lora':'Only after source accuracy AND V35 redraw/color pipeline both pass; later test one local unmet feature with one TF LoRA and a no-TF control in a separate budget. Never use TF LoRA to define this early stage by strength alone.',
    'selected_run_type':'source_semantic_repair',
    'run_types':{
        'source_semantic_repair':{'max_images':2,'description':'choose ONE detail (nails first is recommended), one local Klein edit, inspect; if a second predeclared test is used, same instruction with alternate seed. Do not silently proceed to T03 in the same exhausted budget.'},
        'T03_denoise_pair':{'max_images':2,'precondition':'approved source E1–E7 and source hashes bound','jobs':[{'id':'E_T03_D065','denoise':0.65,'lineart_enabled':False,'lineart_strength':0.0},{'id':'E_T03_D075','denoise':0.75,'lineart_enabled':False,'lineart_strength':0.0}]},
        'T03_CN_ablation':{'max_images':2,'precondition':'approved source E1–E7 bound and redraw/color pipeline works without CN','jobs':[{'id':'E_T03_CN_OFF','denoise':0.65,'lineart_enabled':False,'lineart_strength':0.0},{'id':'E_T03_CN_ON','denoise':0.65,'lineart_enabled':True,'lineart_strength':0.5}]},
        'T06_one_region':{'max_images':2,'precondition':'a mostly accepted image plus one resolved ROI and reviewed masks; ordinary T06 for color, T06b only for structure'}
    },
    'maximum_total_images':2,'budget_scope':'one explicitly selected run type only; ALL AI source editing and sampling count, no free preprocessing generation','chain_run_types_automatically':False,'B_enabled':False,
    'execution_rules':['No T03 until source_semantic_pass is true with matching hashes and all E1–E7 reviews. Current source remains false.','Pick one run type; at most two actual generated images including failed local edits. No automatic second run type, no full sequence.','Each T03 comparison starts independently from the same approved source, fixed seed, identical text/style/CFG/steps; vary only the declared variable.','Any identity loss, premature complete anatomy, neon/false-color failure, extra body part or fabric tearing is a hard fail: stop.','Insufficient redraw is not accepted; at most the other predeclared comparison is allowed if no hard fail. After two failures switch route, do not keep raising weights.','Review local edits before accepting; failures never become the next source. Save all graph/input hashes and image paths.'],
    'pass_fail':{'source_pass':'all E1–E7 true; current cached art is NOT passed','render_pass':'all E1–E7 true AND clearly new ink/cel shading/material structure, not only color shift/sharpening/hash difference','local_pass':'target tiny detail corrected while other approved pixels/anatomy remain intact','hard_fail':['muzzle or facial-bone projection','whole dark claws or black dog nose','elongated fully canine ears or second ear pair','dense fur coat or patches','torn shirt or shorts','neon edges/false skin colors','identity or anatomy loss','complete female Anubis terminal form']},
    'reproducibility':{'semantic_stability_established':False,'current_scope':'same approved source, exact model hashes, graph, parameters and seed; not arbitrary prompts or new viewpoints','fixed_seed_does_not_prove_semantics':True,'future_validation':'only after a passing recipe exists, separately validate predefined other seeds/views with the same E1–E7 rubric; do not claim universal stability from one source'},
    'output_prefix':'Jack_Test/REVIEW_20261101_EARLY_<new_run_id>/<job_id>',
    'archive':str(backup),'previous_method_evidence':'R01/R02 already executed with neon/false-color defects; no local semantic success claimed',
    'robot_next_action':'review/correct source; prepared local Klein nail-tip API is an optional first edit, not a validated result',
    'sources':[
        'https://docs.comfy.org/tutorials/flux/flux-2-klein',
        'https://docs.comfy.org/tutorials/basic/image-to-image',
        'https://docs.comfy.org/tutorials/image/qwen/qwen-image-2-1',
        'https://github.com/Acly/krita-ai-diffusion'
    ]
}

# Executable local single-detail source edit. Original Klein workflow is never modified.
g=json.loads(Path(r'E:\CODEX\ComfyUI\_klein_setup_research\Klein4B_文字改图_单图_API.json').read_text('utf-8-sig'))
g['76']['inputs']['image']='Jack_TF_V3/mid_color_draft.png'
g['74']['inputs']['text']=edit_prompts['nail_tip_only']
g['73']['inputs']['noise_seed']=2026110101
g['9']['inputs']['filename_prefix']='Jack_Test/REVIEW_20261101_EARLY_KLEIN_NAIL/<new_run_id>'
api=OUT/'api/EARLY_Klein_甲尖单点_API.json';api.parent.mkdir(exist_ok=True);api.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n','utf-8')
spec['local_klein_option']['prepared_nail_API']=str(api)
spec['local_klein_option']['submit_guard']='replace output placeholder with unique run id, inspect layout source, count this as image1; no automatic submission'
spec['jobs']=[{'id':'EARLY_SOURCE_REVIEW','operation':'read_current_images_and_check_E1_E7','generates_images':0,'status':'requires_revision'}, {'id':'EARLY_KLEIN_NAIL_OPTION','operation':'optional_single_detail_local_edit','api_graph_file':str(api),'generates_images':1,'status':'prepared_not_submitted','run_if':'operator_or_robot_explicitly_selects_source_semantic_repair; current run generation count < 2'}]
TARGET.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n','utf-8')
(OUT/'A_机器人规格_初期结构准确.json').write_bytes(TARGET.read_bytes())
(OUT/'POS_方法验证.txt').write_text(POS+'\n','utf-8-sig')
(OUT/'NEG_方法验证.txt').write_text(NEG+'\n','utf-8-sig')

card='''B｜Jack 初期结构准确 — ComfyUI手操卡（2026-11-01）
本卡与A_机器人规格_初期结构准确.json描述同一规则。目标不是完整狼人或阿努比斯，而是七项初期变化。
正式终点：Jack TGTF→成年女性阿努比斯；细节not finalized，inherit_old_queen_design=false。本步仍是成年男性Jack。

一、先看清需要画对的是什么
E1 同一对人耳，仅上缘刚尖，耳长/耳根基本仍人类。
E2 鼻头轻微犬形化但仍肤色，不是黑鼻皮。
E3 鼻梁/颊骨/上唇/下颌不伸长，没有吻突或面骨推进。
E4 稀疏细短毛分散在可见皮肤，大面积人皮仍清楚，不是成片毛皮。
E5 肩胸大腿开始增大，两件原衣物同时绷紧，但紫T/卡其短裤布面和缝线完整。
E6 人类短指甲整体仍在，仅远端一小部分甲尖发黑，不是整枚黑甲，更不是突出尖爪。
E7 黄发厚刘海、蓝眼、正常眼镜、成年男性、原衣鞋，慌张查看双手。
现有input_V3两张旧图仅可复用构图/配色：整枚黑爪和较长尖耳不合格。不能继续低噪复制后声称初期通过。

二、输入是否还要image_gen
不需要每次调用。已有图缓存后可完全离线推理；但必须先符合E1–E7。
你可选：①本地Klein指令修母图；②在绘图软件精确改耳/鼻/甲尖；③自己画出正确色稿和线稿。
修改了甲爪/耳轮廓后，最终线稿必须从新色稿同坐标重提，不能继续用旧尖爪/长耳线稿。
批准母图后存为ComfyUI/input/Jack_TF_EARLY/approved_color.png与approved_lineart.png；两张同构图832×1216。
机器人须记录逐项检查和文件hash，source_semantic_pass=true后才能进T03。不能只改布尔值而不检查图。

三、T03：用正确母图重画新线条和赛璐璐层次
1. 载入随包EARLY_T03_初期结构重绘.json，或复制原T03另存新名字。
   原T03有V33、另一套BlackRat和旧女王/IP内容，不能只改一句提示词就直接用。
2. Checkpoint下拉框选indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors。
3. Checkpoint.CLIP→CLIPSetLastLayer；点stop_at_clip_layer填-2；再接LoRA.clip。
   Checkpoint.MODEL→LoRA.model。
4. LoRA下拉框选blackrat_style：IllustriousBlackRat_Style.safetensors。
   点strength_model=0.80，strength_clip=0.80。Power加载器同样只开ILstyle这一行；Species/Mid/BYIL全关，不用BRIL。
5. LoRA.MODEL→KSampler.model；LoRA.CLIP同时接正、负两个CLIP Text Encode。
   正负全文用本目录POS_方法验证.txt与NEG_方法验证.txt，旧字符串整段替换。
6. 色稿LoadImage选approved_color.png→ImageScale（832×1216，lanczos，crop=disabled）→普通VAEEncode→KSampler.latent_image。
   Checkpoint.VAE同时接VAEEncode与VAEDecode。不能用EmptyLatent替代色稿，也不用整图Inpaint编码。
7. 线稿LoadImage选approved_lineart.png→相同ImageScale→Apply ControlNet Advanced.image。
   ControlNetLoader选noob-sdxl-controlnet-lineart_realistic.fp16.safetensors。
   点Apply的strength：起点0.50，可比较0.45–0.55；start_percent=0.00，end_percent=0.75。
   正/负CLIP编码分别进Apply正/负，再进KSampler。现有白底黑线先不自动反相，不重复提线。
8. 历史有霓虹描边，因此先关CN验证基本重绘：strength=0；或KSampler正负直连两个CLIP编码器。
   关CN仍保留色稿VAE latent，不是纯文生图。机器人CN_OFF图会真正绕过CN分支。
9. KSampler点sampler_name=euler_ancestral，scheduler=normal，steps=28，cfg=5.0，denoise=0.65。
   seed=2026110101，control_after_generate=fixed，batch=1。
10. 如选两档降噪对照：两张均从同一approved_color开始，只改0.65→0.75，其他全不改。
    如选CN开/关对照：两张denoise都0.65，只改CN0→0.50。每轮只选一种对照，最多2张，不自动连跑4张。
11. KSampler→VAEDecode→SaveImage；prefix填Jack_Test/REVIEW_20261101_EARLY_<新编号>/<任务名>。
    SaveImage必须接重绘解码图，不能接色稿本身或用原图回贴覆盖重绘结果。

四、T06：已经大部分满意时，修一处小细节
1. 原图LoadImage右键→Open in MaskEditor（在遮罩编辑器打开）。只画需要改的区域，保存蒙版。
   这里用LoadImage的MASK：编辑器内部白=改；如果另用灰度PNG，LoadImageMask选red，白改黑留，别混alpha反相语义。
2. 用70/71/72改X/Y/正方形边长；73改工作边长（通常1024）。图、mask、缩回和回贴必须同一组裁框。
   先看T06c裁框/白区预览；不要凭原图目测跳过。
3. 甲尖只是局部变色，普通T06即可：点denoise从0.30起（0.25–0.40），CN关闭，ILstyle0.60/0.60。
   只遮远端甲尖一小块，保留自然近端甲片；POS用local_prompt_cards.nail_tip_POS。手部裁图不要写full body/全套五官。
4. 若源图已经是突出尖爪或长耳，需要先消去旧突出轮廓：用T06b denoise0.60（0.55–0.65）、局部CN0.45–0.55，或直接手绘正确边线。
   mask要覆盖旧突出部分、目标新边线与其间背景。T06b白区预画线会被重建处理，不能把它当独立线稿控制。
   局部正确线稿必须按相同裁框缩放后，独立接CN；原T06b没有这条线稿支路，需按API接法加，不能假装已有。
5. 眼镜、黄发、未改指甲根部设置保护区；外扩/羽化后再次扣保护，最终回贴别越出允许区。
6. 每次从最新通过版开始，只修一处；验收通过才升版本，失败不继续链式重绘。

五、数值禁区和验收
任何T03/T06/T06b都禁止denoise≤0.50且有效Lineart≥0.75同时出现；普通T06低降噪在CN关闭时允许。
E1–E7任一结构提前完成、衣服撕裂、身份丢失、假色霓虹、明显解剖错，立即停。
T03成品还须有新组织的墨线和赛璐璐层次；仅变色/锐化/hash不同不算重绘通过。
每轮最多2张，所有AI母图编辑也计数。两张失败不堆更多权重，切换下述路线；不跑B、不自动开TF LoRA。

六、下一次一键加载
第一次把母图、模型和数值设好后：点左上工作流名称/Workflow菜单→Save As（另存为），命名Jack_初期结构_已验母图。
再用Export（导出）保存界面Workflow JSON到本资料夹；不要选API格式当作可视工作流。
旧版界面可能显示Save按钮；也可Ctrl+S保存当前工作流。以实际菜单里的Save/Save As/Export为准。
下次把保存的界面JSON拖进ComfyUI画布，或Workflow→Open/Load打开。仍核对种子fixed、输入路径和LoRA文件是否存在。
API JSON供机器人POST /prompt；UI workflow JSON供你Load，两个格式不能混用。
模板会记住参数与输入路径，不会自动保证新姿势/新视角的语义正确；换姿势需新的合格结构输入。

七、纯V35做不到时的本地分界
本机有RTX5080 16GB和约64GB内存，已装Klein4B，优先零下载试本地指令编辑。
载入EARLY_Klein_甲尖单点编辑.json：只改甲尖指令，4步、CFG1、euler，ILstyle不加载（它是SDXL LoRA不能套Klein）。
一条局部指令最多两个预定seed都不服从，就判这个模型在此细节不可靠，转精确mask＋手绘/回贴，而不是继续改一长串提示。
Krita等绘图工具可以精确决定黑色只占甲尖、鼻头色仍为人皮；扩散只负责后续融合，不能覆盖必须精确保留的像素。
Qwen-Image-2.1可作为另一个本地指令编辑候选；官方INT8核心约17.3GB下载，可选提示增强另约9.47GB，本机未装且当前节点需核实/更新，16GB速度/显存未实测，不自动下载安装。
长期要让纯提示也常出这种初期，可考虑专门的初期概念LoRA；必须有一批验收过的多姿态样本和留出测试，单张母图训练不等于迁移语义推理。
只有重绘/颜色/结构都过关后才另测Species/Mid/BYIL：一次一种、局部明确目标，不用权重表示进度，不在本轮自动启用。

八、真实验证状态
当前“初期源图”尚不符合新版甲尖/耳尖要求，source_semantic_pass=false，semantic_transfer_validated=false。
接线与固定seed可复演配置，不代表V35已继承image_gen的理解力。当前文档/模板已准备，没有提交新图或声称稳定复现已通过。
后续稳定性只在已验母图、具体模型hash/graph/seed范围评估；新角度/新姿势不能外推保证。
'''
(OUT/'B_ComfyUI手操卡_初期结构准确.txt').write_text(card,'utf-8-sig')
(OUT/'ComfyUI手操卡.txt').write_text(card,'utf-8-sig')
print(json.dumps({'spec':str(TARGET),'manual':str(OUT/'B_ComfyUI手操卡_初期结构准确.txt'),'source_semantic_pass':False,'new_samples':0},ensure_ascii=False))
