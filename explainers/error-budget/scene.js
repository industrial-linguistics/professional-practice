/* Error-budget explainer.
   render(t) draws the frame for narration time t, so the same scene plays against the audio
   in a browser and steps frame by frame for video (scripts/render_explainer.cjs).
   Beat times below are in authored time: the timeline of the first recorded take. A later take
   (another model, other settings) carries a warp table in narration.js that maps its word times
   back to authored time, so re-voicing needs no re-timing here. */
(function(){
'use strict';
var root=document.querySelector('[data-explainer]'),NARR=window.EXPLAINER_NARRATION;
if(!root||!NARR)return;
var query=new URLSearchParams(location.search),CAPTURE=query.has('capture');
if(CAPTURE)document.body.classList.add('eb-capture');
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
function mix(a,b,u){function h(c,i){return parseInt(c.substr(1+i*2,2),16)}var o='#';for(var i=0;i<3;i++){var v=Math.round(lerp(h(a,i),h(b,i),u)).toString(16);o+=v.length<2?'0'+v:v}return o}
var GREEN='#2cc2a8',RED='#f26b5b',GOLD='#e6ad45',BLUE='#78a8e8',LINE='#33445f',PAPER='#f5f7f9';

/* ---------- stage ---------- */
var svg=el('svg',root,{'class':'eb-svg',viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'Animation: what a 99.9% availability promise allows, how an error budget is spent over a month, and what teams do when it burns too fast. A transcript follows.'});
var defs=el('defs',svg),grad=el('radialGradient',defs,{id:'eb-bg',cx:'28%',cy:'22%',r:'95%'});
el('stop',grad,{offset:0,'stop-color':'#22345a'});el('stop',grad,{offset:1,'stop-color':'#0c1322'});
el('rect',svg,{width:W,height:H,fill:'url(#eb-bg)'});
var kicker=T(svg,'bold track gold',157,84,'IT PROFESSIONAL PRACTICE','start',20),kick2=T(svg,'track muted',560,84,'ERROR BUDGETS','start',20);

/* ================= 1. The promise, and a year of hours ================= */
var WX=157,WY=290,COLS=146,ROWS=60,PITCH=11;
var cells=el('pattern',defs,{id:'eb-cells',x:WX,y:WY,width:PITCH,height:PITCH,patternUnits:'userSpaceOnUse'});
el('rect',cells,{width:9,height:9,rx:1.5,fill:'#2e4063'});
var wallClip=el('rect',el('clipPath',defs,{id:'eb-wall-clip'}),{x:WX,y:WY,height:ROWS*PITCH,width:0});
var S1=G(svg),wall=el('rect',S1,{x:WX,y:WY,width:COLS*PITCH,height:ROWS*PITCH,fill:'url(#eb-cells)','clip-path':'url(#eb-wall-clip)'});
var yearLabel=T(S1,'muted',WX+COLS*PITCH,222,'One year = 8,760 hours','end',30);
var promise1=T(S1,'semi muted',W/2,330,'You promised your app would be available','middle',56);
var bigG=G(S1),big=T(bigG,'display num',0,118,'99.9%','middle',340);
var promise2=T(S1,'semi muted',W/2,860,'of the time','middle',56);
var tagNote=T(S1,'muted',400,222,'promised availability','start',30);
var REDS=[[12,8],[31,40],[47,17],[63,52],[78,29],[95,9],[108,44],[124,22],[139,50]];
var redLayer=null,redCells=REDS.map(function(c){var g=G(null);el('circle',g,{'class':'f-none s-red',r:6,'stroke-width':3});el('rect',g,{'class':'f-red',x:-6,y:-6,width:12,height:12,rx:2});return g});
var nine=T(S1,'display red',WX+COLS*PITCH,1014,'≈ 9 hours of downtime allowed','end',60);
/* ================= 2. SRE turns the promise into arithmetic ================= */
var S2=G(svg);
el('rect',S2,{'class':'f-card s-line',x:330,y:340,width:1260,height:540,rx:18,'stroke-width':2,'fill-opacity':.95});
var sreLine=el('text',S2,{'class':'display',x:400,y:452,'font-size':74}),sreCaps=[];
[['S','ite '],['R','eliability '],['E','ngineering']].forEach(function(p){var a=el('tspan',sreLine);a.textContent=p[0];sreCaps.push(a);el('tspan',sreLine).textContent=p[1]});
var sreBadge=T(S2,'display gold',1520,452,'SRE','end',74);
var eq1=el('text',S2,{'class':'semi num',x:400,y:566,'font-size':56});el('tspan',eq1).textContent='100% − 99.9% = ';el('tspan',eq1,{'class':'red'}).textContent='0.1%';
var eq2=el('text',S2,{'class':'semi num',x:400,y:654,'font-size':48});el('tspan',eq2).textContent='0.1% × 8,760 hours = ';el('tspan',eq2,{'class':'red'}).textContent='8.76 hours';
var tag1=G(S2);el('rect',tag1,{'class':'f-none s-green',x:400,y:742,width:590,height:78,rx:39,'stroke-width':3});
var tag1Name=T(tag1,'bold green',436,792,'SLO','start',32);T(tag1,'muted',516,791,'service level objective','start',26);T(tag1,'semi num',954,792,'99.9%','end',32);
var tag2=G(S2);el('rect',tag2,{'class':'f-none s-red',x:1060,y:742,width:460,height:78,rx:39,'stroke-width':3});
T(tag2,'bold red',1096,792,'Error budget','start',32);T(tag2,'semi num',1484,792,'0.1%','end',32);
redLayer=G(svg);redCells.forEach(function(g){redLayer.appendChild(g)});
var tie=el('line',S2,{'class':'s-muted round',x1:990,y1:781,y2:781,'stroke-width':4,'stroke-dasharray':'2 10'});
function drawS12(t){
 var a=1-E(P(t,21.9,22.5));op(S1,a);op(redLayer,a);op(S2,Math.min(EO(P(t,9.8,10.5)),a));if(a<=0)return;
 op(promise1,vis(t,.7,1.4,5.6,6.1));op(promise2,vis(t,4.6,5,5.6,6.1));
 var pop=EB(P(t,2.95,3.5)),go=E(P(t,5.7,6.6));
 bigG.setAttribute('transform',tr(lerp(960,290,go),lerp(600,198,go),lerp(1,.2,go)*lerp(.6,1,pop)));op(bigG,P(t,2.95,3.2));
 op(tagNote,EO(P(t,6.4,7))*(1-P(t,9.6,10.2)));op(yearLabel,EO(P(t,6,6.6))*(1-P(t,9.6,10.2)));
 var wipe=E(P(t,5.96,7.2));wallClip.setAttribute('width',(COLS*PITCH*wipe).toFixed(1));wall.setAttribute('opacity',lerp(1,.32,E(P(t,9.6,10.4))).toFixed(3));
 var fly=E(P(t,13.4,14.9)),above=t>=13.35; // the hours wait behind the card, then fly onto it
 if(redLayer._above!==above){redLayer._above=above;redCells.forEach(function(g){(above?redLayer:S1).appendChild(g)})}
 redCells.forEach(function(g,i){var s=7.3+i*.07,u=P(t,s,s+.35),x0=WX+REDS[i][0]*PITCH+4.5,y0=WY+REDS[i][1]*PITCH+4.5,x1=1296+i*28,y1=638,ring=P(t,s,s+.9);
  g.setAttribute('transform',tr(lerp(x0,x1,fly),lerp(y0,y1,fly),lerp(lerp(1,2.4,EB(u)),1.85,fly)));op(g,u>0?1:0);
  set(g.firstChild,{r:lerp(6,22,EO(ring)),opacity:fly>0?0:(1-ring).toFixed(3)})});
 op(nine,vis(t,7.35,7.9,13.2,13.8));
 sreCaps.forEach(function(s){s.setAttribute('class',t>12.1?'gold':'')});op(sreBadge,EO(P(t,12.1,12.6)));
 op(eq1,EO(P(t,14.5,15.1)));op(eq2,EO(P(t,15.2,15.8)));
 op(tag1,EO(P(t,17.4,18)));tag1Name.setAttribute('font-size',lerp(32,38,Math.sin(Math.PI*P(t,19.2,19.9))).toFixed(1));
 op(tag2,EO(P(t,20.5,21.1)));var u=E(P(t,21.2,21.7));tie.setAttribute('x2',lerp(990,1060,u));tie.setAttribute('opacity',u>0?1:0);
}

/* ================= 3. Ship, or stop and fix ================= */
var S3=G(svg),GX=960,GY=820,GR=400;
var s3Title=T(S3,'display',157,222,'How reliable must the service be?','start',60);
function arc(f0,f1){var a0=Math.PI*(1-f0),a1=Math.PI*(1-f1);return 'M'+(GX+GR*Math.cos(a0)).toFixed(1)+','+(GY-GR*Math.sin(a0)).toFixed(1)+' A'+GR+','+GR+' 0 0 1 '+(GX+GR*Math.cos(a1)).toFixed(1)+','+(GY-GR*Math.sin(a1)).toFixed(1)}
var arcs=[[0,.745,'s-green'],[.755,.915,'s-gold'],[.925,1,'s-red']].map(function(z){return el('path',S3,{'class':'f-none '+z[2],d:arc(z[0],z[1]),'stroke-width':46,pathLength:1,'stroke-dasharray':'1 1'})});
T(S3,'muted',GX-GR,GY+56,'budget full','middle',24);T(S3,'muted',GX+GR,GY+56,'budget spent','middle',24);
var needle=el('line',S3,{'class':'s-paper round',x1:GX,y1:GY,'stroke-width':10}),hub=el('circle',S3,{'class':'f-paper',cx:GX,cy:GY,r:22});
var sloChip=G(S3);el('rect',sloChip,{'class':'f-card s-green',x:GX-150,y:286,width:300,height:70,rx:35,'stroke-width':3});T(sloChip,'bold green',GX,333,'SLO 99.9%','middle',32);
var goA=T(S3,'display',157,560,'Safe to launch','start',54),goB=T(S3,'display',157,624,'new features','start',54);
var stopA=T(S3,'display',1763,560,'Pause and fix','end',54),stopB=T(S3,'display',1763,624,'instability','end',54);
function drawS3(t){
 var a=Math.min(EO(P(t,22.4,23)),1-E(P(t,31.6,32.2)));op(S3,a);if(a<=0)return;
 op(s3Title,EO(P(t,22.6,23.2)));op(sloChip,EO(P(t,23.5,24.1)));
 arcs.forEach(function(p,i){var u=E(P(t,23.9+i*.35,24.9+i*.35));p.setAttribute('stroke-dashoffset',(1-u).toFixed(4));p.setAttribute('opacity',u>0?1:0)});
 var f=lerp(lerp(.45,.18,E(P(t,26.4,27.3))),.975,E(P(t,29.3,30.2)))+.008*Math.sin(t*9),ang=Math.PI*(1-f),show=EO(P(t,25.5,26));
 set(needle,{x2:(GX+(GR-78)*Math.cos(ang)).toFixed(1),y2:(GY-(GR-78)*Math.sin(ang)).toFixed(1)});op(needle,show);op(hub,show);
 var go=P(t,26.7,27.1)*(1-P(t,29.2,29.6)),stop=P(t,29.6,30);
 [goA,goB].forEach(function(n){n.setAttribute('class',go>.5?'display green':'display dim');op(n,EO(P(t,26.2,26.8)))});
 [stopA,stopB].forEach(function(n){n.setAttribute('class',stop>.5?'display red':'display dim');op(n,EO(P(t,26.2,26.8)))});
}

/* ================= 4. The slice, and a month of minutes ================= */
var S4=G(svg);
var s4Title=T(S4,'display',157,222,'The error budget','start',60);
var slo=el('rect',S4,{'class':'f-green',x:157,y:306,height:76,rx:10}),sloText=T(S4,'bold ink',187,356,'99.9%: the service level objective','start',30);
var sliver=el('rect',S4,{'class':'f-red',x:1761,y:306,width:2.5,height:76});
var lens=G(S4),LX=1500,LY=610,LR=165;
el('line',lens,{'class':'s-muted',x1:1763,y1:382,x2:LX+LR*.766,y2:LY-LR*.643,'stroke-width':2});
el('clipPath',defs,{id:'eb-lens'}).appendChild(el('circle',null,{cx:LX,cy:LY,r:LR}));
var lensIn=el('g',lens,{'clip-path':'url(#eb-lens)'});el('rect',lensIn,{'class':'f-green',x:LX-LR,y:LY-LR,width:LR+14,height:LR*2});el('rect',lensIn,{'class':'f-red',x:LX+14,y:LY-LR,width:LR,height:LR*2});
el('circle',lens,{'class':'f-none s-paper',cx:LX,cy:LY,r:LR,'stroke-width':5});T(lens,'display ink',LX+84,LY+18,'0.1%','middle',50);T(lens,'bold ink',LX-72,LY+12,'99.9%','middle',30);
var lensNote=T(S4,'semi red',LX,LY+LR+58,'allowable failure','middle',36);
var monthLabel=T(S4,'semi',157,520,'One 30-day month = 43,200 minutes','start',34);
var days=[];for(var di=0;di<30;di++)days.push(el('rect',S4,{'class':'f-line',x:157+di*38,y:548,width:30,height:30,rx:5}));
var monthEq=T(S4,'muted num',157,680,'43,200 minutes × 0.1% =','start',34);
var forty=T(S4,'display gold num',150,850,'43 minutes','start',176),fortyNote=T(S4,'semi',157,916,'of downtime allowed each month','start',36);
function drawS4(t){
 var a=Math.min(EO(P(t,32.2,32.8)),1-E(P(t,44.3,44.9)));op(S4,a);if(a<=0)return;
 op(s4Title,EO(P(t,32.4,33)));var g=E(P(t,32.7,33.6));slo.setAttribute('width',(1604*g).toFixed(1));op(sloText,P(t,33.3,33.7));op(sliver,P(t,33.6,33.8));
 var l=EB(P(t,33.8,34.6));lens.setAttribute('transform','translate('+LX+','+LY+') scale('+lerp(.3,1,l).toFixed(3)+') translate('+(-LX)+','+(-LY)+')');op(lens,P(t,33.8,34.1));
 op(lensNote,EO(P(t,34.7,35.3)));op(monthLabel,EO(P(t,38.2,38.8)));
 days.forEach(function(d,i){d.setAttribute('opacity',EO(P(t,38.5+i*.035,38.8+i*.035)).toFixed(3))});
 op(monthEq,EO(P(t,41.1,41.7)));var p=EB(P(t,42.25,42.8));forty.setAttribute('transform',tr(0,lerp(26,0,cl(p))));op(forty,P(t,42.25,42.5));op(fortyNote,EO(P(t,42.9,43.5)));
}

/* ================= 5 to 8. One month of budget, then a faster one ================= */
var Dg=G(svg),TX=157,TW=140,TY0=300,TY1=900,cx0=600,cx1=1763,cy0=450,cy1=880,L1=292,L2=366,BUDGET=43;
var M1=[{d:6,m:14,label:'outage'},{d:13,m:9,label:'slow pages'},{d:19,m:12,label:'outage'},{d:23,m:8,label:'outage'}],M2=[{d:2,m:10},{d:5,m:12},{d:8,m:11}];
var DEPLOYS=[2,4,5,8,10,12,15,17,18,21,22],FIXES=[24,25,27,28,29];
function xD(d){return cx0+d/30*(cx1-cx0)}
function yB(min,C){return cy1-cl(min/C)*(cy1-cy0)}
function left(events,day){var b=BUDGET;events.forEach(function(e){if(e.d<=day)b-=e.m});return b}
function steps(events,day,C,extra){var d='M'+xD(0)+','+yB(BUDGET+extra,C).toFixed(1),b=BUDGET;events.forEach(function(e){if(e.d<=day){d+=' H'+xD(e.d).toFixed(1);b-=e.m;d+=' V'+yB(b+extra,C).toFixed(1)}});return d+' H'+xD(day).toFixed(1)}
var dTitle=T(Dg,'display',157,222,'','start',56);
// tank
T(Dg,'bold track muted',TX,TY0-22,'ERROR BUDGET','start',18);
el('clipPath',defs,{id:'eb-tank'}).appendChild(el('rect',null,{x:TX,y:TY0,width:TW,height:TY1-TY0,rx:18}));
var tankFill=el('rect',el('g',Dg,{'clip-path':'url(#eb-tank)'}),{x:TX,width:TW});
el('rect',Dg,{'class':'f-none s-paper',x:TX,y:TY0,width:TW,height:TY1-TY0,rx:18,'stroke-width':4});
var tankNum=T(Dg,'display num',TX+TW+24,0,'43','start',76),tankUnit=T(Dg,'muted',TX+TW+26,0,'min left','start',24);
// chart
var chart=G(Dg);
el('rect',chart,{'class':'f-gold',x:cx0,y:cy1-.25*(cy1-cy0),width:cx1-cx0,height:.25*(cy1-cy0),'fill-opacity':.08});
var freeze=el('rect',chart,{'class':'f-red',x:xD(23),y:cy0,width:xD(30)-xD(23),height:cy1-cy0,'fill-opacity':.14});
el('line',chart,{'class':'s-muted',x1:cx0,y1:cy0,x2:cx0,y2:cy1,'stroke-width':2});el('line',chart,{'class':'s-muted',x1:cx0,y1:cy1,x2:cx1,y2:cy1,'stroke-width':2});
var yTop=T(chart,'muted num',cx0-16,cy0+8,'43 min','end',24);T(chart,'muted num',cx0-16,cy1+8,'0','end',24);
[[0,'Day 1'],[10,'10'],[20,'20'],[30,'30']].forEach(function(d){T(chart,'muted num',xD(d[0]),cy1+40,d[1],'middle',24)});
var thY=cy1-.25*(cy1-cy0),thLine=el('line',chart,{'class':'s-gold',x1:cx0,y1:thY,x2:cx1,y2:thY,'stroke-width':2,'stroke-dasharray':'10 8'}),thLabel=T(chart,'gold',cx1-12,thY-12,'25% left','end',22);
var thBig=T(chart,'bold gold halo',cx0+24,thY-16,'Below 25%: slow the release pace','start',30),thRing=el('circle',chart,{'class':'f-none s-gold',cx:xD(19),cy:thY,'stroke-width':4});
var freezeLabel=T(chart,'semi red halo',cx1-14,cy0+64,'7 days of feature work paused','end',27);
var ghost=el('path',chart,{'class':'f-none s-muted round','stroke-width':4}),line1=el('path',chart,{'class':'f-none s-paper round','stroke-width':6});
var expected=el('line',chart,{'class':'s-muted round',x1:xD(0),'stroke-width':4,'stroke-dasharray':'4 12'}),expLabel=T(chart,'muted halo',0,0,'budgeted burn','start',24);
var line2=el('path',chart,{'class':'f-none s-red round','stroke-width':6}),proj=el('line',chart,{'class':'round','stroke-width':5,'stroke-dasharray':'14 12'}),projLabel=T(chart,'bold halo',0,0,'','start',28);
var marks1=M1.map(function(e){var g=G(chart);el('circle',g,{'class':'f-red',r:10});T(g,'bold red halo',18,8,e.label+' −'+e.m+' min','start',24);return g});
var marks2=M2.map(function(){return el('circle',chart,{'class':'f-red',r:10})});
var burnLabel=T(chart,'bold red halo',xD(3),cy0-26,'Burning about 3× faster than budgeted','start',30);
var cursor=el('line',chart,{'class':'s-paper',y1:cy0-12,y2:cy1,'stroke-width':2,'stroke-opacity':.45});
// release lanes
var lanes=G(Dg),lane1Label=T(lanes,'bold track muted',cx0,L1-26,'NEW FEATURES','start',18),lane2Label=T(lanes,'bold track muted',cx0,L2-26,'RELIABILITY WORK','start',18);
el('line',lanes,{'class':'s-line round',x1:cx0,y1:L1,x2:cx1,y2:L1,'stroke-width':4});el('line',lanes,{'class':'s-line round',x1:cx0,y1:L2,x2:cx1,y2:L2,'stroke-width':4});
var deploys=DEPLOYS.map(function(d){return el('rect',lanes,{'class':'f-blue',x:-11,y:-11,width:22,height:22,rx:3})}),fixes=FIXES.map(function(d){return el('circle',lanes,{'class':'f-green',r:12})});
var gate=G(lanes);el('rect',gate,{'class':'f-red',x:xD(23)+16,y:L1-34,width:10,height:68,rx:5});T(gate,'bold red',xD(23)+26,L1-46,'Budget spent: feature freeze','end',26);
// people, questions and levers share the top band
var ROLES=[['Product managers',57.9],['Engineers',62.1],['Ops',67.9],['Support',69.6],['Leadership',70.6]],rx=cx0;
var roles=ROLES.map(function(r){var g=G(Dg),w=r[0].length*15.5+52;el('rect',g,{'class':'f-card s-muted',x:0,y:-36,width:w,height:56,rx:28,'stroke-width':2});T(g,'semi',w/2,2,r[0],'middle',27);g._x=rx;g._w=w;rx+=w+26;return g});
var talk=ROLES.slice(1).map(function(r,i){var a=roles[i],b=roles[i+1],x0=a._x+a._w/2,x1=b._x+b._w/2;return el('path',Dg,{'class':'f-none s-gold round',d:'M'+x0+',142 Q'+((x0+x1)/2)+','+(142-46)+' '+x1+',142','stroke-width':3,pathLength:1,'stroke-dasharray':'1 1'})});
var ask=[['Are our releases too risky?','s-blue','f-blue',76.2,470],['Or is the SLO unrealistic?','s-gold','f-gold',78.5,566]].map(function(q){var g=G(Dg);el('rect',g,{'class':'f-card '+q[1],x:1220,y:q[4],width:520,height:80,rx:12,'stroke-width':2});el('rect',g,{'class':q[2],x:1220,y:q[4],width:12,height:80,rx:6});T(g,'semi',1256,q[4]+51,q[0],'start',30);g._t=q[3];return g});
var LEVERS=[['Slow deployments',82.1,600],['Add more testing',83.5,1010],['Adjust the SLO',85.4,1410]];
var levers=LEVERS.map(function(l){var g=G(Dg);g._track=el('rect',g,{x:l[2],y:160,width:92,height:48,rx:24});g._knob=el('circle',g,{'class':'f-paper',cy:184,r:18});T(g,'semi',l[2]+110,195,l[0],'start',30);g._t=l[1];g._x=l[2];return g});
var sloShift=T(Dg,'gold num',1410,246,'99.9% → 99.5%: budget 43 → 216 min','start',23),sloIf=T(Dg,'muted',1410,278,'if customer impact warrants it','start',22);
var D1=[[0,44.9],[6,45.3],[13,46.4],[19,47.7],[23,50],[30,54.3]];
function day1(t){if(t<=D1[0][1])return 0;for(var i=1;i<D1.length;i++)if(t<=D1[i][1])return lerp(D1[i-1][0],D1[i][0],(t-D1[i-1][1])/(D1[i][1]-D1[i-1][1]));return 30}
var End=G(svg),endA=T(End,'display',W/2,500,'Argue about reliability','middle',92),endB=T(End,'display green',W/2,612,'with numbers instead of opinions.','middle',92);
var cred=G(End);T(cred,'muted',W/2,930,'IT Professional Practice · Part 3: High-Velocity Delivery · Error Budgets & SLOs','middle',24);T(cred,'muted',W/2,966,'Voices are AI-generated. The month of incidents and the lever projections are illustrative.','middle',22);
function drawDash(t){
 var a=EO(P(t,44.7,45.4)),dim=lerp(1,.14,E(P(t,88.7,89.5)));op(Dg,a*dim*(1-E(P(t,A_TOTAL-.8,A_TOTAL-.1))));
 op(End,EO(P(t,88.9,89.7))*(1-E(P(t,A_TOTAL-.8,A_TOTAL-.1))));op(cred,EO(P(t,A_DUR-.4,A_DUR+.3)));
 if(a<=0)return;
 var d1=day1(t),month2=P(t,72.8,73.4),d2=8*E(P(t,73.4,74.7)),C=lerp(BUDGET,216,E(P(t,85.6,86.7))),extra=C-BUDGET;
 dTitle.textContent=t<60?'A month of error budget':'Next month';op(dTitle,Math.max(vis(t,44.9,45.5,55,55.6),vis(t,72.9,73.5,80.6,81.1)));
 // budget remaining drives the tank
 var remaining=month2<=0?left(M1,d1):lerp(left(M1,30),left(M2,d2)+extra,E(month2)),frac=cl(remaining/C),ty=TY1-frac*(TY1-TY0);
 set(tankFill,{y:ty.toFixed(1),height:(TY1-ty).toFixed(1),fill:frac>.25?GREEN:frac>0?GOLD:RED});
 tankNum.textContent=String(Math.round(remaining));var ny=Math.min(TY1-12,Math.max(TY0+62,ty+30));tankNum.setAttribute('y',ny);tankUnit.setAttribute('y',ny+32);
 tankNum.setAttribute('class',remaining<.5?'display num red':frac<=.25?'display num gold':'display num');
 // month one
 var m1=lerp(1,0,E(month2));
 line1.setAttribute('d',steps(M1,d1,BUDGET,0));op(line1,m1);ghost.setAttribute('d',steps(M1,30,BUDGET,0));op(ghost,month2*.3*(1-P(t,85.4,85.9)));
 marks1.forEach(function(g,i){var e=M1[i],on=d1>=e.d?1:0,before=left(M1,e.d-.01),after=before-e.m;g.setAttribute('transform',tr(xD(e.d),(yB(before,BUDGET)+yB(after,BUDGET))/2));op(g,on*m1)});
 set(cursor,{x1:xD(d1),x2:xD(d1)});op(cursor,vis(t,44.9,45.2,54.3,54.9));
 op(freeze,vis(t,50.2,50.9,72.6,73.2));op(freezeLabel,vis(t,59.2,59.8,72.4,73));
 var hi=vis(t,62.5,63,65.6,66.3);thLine.setAttribute('stroke-width',lerp(2,5,hi));op(thLabel,1-hi);op(thBig,hi);var pulse=P(t,63.4,64.6);set(thRing,{r:lerp(8,40,EO(pulse))});op(thRing,pulse>0?1-pulse:0);
 // lanes
 op(lanes,1-E(P(t,72.6,73.2)));
 deploys.forEach(function(n,i){var d=DEPLOYS[i],u=cl((d1-d)*1.6);n.setAttribute('transform',tr(xD(d),L1-lerp(40,0,EO(u)))+' rotate(45)');op(n,u)});
 fixes.forEach(function(n,i){var d=FIXES[i],u=cl((d1-d)*1.6);n.setAttribute('transform',tr(xD(d),L2-lerp(40,0,EO(u))));op(n,u)});
 var gd=EB(P(t,50.2,50.8));gate.setAttribute('transform',tr(0,lerp(-60,0,cl(gd))));op(gate,P(t,50.2,50.4));
 lane1Label.textContent=t>53.5?'NEW FEATURES: PAUSED':'NEW FEATURES';lane1Label.setAttribute('class',t>53.5?'bold track red':'bold track muted');lane2Label.setAttribute('class',t>51.9?'bold track green':'bold track muted');
 // people
 roles.forEach(function(g,i){var s=ROLES[i][1],u=EB(P(t,s,s+.45));g.setAttribute('transform',tr(g._x,184-lerp(24,0,cl(u))));op(g,P(t,s,s+.2)*(1-E(P(t,72.4,73))))});
 talk.forEach(function(p,i){var s=69.5+i*.5,u=E(P(t,s,s+.7));p.setAttribute('stroke-dashoffset',(1-u).toFixed(4));op(p,(u>0?.55+.45*Math.sin(t*5-i):0)*(1-E(P(t,72.4,73))))});
 // month two
 line2.setAttribute('d',steps(M2,d2,C,extra));op(line2,month2*(d2>0?1:0));yTop.textContent=Math.round(C)+' min';
 marks2.forEach(function(n,i){var e=M2[i];set(n,{cx:xD(e.d),cy:yB(left(M2,e.d)+extra,C)});op(n,d2>=e.d?1:0)});
 var ex=E(P(t,74.3,75.3));set(expected,{y1:cy0,x2:lerp(xD(0),xD(30),ex),y2:lerp(cy0,cy1,ex)});op(expected,ex>0?1:0);
 set(expLabel,{x:xD(21)+14,y:yB(BUDGET*(1-21/30),BUDGET)-18});op(expLabel,EO(P(t,75,75.5)));
 op(burnLabel,vis(t,74.9,75.5,80.6,81.1));
 ask.forEach(function(g){op(g,vis(t,g._t,g._t+.5,80.6,81.1))});
 // levers and the projection they change
 var on=LEVERS.map(function(l){return E(P(t,l[1],l[1]+.45))});
 levers.forEach(function(g,i){op(g,EO(P(t,81.2+i*.12,81.8+i*.12)));g._track.setAttribute('fill',mix(LINE,GREEN,on[i]));g._knob.setAttribute('cx',lerp(g._x+24,g._x+68,on[i]))});
 op(sloShift,EO(P(t,85.9,86.5)));op(sloIf,EO(P(t,86.6,87.2)));
 var k=lerp(lerp(4.125,1.6,on[0]),.4,on[1]),now=left(M2,8)+extra,zero=8+now/k,endDay=Math.min(30,zero),endLeft=Math.max(0,now-k*(endDay-8)),ok=zero>=30,pa=EO(P(t,81.3,81.9));
 set(proj,{x1:xD(8),y1:yB(now,C),x2:xD(endDay),y2:yB(endLeft,C),stroke:ok?GREEN:RED});op(proj,pa);
 projLabel.textContent=ok?(extra>20?'Budget lasts the month, with room to spare':'Budget just lasts the month'):'Budget gone by day '+Math.floor(zero);
 projLabel.setAttribute('class',ok?'bold halo green':'bold halo red');set(projLabel,{x:ok?xD(9.5):xD(endDay)+18,y:ok?yB(now,C)-30:cy1-26});op(projLabel,pa);
}

/* ---------- render ---------- */
var bar=el('rect',svg,{'class':'f-green',y:H-5,height:5,opacity:.7});
function render(t){
 t=Math.max(0,Math.min(TOTAL,t));var a=authored(t);drawS12(a);drawS3(a);drawS4(a);drawDash(a);
 var out=1-E(P(a,A_TOTAL-.8,A_TOTAL-.1));op(kicker,out);op(kick2,EO(P(a,5.8,6.4))*out);bar.setAttribute('width',(W*t/TOTAL).toFixed(1));
}
var api={render:render,total:TOTAL,narration:DUR,audio:NARR.audio,ready:document.fonts?document.fonts.ready:Promise.resolve()};
window.__explainer=api;
if(CAPTURE){render(Number(query.get('t'))||0);return}

/* ---------- page wiring ---------- */
var audio=document.getElementById('eb-audio'),play=document.getElementById('eb-play'),seek=document.getElementById('eb-seek'),time=document.getElementById('eb-time'),
 caption=document.getElementById('eb-caption'),capBox=document.getElementById('eb-captions'),clock={t:0,playing:false,base:0,at:0};
audio.src=NARR.audio;
function mmss(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function now(){if(!clock.playing)return clock.t;if(!audio.paused&&!audio.ended)return audio.currentTime;return Math.min(TOTAL,clock.base+(performance.now()-clock.at)/1000)}
function paint(){
 var t=now();clock.t=t;render(!clock.playing&&t===0?3.6:t);seek.value=Math.round(t/TOTAL*1000);time.textContent=mmss(t)+' / '+mmss(TOTAL);
 var line=null;NARR.lines.forEach(function(l){if(t>=l.start&&t<l.end+.3)line=l});caption.textContent=line?line.text:'';
}
function loop(){if(!clock.playing)return;paint();if(clock.t>=TOTAL){stop();return}requestAnimationFrame(loop)}
function stop(){clock.playing=false;audio.pause();play.textContent=clock.t>=TOTAL?'Replay':'Play'}
function start(){if(clock.t>=TOTAL-.05)clock.t=0;clock.playing=true;play.textContent='Pause';clock.base=clock.t;clock.at=performance.now();
 if(clock.t<DUR-.05){audio.currentTime=clock.t;audio.play().catch(function(){})}requestAnimationFrame(loop)}
audio.addEventListener('ended',function(){clock.base=DUR;clock.at=performance.now()});
play.addEventListener('click',function(){if(clock.playing)stop();else start()});
seek.addEventListener('input',function(){var was=clock.playing;if(was)audio.pause();clock.t=seek.value/1000*TOTAL;clock.base=clock.t;clock.at=performance.now();if(was&&clock.t<DUR-.05){audio.currentTime=clock.t;audio.play().catch(function(){})}paint()});
capBox.addEventListener('change',function(){caption.hidden=!capBox.checked});
var host=document.getElementById('eb-transcript');
if(host)NARR.lines.forEach(function(l){var p=document.createElement('p'),b=document.createElement('strong');b.textContent=l.speaker+': ';p.appendChild(b);p.appendChild(document.createTextNode(l.text));host.appendChild(p)});
api.ready.then(paint);
})();
