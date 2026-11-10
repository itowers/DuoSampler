"""Teste de fumaça: abre o app num Chrome sem interface, simula toques e microfone, e falha se houver erro de JS.
Uso: python3 testes/smoke.py [caminho do index.html]"""
import asyncio, sys, os
from playwright.async_api import async_playwright
URL='file://'+os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome'),args=['--no-sandbox','--autoplay-policy=no-user-gesture-required','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
        pg=await b.new_page(viewport={'width':626,'height':890})
        errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' else None)
        await pg.goto(URL); await pg.click('#go')
        async def tap(sel,hold=80):
            bx=await pg.locator(sel).first.bounding_box()
            await pg.mouse.move(bx['x']+bx['width']/2,bx['y']+bx['height']/2); await pg.mouse.down(); await pg.wait_for_timeout(hold); await pg.mouse.up()
        ev=lambda: pg.evaluate("new Promise(ok=>{const r=indexedDB.open('samplerduo',1);r.onsuccess=()=>{const q=r.result.transaction('kv').objectStore('kv').get('proj');q.onsuccess=()=>ok(q.result?q.result.loops.map(l=>l.events.length).join(','):'none')}})")
        out={}
        await tap('#aRec'); await pg.wait_for_timeout(500)
        out['contagem']=await pg.inner_text('#aRec')
        await tap('#p0'); await pg.wait_for_timeout(2400)   # durante a contagem: não grava
        for s in ['#p0','#p1','#p4','#p12']: await tap(s); await pg.wait_for_timeout(160)
        for t in ['SEQ','SAMPLE','SOUND','FX','MIX','CFG','LOOPS']:  # modo DRUM: SOUND é a aba KIT
            await pg.click(f'#tabs [data-t={t}]'); await pg.wait_for_timeout(100)
            if t=='SEQ': await pg.click('#st3'); await pg.click('#st5'); await pg.click('#st5'); await pg.click('[data-act=pgnext]')
            if t=='SOUND':
                for k in range(12): await pg.locator('#kgrid .b').nth(k).click()
            if t=='SOUND_SYNTH':
                for c in range(6):
                    await pg.click(f'#ct{c}'); 
                    for k in range(8): await pg.locator('#pgrid .b').nth(k).click()
                for a in ['adiv','aord','arng']: await pg.click(f'[data-act={a}]')
            if t in('FX','MIX'):
                n=await pg.locator('#view .bar').count()
                for k in range(n):
                    bx=await pg.locator('#view .bar').nth(k).bounding_box(); await pg.mouse.click(bx['x']+bx['width']*0.6,bx['y']+bx['height']/2)
        await tap('#modes [data-m=KEYS]'); await tap('#pads .pad >> nth=5',200)
        out['abas_keys']=await pg.inner_text('#tabs')
        await pg.click('#tabs [data-t=SOUND]')
        for c in range(6):
            await pg.click(f'#ct{c}')
            for k in range(8): await pg.locator('#pgrid .b').nth(k).click()
        for a in ['adiv','aord','arng']: await pg.click(f'[data-act={a}]')
        await pg.click('#tabs [data-t=SEQ]'); await pg.click('#st8')
        await tap('#modes [data-m=CHORD]'); await tap('#pads .pad >> nth=6',300); await pg.click('#st10')
        bx=await pg.locator('#xy').bounding_box(); await pg.mouse.click(bx['x']+bx['width']*0.5,bx['y']+bx['height']*0.1)
        await tap('#fArp'); await tap('#pads .pad >> nth=1',700); await tap('#fArp'); await tap('#fStr'); await tap('#pads .pad >> nth=4',300); await tap('#pads .pad >> nth=0',200)
        out['acorde7']=await pg.locator('#pads .pad').nth(1).inner_text()
        await tap('#lp1'); await tap('#pads .pad >> nth=2',300)
        await tap('#modes [data-m=FX]')
        for k in range(16): await tap(f'#pads .pad >> nth={k}',260)
        await pg.wait_for_timeout(1200); out['eventos']=await ev()
        await tap('#aUndo'); await tap('#aRedo'); await pg.click('#tabs [data-t=LOOPS]'); await pg.click('[data-act=ldub][data-i="0"]'); await tap('#lp1'); await pg.wait_for_timeout(1200)
        await tap('#modes [data-m=DRUM]'); await pg.click('#tabs [data-t=SAMPLE]')
        await tap('#p15'); await pg.click('[data-act=mic]'); await pg.wait_for_timeout(1500); await pg.click('[data-act=mic]'); await pg.wait_for_timeout(300)
        for a in ['rev','gate','trim','chopa','chop']: await pg.click(f'[data-act={a}]'); await pg.wait_for_timeout(60)
        await tap('#p15',200); out['sample']=await pg.inner_text('#smInfo')
        await pg.screenshot(path='/tmp/s1.png')
        await pg.wait_for_timeout(1200); await pg.reload(); await pg.click('#go'); await pg.wait_for_timeout(500)
        out['apos_recarregar']=await ev(); out['sample_persistido']=await pg.evaluate("document.querySelectorAll('#pads .pad.smp').length")
        await pg.click('#tabs [data-t=CFG]'); await pg.click('[data-act=cal]'); await pg.wait_for_timeout(2700)
        for k in range(8): await tap('#calB',30); await pg.wait_for_timeout(470)
        await pg.wait_for_timeout(1500); out['latencia']=await pg.inner_text('#cfgInfo')
        await pg.click('[data-act=novo]'); await pg.click('[data-act=novo]'); await pg.click('[data-act=bpml]')
        await tap('#aRec'); await tap('#p0'); await pg.wait_for_timeout(480); await tap('#p1'); await pg.wait_for_timeout(480); await tap('#p0'); await pg.wait_for_timeout(480); await tap('#p1'); await pg.wait_for_timeout(400); await tap('#aRec')
        await pg.wait_for_timeout(1200); out['bpm_loop']=await pg.inner_text('#cBpm'); out['bpm_loop_eventos']=await ev()
        await tap('#modes [data-m=CHORD]'); await pg.click('#tabs [data-t=SEQ]'); await pg.screenshot(path='/tmp/s2.png'); await tap('#modes [data-m=DRUM]'); await pg.click('#tabs [data-t=SOUND]'); await pg.screenshot(path='/tmp/s5.png')
        await pg.set_viewport_size({'width':390,'height':780}); await pg.wait_for_timeout(200); await pg.click('#tabs [data-t=LOOPS]'); await pg.screenshot(path='/tmp/s3.png')
        await pg.click('#tabs [data-t=FX]'); await pg.screenshot(path='/tmp/s4.png')
        for k,v in out.items(): print(k,'=',repr(v))
        print('ERROS',errs); await b.close(); sys.exit(1 if errs else 0)
asyncio.run(main())
