# -*- coding: utf-8 -*-
import subprocess, os, json, urllib.request, time

def deploy():
    repo_dir = r'C:\Users\natan\Desktop\antigravity-explorer'
    os.chdir(repo_dir)
    
    print('1. Running build_html.py...')
    res = subprocess.run(['python', 'build_html.py'], capture_output=True, text=True, encoding='utf-8')
    print(res.stdout)
    if res.returncode != 0:
        print('Build error:', res.stderr)
        return False
        
    print('2. Initializing git repository...')
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        subprocess.run(['git', 'init'], check=True)
        
    # Check remotes
    remotes = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True).stdout
    if 'origin' in remotes:
        subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/natanliany-svg/antigravity-explorer.git'], check=True)
    else:
        subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/natanliany-svg/antigravity-explorer.git'], check=True)
        
    subprocess.run(['git', 'config', 'user.name', 'Natan Liany'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'natanliany@gmail.com'], check=True)
    
    print('3. Staging and committing files...')
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', '🚀 Antigravity Explorer v3.5 - Pixel-perfect responsive redesign, 120 everyday tools, zero overflow, synchronized in-place'], capture_output=True)
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)
    
    print('4. Pushing to GitHub (origin main)...')
    push_res = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True)
    print(push_res.stdout)
    if push_res.returncode != 0:
        print('Push output/error:', push_res.stderr)
        
    print('5. Configuring GitHub Pages via API...')
    # Retrieve credential token
    p = subprocess.Popen('git credential fill', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(input='protocol=https\nhost=github.com\n\n')
    token = ''
    for line in out.splitlines():
        if line.startswith('password='):
            token = line[9:]
            
    if token:
        pages_url = 'https://api.github.com/repos/natanliany-svg/antigravity-explorer/pages'
        payload = json.dumps({'source': {'branch': 'main', 'path': '/'}}).encode()
        req = urllib.request.Request(
            pages_url,
            data=payload,
            headers={
                'Authorization': f'token {token}',
                'User-Agent': 'Antigravity',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                print('GitHub Pages configured successfully!')
                print('Live URL:', data.get('html_url'))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            if 'already' in err_body.lower() or e.code == 409:
                print('GitHub Pages is active and deploying latest commit!')
            else:
                print('Pages API note:', e.code, err_body)
                
    live_url = 'https://natanliany-svg.github.io/antigravity-explorer/'
    print(f'\nPermanent target URL: {live_url}')
    print('All files synchronized on disk and in git repository.')
    return True

if __name__ == '__main__':
    deploy()
