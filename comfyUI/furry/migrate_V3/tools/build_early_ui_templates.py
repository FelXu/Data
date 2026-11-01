"""Write loadable UI copies and matching API templates without executing them."""
from pathlib import Path
import copy
import json
import urllib.request
import uuid

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'本机方法迁移_V3'
SPEC=ROOT/'Jack_男性犬科TF_最小测试矩阵.json'
spec=json.loads(SPEC.read_text('utf-8'))
assert spec['kind']=='robot_early_structure_migration_spec'
if (OUT/'EARLY_T03_初期结构重绘.json').exists() or (OUT/'EARLY_Klein_甲尖单点编辑.json').exists():
    raise SystemExit('UI templates already exist; preserve user edits instead of regenerating them.')
info=json.load(urllib.request.urlopen('http://127.0.0.1:8188/object_info',timeout=20))

def api_to_ui(graph):
    nodes=[];byid={};links=[]
    positions={1:(20,100),990:(20,600),2:(600,100),3:(1200,100),4:(1200,600),
               900:(20,1100),901:(600,1100),902:(1200,1100),
               50:(20,1700),51:(600,1700),52:(1200,1700),53:(1800,850),
               6:(2400,850),7:(3000,850),8:(3500,850)}
    for order,(key,n) in enumerate(graph.items()):
        md=info[n['class_type']];nd={'id':int(key),'type':n['class_type'],
            'pos':list(positions.get(int(key),(0,order*250))),
            'size':[500,420] if n['class_type']=='CLIPTextEncode' else [460,360],
            'flags':{},'order':order,'mode':0,'inputs':[],'outputs':[],
            'properties':{'Node name for S&R':n['class_type']},'widgets_values':[]}
        for section in ['required','optional']:
            for name,desc in md.get('input',{}).get(section,{}).items():
                if name not in n['inputs']:continue
                val=n['inputs'][name];tp=desc[0]
                is_link=isinstance(val,list) and len(val)==2 and str(val[0]) in graph
                inp={'name':name,'type':'COMBO' if isinstance(tp,list) else tp,'link':None}
                if is_link:
                    lid=len(links)+1
                    source=graph[str(val[0])]
                    outtype=info[source['class_type']]['output'][val[1]]
                    links.append([lid,int(val[0]),val[1],int(key),len(nd['inputs']),outtype])
                    inp['link']=lid
                else:
                    inp['widget']={'name':name};nd['widgets_values'].append(val)
                    if n['class_type']=='KSampler' and name=='seed':nd['widgets_values'].append('fixed')
                nd['inputs'].append(inp)
        for idx,tp in enumerate(md.get('output',[])):
            names=md.get('output_name',[])
            nd['outputs'].append({'name':names[idx] if idx<len(names) else tp,'type':tp,'links':[]})
        if n['class_type']=='LoadImage':nd['widgets_values'].append('image')
        nodes.append(nd);byid[nd['id']]=nd
    for lid,src,slot,dst,dslot,tp in links:byid[src]['outputs'][slot]['links'].append(lid)
    return {'id':str(uuid.uuid4()),'revision':0,'last_node_id':max(byid),'last_link_id':len(links),'nodes':nodes,'links':links,'groups':[],'config':{},'extra':{'ds':{'scale':0.24,'offset':[80,500]}},'version':0.4}

def note(ui,nid,title,text,pos,size=(1050,460)):
    ui['nodes'].append({'id':nid,'type':'Note','pos':list(pos),'size':list(size),'flags':{},'order':len(ui['nodes']),'mode':0,'inputs':[],'outputs':[],'properties':{},'widgets_values':[text],'title':title,'color':'#604923','bgcolor':'#806338'})
    ui['last_node_id']=max(ui['last_node_id'],nid)

