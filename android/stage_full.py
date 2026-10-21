# -*- coding: utf-8 -*-
"""完整版 assets：含题图，中文目录名改为 ASCII 并重写题库中的图片路径"""
import os, shutil, subprocess, glob

PROJ = r'C:\Users\zzy\AppData\Local\Temp\apkbuild'
SRC = r'C:\Users\zzy\Documents\Trae-CN\temp_20261020_02\KaoGongWeb'
SLIM = os.path.join(PROJ, 'assets')
FULL = os.path.join(PROJ, 'assets_full')

if os.path.exists(FULL):
    shutil.rmtree(FULL)
shutil.copytree(SLIM, FULL)

os.makedirs(os.path.join(FULL, 'data', 'img'), exist_ok=True)
pairs = [('题目图', 't'), ('公式图', 'f')]
for cn, en in pairs:
    s = os.path.join(SRC, 'data', 'img', cn)
    d = os.path.join(FULL, 'data', 'img', en)
    r = subprocess.run(['robocopy', s, d, '/E', '/NFL', '/NDL', '/NJH', '/NJS', '/NP'],
                       capture_output=True, text=True)
    print(cn, '->', en, 'rc=', r.returncode)

# 重写题库 JSON 内的图片路径
total = 0
for f in glob.glob(os.path.join(FULL, 'data', 'bank', '*.json')):
    t = open(f, encoding='utf-8').read()
    n = t.count('data/img/')
    if n:
        t = t.replace('data/img/题目图/', 'data/img/t/').replace('data/img/公式图/', 'data/img/f/')
        open(f, 'w', encoding='utf-8').write(t)
        total += n

def size(p):
    return sum(os.path.getsize(os.path.join(r, x)) for r, _, fs in os.walk(p) for x in fs) / 1024 / 1024

print('重写图片路径:', total)
print('图片目录: %.1f MB' % size(os.path.join(FULL, 'data', 'img')))
print('assets_full 总计: %.1f MB' % size(FULL))
