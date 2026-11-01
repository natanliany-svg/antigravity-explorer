import subprocess, os

# Create HTML with pre-scrolled body
html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
<script>
window.addEventListener('load', () => {
  setTimeout(() => {
    try {
      const ifr = document.getElementById('ifr');
      ifr.contentDocument.getElementById('cardsGrid').scrollIntoView();
    } catch(e){}
  }, 1200);
});
</script>
</body>
</html>"""

with open(r'C:\Users\natan\Desktop\antigravity-explorer\preview_cards_grid.html', 'w', encoding='utf-8') as f:
    f.write(html)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
out = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\iphone_375_cards_view.png'
cmd = [chrome, '--headless=new', f'--screenshot={out}', '--window-size=600,950', '--virtual-time-budget=2500', '--hide-scrollbars', r'file:///C:/Users/natan/Desktop/antigravity-explorer/preview_cards_grid.html']
subprocess.run(cmd, capture_output=True)
print('Saved', out, os.path.exists(out))
