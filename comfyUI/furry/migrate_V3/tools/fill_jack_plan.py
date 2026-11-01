"""Write the requested six-panel storyboard and a <=12-image test specification."""
from pathlib import Path
import json,shutil,hashlib

ROOT=Path(__file__).resolve().parents[1]
existing_matrix=ROOT/'Jack_男性犬科TF_最小测试矩阵.json'
if existing_matrix.exists():
    raise SystemExit('已有已填写的矩阵；历史生成器停止，避免重置LoRA绑定、实测记录或V2修订。请直接编辑当前文件。')
DATE='2026-11-01'
style={'alias':'ILstyle','filename':None,'strength_model':1.2,'strength_clip':1.2,
       'binding_status':'needs_exact_filename','trained_words':None,
       'binding_rule':'用户确认确切文件后填写；不得根据BlackRat名称猜选，不得用BRIL或其他变体替换；触发词沿用该ILstyle已确认配置。'}
models={
 'species':{'filename':'Species_Transformation_Concept_Illustrious.safetensors','sha256':'8e0e8784a54980f07fb4b8a22d422fca4eaebae86d981398d4ea679416818b69','civitai_version_id':2349624,'version':'Illustrious','trigger_selected':'species_transformation'},
 'mid':{'filename':'Mid_transformation.safetensors','sha256':'b263135f303a7d154959578f0617579775ca09e6240d09621b4f8fc7bf311010','civitai_version_id':1043354,'version':'v2.0 / Illustrious','trigger_selected':'transformation, mid transformation, transfur, furry'},
 'byil':{'filename':'transformation：LoraBYIL_transformation.safetensors','sha256':'6631a2a95804a26fb0e5277ba51d28407810a44d098a63fcab58122ff4bc3535','civitai_version_id':1371746,'version':'IL - Transformation','trigger_selected':'transformation'}
}
identity='solo, single character, (adult man:1.25), male, Jack, slim slender build, blue eyes, shaggy medium-length blond hair, thick bangs, opaque purple short-sleeved T-shirt, khaki shorts, intact sneakers, unchanged clothing, clean illustration'
common_negative='low quality, blurry, bad anatomy, extra person, duplicate character, extra arms, extra legs, extra fingers, missing fingers, fused fingers, extra ears, duplicate ears, duplicate glasses, floating eyewear, costume head, animal costume, horns, wings, crown, necklace, collar, armband, long black hair, huge muscles, different outfit, long trousers, boots, torn clothing, missing clothing, transparent clothing, bare feet, cropped head, cropped feet, text, watermark, multiple panels, collage'

