# -*- coding: utf-8 -*-
import subprocess, os, json, time

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
sc_dir = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots'
os.makedirs(sc_dir, exist_ok=True)

test_cases = [
    # (name, width, height, html_snippet)
    (
        "final_mobile_375_top.png",
        600, 950,
        """<!DOCTYPE html><html><body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
        <iframe id="ifr" src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
        </body></html>"""
    ),
    (
        "final_mobile_375_cards.png",
        600, 950,
        """<!DOCTYPE html><html><body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
        <iframe id="ifr" src="index.html#cardsGrid" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
        <script>
        window.onload = () => {
            setTimeout(() => {
                try {
                    const ifr = document.getElementById('ifr');
                    ifr.contentDocument.getElementById('cardsGrid').scrollIntoView();
                }catch(e){}
            }, 1200);
        };
        </script></body></html>"""
    ),
    (
        "final_mobile_375_modal.png",
        600, 950,
        """<!DOCTYPE html><html><body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
        <iframe id="ifr" src="index.html#tool-plan" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
        </body></html>"""
    ),
    (
        "final_mobile_375_wizard.png",
        600, 950,
        """<!DOCTYPE html><html><body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
        <iframe id="ifr" src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
        <script>
        window.onload = () => {
            setTimeout(() => {
                try {
                    const ifr = document.getElementById('ifr');
                    ifr.contentDocument.getElementById('btnWizardToggle').click();
                    setTimeout(() => {
                        ifr.contentDocument.getElementById('wizardPanel').scrollIntoView();
                    }, 400);
                }catch(e){}
            }, 1000);
        };
        </script></body></html>"""
    ),
    (
        "final_tablet_768_top.png",
        950, 1150,
        """<!DOCTYPE html><html><body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
        <iframe id="ifr" src="index.html" style="width:768px;height:1024px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
        </body></html>"""
    ),
    (
        "final_desktop_1440_top.png",
        1440, 900,
        """<!DOCTYPE html><html><body style="margin:0;padding:0;background:#05070f;">
        <iframe id="ifr" src="index.html" style="border:none;width:1440px;height:900px;"></iframe>
        </body></html>"""
    ),
    (
        "final_desktop_1440_cards.png",
        1440, 900,
        """<!DOCTYPE html><html><body style="margin:0;padding:0;background:#05070f;">
        <iframe id="ifr" src="index.html" style="border:none;width:1440px;height:900px;"></iframe>
        <script>
        window.onload = () => {
            setTimeout(() => {
                try {
                    const ifr = document.getElementById('ifr');
                    ifr.contentDocument.getElementById('cardsGrid').scrollIntoView();
                }catch(e){}
            }, 1200);
        };
        </script></body></html>"""
    )
]

for filename, win_w, win_h, html_src in test_cases:
    tmp_path = r'C:\Users\natan\Desktop\antigravity-explorer\tmp_render.html'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(html_src)
    
    out_img = os.path.join(sc_dir, filename)
    cmd = [
        chrome, '--headless=new',
        '--allow-file-access-from-files',
        f'--screenshot={out_img}',
        f'--window-size={win_w},{win_h}',
        '--virtual-time-budget=3000',
        '--hide-scrollbars',
        f'file:///{tmp_path}'
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Generated {filename}: {os.path.exists(out_img)} ({os.path.getsize(out_img)} bytes)")

print("\n--- Testing Exact Layout Metrics (Overflow check) ---")
metric_script = """<!DOCTYPE html><html><body>
<iframe id="ifr" src="index.html" style="border:none;"></iframe>
<div id="res"></div>
<script>
async function test() {
    const ifr = document.getElementById('ifr');
    const out = {};
    for (const w of [320, 375, 414, 768, 1024, 1440]) {
        ifr.style.width = w + 'px';
        ifr.style.height = '800px';
        await new Promise(r => setTimeout(r, 400));
        const doc = ifr.contentDocument;
        const scrollW = doc.documentElement.scrollWidth;
        const clientW = doc.documentElement.clientWidth;
        const bad = [];
        doc.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > w + 1 || rect.left < -1) {
                bad.push({tag: el.tagName, cls: el.className, w: rect.width, r: rect.right});
            }
        });
        out[w] = {scrollW: scrollW, clientW: clientW, overflows: scrollW > w, badCount: bad.length};
    }
    document.getElementById('res').textContent = 'PAYLOAD_START' + JSON.stringify(out) + 'PAYLOAD_END';
}
window.onload = () => setTimeout(test, 500);
</script></body></html>"""

m_path = r'C:\Users\natan\Desktop\antigravity-explorer\tmp_metric.html'
with open(m_path, 'w', encoding='utf-8') as f:
    f.write(metric_script)

cmd = [chrome, '--headless=new', '--allow-file-access-from-files', '--dump-dom', '--virtual-time-budget=6000', '--window-size=1600,1200', f'file:///{m_path}']
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
for line in res.stdout.splitlines():
    if 'PAYLOAD_START' in line and '<script>' not in line:
        import html
        raw = html.unescape(line.split('PAYLOAD_START')[1].split('PAYLOAD_END')[0])
        try:
            print("Layout metrics across resolutions:", json.dumps(json.loads(raw), indent=2))
        except Exception as e:
            print("Error parsing metrics:", e, raw[:100])
        break
