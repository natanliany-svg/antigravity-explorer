import subprocess, os

iframe_html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
</body>
</html>"""

preview_file = r'C:\Users\natan\Desktop\antigravity-explorer\preview_375.html'
with open(preview_file, 'w', encoding='utf-8') as f:
    f.write(iframe_html)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
out_png = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\iphone_375_frame.png'
cmd = [chrome, '--headless=new', f'--screenshot={out_png}', '--window-size=600,950', '--hide-scrollbars', f'file:///{preview_file}']
subprocess.run(cmd, capture_output=True)
print('Saved', out_png, os.path.exists(out_png))