frames=[
 {'n':1,'title':'人类起点','new':'无转化；建立约175cm、瘦弱成年男性的比较基准。',
  'retain':'偏长凌乱黄发、厚刘海、蓝眼、正常佩戴同一副黑框眼镜；紫色短袖T、卡其短裤、运动鞋完整。',
  'not_yet':'兽耳、犬吻、目标色短毛、爪、尾、角、翼，以及明显体型或性别变化。',
  'lora':'ILstyle Model/Clip=1.20/1.20；全部转化LoRA关闭。',
  'check':'单人、成年男性、瘦型；衣物不是旧版长裤/靴子；只有一副眼镜、两只人耳。身高为设定值，靠同机位比例比较，不从孤立像素推算米数。',
  'action':'自然站立，微侧身；建立统一地面线、头顶和鞋底留白。',
  'mask':'无需局修；保存人类基准图与完整参数。',
  'glasses':'G0：正常佩戴。',
  'english':'Jack remains fully human at the start of the transformation, wearing his black rectangular glasses and unchanged clothes, with shaggy blond hair, thick bangs and a relaxed balanced stance.'},
 {'n':2,'title':'手部初变','new':'手背小范围出现炭灰色短毛；指甲略尖，掌指体块轻微增厚；暂按五指含拇指。',
  'retain':'人类脸、耳、鼻口、体型、腿与鞋；黄发厚刘海、蓝眼和眼镜均不变。',
  'not_yet':'完整兽爪、全身毛色覆盖、兽耳、犬吻、尾；不能因转化标签直接跳终态。',
  'lora':'ILstyle 1.20/1.20 + Species 0.80/0.80，仅一种转化LoRA；手部蒙版局修。',
  'check':'变化停在手，五指仍能逐一追踪；不是手套或多长手；衬袖、短裤和鞋保持原样。',
  'action':'低头观察双手，重心仍在双脚；不突然改变身高和肌肉量。',
  'mask':'T06先改手背与指甲；若需重建手指轮廓，T06b包含手腕和指尖外的空白，逐手处理。',
  'glasses':'G0：正常佩戴，镜框不变。',
  'english':'During an early canine transformation, only Jack’s hands gain small patches of charcoal-gray short fur and slightly pointed nails, while his human face, blond bangs, glasses and clothes remain unchanged.'},
 {'n':3,'title':'耳与前臂过渡','new':'原有双耳逐渐拉长并改变耳根位置；前臂出现目标色短毛；鼻口仍接近人类。',
  'retain':'黄发和厚刘海仍明显；人类鼻口特征、蓝眼、瘦型、原衣鞋及一副眼镜继续保留。',
  'not_yet':'完整胡狼头、长吻、全身终态、可见尾或明显趾行脚；不额外生成第二对耳。',
  'lora':'ILstyle 1.20/1.20 + Species 0.80/0.80；由阶段文字/草图推进形态，不靠升权重表示百分比。',
  'check':'原人耳连续成为犬耳，不能同时保留完整人耳和头顶兽耳；发色不变成黑长发；眼镜还能辨认。',
  'action':'轻微转头或抬手摸耳；先用侧面/三分之四草图核对耳根。',
  'mask':'耳与前臂分两次修。耳部裁框带头颈与原耳根，蒙版覆盖耳将长到的背景，黄发刘海尽量保留在未重绘区。',
  'glasses':'G0→G1前奏：镜腿可略松动，仍佩戴；不提前掉落。',
  'english':'Jack reaches an early mid-stage canine transformation as his original ears lengthen and his forearms gain short charcoal-gray fur, while his face stays mostly human and his blond bangs, blue eyes, glasses and outfit are retained.'},
 {'n':4,'title':'头部中期与眼镜事件','new':'同一个鼻端、上下颌和颊部协同形成短犬吻；耳形更明确，但仍能读出人类与犬科混合状态。',
  'retain':'成年男性身份、蓝眼、金黄发色及厚刘海的主要轮廓；保持瘦型和原衣鞋；沿用已变化的手臂。',
  'not_yet':'完整终态犬头、极长吻、完全覆盖的躯干体色、可见尾、角或翼；不能像套狗头面具。',
  'lora':'ILstyle 1.20/1.20 + Mid v2 0.80/0.80，主要用于头部裁块；若不合格，改测Species或BYIL，不叠加补救。',
  'check':'鼻、颊、下颌连接自然；还不是完整anthro；黄发和男性身份没有漂移；眼镜事件只发生在这一副眼镜上。',
  'action':'轻扶镜框、略惊讶；头身比例连续，不改变相机或全图站位。',
  'mask':'T03先画混合头轮廓，再T06b重建头颈局部；不要紧贴鼻尖裁框。完成脸后再用小蒙版单独做镜框变化。',
  'glasses':'G1（草案）：镜腿/鼻梁轻微撑开、眼镜下滑，不碎裂；备选G_keep为镜框适配后继续佩戴，两方案不混用。',
  'english':'In a controlled mid-stage transformation, Jack’s nose, cheeks and jaw form a short canine muzzle while human facial traits and blond bangs remain visible, and his single black rectangular frame bends slightly and slips down his nose.'},
 {'n':5,'title':'接近男性犬科终态','new':'犬科头更明确；外露颈、前臂、小腿逐渐统一为暂定短毛材质；仅在尾方案确认且遮挡草图合理后，加入身后可见的短尾轮廓。',
  'retain':'偏长黄发、蓝眼、男性瘦型、约原身高和同一套完整衣鞋；已变化部位保持原配色。',
  'not_yet':'与末格完全相同的所有细节；不出现女王体型、黑长发、首饰或四足姿态；鞋里不强行露出脚趾。',
  'lora':'ILstyle 1.20/1.20 + Species 0.80/0.80；只处理尚未统一的局部，不全图反复重绘。',
  'check':'仍为瘦型成年男性；材质不在短毛/黑皮间随机切换；短裤不撕裂，尾不穿透布面；一副眼镜的位置连续。',
  'action':'恢复站稳、观察自己的手；保持双足站立和穿鞋轮廓。',
  'mask':'分开处理头颈、前臂、小腿。尾出口未确认时不生成可见尾根；不能凭空给短裤开洞。',
  'glasses':'G2（草案）：同一副眼镜已经落在左侧鞋旁；鼻梁上不再有第二副。不要同一格既戴着又掉在地上。',
  'english':'Jack is nearly a male jackal anthro with a clearer canine head and matching short charcoal-gray fur on exposed areas, retaining his blond hair, blue eyes and unchanged clothes, with his glasses now resting beside his left shoe.'},
 {'n':6,'title':'终态草案而非定稿','new':'完整男性犬科/阿努比斯风anthro：暂定细长直立胡狼耳、适度犬吻、炭灰短毛；保留黄发、蓝眼、瘦型和原衣鞋；尾与指趾按最终拍板方案落实。',
  'retain':'同一个男性Jack，约175cm的比较尺度；紫T、卡其短裤、运动鞋原样；若走掉落方案，眼镜保持在同一地面位置。',
  'not_yet':'本格应无未完成的过渡补丁；仍不增加角、翼、巨大肌肉、女王造型、额外人物或首饰。',
  'lora':'ILstyle 1.20/1.20；转化LoRA优先关闭，防止卡在mid状态。终态由明确外型和确认后的终态参考负责。',
  'check':'终态选项未拍板前标为草案；只有一对耳和一套肢体；手指按暂定五指；脚趾在运动鞋内，不作可见趾数/肉垫验收。',
  'action':'平静站立或看向观众；与起点对照同一地面线和画幅。',
  'mask':'通过身份与结构验收后再T13导出；不对满意部分持续全图降噪。',
  'glasses':'G3：沿用G2地面位置；若选择G_keep，4—6格整体改成同一副适配后佩戴的眼镜。',
  'english':'Jack settles into a slender adult male Anubis-inspired jackal anthro with upright ears and a moderate canine muzzle, keeping his shaggy blond hair, thick bangs, blue eyes, original outfit and the established glasses position.'}
]

