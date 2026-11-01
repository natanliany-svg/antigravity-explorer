import subprocess, json, os

with open(r'C:\Users\natan\Desktop\antigravity-explorer\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

diag = """
<script>
window.addEventListener('load', () => {
  const wide = [];
  document.querySelectorAll('*').forEach(el => {
    const rect = el.getBoundingClientRect();
    if(rect.width > 375.5 || rect.right > 375.5 || rect.left < -0.5) {
      if(el.id !== '__DIAG_RESULT__') {
        wide.push({tag: el.tagName, id: el.id, cls: (el.className || '').toString().slice(0,35), w: Math.round(rect.width), l: Math.round(rect.left), r: Math.round(rect.right)});
      }
    }
  });
  const fs = document.createElement('div');
  fs.id = '__DIAG_RESULT__';
  fs.textContent = JSON.stringify(wide);
  document.body.appendChild(fs);
});
</script>
"""

test_html = r'C:\Users\natan\Desktop\antigravity-explorer\test_diag.html'
with open(test_html, 'w', encoding='utf-8') as f:
    f.write(content.replace('</body>', diag + '</body>'))

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [chrome, '--headless=new', '--dump-dom', '--virtual-time-budget=3000', '--window-size=375,812', f'file:///{test_html}']
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

found = False
for line in res.stdout.splitlines():
    if '__DIAG_RESULT__' in line:
        idx = line.find('__DIAG_RESULT__">')
        if idx != -1:
            raw = line[idx+17:].split('</div>')[0]
            try:
                data = json.loads(raw)
                print(f"Total offending elements: {len(data)}")
                for d in data:
                    print(d)
                found = True
            except Exception as e:
                print("Parse error:", e)
if not found:
    print("Could not find diagnostic element")
