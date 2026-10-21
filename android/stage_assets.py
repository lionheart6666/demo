# -*- coding: utf-8 -*-
"""把 KaoGongWeb 复制到 apkbuild/assets，中文题库文件名改为 ASCII 并同步 manifest"""
import os, json, shutil, re

SRC = r'C:\Users\zzy\Documents\Trae-CN\temp_20261020_02\KaoGongWeb'
DST = r'C:\Users\zzy\AppData\Local\Temp\apkbuild\assets'

if os.path.exists(DST):
    shutil.rmtree(DST)
os.makedirs(os.path.join(DST, 'data', 'bank'), exist_ok=True)
os.makedirs(os.path.join(DST, 'vendor'), exist_ok=True)

shutil.copy(os.path.join(SRC, 'index.html'), os.path.join(DST, 'index.html'))
shutil.copy(os.path.join(SRC, 'vendor', 'xlsx.full.min.js'),
            os.path.join(DST, 'vendor', 'xlsx.full.min.js'))

manifest_path = os.path.join(SRC, 'data', 'bank', 'manifest.json')
man = json.load(open(manifest_path, encoding='utf-8'))
name_map = {}
idx = 0

for key, info in man.items():
    fn = info['f']
    new_fn = fn
    if re.search(r'[^\x00-\x7F]', fn):
        idx += 1
        new_fn = 'p%02d.json' % idx
        name_map[fn] = new_fn
    src = os.path.join(SRC, 'data', 'bank', fn)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(DST, 'data', 'bank', new_fn))
        info['f'] = new_fn
    else:
        print('MISSING:', fn)

json.dump(man, open(os.path.join(DST, 'data', 'bank', 'manifest.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'))

# 申论题库（英文名，直接复制）
sl = os.path.join(SRC, 'data', 'bank', 'shenlun.json')
if os.path.exists(sl):
    shutil.copy(sl, os.path.join(DST, 'data', 'bank', 'shenlun.json'))

# 历年真题索引（ASCII 文件名，直接复制）
pp = os.path.join(SRC, 'data', 'bank', 'papers.json')
if os.path.exists(pp):
    shutil.copy(pp, os.path.join(DST, 'data', 'bank', 'papers.json'))
else:
    print('MISSING: papers.json')

print('题图目录不打包（精简版）')
print('重命名文件数:', len(name_map))
print('assets 总大小: %.1f MB' % (sum(
    os.path.getsize(os.path.join(r, f))
    for r, _, fs in os.walk(DST) for f in fs) / 1024 / 1024))
