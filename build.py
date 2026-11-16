import re,base64,hashlib,os,glob
src=glob.glob('*index_2_1.html')[0]
s=open(src,encoding='utf8').read()
os.makedirs('img',exist_ok=True)
rx=re.compile(r'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)')
seen={};n=[0]
def rep(m):
    h=hashlib.md5(m.group(2).encode()).hexdigest()
    if h not in seen:
        n[0]+=1
        ext={'jpeg':'jpg','png':'png','webp':'webp'}[m.group(1)]
        name='img/%02d.%s'%(n[0],ext)
        open(name,'wb').write(base64.b64decode(m.group(2)))
        seen[h]=name
    return seen[h]
t=rx.sub(rep,s)
t=t.replace("location.hostname.includes('houseofballoon')?location.href:'https://claude.ai/artifact/LM8jMBnzMQzMWbStyrZwW1'","location.href.split('#')[0]")
t=t.replace('</head>','<style>@media(min-width:900px){body{max-width:600px;margin:0 auto;box-shadow:0 0 80px #0006}}</style><script src="sync.js"></script></head>',1)
import ast,json
m=re.search(r'R3=(\[[^\]]*\])',t);a=[x for i,x in enumerate(json.loads(m.group(1))) if i not in (3,17)];t=t[:m.start(1)]+json.dumps(a)+t[m.end(1):]
m=re.search(r'T3=(\[\[.*?\]\]);',t,re.S);b=[x for i,x in enumerate(ast.literal_eval(m.group(1))) if i not in (3,17)];t=t[:m.start(1)]+repr(b)+t[m.end(1):]
t=re.sub(r'<div id="ofr".*?</div></div></div>','',t,flags=re.S)
t=t.replace('<a class="pill" href="#" onclick="openOffer();return false">🎁 Offers</a>','')
# --- v2: photos IndexedDB (sync.js) ke liye main script ko deferred start karo ---
anc='<script>const io=new IntersectionObserver('
if t.count(anc)==1:
    t=t.replace(anc,'<script>window.hobStart=function(){if(window.__hs)return;if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",window.hobStart);return}var t=document.getElementById("hobmain");if(!t)return;window.__hs=1;var s=document.createElement("script");s.text=t.text;document.body.appendChild(s)};setTimeout(function(){window.hobStart()},3500);if(window.__idbReady)window.hobStart()</script><script type="text/hobmain" id="hobmain">const io=new IntersectionObserver(')
