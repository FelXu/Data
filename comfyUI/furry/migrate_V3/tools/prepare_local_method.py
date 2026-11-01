"""Prepare local, inspectable method specification and manual card; no sampling."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
COMFY=Path(r'E:\ComfyUI-aki-v3\ComfyUI')
TARGET=ROOT/'Jack_男性犬科TF_最小测试矩阵.json'
old=json.loads(TARGET.read_text('utf-8-sig'))
if old.get('kind')=='robot_local_method_transfer_spec':
    raise SystemExit('Method already prepared; edit the current spec directly to preserve execution state.')
archive=ROOT/'verification/method_transfer_20261101'
archive.mkdir(exist_ok=True)
backup=archive/'matrix_before_method_transfer.json'
assert not backup.exists()
shutil.copy2(TARGET,backup)
out=ROOT/'本机方法迁移_V3';out.mkdir(exist_ok=True)

POS=(
    'blackrat_style, blackrat, a freshly redrawn finished illustration, clean expressive ink contours, '
    'developed cel shading and coherent form shadows, solo adult male Jack in an early canine transformation, '
    'golden-yellow shaggy medium-length hair with thick bangs, blue eyes, black rectangular glasses worn normally, '
    'an incomplete very short muzzle only beginning at the nose tip and front jaw, recognizable human cheeks and lips, '
    'the same original pair of ears partly lengthening, sparse fine short hairs scattered over mostly visible human skin, '
    'one single newly grown short charcoal claw on each visible fingertip, no separate rounded human nail plate, '
    'moderately expanding shoulders and chest, opaque purple cotton T-shirt and khaki shorts BOTH showing taut seams and fabric tension, '
    'startled expression, mouth slightly open, body recoiling, knees slightly bent, both hands at chest height checking the change, '
    'closed sneakers, full-body three-quarter view, simple light background, '
    'preserve identity and the readable intermediate anatomy while rebuilding rough draft contours, hair strands, garment folds and shading'
)
NEG=(
    'low quality, blurry, bad anatomy, extra characters, extra limbs, extra fingers, fused fingers, '
    'fully transformed Anubis, complete canine head, long muzzle, lost human cheeks, full fur coat, dense furry gloves, '
    'double nail plates, rounded human nails under claws, long hooked talons, extra ears, tail, '
    'missing glasses, broken glasses, different hair color, changed outfit, missing clothing, transparent fabric, '
    'calm greeting pose, waving, confident smile, horns, crown, jewelry, '
    'near-identical tracing, copied sketch strokes, unfinished color blocking, rough underpainting, '
    'neon outlines, rainbow contour lines, fluorescent skin, false colors, color posterization, '
    'unrequested handheld object, phone, book, text, watermark, collage, cropped head, cropped feet'
)
inputs={}
for key,name,alias in [('color','Jack_TF_V3_mid_color.png','mid_color_draft.png'),('lineart','Jack_TF_V3_mid_lineart.png','mid_lineart.png')]:
    source=ROOT/'input_V3'/name;dest=COMFY/'input/Jack_TF_V3'/alias
    assert source.read_bytes()==dest.read_bytes()
    inputs[key]={'source_file':str(source),'comfy_input_relative':'Jack_TF_V3/'+alias,
                 'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                 'role':'layout/color draft, never the finished output' if key=='color' else 'spatial outline condition; same coordinates as color draft'}

spec={
    'kind':'robot_local_method_transfer_spec','schema_version':4,'workflow_family':'Jack V3',
    'revision':'V3_local_method_transfer_20261101','date':'2026-11-01','status':'method_prepared_not_submitted',
    'purpose':'方法迁移：把明确的中期轮廓/配色/身份转为本机可复用输入，以新墨线与赛璐璐层次重画；不承诺等同image_gen模型能力。',
    'formal_endpoint':{'character':'Jack','sequence_type':'TGTF','target':'adult female anthropomorphic Anubis','appearance_details':'not finalized','inherit_old_queen_design':False},
    'current_stage_subject':'adult male Jack in the supplied early-stage structural draft; do not inject the terminal female Anubis design into this method test',
    'checkpoint':'indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors',
    'style':{'alias':'ILstyle','filename':'blackrat_style：IllustriousBlackRat_Style.safetensors','strength_model':0.8,'strength_clip':0.8,'trigger_words':['blackrat_style','blackrat'],'BRIL_enabled':False},
    'inputs':inputs,
    'sampling_defaults':{'width':832,'height':1216,'batch_size':1,'steps':28,'cfg':5.0,'sampler':'euler_ancestral','scheduler':'normal','seed':2026110101,'ui_control_after_generate':'fixed','clip_last_layer':-2,'denoise_tiers':[0.65,0.75],'OpenPose_enabled':False,'IPAdapter_enabled':False},
    'lineart':{'model':'noob-sdxl-controlnet-lineart_realistic.fp16.safetensors','strength_default':0.5,'strength_range':[0.45,0.55],'start':0.0,'end':0.75,'input':'inputs.lineart','input_preprocessing':'provided lineart is used directly, same-size scale only; do not re-extract or automatically invert','end_semantics':'model-noise-time percentage, not an exact count of this img2img run steps'},
    'selected_mode':'lineart_ablation',
    'selection_reason':'已查看历史R01/R02，出现霓虹描边/异常肤色，未通过。默认先以同降噪做CN关/开排查，不能把旧两图当成成功迁移。根因尚未确认。',
    'modes':{
        'lineart_ablation':{'purpose':'当前建议：固定denoise0.65，先关CN再开CN，只有CN变量不同',
                            'jobs':[{'id':'M01_CN_OFF_D065','denoise':0.65,'lineart_enabled':False,'lineart_strength':0.0},
                                    {'id':'M02_CN_ON_D065','denoise':0.65,'lineart_enabled':True,'lineart_strength':0.5}]},
        'denoise_pair':{'purpose':'色彩管线正常后使用：固定CN0.50，只比较0.65/0.75',
                         'jobs':[{'id':'D01_D065_CN050','denoise':0.65,'lineart_enabled':True,'lineart_strength':0.5},
                                 {'id':'D02_D075_CN050','denoise':0.75,'lineart_enabled':True,'lineart_strength':0.5}]}
    },
    'prompts':{'positive_full':POS,'negative_full':NEG,'append_again':False},
    'transformation_loras':{
        key:{'enabled':False,'strength_model':0.0,'strength_clip':0.0,'filename':old['models'][key]['filename']}
        for key in ['species','mid','byil']
    },
    'transformation_lora_reactivation':[
        '先同时通过重绘、正常配色、身份和中期结构验收；未通过时不能靠开启TF LoRA修复。',
        '之后另立新预算，仅当某处转化特征缺失时，先编辑该处线稿/色稿，再做局部的单一TF LoRA与关闭对照。',
        'Species、Mid、BYIL只选一种；沿用确切版本的已核实触发配置，不合并触发词，不用权重代替阶段百分比。',
        '本方法不在运行末尾自动开启任意TF LoRA，终态具体外观未定前不把旧女王细节写回。'
    ],
    'budget_scope':'one explicitly selected mode per run; previous samples are historical, not a new allowance',
    'maximum_total_images':2,'maximum_remaining_comfy_sampler_images':2,'B_enabled':False,
    'parameter_guards':{'forbidden_expression':'denoise <= 0.5 AND effective_lineart_strength >= 0.75','on_violation':'abort_before_enqueue','never_chain_generated_outputs':True,'never_save_color_draft_as_finished_result':True},
    'execution_policy':[
        '只选一个mode编译并运行其jobs，最多2张，不能把两个mode当四张连跑；编译不提交。',
        '两张都从原始color输入独立开始，固定相同seed、style、steps/CFG/采样器和文本；不得使用旧S01或第一张输出作第二张源。',
        '每次只提交一个job，保存prompt_id与完整graph，查看结果后才决定是否进入该mode第二张。',
        '任何hard_failure出现立即停止整轮；若只是重绘不足而无硬失败，可在上限内完成另一项预设对照，仍不能算验收通过。',
        '两张后没有合格结果就停止，保留记录；不自动加seed、不加第三张、不切另一个mode、不启用TF LoRA。'
    ],
    'hard_failures':[
        '霓虹/红黄彩色描边、明显绿灰异常肤色或严重颜色破坏。',
        '完整犬头/长吻、全身毛皮，或直接跳到完整女性阿努比斯终态，中期结构消失。',
        '黄发/蓝眼/正常眼镜身份锁明显丢失，原衣物覆盖消失，角色数量错误。',
        '明显手指/肢体/耳连接错误，或凭空拿手机、书本等未要求物体。'
    ],
    'acceptance':{
        'new_drawing':'并排对比源色稿：可见新组织的墨线，头发/五官或衣褶确有重建，出现成熟赛璐璐明暗层次；仅换色、锐化或PNG/hash不同不算通过。',
        'structure':'仍可读出人类颊部＋未完成的短吻、原耳过渡、稀疏初期短毛/短尖爪、衣裤受力和惊慌查看双手。',
        'source_is_not_final':True,'all_hard_checks_required':True
    },
    'robot_contract':{
        'compiler':'tools/compile_local_method.py',
        'compiler_modes':'--mode lineart_ablation OR --mode denoise_pair; compile only, never submits',
        'jobs':'Only current top-level jobs are executable; modes are alternative recipes, never traverse both.',
        'api_submission':'POST http://127.0.0.1:8188/prompt with {"prompt": <parsed job.api_graph_file>, "client_id": "jack-local-method"}',
        'history':'Use returned prompt_id to read /history/{prompt_id}; unknown submission status must be checked before retry.',
        'output':'SaveImage prefixes are relative to ComfyUI/output; new unique REVIEW run tag prevents overwriting old results.',
        'legacy_runner_compatible':False,
        'quality_review':'No auto-pass based on queue success or image hash; require recorded visual checks before next job.'
    },
    'prior_evidence':{'archived_spec':str(backup),'R01_R02_status':'executed; observed neon edge/false-color defects, not accepted','pipeline_equivalence_claimed':False,'new_jobs_submitted_this_turn':0},
    'sources':[{'url':'https://docs.comfy.org/tutorials/basic/image-to-image','supports':'VAE img2img及降噪对输入保持程度的影响'},
               {'url':'https://blog.comfy.org/p/preprocessor-and-frame-interpolation','supports':'Lineart为轮廓信息，颜色/材质需要其他条件'},
               {'local':'_ops_V3/graph_V3_S01_R01_T03.json and 场景实操模板/api/T03_草图定稿_角色参考加线稿.json','supports':'接线和旧T03内容按本机核对；参数是待验起点而非质量保证'}]
}
TARGET.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n','utf-8')
(out/'POS_方法验证.txt').write_text(POS+'\n','utf-8-sig')
(out/'NEG_方法验证.txt').write_text(NEG+'\n','utf-8-sig')

card='''Jack V3 本机方法迁移 — ComfyUI手操卡
日期：2026-11-01。迁移的是“明确中期草图→受控重画→验收”的方法，不等于复刻image_gen模型能力。
正式终点：Jack TGTF→成年女性阿努比斯anthro；appearance_details=not finalized；inherit_old_queen_design=false。
本次输入仍是当前成年男性Jack早期结构，只验证能否画出新画；终态词不加入本次POS。

0 准备与选择模式
原T03仍含V33、另一套BlackRat v1、旧女王文字及IP参考。手动另存自己的工作副本；按以下完整替换，不能仅往旧提示后追加。
本卡不会自动修改已保存T03/T11或运行图片。配套机器人API是API图，不是界面workflow JSON。
历史R01/R02已执行但有霓虹描边、异常肤色，不能说通过。因此当前先选“Lineart关/开”同降噪诊断模式；关CN在前。
模式A：同一denoise0.65，CN=0与0.50，其他固定。最多2张。
模式B：配色正常后另选一轮，CN固定0.50，denoise=0.65与0.75。最多2张。
每轮只选一种模式，不把两种模式合计四张自动连跑。以下节点数值为可复用起点，画质需验收。

1 色稿分支（决定构图/配色的起点，不是最终图）
Load Image：Jack_TF_V3/mid_color_draft.png
→ ImageScale：lanczos，832×1216，crop=disabled
→ VAEEncode（普通VAE编码）
→ KSampler.latent_image。
VAEEncode.vae接Checkpoint的VAE。不要用EmptyLatentImage替代，也不要用VAEEncodeForInpaint处理整张色稿。
实际节点可对照900→901→902→6；原T03的空latent5不再接采样器。
源文件：../input_V3/Jack_TF_V3_mid_color.png；Comfy输入副本已存在。

2 线稿分支（只提供结构条件）
Load Image：Jack_TF_V3/mid_lineart.png
→ ImageScale：同为832×1216、crop=disabled
→ ControlNetApplyAdvanced.image。
ControlNetLoader：noob-sdxl-controlnet-lineart_realistic.fp16.safetensors
常规强度0.45–0.55，起点0.50；start=0.00、end=0.75。
正/负CLIP编码分别接ControlNetApplyAdvanced的positive/negative，再将它两个输出接KSampler对应输入；可选vae接同一个Checkpoint.VAE。
可对照50→51→53；52是模型。当前已有线稿先原样使用，不重复提线、不自动反相。
end=.75是模型噪声时间范围，不能精确说成“本次28步前21步”。

3 底模、画风与文本
Checkpoint：indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors
Checkpoint.MODEL→LoRA Loader.model。
Checkpoint.CLIP→CLIPSetLastLayer(stop_at_clip_layer=-2)→LoRA Loader.clip。
LoRA：blackrat_style：IllustriousBlackRat_Style.safetensors；Model=0.80，Clip=0.80。
触发词仅blackrat_style, blackrat；不用BRIL、别套另一套BlackRat触发词。
LoRA的MODEL→KSampler.model；LoRA的CLIP同时→正、负两个CLIP Text Encode。
如用Power Lora Loader：只开启这一个风格行，Model/Clip均0.80，其余行关闭。Species/Mid/BYIL本轮全部关闭。
将本目录POS_方法验证.txt和NEG_方法验证.txt全文分别复制到正负编码器。
改原T03时，完整替换旧20–24字符串链/旧NEG，或新增两个CLIP Text Encode粘贴全文并改接；不能保留旧女王串词。
将KSampler.model从旧64(IPAdapter)输出改接LoRA.MODEL，断开旧60–64参考影响。OpenPose与IP均不使用。

4 采样与两档对照
KSampler：euler_ancestral；scheduler=normal；steps=28；CFG=5.0；seed=2026110101；batch=1。
界面seed旁的control_after_generate必须设fixed，不能留randomize/increment。两个任务都读原始色稿。
模式B只改denoise：第一张0.65，第二张0.75。不要同时改style、CN、CFG、seed或POS/NEG。
更高降噪通常允许离开原稿更多，也更容易损失结构；0.75不是必然更好。
禁止组合：denoise≤0.50且有效CN强度≥0.75。色稿不能直接作为最终输出。

5 解码和保存
KSampler.LATENT→VAEDecode.samples；同一个Checkpoint.VAE→VAEDecode.vae。
VAEDecode.IMAGE→SaveImage。
SaveImage前缀：Jack_Test/REVIEW_20261101_Jack_METHOD_<本轮新编号>/<任务名>
它相对ComfyUI/output，不要把原色稿直接接SaveImage，也不要用原图回贴覆盖采样结果。
每次记录prompt_id、完整API、输入hash、seed/参数和实际输出文件。

6 如何关闭Lineart做对照
手动最简单：节点53 strength=0，其他连线不变；或把KSampler正/负直接连正/负CLIP编码器，绕过53。
机器人生成的CN_OFF图采用真实绕过：不加载CN节点，KSampler直接接两个CLIP编码。
模式A第一张关CN，第二张CN=.50，两张都denoise=.65，其余完全相同。不能拿denoise=.75的图与关CN .65图归因比较。
模式A替代模式B，不是追加第三张。关CN仍读同一色稿VAE latent，不是纯文生图。
若只有开CN才出现霓虹/假色，停止后另做该ControlNet输入/匹配排查；若关CN也异常，先检查底模/LoRA/编码解码配套，不能靠提高CFG/叠NEG硬推。根因尚未证实。

7 验收与停机
必须是“可辨的新画”：并排看头发、五官、衣褶，确有重建墨线和赛璐璐明暗；仅色偏/锐化/hash变化不通过。
同时保持人类颊部与未完成短吻、原耳过渡、稀疏短毛和单一短尖爪、衣裤受力、惊慌查看双手。
霓虹彩边/异常肤色、严重解剖错、身份丢失、凭空手持物体、完整终态均为硬失败：立即停本轮，后项不排。
若只重绘不足但无硬失败，可完成同模式另一项预设对照；最多两张后仍未通过就停止，无B、不重抽、不自动换模式。

8 什么时候再开Species/Mid/BYIL
先让重绘、正常配色、身份和中期结构全部通过。复制色稿仍很像时，开TF LoRA不是解决办法。
以后某个局部转化特征仍弱，先画清该处目标轮廓，再在另立预算的局部测试中，一次只开一种TF LoRA与关闭对照。
权重不是进度百分比；不混触发合集，不把女性阿努比斯终态整套词提前写进当前早期格，不继承旧女王设定。

机器人使用
同名Jack_男性犬科TF_最小测试矩阵.json为执行规格。当前已编译的job.api_graph_file可作为POST /prompt的prompt对象。
tools/compile_local_method.py --mode lineart_ablation 或 --mode denoise_pair 会重新生成一个模式的两份API并更新当前jobs，只编译，不提交。
只遍历顶层jobs，绝不能同时遍历modes里的候选列表。旧A/V2/V3运行脚本不兼容新schema。
来源：https://docs.comfy.org/tutorials/basic/image-to-image
https://blog.comfy.org/p/preprocessor-and-frame-interpolation
'''
(out/'ComfyUI手操卡.txt').write_text(card,'utf-8-sig')
print(json.dumps({'spec':str(TARGET),'manual':str(out/'ComfyUI手操卡.txt'),'default_mode':spec['selected_mode'],'image_jobs_submitted':0},ensure_ascii=False))
