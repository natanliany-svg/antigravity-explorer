import subprocess, json, os, html

script_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#000;">
<iframe id="ifr" src="index.html" style="border:none;margin:0;padding:0;display:block;width:{W}px;height:{H}px;"></iframe>
<div id="output"></div>
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const ifr = document.getElementById('ifr');
        const doc = ifr.contentDocument;
        const scrollW = doc.documentElement.scrollWidth;
        const clientW = doc.documentElement.clientWidth;
        const bodyW = doc.body.scrollWidth;
        const overflowing = [];
        
        doc.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.right > {W} + 1 || r.left < -1) {
                overflowing.push({
                    tag: el.tagName,
                    id: el.id,
                    cls: (el.className || '').toString().slice(0, 35),
                    w: Math.round(r.width),
                    l: Math.round(r.left),
                    r: Math.round(r.right),
                    txt: (el.innerText || '').slice(0, 25).trim().replace(/[\\n\\r]+/g, ' ')
                });
            }
        });
        
        const res = {
            width: {W},
            height: {H},
            scrollW: scrollW,
            clientW: clientW,
            bodyW: bodyW,
            overflowCount: overflowing.length,
            overflowing: overflowing.slice(0, 15)
        };
        const prefix = '___DATA' + '_PAYLOAD___';
        const suffix = '___END' + '_PAYLOAD___';
        document.getElementById('output').textContent = prefix + JSON.stringify(res) + suffix;
    }, 1500);
});
</script>
</body>
</html>"""

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
harness_file = r'C:\Users\natan\Desktop\antigravity-explorer\harness_single.html'

for w, h in [(320, 568), (360, 640), (375, 812), (414, 896), (768, 1024), (1024, 768), (1440, 900)]:
    with open(harness_file, 'w', encoding='utf-8') as f:
        f.write(script_template.replace('{W}', str(w)).replace('{H}', str(h)))
    
    cmd = [chrome, '--headless=new', '--dump-dom', '--virtual-time-budget=3500', '--window-size=1600,1200', f'file:///{harness_file}']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    found = False
    for line in res.stdout.splitlines():
        if '___DATA_PAYLOAD___' in line and '<script>' not in line:
            raw = line.split('___DATA_PAYLOAD___')[1].split('___END_PAYLOAD___')[0]
            raw = html.unescape(raw)
            try:
                data = json.loads(raw)
                print(f"Viewport {w}x{h}: scrollW={data['scrollW']}, bodyW={data['bodyW']}, overflows={data['overflowCount']}")
                if data['overflowCount'] > 0:
                    print("  Sample overflowing elements:")
                    for o in data['overflowing']:
                        print(f"    - <{o['tag']} id='{o['id']}' class='{o['cls']}'> w={o['w']} l={o['l']} r={o['r']} text='{o['txt']}'")
                found = True
                break
            except Exception as e:
                print(f"Viewport {w}x{h}: parse error: {e}, raw was: {raw[:100]}")
    if not found:
        print(f"Viewport {w}x{h}: NO RESULT")