test_positive='species_transformation, transformation, mid transformation, transfur, furry, '+identity+', a controlled mid-stage human-to-anthro jackal transformation, a short canine muzzle forming while human facial traits remain recognizable, partially lengthened upright ears, charcoal-gray short fur limited to the hands and distal forearms, upper arms and torso retain the human stage, wearing one undamaged pair of black rectangular glasses, one hand raised, balanced standing posture, full body, three-quarter view, simple neutral gray background, soft even lighting, no visible tail yet'
test_negative=common_negative+', complete transformation, fully formed jackal head, completely unchanged human appearance, visible tail, falling glasses, bent glasses, broken glasses'
seed_a=2026110101;seed_b=2026110102
jobs=[]
for number,family,weight in [(1,None,0),(2,'species',.8),(3,'species',1.),(4,'species',1.3),(5,'mid',.8),(6,'byil',.6),(7,'byil',.8),(8,'byil',1.)]:
    jobs.append({'id':f'A{number:02d}','seed':seed_a,'transformation_lora':family,'strength_model':weight,'strength_clip':weight,'batch_size':1,'images':1})
jobs += [
 {'id':'B01','seed':seed_b,'transformation_lora':None,'strength_model':0,'strength_clip':0,'batch_size':1,'images':1},
 {'id':'B02','seed':seed_b,'copy_best_passing_from':['A02','A03','A04'],'skip_if_none_pass':True,'batch_size':1,'images':1},
 {'id':'B03','seed':seed_b,'transformation_lora':'mid','strength_model':.8,'strength_clip':.8,'batch_size':1,'images':1},
 {'id':'B04','seed':seed_b,'copy_best_passing_from':['A06','A07','A08'],'skip_if_none_pass':True,'batch_size':1,'images':1}
]
matrix={
 'kind':'robot_test_matrix_spec_not_comfy_workflow','date':DATE,'status':'not_run','maximum_total_images':12,
 'purpose':'只测一种转化LoRA及其权重，对固定中期目标的影响和第二种子敏感性；不生成完整六格。',
 'checkpoint':'indigoVoidFurryFusedXL_noobaiV35_fp32.safetensors','style':style,'models':models,
 'input_profile':{'reuse_template':'T02_单人动作_角色参考加骨架','execution_mode':'single_output_api_only',
  'pose_input':'OC_advanced/pose_wave.png','controlnet':'noobaiXLControlnet_openposeModel.safetensors',
  'control_strength':.7,'control_start':0.,'control_end':.85,'ip_weight':0.,'lineart_enabled':False,
  'latent':'EmptyLatentImage','width':832,'height':1216,'batch_size':1,'denoise':1.,
  'sampler':'euler_ancestral','scheduler':'normal','steps':22,'cfg':7.,
  'clip_skip':2,'comfy_clip_last_layer':-2},
 'positive_common_to_all_jobs':test_positive,'negative_common_to_all_jobs':test_negative,
 'trigger_rule':'固定的温和触发词合集用于所有行，包括无转化LoRA基线；ILstyle自身已确认触发词也必须所有行相同。此轮不比较触发词写法。',
 'mid_target':'独立诊断中期：短吻正在形成、人脸仍可辨认、耳部分拉长、手/前臂目标色；其余仍人类。眼镜固定正常佩戴，暂停分镜中的掉落事件。',
 'preflight':[
  '先绑定用户确认的ILstyle确切文件及触发词；当前alias未能唯一映射，不能自动猜成BRIL、BlackRat v1或其他文件。',
  '核对三个本机转化LoRA文件与记录的SHA256；若文件不匹配，不冒充已核实版本。',
  '确认T02的固定骨架图存在；没有则准备一个固定姿势输入后再开始，不在12张之外自动追加生成参考图。',
  '替换测试用正负面全文，不在旧女王提示后追加；不要读取旧女王参考作为身份条件，IP权重固定0。',
  'Clip Skip全行统一为2，CLIPSetLastLayer=-2须接到全部文字编码路径；style与转化LoRA仍走原MODEL/CLIP路线。',
  '每行只开ILstyle与当前一种转化LoRA；BRIL及其余LoRA关闭；T11四输出不用于这次计数。',
  '临时API任务可以准备；不覆盖用户已保存的工作流JSON，不运行完整六格。',
  '检查队列空闲后再提交；对未知提交结果先查本次prompt_id，不能盲目重试。'
 ],
 'jobs':jobs,
 'hard_fail':['多角色或男性身份明显改变','瘦型明显变成巨大肌肉体型','黄发/厚刘海/蓝眼/固定眼镜状态明显丢失','服装改变、缺衣、长裤/靴子替代原衣鞋','完全停在人形或直接跳到完整终态','多一对耳、多肢、多指或明显口鼻连接错误'],
 'score_0_to_2_each':['阶段匹配','Jack身份保留','服装与眼镜状态','耳吻手结构','画风与中间调保持'],
 'selection_rule':'无硬失败后，总分优先；同分选较低权重。A组同类全部不通过就跳过该类B复验，不能挑最好看的失败图硬当赢家。',
 'replication_rule':'用Seed B对照B01再看各类赢家；只复验固定中期与seed敏感性，不把两个种子称作统计稳定性保证。Mid本轮只测0.8，不声称已找到其最佳权重。',
 'budget_rule':'最多12个输出图，每任务batch=1，不另加预览采样、重试图、额外seed或组合LoRA；失败提交也须计入已实际生成的图数。',
 'output_record_fields':['job_id','prompt_id','checkpoint_filename','style_filename','lora_filename','lora_sha256','seed','strength_model','strength_clip','positive','negative','pose_input_hash','output_file','hard_fail_reasons','scores','review_notes'],
 'notes':['这组steps/CFG/ControlNet为固定工程比较起点，不是已测试的最佳画质参数。','Species训练元数据写clip_skip=1；本轮为隔离变量统一用2，并非宣称是其最优设置。','不要复制作者默认NEG；实际NEG没有1girl、female、breasts等性别/体型默认词。']
}