# T03 uses approved files intentionally not yet present: accidental queuing must not use old full claws.
g=json.loads((ROOT/'_ops_V3/graph_V3_S01_R01_T03.json').read_text('utf-8-sig'))
g['1']['inputs']['ckpt_name']=spec['checkpoint']
g['2']['inputs'].update(strength_model=.8,strength_clip=.8,lora_name=spec['style']['filename'])
g['3']['inputs']['text']=spec['prompts']['positive_full'];g['4']['inputs']['text']=spec['prompts']['negative_full']
g['900']['inputs']['image']='Jack_TF_EARLY/approved_color.png'
g['50']['inputs']['image']='Jack_TF_EARLY/approved_lineart.png'
g['53']['inputs'].update(strength=0.0,start_percent=0.0,end_percent=.75)
g['6']['inputs'].update(seed=2026110101,steps=28,cfg=5.,denoise=.65,sampler_name='euler_ancestral',scheduler='normal')
g['8']['inputs']['filename_prefix']='Jack_Test/REVIEW_20261101_EARLY_T03/output'
api=OUT/'api/EARLY_T03_待绑定母图_API.json';api.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n','utf-8')
ui=api_to_ui(g)
note(ui,10000,'先看这里｜未验母图不得运行',
     '本模板：初期结构正确的母图→V35＋ILstyle新墨线/赛璐璐重绘。\n当前input_V3旧图的整黑尖爪和长尖耳不符合新规则，不能直接叫作初期通过。\n先修成：原人耳仅刚尖、鼻头仍肤色且无吻突、人甲保留仅甲尖小块变黑、衣物撑紧但未破。\n批准后把同源色稿/线稿放input/Jack_TF_EARLY/approved_color.png与approved_lineart.png，或在两个LoadImage重新上传。\n这两个默认文件尚未创建，防止误把旧爪稿直接排队。\n本机语义稳定性尚未验证；本模板不自动运行。', (20,-520),(1100,520))
note(ui,10001,'参数怎么改｜一次只比较一个变量',
     '2 LoRA只开ILstyle，Model/Clip=.80；990为CLIP=-2。\n6 KSampler：28步、CFG5、Euler a/normal、seed固定2026110101。\n当前CN强度0=关闭，denoise=.65。\n两档降噪只改6.denoise=.65/.75，其他都不变，始终读原母图。\nCN对照则两张denoise都.65，只改53.strength=0/.50；start0/end.75。\n禁止denoise≤.50且CN≥.75。\n每轮最多2张，假色/结构提前完成立即停，不自动第三张。', (1800,150),(1050,560))
ui_file=OUT/'EARLY_T03_初期结构重绘.json';ui_file.write_text(json.dumps(ui,ensure_ascii=False,indent=2)+'\n','utf-8')

klein=json.loads(Path(r'E:\CODEX\ComfyUI\_klein_setup_research\Klein4B_文字改图_单图_扁平工作流.json').read_text('utf-8-sig'))
for n in klein['nodes']:
    if n['id']==76:n['widgets_values']=['Jack_TF_V3/mid_color_draft.png','image']
    if n['id']==74:n['widgets_values']=[spec['local_klein_option']['instructions']['nail_tip_only']]
    if n['id']==73:n['widgets_values']=[2026110101,'fixed']
    if n['id']==9:n['widgets_values']=['Jack_Test/REVIEW_20261101_EARLY_KLEIN_NAIL/output']
note(klein,10000,'本地语义编辑｜只验证甲尖这一处',
     '这是Klein4B源图编辑副本，不修改原Jack_FLUX2_Klein4B_文字改图工作流。\n点74的文字只改一处：恢复短人甲，保留自然近端甲片，只有远端一小块变黑；去掉整黑尖爪。\n4步/CFG1/euler，不能套V35的CFG5和ILstyle。\n当前源图只作布局参考；改完后仍逐项检查E1–E7，耳/鼻等不自动视作通过。\n每轮最多2张；不能服从就停，改精确mask/绘制，不无限抽图。', (0,-550),(1100,450))
kfile=OUT/'EARLY_Klein_甲尖单点编辑.json';kfile.write_text(json.dumps(klein,ensure_ascii=False,indent=2)+'\n','utf-8')
kg_path=Path(spec['local_klein_option']['prepared_nail_API']);kg=json.loads(kg_path.read_text('utf-8'))
kg['9']['inputs']['filename_prefix']='Jack_Test/REVIEW_20261101_EARLY_KLEIN_NAIL_'+uuid.uuid4().hex[:8]+'/K01'
kg_path.write_text(json.dumps(kg,ensure_ascii=False,indent=2)+'\n','utf-8')
spec['ui_workflows']={'T03':str(ui_file),'local_Klein_edit':str(kfile)}
spec['t03_template_api']=str(api)
spec['local_klein_option']['prepared_nail_UI']=str(kfile)
TARGET=SPEC;TARGET.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n','utf-8')
(OUT/'A_机器人规格_初期结构准确.json').write_bytes(TARGET.read_bytes())
print(json.dumps({'UI_T03':str(ui_file),'UI_Klein':str(kfile),'requires_source_review':True,'submitted':False},ensure_ascii=False,indent=2))
