/* P1 outage trailer for the Incident Triage Lab.
   render(t) draws the frame for narration time t, so the same scene plays against the audio
   in a browser and steps frame by frame for video (scripts/render_explainer.cjs).
   Beat times below are in authored time: the timeline of the first recorded take. A later take
   carries a warp table in narration.js that maps its word times back to authored time, so
   re-voicing needs no re-timing here. The outage, its clock and its counts are illustrative. */
(function(){
'use strict';
var root=document.querySelector('[data-explainer]'),NARR=window.EXPLAINER_NARRATION;
if(!root||!NARR)return;
var query=new URLSearchParams(location.search),CAPTURE=query.has('capture');
if(CAPTURE)document.body.classList.add('p1-capture');
var W=1920,H=1080,DUR=NARR.duration,TOTAL=DUR+2.6,NS='http://www.w3.org/2000/svg';
var A_DUR=NARR.authored_duration||DUR,A_TOTAL=A_DUR+2.6,WARP=NARR.warp||[];
function authored(t){ // narration time in this take -> time in the authored take
 var n=WARP.length;if(!n)return t;if(t>=WARP[n-1][0])return WARP[n-1][1]+(t-WARP[n-1][0]);
 for(var i=1;i<n;i++)if(t<=WARP[i][0]){var a=WARP[i-1],b=WARP[i];return a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0])}
 return t;
}

