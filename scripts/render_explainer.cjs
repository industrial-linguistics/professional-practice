#!/usr/bin/env node
/* Render an animated explainer (explainers/<name>/) to stills or a narrated MP4.

   The scene draws any moment on request (window.__explainer.render(t)), so this steps it
   frame by frame in headless Chromium and never depends on real-time playback.

     node scripts/render_explainer.cjs --stills 4,8,20,43,50,75,90   # PNGs to check
     node scripts/render_explainer.cjs                                # output/explainers/error-budget.mp4

   Requires Playwright (Chromium) and ffmpeg. Uses the committed narration; generates no audio.
   The MP4's audio is normalised to -16 LUFS. */
'use strict';
const fs=require('fs'),path=require('path'),http=require('http'),{spawnSync}=require('child_process');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..');
const args=process.argv.slice(2);
function opt(name,fallback){const i=args.indexOf('--'+name);return i<0?fallback:args[i+1]}
const NAME=opt('name','error-budget'),FPS=Number(opt('fps',30)),WORKERS=Number(opt('workers',4)),W=1920,H=1080;
const SRC=path.join(ROOT,'explainers',NAME),OUT=path.resolve(ROOT,opt('out','output/explainers')),STILLS=opt('stills',null);
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.mp3':'audio/mpeg','.png':'image/png'};
function serve(){
 return new Promise(resolve=>{
  const server=http.createServer((req,res)=>{
   let file=path.join(SRC,decodeURIComponent(req.url.split('?')[0]));
   if(!file.startsWith(SRC)){res.writeHead(403);res.end();return}
   if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
   if(!fs.existsSync(file)){res.writeHead(404);res.end();return}
   res.writeHead(200,{'Content-Type':TYPES[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);
  });
  server.listen(0,'127.0.0.1',()=>resolve(server));
 });
}
async function open(browser,base){
 const page=await browser.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
 page.on('pageerror',e=>{console.error('Page error:',e.message);process.exitCode=1});
 await page.goto(base+'/?capture=1');
 await page.waitForFunction(()=>window.__explainer);
 await page.evaluate(()=>window.__explainer.ready);
 return page;
}
(async()=>{
 if(!fs.existsSync(path.join(SRC,'index.html')))throw Error('No explainer at '+SRC);
 fs.mkdirSync(OUT,{recursive:true});
 const server=await serve(),base='http://127.0.0.1:'+server.address().port,browsers=[await chromium.launch()];
 try{
  const first=await open(browsers[0],base);
  if(STILLS){
   const dir=path.join(OUT,NAME+'-stills');fs.mkdirSync(dir,{recursive:true});
   for(const t of STILLS.split(',').map(Number)){
    await first.evaluate(x=>window.__explainer.render(x),t);
    const file=path.join(dir,t.toFixed(2).padStart(6,'0')+'.png');await first.screenshot({path:file});console.log(file);
   }
   return;
  }
  const info=await first.evaluate(()=>({total:window.__explainer.total,audio:window.__explainer.audio}));
  const frames=Math.ceil(info.total*FPS),dir=path.join(OUT,NAME+'-frames');
  fs.mkdirSync(dir,{recursive:true});
  // One browser per worker: screenshots inside a single browser run one at a time.
  const pages=[first];
  while(pages.length<WORKERS){const b=await chromium.launch();browsers.push(b);pages.push(await open(b,base))}
  let next=0,done=0;const started=Date.now();
  await Promise.all(pages.map(async page=>{
   for(;;){const n=next++;if(n>=frames)return;
    await page.evaluate(x=>window.__explainer.render(x),n/FPS);
    await page.screenshot({path:path.join(dir,String(n).padStart(5,'0')+'.png')});
    if(++done%300===0)console.log(done+' / '+frames+' frames, '+((Date.now()-started)/1000).toFixed(0)+' s');
   }
  }));
  const mp4=path.join(OUT,NAME+'.mp4');
  const run=spawnSync('ffmpeg',['-nostdin','-y','-v','error','-framerate',String(FPS),'-start_number','0','-i',path.join(dir,'%05d.png'),'-i',path.join(SRC,info.audio),
   '-map','0:v','-map','1:a','-frames:v',String(frames),'-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r',String(FPS),
   '-c:a','aac','-b:a','192k','-ar','48000','-af','loudnorm=I=-16:TP=-1.5:LRA=11,apad','-t',info.total.toFixed(3),'-movflags','+faststart',mp4],{stdio:'inherit'});
  if(run.status!==0)throw Error('ffmpeg failed');
  console.log(mp4+' ('+(fs.statSync(mp4).size/1e6).toFixed(1)+' MB, '+info.total.toFixed(1)+' s). Frames are in '+dir+'; delete them when done.');
 }finally{await Promise.all(browsers.map(b=>b.close()));server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