lines=['Furry TF 阶段规划表 — Jack 男性犬科／阿努比斯风草案',f'填写日期：{DATE}',
 '角色：Jack；成年男性。此表仅用于本次新分镜，不改旧女王或绿龙的正式设定。',
 '起始形态：约175cm、瘦弱；偏长凌乱黄发和厚刘海；蓝眼、黑框眼镜；紫色短袖T＋卡其短裤＋运动鞋。',
 '目标形态（正式确认，留空）：',
 '暂定终态草案：男性犬科／胡狼阿努比斯风anthro，约原身高与瘦型，适度犬吻；仍保留金黄色头发、蓝眼和原衣鞋。不是旧阿努比斯女王。',
 '固定母参考文件：待指定本次衣装与发型匹配的人类母图；不默认套用旧版长裤／靴子Jack图。',
 '固定服装／背景／镜头／光线：紫T、卡其短裤、运动鞋完整；建议灰底、柔和同向光、同一全身机位，耳尖和鞋底留白。',
 '暂定选项（只用于构思，未拍板）：',
 'E 耳形：细长直立胡狼耳／中长三角犬耳；内耳暂用灰色，不自动继承旧女王金色。',
 'F 毛色和材质：暂用炭灰色短毛；可选全黑短毛、黑褐短毛或无毛黑皮。短毛与黑皮不能在格间随机切换。',
 'T 尾：细短短毛犬尾／中等犬尾／暂不外露，长度和末端毛量待定。尾根出口关系必须先画草图；服装严格不动时优先遮挡，不凭空开洞或让尾穿裤。',
 'D 指趾：手暂五指含拇指；脚趾数留空。运动鞋一直保留，本序列不验收可见脚趾或肉垫；明显趾行／露趾与原鞋冲突时须另定鞋形方案。',
 'H 黄发：本草案默认六格都保留黄发识别线索；晚期是否减少刘海，待决定。',
 'G 眼镜：草案G_drop为第4格轻微变形下滑、第5格已落地、第6格地面原位；备选G_keep为适配后一直佩戴。两案只选一。',
 '方法：R01追踪同一部位跨形态结构；R02每格分别记新增／沿用／尚未出现；R04先定姿势再局部迭代并筛选。',
 '说明：以下六格是分镜规划，不把T11改为六分支。权重为待测起点，不是转化百分比。',
 '每格正向组合：已确认ILstyle触发词＋英文固定身份块＋当前转化LoRA的温和触发词＋本格方向句。Species用species_transformation；Mid用transformation, mid transformation；BYIL用transformation；关闭转化LoRA的起点/终点不额外加这些触发词。',
 '画风固定：ILstyle Model=Clip=1.20；不混BRIL或其他BlackRat。ILstyle确切文件名与其触发词尚待绑定，不能由别名猜选。',
 '转化LoRA一次仅开一种。下列逐格建议是候选，不表示三种已混合验证；正式制作优先沿用矩阵中表现一致的方案。',
 '若BYIL胜出：第2格可从0.60试，第3／4格0.80，第5格1.00；替换原转化LoRA，不与其叠加。终态优先关闭转化LoRA。','',
 '英文固定身份块（每格前置，眼镜与变化状态留给本格句）：',identity,'',
 '全局NEG草案（没有复制作者默认性别／体型NEG，保留厚刘海与黄发）：',common_negative,'']