t=t.replace('800/Math.max(im.width,im.height)','720/Math.max(im.width,im.height)').replace("toDataURL('image/jpeg',.7)","toDataURL('image/jpeg',.65)")
# --- v3: Our Work = dono packages ki photos (8,000 pehle) ---
OWC=".cf.g{display:none!important}\n#gw{padding:0 12px 18px}\n#gw .gt{display:flex;gap:8px;margin:2px 0 12px;overflow-x:auto;scrollbar-width:none}\n#gw .gt button{flex:none;border:1px solid #fff4;background:#ffffff12;color:#fff;border-radius:18px;padding:8px 14px;font-weight:800;font-size:13px;font-family:inherit}\n#gw .gt button.on{background:linear-gradient(135deg,#ffd24d,#ff8a00);color:#1a1200;border-color:transparent}\n#gw .gg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}\n#gw .gi{position:relative;aspect-ratio:3/4;border-radius:12px;overflow:hidden;background:#ffffff10;border:1px solid #fff2}\n#gw .gi img{width:100%;height:100%;object-fit:cover;display:block}\n#gw .gi i{position:absolute;left:4px;bottom:4px;font-weight:800;font-size:10px;line-height:1;font-style:normal;background:#000a;color:#ffd24d;padding:3px 6px;border-radius:8px}\n#gw .gm{display:block;margin:12px auto 0;border:0;border-radius:20px;padding:11px 22px;font-weight:800;font-size:14px;font-family:inherit;color:#1a1200;background:linear-gradient(135deg,#ffd24d,#ff8a00)}\n#gw .gh{margin:0 0 10px;font-size:12px;opacity:.75;text-align:center}\n"
OWJ="/* ===== Our Work: dono packages (8,000 pehle, phir 3,000) ki photos, theme/colour ke hisaab se arranged ===== */\n(function(){\nvar anc=document.querySelector('.cf.g');if(!anc)return;\nvar box=document.getElementById('gw');if(!box){box=document.createElement('div');box.id='gw';anc.parentNode.insertBefore(box,anc)}\nvar TAB='all',MAX=12,SHOW=12;\nvar O8=['Cocomelon','Spiderman','Frozen','Butterfly','Safari','Entry Gate'],O3=['Purple','Pink','Blue','Gold','Black','White','Green','Red','Multi'];\nfunction items(p,ord,lab){var out=[];p.B.forEach(function(s,k){if(p.H.indexOf(k)<0)out.push({s:s,t:p.T[k]||[]})});p.EX.forEach(function(s,k){out.push({s:s,t:(p.TX&&p.TX[k])||['Multi']})});\n out.forEach(function(o,i){o.i=i;o.l=lab;var r=99;for(var j=0;j<o.t.length;j++){var x=ord.indexOf(o.t[j]);if(x>=0){r=x;break}}o.r=r});\n out.sort(function(a,b){return a.r-b.r||a.i-b.i});return out}\nfunction other(){var o=[];try{document.querySelectorAll('.cf.g img').forEach(function(m){o.push({s:m.getAttribute('src'),l:''})})}catch(e){}return o}\nfunction all(){var a=[],b=[],c=[];try{a=items(PKS.p8,O8,'\u20b98,000');b=items(PKS.p3,O3,'\u20b93,000')}catch(e){}c=other();return{a:a,b:b,c:c}}\nfunction draw(){var d=all(),L=TAB=='8'?d.a:TAB=='3'?d.b:TAB=='o'?d.c:d.a.concat(d.b,d.c);\n var tabs=[['all','All ('+(d.a.length+d.b.length+d.c.length)+')'],['8','\u20b98,000 ('+d.a.length+')'],['3','\u20b93,000 ('+d.b.length+')']];if(d.c.length)tabs.push(['o','Events ('+d.c.length+')']);\n var sh=L.slice(0,SHOW);\n box.innerHTML='<div class=\"gt\">'+tabs.map(function(t){return'<button data-t=\"'+t[0]+'\" class=\"'+(TAB==t[0]?'on':'')+'\">'+t[1]+'</button>'}).join('')+'</div><div class=\"gg\">'+sh.map(function(o,i){return'<div class=\"gi\" data-i=\"'+i+'\"><img loading=\"lazy\" alt=\"\" src=\"'+o.s+'\">'+(TAB=='all'&&o.l?'<i>'+o.l+'</i>':'')+'</div>'}).join('')+'</div>'+(L.length>SHOW?'<button class=\"gm\">Aur photos dekho ('+(L.length-SHOW)+')</button>':'');\n box._L=sh}\nbox.addEventListener('click',function(e){var t=e.target.closest('.gt button');if(t){TAB=t.dataset.t;SHOW=MAX;draw();return}\n if(e.target.closest('.gm')){SHOW+=18;draw();return}\n var g=e.target.closest('.gi');if(g){var o=box._L[+g.dataset.i];if(o&&window.zm){zm.firstChild.src=o.s;zm.classList.add('on')}}});\n['sv3','svP'].forEach(function(n){var f=window[n];if(typeof f=='function'){window[n]=function(){var r=f.apply(this,arguments);try{draw()}catch(x){}return r}}});\nwindow.__owDraw=draw;draw();\n})();\n"
k=t.rfind('</script></body></html>')
if k>0 and 'id="gw"' not in t:
    t=t[:k]+OWJ+t[k:]
    t=t.replace('</head>','<style>'+OWC+'</style></head>',1)
open('index.html','w',encoding='utf8').write(t)
print(n[0],len(s),len(t))
