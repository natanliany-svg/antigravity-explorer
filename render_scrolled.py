import subprocess, os, time

def render_scrolled_iphone():
    # 1. Scrolled to cards
    html1 = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html" style="width:375px;height:812px;border:2px solid #00f0ff;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(0,240,255,0.4);"></iframe>
<script>
window.addEventListener('load', () => {
  const ifr = document.getElementById('ifr');
  setTimeout(() => {
    ifr.contentWindow.scrollTo(0, 580);
  }, 1000);
});
</script>
</body>
</html>"""
    with open(r'C:\Users\natan\Desktop\antigravity-explorer\preview_scrolled.html', 'w', encoding='utf-8') as f:
        f.write(html1)
        
    # 2. Modal open
    html2 = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:20px;background:#020510;display:flex;justify-content:center;">
<iframe id="ifr" src="index.html#tool-plan" style="width:375px;height:812px;border:2px solid #ff00ea;border-radius:24px;overflow:hidden;box-shadow:0 0 30px rgba(255,0,234,0.4);"></iframe>
</body>
</html>"""
    with open(r'C:\Users\natan\Desktop\antigravity-explorer\preview_modal.html', 'w', encoding='utf-8') as f:
        f.write(html2)

    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    
    out1 = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\iphone_375_cards.png'
    cmd1 = [chrome, '--headless=new', f'--screenshot={out1}', '--window-size=600,950', '--virtual-time-budget=2000', '--hide-scrollbars', r'file:///C:/Users/natan/Desktop/antigravity-explorer/preview_scrolled.html']
    subprocess.run(cmd1, capture_output=True)
    
    out2 = r'C:\Users\natan\Desktop\antigravity-explorer\screenshots\iphone_375_modal.png'
    cmd2 = [chrome, '--headless=new', f'--screenshot={out2}', '--window-size=600,950', '--virtual-time-budget=2000', '--hide-scrollbars', r'file:///C:/Users/natan/Desktop/antigravity-explorer/preview_modal.html']
    subprocess.run(cmd2, capture_output=True)
    
    print('Generated scrolled and modal previews')

if __name__ == '__main__':
    render_scrolled_iphone()
