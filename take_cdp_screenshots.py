import asyncio, json, urllib.request, subprocess, time, base64, os

msg_id = 0

async def call_cdp(ws, method, params=None):
    global msg_id
    msg_id += 1
    req_id = msg_id
    req = {'id': req_id, 'method': method}
    if params:
        req['params'] = params
    await ws.send(json.dumps(req))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == req_id:
            return resp.get('result', {})

async def capture_viewport(ws_url, out_path, width, height, dsf=1, is_mobile=False):
    import websockets
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        await call_cdp(ws, 'Page.enable')
        await call_cdp(ws, 'DOM.enable')
        
        # Override Device Metrics
        await call_cdp(ws, 'Emulation.setDeviceMetricsOverride', {
            'width': width,
            'height': height,
            'deviceScaleFactor': dsf,
            'mobile': is_mobile
        })
        
        # Navigate
        html_url = 'file:///C:/Users/natan/Desktop/antigravity-explorer/index.html'
        await call_cdp(ws, 'Page.navigate', {'url': html_url})
        
        await asyncio.sleep(2.0)
        
        # Layout metrics
        metrics = await call_cdp(ws, 'Runtime.evaluate', {
            'expression': '''
            ({
                scrollW: document.documentElement.scrollWidth,
                clientW: document.documentElement.clientWidth,
                innerW: window.innerWidth,
                overflows: document.documentElement.scrollWidth > window.innerWidth
            })
            ''',
            'returnByValue': True
        })
        val = metrics.get('result', {}).get('value', {})
        print(f"[{width}x{height}] Layout:", val)
        
        # Screenshot
        shot = await call_cdp(ws, 'Page.captureScreenshot', {'format': 'png'})
        data_b64 = shot.get('data', '')
        if data_b64:
            with open(out_path, 'wb') as f:
                f.write(base64.b64decode(data_b64))
            print(f"Saved {out_path} ({os.path.getsize(out_path)} bytes)")

def run():
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    p = subprocess.Popen([chrome, '--headless=new', '--remote-debugging-port=9222', 'about:blank'])
    time.sleep(1.5)
    
    try:
        req = urllib.request.urlopen('http://127.0.0.1:9222/json/list')
        targets_list = json.loads(req.read().decode())
        ws_url = targets_list[0]['webSocketDebuggerUrl']
        
        os.makedirs(r'C:\Users\natan\Desktop\antigravity-explorer\screenshots', exist_ok=True)
        
        targets = [
            (r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\cdp_mobile_375.png', 375, 812, 2, True),
            (r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\cdp_mobile_414.png', 414, 896, 2, True),
            (r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\cdp_tablet_768.png', 768, 1024, 1, True),
            (r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\cdp_desktop_1440.png', 1440, 900, 1, False),
        ]
        
        for path, w, h, dsf, mob in targets:
            asyncio.run(capture_viewport(ws_url, path, w, h, dsf, mob))
            
    finally:
        p.kill()

if __name__ == '__main__':
    run()
