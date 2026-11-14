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
open('index.html','w',encoding='utf8').write(t)
print(n[0],len(s),len(t))
