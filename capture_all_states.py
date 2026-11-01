import subprocess, os, time

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
sc_dir = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots'
os.makedirs(sc_dir, exist_ok=True)

# 1. Cards View (scrolled) Mobile
h_cards_mob = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html#cardsGrid" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;"></iframe>
<script>
window.onload = () => {
    setTimeout(() => {
        try {
            const ifr = document.getElementById('ifr');
            ifr.contentDocument.getElementById('cardsGrid').scrollIntoView();
        }catch(e){}
    }, 1200);
};
</script>
</body></html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\pv_cards_mob.html', 'w', encoding='utf-8') as f:
    f.write(h_cards_mob)

# 2. Modal View Mobile
h_modal_mob = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html#tool-plan" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;"></iframe>
</body></html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\pv_modal_mob.html', 'w', encoding='utf-8') as f:
    f.write(h_modal_mob)

# 3. Wizard Open Mobile
h_wiz_mob = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;"></iframe>
<script>
window.onload = () => {
    setTimeout(() => {
        try {
            const ifr = document.getElementById('ifr');
            ifr.contentDocument.getElementById('btnWizardToggle').click();
            setTimeout(() => {
                ifr.contentDocument.getElementById('wizardPanel').scrollIntoView();
            }, 300);
        }catch(e){}
    }, 1000);
};
</script>
</body></html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\pv_wiz_mob.html', 'w', encoding='utf-8') as f:
    f.write(h_wiz_mob)

# 4. Desktop Scrolled to Cards
h_cards_dt = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#05070f;">
<iframe id="ifr" src="index.html#cardsGrid" style="border:none;width:1440px;height:900px;"></iframe>
<script>
window.onload = () => {
    setTimeout(() => {
        try {
            const ifr = document.getElementById('ifr');
            ifr.contentDocument.getElementById('cardsGrid').scrollIntoView();
        }catch(e){}
    }, 1200);
};
</script>
</body></html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\pv_cards_dt.html', 'w', encoding='utf-8') as f:
    f.write(h_cards_dt)

shots = [
    (r'C:\Users\natan\Desktop\antigravity-explorer\pv_cards_mob.html', os.path.join(sc_dir, 'v4_cards_mob_375.png'), '600,950'),
    (r'C:\Users\natan\Desktop\antigravity-explorer\pv_modal_mob.html', os.path.join(sc_dir, 'v4_modal_mob_375.png'), '600,950'),
    (r'C:\Users\natan\Desktop\antigravity-explorer\pv_wiz_mob.html', os.path.join(sc_dir, 'v4_wiz_mob_375.png'), '600,950'),
    (r'C:\Users\natan\Desktop\antigravity-explorer\pv_cards_dt.html', os.path.join(sc_dir, 'v4_cards_dt_1440.png'), '1440,900'),
]

for html_file, out_png, win_size in shots:
    cmd = [
        chrome, '--headless=new',
        '--allow-file-access-from-files',
        f'--screenshot={out_png}',
        f'--window-size={win_size}',
        '--virtual-time-budget=3000',
        '--hide-scrollbars',
        f'file:///{html_file}'
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Captured {out_png}: exists={os.path.exists(out_png)}")

print("Done capture batch.")