/* ---------- helpers ---------- */
function cl(x){return x<0?0:x>1?1:x}
function P(t,a,b){return cl((t-a)/(b-a))}
function lerp(a,b,u){return a+(b-a)*u}
function E(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
function EO(x){return 1-Math.pow(1-x,3)}
function EB(x){if(x<=0)return 0;if(x>=1)return 1;var s=1.7;x-=1;return x*x*((s+1)*x+s)+1}
function vis(t,a,b,c,d){return Math.min(EO(P(t,a,b)),1-E(P(t,c,d)))}
function set(n,attrs){for(var k in attrs)n.setAttribute(k,attrs[k]);return n}
function el(name,parent,attrs){var n=document.createElementNS(NS,name);if(attrs)set(n,attrs);if(parent)parent.appendChild(n);return n}
function op(n,v){v=cl(v);if(v<.004)n.setAttribute('display','none');else{n.removeAttribute('display');n.setAttribute('opacity',v.toFixed(3))}return n}
function T(parent,cls,x,y,str,anchor,size){var n=el('text',parent,{'class':cls,x:x,y:y,'text-anchor':anchor||'start','font-size':size||24});n.textContent=str;return n}
function G(parent){return el('g',parent)}
function tr(x,y,k){return 'translate('+x.toFixed(2)+','+y.toFixed(2)+')'+(k===undefined?'':' scale('+k.toFixed(4)+')')}
function pop(g,x,y,u){g.setAttribute('transform',tr(x,y,lerp(.6,1,EB(u))));op(g,cl(u*4))} // scale in around (x,y)
function popAt(g,cx,cy,u){var k=lerp(.6,1,EB(u));g.setAttribute('transform','translate('+cx+','+cy+') scale('+k.toFixed(4)+') translate('+(-cx)+','+(-cy)+')');op(g,cl(u*4))} // same, for groups drawn in page coordinates
function noise(n){var v=Math.sin(n*12.9898)*43758.5453;return v-Math.floor(v)}
function commas(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
var GREEN='#2cc2a8',RED='#f26b5b',GOLD='#e6ad45',BLUE='#78a8e8',LINE='#33445f',PAPER='#f5f7f9',CARD='#0b1220';

/* ---------- stage ---------- */
var svg=el('svg',root,{'class':'p1-svg',viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'Animation: checkout fails in every region, alerts flood in, a P1 response assigns four roles and works from one incident record, and then the Incident Triage Lab puts five tickets in the learner’s queue. A transcript follows.'});
var defs=el('defs',svg),grad=el('radialGradient',defs,{id:'p1-bg',cx:'28%',cy:'22%',r:'95%'});
el('stop',grad,{offset:0,'stop-color':'#22345a'});el('stop',grad,{offset:1,'stop-color':'#0c1322'});
el('rect',svg,{width:W,height:H,fill:'url(#p1-bg)'});
var kicker=T(svg,'bold track gold',157,84,'IT PROFESSIONAL PRACTICE','start',20),kick2=T(svg,'track muted',560,84,'INCIDENT TRIAGE LAB','start',20),scenario=T(svg,'track dim',1763,84,'ILLUSTRATIVE SCENARIO','end',16);

/* ================= 1 and 2. The outage, then the alert flood ================= */
var FAIL=3.48,Ar=G(svg);
var clock=T(Ar,'display num',157,238,'08:41','start',86);
var status=G(Ar),statusBox=el('rect',status,{x:440,y:182,width:400,height:58,rx:29,'stroke-width':3,fill:CARD}),statusDot=el('circle',status,{cx:474,cy:211,r:9}),statusText=T(status,'bold',496,220,'','start',24);
var REGIONS=['Asia-Pacific','Europe','Americas'],regions=REGIONS.map(function(name,i){var g=G(Ar),x=1763-(3-i)*214+14;
 el('rect',g,{'class':'f-card s-line',x:x,y:186,width:200,height:50,rx:25,'stroke-width':2});g._dot=el('circle',g,{cx:x+26,cy:211,r:8});T(g,'semi',x+44,219,name,'start',22);return g});
var stamp=G(Ar);el('rect',stamp,{'class':'f-card s-red',x:-250,y:-44,width:500,height:88,rx:12,'stroke-width':5});T(stamp,'display red',0,15,'MAJOR INCIDENT · P1','middle',42);
// architecture: nodes, edges and the requests that flow through them
var NODES={customers:[272,540,'Customers'],cdn:[600,540,'Web front end','CDN'],gateway:[900,540,'API gateway'],payments:[1230,390,'Payments'],inventory:[1230,540,'Inventory'],orders:[1230,690,'Orders'],provider:[1600,390,'Payment provider',null,270],database:[1600,620,'Database','clustered']};
function half(k){return (NODES[k][4]||230)/2}
var EDGES=[['customers','cdn'],['cdn','gateway'],['gateway','payments'],['gateway','inventory'],['gateway','orders'],['payments','provider'],['inventory','database'],['orders','database']];
var edgeG=G(Ar),edges=EDGES.map(function(e){var a=NODES[e[0]],b=NODES[e[1]];return el('line',edgeG,{'class':'s-line round',x1:a[0]+half(e[0]),y1:a[1],x2:b[0]-half(e[1]),y2:b[1],'stroke-width':4})});
var ROUTES=[['customers','cdn','gateway','payments','provider'],['customers','cdn','gateway','inventory','database'],['customers','cdn','gateway','orders','database']].map(function(r){
 var pts=r.map(function(k){return [NODES[k][0],NODES[k][1]]}),len=[0];for(var i=1;i<pts.length;i++)len.push(len[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));return {pts:pts,len:len,total:len[len.length-1]}});
function along(route,d){for(var i=1;i<route.pts.length;i++)if(d<=route.len[i]){var u=(d-route.len[i-1])/(route.len[i]-route.len[i-1]);return [lerp(route.pts[i-1][0],route.pts[i][0],u),lerp(route.pts[i-1][1],route.pts[i][1],u)]}return route.pts[route.pts.length-1]}
var dotG=G(Ar),dots=[];for(var di=0;di<21;di++)dots.push(el('circle',dotG,{r:7}));
var nodeG=G(Ar),nodes={};Object.keys(NODES).forEach(function(k){var n=NODES[k],g=G(nodeG),h=n[3]?96:84,w=half(k);
 g._box=el('rect',g,{x:n[0]-w,y:n[1]-h/2,width:w*2,height:h,rx:14,'stroke-width':3,fill:CARD,stroke:LINE});if(k==='provider')g._box.setAttribute('stroke-dasharray','9 7');
 T(g,'semi',n[0],n[1]+(n[3]?-2:9),n[2],'middle',26);if(n[3])T(g,'muted',n[0],n[1]+28,n[3],'middle',20);
 g._badge=G(g);el('circle',g._badge,{r:19,fill:k==='payments'?RED:GOLD});T(g._badge,'bold ink',0,9,'!','middle',26);g._x=n[0]+w-14;g._y=n[1]-h/2+4;nodes[k]=g});
var burst=el('circle',Ar,{'class':'f-none s-red',cx:NODES.payments[0]-115,cy:NODES.payments[1],'stroke-width':4});
var toast=G(Ar);el('rect',toast,{'class':'f-card s-red',x:-190,y:-36,width:380,height:72,rx:12,'stroke-width':3});T(toast,'bold red',-164,9,'✕','start',26);T(toast,'semi',-128,8,'Payment service unavailable','start',21);
// teams, each around the slice it can see
var TEAMS=[['Network team',GOLD,470,476,560,128,750,446,16.79],['Application team',BLUE,1096,326,268,428,1230,296,17.83],['Database team',GREEN,1468,548,264,146,1600,728,15.99]];
var teams=TEAMS.map(function(d){var g=G(Ar);g._box=el('rect',g,{x:d[2],y:d[3],width:d[4],height:d[5],rx:20,fill:'none',stroke:d[1],'stroke-width':3,'stroke-dasharray':'10 9'});
 g._chip=G(g);var w=d[0].length*14.2+44;el('rect',g._chip,{x:-w/2,y:-25,width:w,height:50,rx:25,fill:CARD,stroke:d[1],'stroke-width':3});T(g._chip,'bold',0,8,d[0],'middle',23).setAttribute('fill',d[1]);
 g._q=T(g,'display',d[6]+w/2+16,d[7]+14,'?','start',44);g._q.setAttribute('fill',d[1]);g._d=d;return g});
// bottom band, first the business view
var biz=G(Ar);T(biz,'bold track muted',157,852,'ORDERS COMPLETED','start',18);var orders=T(biz,'display num',153,940,'','start',88),ordersNote=T(biz,'semi red',157,984,'none since 08:42','start',24);
T(biz,'bold track muted',620,852,'ORDERS PER MINUTE','start',18);var bars=[];for(var bi=0;bi<28;bi++)bars.push(el('rect',biz,{x:620+bi*19,width:14,rx:3}));
el('line',biz,{'class':'s-line',x1:620,y1:970,x2:1152,y2:970,'stroke-width':2});
var PRESS=[['Store managers: card payments are failing',11.24],['Customers: is checkout down?',11.9],['Executive: when will it be back?',12.5]];
var press=PRESS.map(function(d,i){var g=G(Ar);el('rect',g,{'class':'f-card s-line',x:0,y:-27,width:533,height:54,rx:27,'stroke-width':2});T(g,'semi',26,8,d[0],'start',22);g._t=d[1];g._y=870+i*62;return g});
// then the monitoring view
var alerts=G(Ar);T(alerts,'bold track muted',157,852,'ALERTS FIRING','start',18);var alertNum=T(alerts,'display num red',153,940,'0','start',88);
var FEED=['payments · errors','gateway · timeouts','CDN · error pages','orders · queue growing','database · connections','provider · no response'];
var feed=FEED.map(function(s,i){var g=G(alerts),x=430+(i%2)*400,y=884+Math.floor(i/2)*46;el('circle',g,{cx:x,cy:y-8,r:7,fill:i===0||i===5?RED:GOLD});T(g,'semi',x+20,y,s,'start',24);return g});
var slice=G(Ar);T(slice,'display',1230,900,'Each team sees only','start',36);T(slice,'display',1230,948,'its own slice.','start',36);
var ASK=[['Who decides?',26.31],['Who tells customers?',27.19],['Who tests the fix?',27.79],['Who writes it down?',28.23]];
var asks=ASK.map(function(d,i){var g=G(Ar);el('rect',g,{'class':'f-card s-gold',x:-190,y:-42,width:380,height:84,rx:14,'stroke-width':3});T(g,'display',0,12,d[0],'middle',31);g._t=d[1];g._x=157+190+i*408;return g});
function drawOutage(t){
 var a=Math.min(EO(P(t,.2,.8)),1-E(P(t,29.3,29.9)));op(Ar,a);if(a<=0)return;
 clock.textContent=t<1?'08:41':t<11.7?'08:42':t<24.3?'08:43':'08:44';
 var tick=Math.max(Math.sin(Math.PI*P(t,1,1.5)),Math.sin(Math.PI*P(t,11.7,12.2)),Math.sin(Math.PI*P(t,24.3,24.8)));clock.setAttribute('font-size',(86+10*tick).toFixed(1));
 var failed=t>=FAIL,col=failed?RED:GREEN;set(statusBox,{stroke:col});statusDot.setAttribute('fill',col);statusText.textContent=failed?'CHECKOUT · FAILING':'CHECKOUT · HEALTHY';statusText.setAttribute('fill',col);
 var sp=failed?Math.sin(Math.PI*P(t,FAIL,FAIL+.5)):0;status.setAttribute('transform','translate(640,211) scale('+(1+.08*sp).toFixed(3)+') translate(-640,-211)');
 regions.forEach(function(g,i){g._dot.setAttribute('fill',t>=4.28+i*.12?RED:GREEN);op(g,1-E(P(t,22.6,23.2)))});
 var st=EB(P(t,24.07,24.6));stamp.setAttribute('transform','translate(1500,212) rotate(-4) scale('+lerp(1.6,1,st).toFixed(3)+')');op(stamp,P(t,24.07,24.25));
 // requests
 dots.forEach(function(c,i){var r=ROUTES[i%3],d=(t*430+i*(r.total/7)+(i%3)*90)%r.total,p=along(r,d),blocked=failed&&i%3===0&&d>r.len[3]-118;
  set(c,{cx:p[0].toFixed(1),cy:p[1].toFixed(1),fill:failed&&i%3===0&&d>r.len[2]?RED:PAPER});op(c,blocked?0:failed?(i%3===0?.95:.4):.9)});
 var bp=(t*1.9)%1;set(burst,{r:lerp(8,34,EO(bp))});op(burst,failed?(1-bp)*.9:0);
 edges[5].setAttribute('class',failed?'s-red round':'s-line round');edges[5].setAttribute('stroke-dasharray',failed?'6 10':'none');
 Object.keys(nodes).forEach(function(k,i){var g=nodes[k],u=k==='payments'?P(t,FAIL,FAIL+.3):P(t,13.5+i*.2,13.8+i*.2);
  g._box.setAttribute('stroke',k==='payments'&&failed?RED:LINE);if(k==='customers')u=0;pop(g._badge,g._x,g._y,u)});
 pop(toast,347,650,P(t,5.96,6.4));if(t>13)op(toast,1-P(t,13,13.4));
 teams.forEach(function(g){var d=g._d,u=E(P(t,d[8],d[8]+.6));g._box.setAttribute('stroke-opacity',u.toFixed(3));op(g._box,u);pop(g._chip,d[6],d[7],P(t,d[8],d[8]+.4));
  op(g._q,EO(P(t,20.63,21.1))*(1-P(t,25,25.4)));op(g,1)});
 // bottom band
 op(biz,1-E(P(t,13,13.5)));var n=1204+Math.floor(2.6*Math.min(t,FAIL));orders.textContent=commas(n);orders.setAttribute('class',t>=9.29?'display num red':'display num');op(ordersNote,EO(P(t,9.29,9.7)));
 var step=Math.floor(t/.3);bars.forEach(function(b,k){var s=(step-(27-k))*.3,h=s<FAIL?46+38*noise(step-(27-k)):4;set(b,{y:970-h,height:h,fill:s<FAIL?PAPER:RED,opacity:s<FAIL?.75:1})});
 press.forEach(function(g){pop(g,1230,g._y,P(t,g._t,g._t+.4));if(t>13)op(g,1-P(t,13,13.4))});
 op(alerts,Math.min(EO(P(t,13.4,13.9)),1-E(P(t,25,25.5))));alertNum.textContent=String(Math.round(41*E(P(t,13.5,16.2))+Math.max(0,t-16.2)*.9));
 feed.forEach(function(g,i){op(g,EO(P(t,13.7+i*.25,14+i*.25)))});
 op(slice,vis(t,20.63,21.2,25,25.5));
 asks.forEach(function(g){pop(g,g._x,922,P(t,g._t,g._t+.4))});
}

/* ================= 3. The response: cadence, roles, one record ================= */
var Rs=G(svg),rsHead=T(Rs,'display',157,226,'P1 response cadence','start',56),rsClock=T(Rs,'display num',1763,226,'08:44','end',56);
var STEPS=[['Declare',34.91],['Assign',38.1],['Set cadence',43.72],['Restore',45.6],['Hand off',49.29]];
var track=el('line',Rs,{'class':'s-line round',x1:157,y1:320,y2:320,'stroke-width':4});
var pre=G(Rs);T(pre,'bold track muted',157,560,'CADENCE','start',18);el('line',pre,{'class':'s-line round',x1:157,y1:620,x2:1763,y2:620,'stroke-width':4});
var ticks=[0,1,2,3,4,5,6,7].map(function(i){var g=G(pre),x=190+i*216;el('line',g,{'class':'s-green round',x1:x,y1:596,x2:x,y2:644,'stroke-width':7});T(g,'muted',x,684,i?'update':'declare','middle',21);g._t=31.62+i*.36;return g});
var beat=el('circle',pre,{'class':'f-gold',cy:620,r:11});
var diag=G(pre);T(diag,'bold track muted',157,790,'DIAGNOSIS','start',18);el('line',diag,{'class':'s-line round',x1:157,y1:850,x2:1763,y2:850,'stroke-width':4,'stroke-dasharray':'4 14'});
var guess=G(diag);el('circle',guess,{r:32,fill:CARD,stroke:GOLD,'stroke-width':4,'stroke-dasharray':'7 7'});T(guess,'display gold',0,14,'?','middle',40);T(diag,'muted',157,914,'root cause: not known yet','start',23);
var declared=G(Rs);el('rect',declared,{'class':'f-card s-red',x:-380,y:-78,width:760,height:156,rx:20,'stroke-width':4});T(declared,'display',-336,26,'P1 declared','start',76);T(declared,'display num red',336,26,'08:44','end',76);
var steps=STEPS.map(function(d,i){var g=G(Rs),x=157+i*326;g._box=el('rect',g,{x:x,y:280,width:300,height:80,rx:40,'stroke-width':3});g._text=T(g,'display',x+150,331,d[0],'middle',30);g._t=d[1];return g});
var cadNote=T(Rs,'semi muted',157,414,'A cadence before a perfect diagnosis','start',30);
var rec=G(Rs);el('rect',rec,{'class':'f-card s-line',x:157,y:440,width:760,height:530,rx:16,'stroke-width':3});
T(rec,'bold track muted',189,486,'INCIDENT RECORD','start',18);T(rec,'semi',189,530,'Checkout unavailable, all regions','start',30);
el('rect',rec,{'class':'f-red',x:815,y:466,width:74,height:42,rx:8});T(rec,'bold ink',852,496,'P1','middle',25);el('line',rec,{'class':'s-line',x1:189,y1:556,x2:885,y2:556,'stroke-width':2});
var LINES=[['08:44',[['P1 declared.',36.6],[' One record opened.',36.9]]],['08:45',[['Commander',39.98],[' · Communications',41.02],[' · Resolver',41.98],[' · Scribe',42.59]]],['08:46',[['Next update due 09:00',44.31]]],
 ['08:58',[['Safest recovery path tested',46.37]]],['09:07',[['Service verified: purchases completing',48.4]]],['09:10',[['Every open action has an owner',50.3]]]];
var lines=LINES.map(function(d,i){var y=604+i*62,time=T(rec,'num muted',189,y,d[0],'start',23),text=el('text',rec,{x:292,y:y,'font-size':i===1?22.5:25,'class':'semi'});
 var parts=d[1].map(function(p){var s=el('tspan',text);s.textContent=p[0];s._t=p[1];return s});return {time:time,parts:parts,t0:d[1][0][1],clock:d[0]}});
var ROLES=[['Commander','sets priorities',GOLD,39.98],['Communications','publishes updates',BLUE,41.02],['Resolver','tests recovery',GREEN,41.98],['Scribe','logs decisions',PAPER,42.59]];
var roles=ROLES.map(function(d,i){var g=G(Rs);g._box=el('rect',g,{x:-92,y:-100,width:184,height:200,rx:16,fill:CARD,stroke:LINE,'stroke-width':3});el('circle',g,{cx:0,cy:-44,r:30,fill:d[2]});
 el('path',g,{d:'M-40,26 a40,34 0 0 1 80,0',fill:d[2],transform:'translate(0,-6) scale(.78)'});T(g,'bold',0,52,d[0],'middle',19.5);T(g,'muted',0,80,d[1],'middle',18);
 g._ring=el('rect',g,{x:-92,y:-100,width:184,height:200,rx:16,fill:'none',stroke:d[2],'stroke-width':4});g._x=960+92+i*206;g._t=d[3];return g});
var upd=G(Rs);el('rect',upd,{'class':'f-card s-line',x:960,y:690,width:386,height:280,rx:16,'stroke-width':3});T(upd,'bold track muted',992,736,'NEXT UPDATE','start',18);
el('circle',upd,{'class':'f-none s-line',cx:1068,cy:852,r:70,'stroke-width':14});var ring=el('circle',upd,{'class':'f-none s-green',cx:1068,cy:852,r:70,'stroke-width':14,'stroke-linecap':'round',transform:'rotate(-90 1068 852)',pathLength:1});
var hand=el('line',upd,{'class':'s-paper round',x1:1068,y1:852,x2:1068,y2:806,'stroke-width':5});el('circle',upd,{'class':'f-paper',cx:1068,cy:852,r:7});
T(upd,'display num',1162,846,'09:00','start',54);T(upd,'muted',1164,884,'agreed and kept','start',20);
var svc=G(Rs);el('rect',svc,{'class':'f-card s-line',x:1378,y:690,width:385,height:280,rx:16,'stroke-width':3});T(svc,'bold track muted',1410,736,'CHECKOUT','start',18);var svcState=T(svc,'display',1410,790,'','start',36);
el('line',svc,{'class':'s-line round',x1:1440,y1:868,x2:1700,y2:868,'stroke-width':4});var svcNodes=[1440,1570,1700].map(function(x){return el('circle',svc,{cx:x,cy:868,r:17,fill:CARD,'stroke-width':4})});
var svcDots=[0,1,2,3].map(function(){return el('circle',svc,{cy:868,r:6,fill:GREEN})}),svcNote=T(svc,'semi green',1410,938,'orders completing again','start',22);
function drawResponse(t){
 var a=Math.min(EO(P(t,29.7,30.3)),1-E(P(t,51.35,51.95)));op(Rs,a);if(a<=0)return;
 var now='08:44';lines.forEach(function(l){if(t>=l.t0)now=l.clock});rsClock.textContent=now;
 var grow=E(P(t,30.3,31.6));track.setAttribute('x2',lerp(157,1763,grow));
 op(pre,vis(t,31.4,31.9,34.45,34.9));ticks.forEach(function(g){op(g,EO(P(t,g._t,g._t+.25)))});
 set(beat,{cx:Math.min(1763,190+Math.max(0,t-31.62)/.36*216).toFixed(1)});op(diag,EO(P(t,33.06,33.6)));guess.setAttribute('transform',tr(960+430*Math.sin(t*1.7)+90*Math.sin(t*4.3),850));
 pop(declared,960,690,P(t,34.91,35.4));if(t>36.3)op(declared,1-P(t,36.3,36.6));
 steps.forEach(function(g,i){var on=P(t,g._t,g._t+.35),next=i<4?STEPS[i+1][1]:1e9,done=t>=next;op(g,EO(P(t,30.4+i*.2,30.9+i*.2)));
  set(g._box,{fill:on>0?(done?'#12343a':'#17494a'):CARD,stroke:on>0?GREEN:LINE});g._text.setAttribute('class',on>0?'display':'display dim');
  var s=1+.07*Math.sin(Math.PI*on),cx=157+i*326+150;g.setAttribute('transform','translate('+cx+',320) scale('+s.toFixed(3)+') translate('+(-cx)+',-320)')});
 op(cadNote,vis(t,31.62,32.2,34.5,34.9));
 popAt(rec,537,705,P(t,36.45,36.95));
 lines.forEach(function(l){op(l.time,EO(P(t,l.t0,l.t0+.3)));l.parts.forEach(function(s){s.setAttribute('fill-opacity',EO(P(t,s._t,s._t+.3)).toFixed(3))})});
 roles.forEach(function(g){var u=P(t,g._t,g._t+.45);pop(g,g._x,560,u);var r=P(t,g._t+.1,g._t+.9);
  g._ring.setAttribute('transform','scale('+lerp(1,1.16,EO(r)).toFixed(3)+')');g._ring.setAttribute('opacity',r>0?(1-r).toFixed(3):0)});
 popAt(upd,1153,830,P(t,43.9,44.4));var left=1-.42*P(t,44.3,51.5);ring.setAttribute('stroke-dasharray',left.toFixed(4)+' 1');hand.setAttribute('transform','rotate('+(-360*(1-left)).toFixed(1)+' 1068 852)');
 popAt(svc,1570,830,P(t,45.4,45.9));var ok=t>=48.4,testing=t>=45.6&&!ok,col=ok?GREEN:testing?GOLD:RED;
 svcState.textContent=ok?'Verified':testing?'Testing recovery':'Failing';svcState.setAttribute('fill',col);svcNodes.forEach(function(c,i){c.setAttribute('stroke',i===1?col:ok?GREEN:LINE)});
 svcDots.forEach(function(c,i){var d=((t*.9+i*.25)%1);set(c,{cx:lerp(1440,1700,d)});op(c,ok?1:0)});op(svcNote,EO(P(t,48.6,49.1)));
}

/* ================= 4. The offer: seven lessons, then five tickets ================= */
var Of=G(svg),ofHead=T(Of,'display',157,226,'','start',56),ofCount=T(Of,'display green',1763,226,'7 narrated lessons','end',40);
var LESSONS=[['Overview of','ITIL 4'],['Service value','chain'],['Incident vs','request'],['Escalation and','support tiers'],['Major incident','drill'],['ServiceNow','visual guide'],['Job roles across','the lifecycle']];
var tiles=LESSONS.map(function(d,i){var g=G(Of),hot=i===4;el('rect',g,{x:-108,y:-65,width:216,height:130,rx:14,fill:hot?'#17494a':CARD,stroke:hot?GREEN:LINE,'stroke-width':3});
 T(g,hot?'display green':'display dim',-90,-24,String(i+1),'start',30);T(g,'semi',-90,14,d[0],'start',22);T(g,'semi',-90,42,d[1],'start',22);g._x=157+108+i*231;return g});
var recap=T(Of,'muted',W/2,760,'Declare · Assign · Set cadence · Restore · Hand off','middle',30),big7=T(Of,'display green',W/2,760,'7 narrated lessons','middle',76),bigLab=T(Of,'display',W/2,856,'in the Incident Triage Lab','middle',76);
var yourTurn=T(Of,'display',W/2,690,'Your turn.','middle',120);
var queue=G(Of);var queueLabel=T(queue,'bold track muted',157,452,'YOUR QUEUE','start',18);
var TICKETS=[['08:42','Every store has stopped taking payments'],['09:05','A new analyst starts next Monday'],['11:20','Payroll slows down every Friday'],['13:10','The public certificate expires in 14 days'],['16:35','The CEO is locked out before a flight']];
var tickets=TICKETS.map(function(d,i){var g=G(queue);g._box=el('rect',g,{x:0,y:0,width:620,height:88,rx:12,fill:CARD,'stroke-width':3});T(g,'num muted',22,54,d[0],'start',21);T(g,'semi',100,54,d[1],'start',21);g._y=470+i*98;return g});
var panel=G(Of);el('rect',panel,{'class':'f-card s-green',x:800,y:470,width:963,height:488,rx:16,'stroke-width':3});
T(panel,'bold track muted',832,514,'08:42 · SERVICE DESK QUEUE','start',18);T(panel,'semi',832,558,'Every store has stopped taking payments','start',30);el('line',panel,{'class':'s-line',x1:832,y1:582,x2:1731,y2:582,'stroke-width':2});
var CHOICES=[['Record type','Incident',61.48],['Priority','P1 — critical',62.91],['Next owner','Major-incident path and the service owner',63.86]];
var choices=CHOICES.map(function(d,i){var y=624+i*54,g=G(panel);T(g,'muted',832,y,d[0],'start',22);var chip=G(g),w=d[1].length*12.6+66;
 el('rect',chip,{x:0,y:-23,width:w,height:46,rx:23,fill:'#17494a',stroke:GREEN,'stroke-width':2});T(chip,'bold green',20,8,'✓','start',22);T(chip,'semi',46,8,d[1],'start',22);g._chip=chip;g._y=y-8;g._t=d[2];return g});
var update=G(panel);T(update,'muted',832,786,'First update','start',22);
var upd1=T(update,'semi',1042,786,'“We are investigating a widespread payment outage','start',22),upd2=T(update,'semi',1042,817,'affecting all stores. A major incident is active;','start',22),upd3=T(update,'semi',1042,848,'next update at 09:00.”','start',22);
var score=G(panel);T(score,'muted',832,926,'Score','start',22);el('rect',score,{'class':'f-line',x:920,y:908,width:330,height:20,rx:10});var scoreFill=el('rect',score,{'class':'f-green',x:920,y:908,height:20,rx:10});
el('line',score,{'class':'s-paper',x1:920+231,y1:900,x2:920+231,y2:936,'stroke-width':3});T(score,'muted',920+231,896,'pass mark 70%','middle',17);
var arrow=el('path',score,{'class':'f-none s-muted round',d:'M1272,918 H1334 M1320,906 L1334,918 L1320,930','stroke-width':4});
var lms=G(score);el('rect',lms,{'class':'f-bg s-blue',x:1352,y:890,width:379,height:56,rx:12,'stroke-width':3});T(lms,'bold blue',1372,926,'LMS','start',22);T(lms,'semi',1430,926,'completion · score · resume','start',20);
function drawOffer(t){
 var a=Math.min(EO(P(t,51.9,52.5)),1-E(P(t,68.85,69.35)));op(Of,a);if(a<=0)return;
 ofHead.textContent=t<57.9?'The major incident drill':'Incident Triage Lab';op(ofHead,Math.min(EO(P(t,52,52.5)),t<57.9?1-P(t,57.5,57.9):EO(P(t,57.9,58.4))));
 op(ofCount,EO(P(t,58.2,58.7)));
 op(recap,vis(t,52.3,52.8,53.9,54.3));op(big7,vis(t,54.47,54.95,57.5,57.9));op(bigLab,vis(t,56.15,56.6,57.5,57.9));
 var dimTiles=lerp(1,.4,E(P(t,58,58.6))),rowY=lerp(560,335,E(P(t,57.8,58.6))),settle=E(P(t,53.95,54.6));
 tiles.forEach(function(g,i){var s=i===4?52.05:54.25+(i<4?i:i-1)*.13,u=P(t,s,s+.4),k=lerp(.6,1,EB(u))*(i===4?lerp(1.5,1,settle):1),x=i===4?lerp(W/2,g._x,settle):g._x;
  g.setAttribute('transform',tr(x,rowY,k));op(g,u>=1?dimTiles:cl(u*4))});
 op(yourTurn,vis(t,58.05,58.5,59.3,59.7));op(queueLabel,EO(P(t,59.4,59.8)));
 tickets.forEach(function(g,i){var s=59.75+i*.17,u=P(t,s,s+.45);g.setAttribute('transform',tr(157,g._y-lerp(70,0,EO(u))));op(g,cl(u*3));g._box.setAttribute('stroke',i===0&&t>=61.2?GREEN:LINE)});
 popAt(panel,1281,714,P(t,61.05,61.5));
 choices.forEach(function(g){pop(g._chip,1042,g._y,P(t,g._t,g._t+.4))});
 op(update,EO(P(t,64.35,64.8)));op(upd1,EO(P(t,64.7,65.1)));op(upd2,EO(P(t,65,65.4)));op(upd3,EO(P(t,65.3,65.7)));
 op(score,EO(P(t,66.41,66.9)));scoreFill.setAttribute('width',(330*E(P(t,66.6,67.5))).toFixed(1));op(arrow,EO(P(t,67,67.4)));popAt(lms,1541,918,P(t,67.35,67.8));
}

/* ================= 5. The name, and what you do ================= */
var En=G(svg),enName=T(En,'display',W/2,470,'Incident Triage Lab','middle',150),enFrom=T(En,'semi muted',W/2,556,'from IT Professional Practice','middle',42);
var enLine=T(En,'display green',W/2,712,'Practise the response before you need it.','middle',68);
var enWhat=T(En,'muted',W/2,806,'Seven narrated lessons · a five-ticket assessed simulation · SCORM reporting · worksheet · facilitator guide','middle',26);
var cred=G(En);T(cred,'muted',W/2,950,'IT Professional Practice · Part 1: ITIL 4 Foundations · Major Incident Management Drill','middle',24);
T(cred,'muted',W/2,986,'Voices are AI-generated. The outage, its clock times and its counts are an illustrative scenario.','middle',22);
function drawEnd(t){
 var a=Math.min(EO(P(t,69.3,69.8)),1-E(P(t,A_TOTAL-.8,A_TOTAL-.1)));op(En,a);if(a<=0)return;
 var u=EB(P(t,69.5,70.1));enName.setAttribute('transform','translate('+W/2+',420) scale('+lerp(.82,1,u).toFixed(3)+') translate('+(-W/2)+',-420)');op(enName,P(t,69.5,69.75));
 op(enFrom,EO(P(t,71.2,71.7)));op(enLine,EO(P(t,73.6,74.2)));enLine.setAttribute('transform',tr(0,lerp(22,0,EO(P(t,73.6,74.3)))));op(enWhat,EO(P(t,75.1,75.7)));op(cred,EO(P(t,A_DUR-.6,A_DUR+.1)));
}

/* ---------- render ---------- */
var bar=el('rect',svg,{'class':'f-green',y:H-5,height:5,opacity:.7});
function render(t){
 t=Math.max(0,Math.min(TOTAL,t));var a=authored(t);drawOutage(a);drawResponse(a);drawOffer(a);drawEnd(a);
 var out=1-E(P(a,A_TOTAL-.8,A_TOTAL-.1));op(kicker,out);op(kick2,out);op(scenario,vis(a,.4,1,51.4,51.9));bar.setAttribute('width',(W*t/TOTAL).toFixed(1));
}
var api={render:render,total:TOTAL,narration:DUR,audio:NARR.audio,ready:document.fonts?document.fonts.ready:Promise.resolve()};
window.__explainer=api;
if(CAPTURE){render(Number(query.get('t'))||0);return}

/* ---------- page wiring ---------- */
var audio=document.getElementById('p1-audio'),play=document.getElementById('p1-play'),seek=document.getElementById('p1-seek'),time=document.getElementById('p1-time'),
 caption=document.getElementById('p1-caption'),capBox=document.getElementById('p1-captions'),clockState={t:0,playing:false,base:0,at:0};
audio.src=NARR.audio;
function mmss(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function now(){if(!clockState.playing)return clockState.t;if(!audio.paused&&!audio.ended)return audio.currentTime;return Math.min(TOTAL,clockState.base+(performance.now()-clockState.at)/1000)}
function paint(){
 var t=now();clockState.t=t;render(!clockState.playing&&t===0?8.2:t);seek.value=Math.round(t/TOTAL*1000);time.textContent=mmss(t)+' / '+mmss(TOTAL);
 var line=null;NARR.lines.forEach(function(l){if(t>=l.start&&t<l.end+.3)line=l});caption.textContent=line?line.text:'';
}
function loop(){if(!clockState.playing)return;paint();if(clockState.t>=TOTAL){stop();return}requestAnimationFrame(loop)}
function stop(){clockState.playing=false;audio.pause();play.textContent=clockState.t>=TOTAL?'Replay':'Play'}
function start(){if(clockState.t>=TOTAL-.05)clockState.t=0;clockState.playing=true;play.textContent='Pause';clockState.base=clockState.t;clockState.at=performance.now();
 if(clockState.t<DUR-.05){audio.currentTime=clockState.t;audio.play().catch(function(){})}requestAnimationFrame(loop)}
audio.addEventListener('ended',function(){clockState.base=DUR;clockState.at=performance.now()});
play.addEventListener('click',function(){if(clockState.playing)stop();else start()});
seek.addEventListener('input',function(){var was=clockState.playing;if(was)audio.pause();clockState.t=seek.value/1000*TOTAL;clockState.base=clockState.t;clockState.at=performance.now();if(was&&clockState.t<DUR-.05){audio.currentTime=clockState.t;audio.play().catch(function(){})}paint()});
capBox.addEventListener('change',function(){caption.hidden=!capBox.checked});
var host=document.getElementById('p1-transcript');
if(host)NARR.lines.forEach(function(l){var p=document.createElement('p'),b=document.createElement('strong');b.textContent=l.speaker+': ';p.appendChild(b);p.appendChild(document.createTextNode(l.text));host.appendChild(p)});
api.ready.then(paint);
})();
