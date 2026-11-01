import subprocess, os, time

script = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#05070f;">
<iframe id="ifr" src="index.html" style="border:none;width:1440px;height:900px;"></iframe>
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const ifr = document.getElementById('ifr');
        ifr.contentDocument.querySelector('.toolbar').scrollIntoView();
    }, 1000);
});
</script>
</body>
</html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\preview_toolbar_desktop.html', 'w', encoding='utf-8') as f:
    f.write(script)

script_mob = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;"></iframe>
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const ifr = document.getElementById('ifr');
        ifr.contentDocument.querySelector('.toolbar').scrollIntoView();
    }, 1200);
});
</script>
</body>
</html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\preview_toolbar_mobile.html', 'w', encoding='utf-8') as f:
    f.write(script_mob)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
out1 = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\toolbar_cards_desktop.png'
out2 = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\toolbar_cards_mobile.png'

subprocess.run([chrome, '--headless=new', f'--screenshot={out1}', '--window-size=1440,900', '--virtual-time-budget=2500', '--hide-scrollbars', r'file:///C:/Users/natan/Desktop/antigravity-explorer/preview_toolbar_desktop.html'])
subprocess.run([chrome, '--headless=new', f'--screenshot={out2}', '--window-size=600,950', '--virtual-time-budget=2500', '--hide-scrollbars', r'file:///C:/Users/natan/Desktop/antigravity-explorer/preview_toolbar_mobile.html'])

print('Screenshots generated.')
