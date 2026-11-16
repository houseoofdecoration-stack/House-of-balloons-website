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
OWC=""
OWJ="/* ===== Our Work: purani swipe style \u2013 original 6 photos ke baad \u20b98,000 aur \u20b93,000 package ki photos (theme/colour ke hisaab se arranged) ===== */\n(function(){\nvar box=document.querySelector('.cf.g');if(!box)return;\nvar base=[].slice.call(box.children);\nvar O8=['Cocomelon','Spiderman','Frozen','Butterfly','Safari','Entry Gate'],O3=['Purple','Pink','Blue','Gold','Black','White','Green','Red','Multi'];\nfunction items(p,ord){var out=[];p.B.forEach(function(s,k){if(p.H.indexOf(k)<0)out.push({s:s,t:p.T[k]||[]})});p.EX.forEach(function(s,k){out.push({s:s,t:(p.TX&&p.TX[k])||['Multi']})});\n out.forEach(function(o,i){o.i=i;var r=99;for(var j=0;j<o.t.length;j++){var x=ord.indexOf(o.t[j]);if(x>=0){r=x;break}}o.r=r});\n out.sort(function(a,b){return a.r-b.r||a.i-b.i});return out}\nfunction draw(){var L=[];try{L=items(PKS.p8,O8).concat(items(PKS.p3,O3))}catch(e){}\n [].slice.call(box.querySelectorAll('.gx')).forEach(function(n){n.remove()});\n var f=document.createDocumentFragment();L.forEach(function(o){var d=document.createElement('div');d.className='gx';var i=document.createElement('img');i.loading='lazy';i.alt='';i.src=o.s;d.appendChild(i);f.appendChild(d)});box.appendChild(f)}\nbox.addEventListener('click',function(e){var g=e.target.closest('.gx');if(g&&window.zm){zm.firstChild.src=g.firstChild.src;zm.classList.add('on')}});\n['sv3','svP'].forEach(function(n){var f=window[n];if(typeof f=='function'){window[n]=function(){var r=f.apply(this,arguments);try{draw()}catch(x){}return r}}});\ndraw();\n})();\n"
k=t.rfind('</script></body></html>')
if k>0 and 'id="gw"' not in t:
    t=t[:k]+OWJ+t[k:]
    t=t.replace('</head>','<style>'+OWC+'</style></head>',1)
open('index.html','w',encoding='utf8').write(t)
print(n[0],len(s),len(t))