for f in frames:
    lines += [f"第{f['n']}格：{f['title']}",f"新增特征：{f['new']}",f"沿用特征：{f['retain']}",
              f"尚未出现／本格排除：{f['not_yet']}",f"建议LoRA＋权重：{f['lora']}",f"动作／表情／重心：{f['action']}",
              f"草图与蒙版：{f['mask']}",f"眼镜独立节点：{f['glasses']}",f"验收点：{f['check']}",
              '参考图／seed／实际参数／候选文件：待本格执行时记录。',f"英文方向句：{f['english']}",'']
lines += ['最小测试矩阵：8张主筛＋最多4张复验，合计≤12张。',
 '完整机器清单：Jack_男性犬科TF_最小测试矩阵.json；这是执行规格，不是可直接拖入ComfyUI的workflow JSON。',
 '测试固定：仅一张中期诊断图；T02单输出临时API；V35 fp32；ILstyle 1.2/1.2；832×1216；Euler a / normal；22步；CFG7；denoise1；Clip Skip2；同一骨架OC_advanced/pose_wave.png，强度0.7、截止0.85；IP=0；无Lineart。',
 '所有行共用同一段正负面与触发词合集；只变转化LoRA/权重及预定seed。每任务batch=1，不生成四格T11整套，不测试LoRA叠加。',
 'A种子=2026110101：A01无转化；A02 Species0.8；A03 Species1.0；A04 Species1.3；A05 Mid v2 0.8；A06 BYIL0.6；A07 BYIL0.8；A08 BYIL1.0。',
 'B种子=2026110102：B01无转化；B02 A组最佳合格Species；B03 Mid v2 0.8；B04 A组最佳合格BYIL。某类全失败就跳过该类复验，不硬选赢家。',
 '权重均指Model=Clip=w。Mid本轮只测0.8，预算优先用于各类在第二种子下的复验。',
 '中期目标：人类脸仍可辨认＋短犬吻正在形成＋耳部分拉长＋仅手／前臂局部短毛；不执行眼镜事件，固定正常佩戴；无可见尾。',
 '验收：先剔除男性／单人／衣装／黄发蓝眼／眼镜状态／解剖硬失败，再比较阶段、身份、衣物、结构与画风。既不能全人类不变，也不能跳完整终态。',
 '两种seed是初筛复验，不构成统计稳定性保证。所有数值都是待执行方案，本次未提交出图任务。','',
 '模型核对：Species版本2349624（Illustrious）；本机Mid版本1043354（v2.0 / Illustrious）；BYIL版本1371746（IL - Transformation），已按本机文件完整SHA256匹配Civitai元数据。',
 'Mid与BYIL训练元数据均记clip_skip=2；Species记1。本轮为了固定编码统一2，不把它说成Species最优设置。']

plan=ROOT/'阶段规划表_填写用.txt'
backup=ROOT/'verification/阶段规划表_填写前_20261101.txt';backup.parent.mkdir(exist_ok=True)
if plan.exists() and not backup.exists():shutil.copy2(plan,backup)
plan.write_text('\n'.join(lines)+'\n','utf-8-sig')
(ROOT/'Jack_男性犬科TF_最小测试矩阵.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2),'utf-8')
(ROOT/'Jack_男性犬科TF_六格规划.json').write_text(json.dumps({'date':DATE,'formal_target':None,'frames':frames,'method_sources':['R01','R02','R04'],'status':'draft_pending_character_choices'},ensure_ascii=False,indent=2),'utf-8')
print('Saved original six-panel TXT and machine-readable test specification; no image jobs submitted.')
