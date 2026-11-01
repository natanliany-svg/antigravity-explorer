# -*- coding: utf-8 -*-
import json, os

bundle_path = r'C:\Users\natan\Desktop\antigravity-explorer\bundle.json'
with open(bundle_path, 'r', encoding='utf-8') as f:
    bundle = json.load(f)

json_str = json.dumps(bundle, ensure_ascii=False)

# Read template parts
with open(r'C:\Users\natan\Desktop\antigravity-explorer\template_head.html', 'r', encoding='utf-8') as f:
    head = f.read()
with open(r'C:\Users\natan\Desktop\antigravity-explorer\template_tail.html', 'r', encoding='utf-8') as f:
    tail = f.read()

full_html = head + '\nconst DATA = ' + json_str + ';\n' + tail

out1 = r'C:\Users\natan\Desktop\antigravity-explorer\index.html'
out2 = r'C:\Users\natan\Desktop\מדריך_הסוכנים_והכלים.html'
out3 = r'C:\Users\natan\.gemini\antigravity\brain\8591114d-99e6-4042-b82e-79a355de8668\antigravity-explorer.html'

for out_path in [out1, out2, out3]:
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f'Wrote {out_path} ({os.path.getsize(out_path)} bytes)')
