"""Build a portable, self-contained reference reader from curated source records."""
from pathlib import Path
from html import escape as e
import json

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'资料来源.json').read_text('utf-8'))
sources=data['sources']
cards=[]
for s in sources:
    extra=(f'<a href="{e(s["extra_url"])}" target="_blank" rel="noopener noreferrer">{e(s["extra_label"])}</a>' if s.get('extra_url') else '')
    search=e(' '.join(str(v) for v in s.values()))
    cards.append(f'''<article id="{s['id']}" data-category="{e(s['category'])}" data-search="{search}">
<div class="card-meta"><span>{s['id']} · {e(s['category'])}</span><span>{e(s['date'])}</span></div>
<h3>{e(s['title'])}</h3><p class="byline">{e(s['author'])} · {e(s['language'])}</p>
<p class="badge">{e(s['evidence'])}</p>
<p><b>看哪里：</b>{e(s['read'])}</p><p><b>用到Jack：</b>{e(s['practice'])}</p>
<p class="limit"><b>适用范围：</b>{e(s['limit'])}</p>
<div class="source-links"><a href="{e(s['url'])}" target="_blank" rel="noopener noreferrer">打开作者原文</a>{extra}</div></article>''')

html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Furry TF 序列参考资料</title><style>
:root{font-family:"Microsoft YaHei UI","Microsoft YaHei",system-ui,sans-serif;color:#243d43;background:#f6f7f3;font-size:16px;line-height:1.8}*{box-sizing:border-box}body{margin:0}header,main,footer{max-width:1180px;margin:auto;padding:28px 26px}header{padding-top:40px}h1{font-size:34px;line-height:1.4;margin:12px 0 18px}h2{font-size:25px;line-height:1.5;margin:0 0 18px}h3{font-size:20px;line-height:1.5;margin:14px 0 8px}p{margin:12px 0}a{color:#176c64;overflow-wrap:anywhere}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #c79630;outline-offset:3px}.eyebrow,.small,.byline{font-size:13px;color:#607970}.lead{max-width:920px;font-size:18px}.nav,.flow,.source-links,.filterbar{display:flex;gap:10px;flex-wrap:wrap}.nav a,.source-links a,.download{display:inline-block;background:#e7eee7;padding:8px 13px;text-decoration:none;border-radius:5px}.notice{background:#e7eee7;padding:18px 22px;border-left:4px solid #397b67;border-radius:5px}.notice p{margin:6px 0}.start{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.start a{background:white;border:1px solid #d5dfd7;border-radius:8px;padding:18px;text-decoration:none;color:#294a46}.start strong{display:block;font-size:18px;margin-bottom:8px}.start span{display:block;font-size:14px;color:#5d746b}section{margin:0 0 40px;scroll-margin-top:90px}.filterbar{position:sticky;top:0;z-index:5;background:#f6f7f3f5;border-top:1px solid #d5dfd7;border-bottom:1px solid #d5dfd7;padding:14px 0;align-items:center;margin:0 0 20px}input{font:inherit;min-width:220px;flex:1;border:1px solid #b9cbc0;border-radius:5px;padding:9px 12px;background:white}button{font:inherit;cursor:pointer;border:1px solid #b9cbc0;border-radius:5px;background:white;color:#33594c;padding:8px 12px}button.active{background:#245f50;color:white}.count{font-size:13px;color:#607970;min-width:75px}.resources{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}article{background:white;border:1px solid #d5dfd7;border-radius:8px;padding:22px;scroll-margin-top:120px}article:target{outline:3px solid #b68c35;outline-offset:3px}.card-meta{display:flex;gap:12px;justify-content:space-between;font-size:12px;color:#5b7b6e}.badge{font-size:13px;color:#36745e}.limit{background:#f4f5ee;border-radius:5px;padding:10px 13px;font-size:14px}.source-links{margin-top:18px;font-size:14px}.flow span{background:#e7eee7;padding:10px 15px;border-radius:5px}.flow i{font-style:normal;align-self:center;color:#728a7f}.table-wrap{overflow:auto;background:white;border:1px solid #d5dfd7;border-radius:7px}table{border-collapse:collapse;width:100%;min-width:740px;font-size:14px}th,td{text-align:left;vertical-align:top;padding:13px 15px;border-bottom:1px solid #dfe7df}th{background:#e7eee7}td:first-child{min-width:110px;font-weight:bold}tr:last-child td{border-bottom:0}.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}.box{padding:20px 22px;border:1px solid #d5dfd7;border-radius:8px;background:white}.box h3{margin-top:0}ol,ul{padding-left:24px}li{margin:9px 0}.empty{padding:22px;background:#fff3d8;border-radius:6px}.hidden{display:none!important}footer{font-size:13px;color:#607970;border-top:1px solid #d5dfd7;padding-bottom:45px}@media(max-width:780px){header,main,footer{padding-left:17px;padding-right:17px}h1{font-size:28px}.start,.resources,.two{grid-template-columns:1fr}.filterbar{position:static}.card-meta{flex-direction:column;gap:2px}article{padding:19px}}@media print{.nav,.filterbar,.download,.source-links{display:none}.resources,.start,.two{display:block}body{background:white;font-size:10pt}header,main,footer{padding:12px 0}article,.box{break-inside:avoid;margin-bottom:16px}a{color:inherit}section{margin-bottom:24px}table{min-width:0;font-size:9pt}.resources .hidden{display:block!important}#empty{display:none!important}h1{font-size:24pt}h2{font-size:17pt}h3{font-size:13pt}}
</style></head><body><header><div class="eyebrow">Jack 创作资料 · 整理于 2026-11-01 · 12份精选</div><h1>Furry TF 序列参考资料</h1>
<p class="lead">先把人形、中间态和终态的结构画清楚，再让模型生成各格。这里优先收录直接讨论TF设计的作者资料，再补兽人结构、分镜方法和ComfyUI工具。</p>
<div class="notice"><p>这里的furry涵盖兽人和拟兽角色，不表示身体必须长毛。女王的平滑哑光黑皮、绿龙的鳞片与腹甲，仍按你的OC设定区分。</p><p>正文与中文阅读指引可离线阅读；教程配图在原站查看，作者原文链接需要联网。</p></div>
<nav class="nav" aria-label="内容导航"><a href="#first">先看这三份</a><a href="#library">全部资料</a><a href="#routes">先选变化路线</a><a href="#parts">按部位查</a><a href="#plan">阶段规划</a><a href="#workflows">现有模板对应</a></nav></header><main>
<section id="first"><h2>先看这三份</h2><div class="start"><a href="#R01"><strong>① 中间态怎么设计</strong><span>MsRedNebula：在人与狼的结构之间构思可信的混合形态。</span></a><a href="#R02"><strong>② 一组TF怎样分阶段</strong><span>Dawn：观察头、手与整体轮廓如何形成可读差别。</span></a><a href="#R04"><strong>③ AI作者怎么迭代</strong><span>FaceDeer：先确定姿势，再图生图添加特征、筛选候选。</span></a></div></section>
<section id="library"><h2>资料清单</h2><p>“TF设计”最接近转化本身；“结构参考”帮助判断画面是否成立；“分镜”帮助组织阅读；“ComfyUI工具”只说明控制方法，不代表模型已通过你的OC转化测试。</p>
<div class="filterbar"><input id="search" type="search" aria-label="搜索资料" placeholder="搜索：耳、吻、手、脚、尾、翼、蒙版……"><button class="active" data-filter="全部">全部</button><button data-filter="TF设计">TF设计</button><button data-filter="结构参考">结构参考</button><button data-filter="分镜">分镜</button><button data-filter="ComfyUI工具">ComfyUI工具</button><span class="count" id="count" role="status">12 / 12 份</span></div><div class="resources">CARDS</div><p id="empty" class="empty hidden">没有匹配的资料。清空搜索或选择“全部”。</p></section>
<section id="routes"><h2>先选变化路线，再决定参考结构</h2><div class="table-wrap"><table><thead><tr><th>路线</th><th>终点特征</th><th>制作时重点保留什么</th></tr></thead><tbody>
<tr><td>人类 → 兽人</td><td>仍以双足站立、能使用双手；头、足、皮肤或尾部拟兽化。</td><td>保持角色身份与双足重心。Jack女王和你的站立绿龙都应先按各自母图规划。</td></tr>
<tr><td>人类／兽人 → 四足兽</td><td>肩胛、胸廓、脊柱、骨盆与四肢分工一起变化。</td><td>另排四足结构草图；不能仅把双足兽人的手放到地上，就视为完成。</td></tr>
<tr><td>兽人 → 另一拟兽形态</td><td>保持部分身份线索，同时改变物种、材质或附肢。</td><td>先列两形态共有的特征，再规划差异。参考图只帮助影响外观，阶段仍需人工定义。</td></tr></tbody></table></div><p class="small">以上是制作路线的归纳；物种结构可查R05—R07，跨形态部位对应可查R01、R03。不是要求所有TF都遵循同一变化顺序。</p></section>
<section id="parts"><h2>按当前部位查参考</h2><div class="table-wrap"><table><thead><tr><th>部位</th><th>先看</th><th>你要先决定的事</th><th>用于生成前的检查</th></tr></thead><tbody>
<tr><td>耳朵</td><td><a href="#R01">R01</a>、<a href="#R05">R05</a></td><td>耳根位置、长度与内外配色；原人耳何时淡出。</td><td>不要中途多出一对耳。女王金色只在内耳，按你的设定保留。</td></tr>
<tr><td>脸与吻部</td><td><a href="#R01">R01</a>、<a href="#R03">R03</a></td><td>鼻、上颌、下颌与颊部如何对应；每格的突出程度。</td><td>先用侧面或三分之四草图看体块连接，再细化眼神和表情。</td></tr>
<tr><td>手与爪</td><td><a href="#R01">R01</a>、<a href="#R05">R05</a></td><td>固定指头数量；指节、爪尖、掌垫各在哪一格改变。</td><td>先确认结构与抓握，再处理材质。不要将指爪长度变化与多长手指混在一起。</td></tr>
<tr><td>趾行脚</td><td><a href="#R07">R07</a>、<a href="#R01">R01</a></td><td>髋、膝、踝、趾的对应，以及足跟离地后的重心。</td><td>后突的踝部不是额外反向膝；真实犬的指趾数量不直接决定OC设计。</td></tr>
<tr><td>尾巴</td><td><a href="#R01">R01</a>、<a href="#R03">R03</a></td><td>尾根连接、朝向与长度；女王细短尾和绿龙长尾分开规划。</td><td>蒙版同时覆盖连接根部与将要出现的尾部空间。</td></tr>
<tr><td>龙翼</td><td><a href="#R06">R06</a></td><td>双手保留还是变翼；翼根、关节、长指和翼膜的连续关系。</td><td>提前留出画幅。构图中的翼要与肩背相连，数量及根部位置跨格一致。</td></tr>
<tr><td>黑皮／鳞片／腹甲</td><td><a href="#R05">R05</a>、<a href="#R06">R06</a>；以母图为准</td><td>材质边界、基础色和阴影范围；哪些是设定，哪些只是光照。</td><td>女王不照搬狼人长毛；仅偏亮优先用T12调色，结构错误才重建。</td></tr></tbody></table></div><p class="small">此表是针对Jack的制作建议。原教程中的物种、毛发、肢体数量与服装不自动成为你的角色设定。</p></section>
<section id="plan"><h2>先做关键状态，再补过渡格</h2><p class="notice">六格规划表保留为历史草案。正式终点方向现为Jack TGTF→成年女性阿努比斯，细节未定，不继承旧女王设计；当前只迁移男性Jack的准确初期结构。请使用<a href="本机方法迁移_V3/A_机器人规格_初期结构准确.json">A机器人规格</a>和<a href="本机方法迁移_V3/B_ComfyUI手操卡_初期结构准确.txt">B手操卡</a>，或同内容的<a href="Jack_男性犬科TF_最小测试矩阵.json" download>当前执行规格</a>。每次显式选一条路线，最多2张。旧input_V3的整黑尖爪/较长尖耳仅供布局参考，尚未通过最新初期验收；先修母图再T03重绘。已有本地Klein与T03的EARLY界面模板。当前没有新采样，也未声称语义稳定性已通过。</p><div class="flow" aria-label="制作流程"><span>确认首尾母图</span><i>→</i><span>画关键轮廓</span><i>→</i><span>逐格落实变化</span><i>→</i><span>局部验收修正</span><i>→</i><span>高清与拼页</span></div>
<div class="two" style="margin-top:20px"><div class="box"><h3>每格填写五项</h3><ol><li>这还是同一个角色的哪些特征？</li><li>本格已经变化的部位是什么？</li><li>哪些部位暂时维持上一状态？</li><li>动作、表情与重心是否读得清楚？</li><li>新轮廓需要多大的蒙版和周边空间？</li></ol><a class="download" download href="阶段规划表_填写用.txt">查看Jack已填写的六格规划表</a></div><div class="box"><h3>阿努比斯女王与绿龙分开记</h3><p>女王：耳内金色、黑皮与头发分开、细短尾、黑色爪与肉垫。不要将狼人教程里的鬃毛或蓬松尾当作默认。</p><p>绿龙：绿色体表、浅色腹甲与翼膜分区；角、背棘、翼与长尾各自追踪。手和脚的数量沿用最终确认图。</p><p>服装、背景、镜头和光线也应记录。需要变化时，在分镜表里明确说明。</p></div></div>
<p>固定机位的小幅变化可从验收通过的上一格局部编辑；大幅换角度或换动作，则按首尾母图分别制作各格。始终保留固定参考，发现错误先修这一格，再继续。LoRA强度、IP权重和降噪都不是转化百分比。</p>
<p class="small">这套练习安排综合了R01、R03、R08的结构与关键姿势思路，并结合现有模板作出；不是任何作者承诺的自动TF算法。</p></section>
<section id="workflows"><h2>与你现有模板的对应</h2><div class="table-wrap"><table><thead><tr><th>模板</th><th>适合做什么</th><th>要记住的边界</th></tr></thead><tbody>
<tr><td>T11</td><td>四个主要形态的候选和阶段文字。</td><td>目前是四格独立生成、首尾双参考，不是自动连续转化；没有现成的每格姿势／线稿分支。</td></tr>
<tr><td>T02／T03</td><td>单格身体动作，以及耳、吻、尾、翼的轮廓草图。</td><td>骨架主要说明姿态；新附肢轮廓须在草图里画清楚。控制模型要与SDXL匹配。</td></tr>
<tr><td>T06c → T06／T06b</td><td>检查裁框与蒙版，再微调或重建变化部位。</td><td>增加新轮廓时，蒙版留出空白空间并保留连接处上下文；小裁块只写相关局部。</td></tr>
<tr><td>T12／T13</td><td>仅亮度偏差时调暗；通过结构验收后再导出高清。</td><td>纯放大不能纠正手脚结构，调暗也不能恢复已经丢失的线条。</td></tr>
<tr><td>T14B</td><td>四张已经确认的成图拼成2×2。</td><td>只拼四张。六格规划可分两页或另行排版，不会因文字写六格就自动扩展T11／T14B。</td></tr>
<tr><td>Klein文字改图</td><td>试做某一格的语义修改。</td><td>先检查画风与身份保持，满意局部再回贴；不与SDXL LoRA直接混接。</td></tr></tbody></table></div>
<div class="notice"><p>本机核对：现有T11文件仍写着Indigo V33；你当前checkpoint目录中已有V35 fp32。使用前先核对底模下拉框。本次整理的是资料，没有修改任何工作流JSON，也没有新增模型或提交生成。</p><p>配套模板在教学总手册的“场景实操模板”文件夹；从“开始选模板.html”取用对应JSON。单独移动本资料文件夹也可阅读正文和访问作者链接。</p></div></section>
<section><h2>怎样挑新的参考资料</h2><p>优先选择展示中间草图、完整参数或失败修正的作者原文。只展示终态、只有一条成品提示词、只写“支持TF”的模型介绍，不能说明怎样控制多格过程。这里的绘画资料用于设计结构，工具资料用于落实控制，效果仍要用你的母图逐格验收。</p></section>
</main><footer><p>资料整理日期：2026-11-01。12条主资料均附作者原文链接；教程配图仍在原站，未复制进本包。Dawn教程的直连可能受限；其余条目以本轮作者正文或节点文档为核对依据。</p><p>离线移动时保留本资料文件夹；与工作流一起移动时，复制整个“教学总手册”。</p></footer>
<script>
const input=document.getElementById('search');const cards=[...document.querySelectorAll('article[data-category]')];const buttons=[...document.querySelectorAll('[data-filter]')];let category='全部';function apply(){const q=input.value.trim().toLowerCase();let visible=0;for(const c of cards){const show=(category==='全部'||c.dataset.category===category)&&(!q||c.dataset.search.toLowerCase().includes(q));c.classList.toggle('hidden',!show);if(show)visible++;}document.getElementById('count').textContent=visible+' / '+cards.length+' 份';document.getElementById('empty').classList.toggle('hidden',visible!==0);}input.addEventListener('input',apply);for(const b of buttons)b.addEventListener('click',()=>{category=b.dataset.filter;for(const x of buttons)x.classList.toggle('active',x===b);apply();});document.querySelectorAll('.start a, #parts a').forEach(a=>a.addEventListener('click',()=>{input.value='';category='全部';for(const b of buttons)b.classList.toggle('active',b.dataset.filter==='全部');apply();}));
</script></body></html>'''
html=html.replace('CARDS','\n'.join(cards))
(ROOT/'Furry_TF序列参考资料.html').write_text(html,'utf-8')
worksheet=['Furry TF 阶段规划表','填写日期：','角色：Jack','起始形态：','目标形态：','固定母参考文件：','固定服装／背景／镜头／光线：','终态指趾数量、尾和翼设置：','说明：以下是六行规划，不是六格工作流。T11目前有四分支；额外格可单独制作。','']
for i,label in enumerate(['起点','变化一','变化二','变化三','接近终态','终态'],1):
    worksheet += [f'第{i}格：{label}','固定身份特征：','已经变化的部位：','仍保留上一状态的部位：','尚不应该出现的终态特征：','动作／表情／重心：','要画的轮廓与连接点：','蒙版范围与上下文：','参考图片／seed／模型／LoRA／IP／降噪：','验收：耳吻手脚数量正确？颜色材质连续？尾翼接根正确？服装背景连续？','候选图文件与备注：','']
if not (ROOT/'阶段规划表_填写用.txt').exists():
    (ROOT/'阶段规划表_填写用.txt').write_text('\n'.join(worksheet),'utf-8-sig')
(ROOT/'开始阅读.txt').write_text('Furry TF 序列参考资料 — 2026-11-01\n\n先读本机方法迁移_V3/开始阅读.txt。A_机器人规格_初期结构准确.json与B_ComfyUI手操卡_初期结构准确.txt是当前并列说明。\n最新版初期：人耳仅刚尖、鼻头仍肤色、无吻突/面骨变化、稀疏短毛、撑衣未破、人甲保留仅甲尖局部变黑。旧input_V3仅作布局参考，尚不合格；每轮只选一条路线最多2张。\n正式终点方向为Jack TGTF到成年女性阿努比斯，细节未定，不继承旧女王。六格规划保留历史，不表示T11已扩为六格。\nFurry_TF序列参考资料.html可离线阅读R01/R02/R04；作者原文需联网。当前另存了EARLY界面模板，没有改原T03/T11或原Klein工作流、没有新采样。\n与工作流一起移动时复制整个教学总手册。\n','utf-8-sig')
print(json.dumps({'sources':len(sources),'page':str(ROOT/'Furry_TF序列参考资料.html')},ensure_ascii=False))
