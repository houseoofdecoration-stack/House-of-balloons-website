/* House of Balloons – live edit sync (owner edits -> Firebase -> everyone sees) */
(function(){
var K='AIzaSyDmHZw0NogvE9CClsbWUngRROFXoVRB_aM',P='house-of-balloon-crm';
var FS='https://firestore.googleapis.com/v1/projects/'+P+'/databases/(default)/documents/hob_site';
var RX=/^hob(CA|[HXT]\d+)$/,CH=600000;
var LS=window.localStorage,gi=LS.getItem.bind(LS),osi0=Storage.prototype.setItem;
function g(k){try{return gi(k)}catch(e){return null}}
function s(k,v){try{osi0.call(LS,k,v)}catch(e){}}
var tok=null,tokExp=0,timers={};
/* ---- push (owner only) ---- */
function authH(){return {'Authorization':'Bearer '+tok,'Content-Type':'application/json'}}
function patch(path,fields,mask){
  var u=FS+'/'+path+(mask?'?'+mask.map(function(m){return 'updateMask.fieldPaths='+encodeURIComponent(m)}).join('&'):'');
  return fetch(u,{method:'PATCH',headers:authH(),body:JSON.stringify({fields:fields})}).then(function(r){if(!r.ok)throw new Error('save '+r.status);return r});
}
function push(key){
  if(!tok)return Promise.resolve();
  var v=g(key)||'',n=Math.max(1,Math.ceil(v.length/CH)),ps=[];
  for(var i=0;i<n;i++)ps.push(patch(key+'_'+i,{d:{stringValue:v.slice(i*CH,(i+1)*CH)}}));
  return Promise.all(ps).then(function(){
    var t=Date.now(),f={},m=[];f[key]={integerValue:String(t)};f[key+'_n']={integerValue:String(n)};m=[key,key+'_n'];
    return patch('_v',f,m).then(function(){s('hobV_'+key,String(t));toast('✅ Save ho gaya – ab sabko dikhegi')});
  }).catch(function(e){toast('⚠ Save nahi hua – internet/login check karo')});
}
function queue(key){clearTimeout(timers[key]);timers[key]=setTimeout(function(){ensureTok().then(function(){push(key)})},700)}
var osi=Storage.prototype.setItem;
Storage.prototype.setItem=function(k,v){
  var r=osi.call(this,k,v);
  if(this===LS&&RX.test(k)){if(tok)queue(k);else{var on=false;try{on=!!OW}catch(e){}if(on)toast('⚠ Login nahi hai – Owner dabake login karo, tab save hoga')}}
  return r;
};
/* ---- auth ---- */
function ensureTok(){
  if(tok&&Date.now()<tokExp-60000)return Promise.resolve();
  var rt=g('hobRT');if(!rt){tok=null;return Promise.reject()}
  return fetch('https://securetoken.googleapis.com/v1/token?key='+K,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'grant_type=refresh_token&refresh_token='+encodeURIComponent(rt)})
   .then(function(r){return r.json()}).then(function(j){if(!j.id_token){LS.removeItem('hobRT');tok=null;throw 0}tok=j.id_token;tokExp=Date.now()+(+j.expires_in||3600)*1000;s('hobRT',j.refresh_token)});
}
function login(email,pw){
  return fetch('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key='+K,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email,password:pw,returnSecureToken:true})})
   .then(function(r){return r.json()}).then(function(j){if(!j.idToken)throw new Error(j.error&&j.error.message||'login');tok=j.idToken;tokExp=Date.now()+(+j.expiresIn||3600)*1000;s('hobRT',j.refreshToken);s('hobEM',email)});
}
function toast(m){var d=document.getElementById('hobToast');if(!d){d=document.createElement('div');d.id='hobToast';d.style.cssText='position:fixed;left:50%;bottom:90px;transform:translateX(-50%);background:#000d;color:#fff;padding:10px 16px;border-radius:20px;font:600 13px Outfit,system-ui;z-index:99999;transition:opacity .3s';(document.body||document.documentElement).appendChild(d)}d.textContent=m;d.style.opacity=1;clearTimeout(d._t);d._t=setTimeout(function(){d.style.opacity=0},4500)}
function modal(cb){
  var o=document.createElement('div');o.style.cssText='position:fixed;inset:0;background:#000b;z-index:99998;display:flex;align-items:center;justify-content:center;padding:20px';
  o.innerHTML='<form style="background:#1a1030;border:1px solid #fff3;border-radius:18px;padding:20px;width:100%;max-width:340px;color:#fff;font:14px Outfit,system-ui"><b style="font-size:17px">👑 Owner login</b><p style="opacity:.7;margin:6px 0 12px;font-size:12px">Sirf owner ke liye</p><input name=e type=email placeholder=Email autocomplete=username style="width:100%;padding:11px;border-radius:10px;border:1px solid #fff3;background:#0006;color:#fff;margin-bottom:8px"><input name=p type=password placeholder="Password / PIN" autocomplete=current-password style="width:100%;padding:11px;border-radius:10px;border:1px solid #fff3;background:#0006;color:#fff"><div class=m style="color:#ff8a80;font-size:12px;min-height:18px;margin:6px 0"></div><div style="display:flex;gap:8px"><button type=submit style="flex:1;padding:11px;border:0;border-radius:10px;background:linear-gradient(90deg,#ff3d9a,#7c4dff);color:#fff;font-weight:700">Login</button><button type=button class=c style="padding:11px 16px;border:1px solid #fff3;border-radius:10px;background:none;color:#fff">Cancel</button></div></form>';
  document.body.appendChild(o);var f=o.firstChild;f.e.value=g('hobEM')||'';(f.e.value?f.p:f.e).focus();
  f.querySelector('.c').onclick=function(){o.remove();cb(false)};
  f.onsubmit=function(ev){ev.preventDefault();var m=f.querySelector('.m');m.textContent='…';login(f.e.value.trim(),f.p.value).then(function(){o.remove();cb(true)}).catch(function(){m.textContent='Email ya password galat hai'})};
}
/* ---- pull (everyone) ---- */
var pulling=false;
function num(f,k){return f&&f[k]&&f[k].integerValue?+f[k].integerValue:0}
function pull(){
  return fetch(FS+'/_v').then(function(r){return r.ok?r.json():null}).then(function(j){
    if(!j||!j.fields)return;var f=j.fields,keys=[];
    Object.keys(f).forEach(function(k){if(RX.test(k)&&num(f,k)!==+(g('hobV_'+k)||0))keys.push(k)});
    if(!keys.length)return;
    pulling=true;
    return Promise.all(keys.map(function(k){
      var n=num(f,k+'_n')||1,ps=[];
      for(var i=0;i<n;i++)ps.push(fetch(FS+'/'+k+'_'+i).then(function(r){return r.json()}).then(function(d){return d.fields.d.stringValue||''}));
      return Promise.all(ps).then(function(a){s(k,a.join(''));s('hobV_'+k,String(num(f,k)))});
    })).then(function(){pulling=false;if(!tok&&!sessionStorage.getItem('hobRL')){try{sessionStorage.setItem('hobRL','1')}catch(e){}location.reload()}});
  }).catch(function(){pulling=false});
}
/* first owner login: publish local edits that remote does not have yet */
function publishLocal(){
  return fetch(FS+'/_v').then(function(r){return r.ok?r.json():{}}).then(function(j){
    var f=(j&&j.fields)||{},ps=[];
    for(var i=0;i<LS.length;i++){var k=LS.key(i);if(RX.test(k)&&!f[k]&&g(k))ps.push(k)}
    return ps.reduce(function(p,k){return p.then(function(){return push(k)})},Promise.resolve());
  });
}
pull();
/* ---- owner button gate ---- */
window.addEventListener('load',function(){
  var o=window.togOW;if(typeof o!=='function')return;
  window.togOW=function(){
    var on=false;try{on=!!OW}catch(e){}
    if(on){return o.apply(this,arguments)}
    var self=this,args=arguments;
    ensureTok().then(function(){o.apply(self,args)},function(){
      modal(function(ok){if(ok){o.apply(self,args);publishLocal()}});
    });
  };
  if(g('hobRT'))ensureTok().then(publishLocal,function(){});
});
})();
