# -*- coding: utf-8 -*-
"""手工构建 APK：aapt2 + javac + d8 + zipalign + apksigner（无需 Gradle）"""
import os, subprocess, shutil, sys, zipfile

SDK = r'C:\Users\zzy\AppData\Local\Temp\android-sdk'
JDK = os.path.join(SDK, 'jdk', 'jdk-17.0.2')
BT = os.path.join(SDK, 'android-14')
PLATFORM = os.path.join(SDK, 'android-13', 'android.jar')
PROJ = r'C:\Users\zzy\AppData\Local\Temp\apkbuild'
BUILD = os.path.join(PROJ, 'build')
ASSETS = sys.argv[1] if len(sys.argv) > 1 else 'assets'
OUT_APK = sys.argv[2] if len(sys.argv) > 2 else r'C:\Users\zzy\AppData\Local\Temp\公路.apk'

ENV = dict(os.environ)
ENV['JAVA_HOME'] = JDK
ENV['PATH'] = os.path.join(JDK, 'bin') + os.pathsep + BT + os.pathsep + ENV['PATH']

def run(args, cwd=PROJ):
    print('>>', ' '.join(args[:3]), '...')
    p = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if p.stdout.strip():
        print(p.stdout.strip()[-1500:])
    if p.returncode != 0:
        print('STDERR:', p.stderr.strip()[-3000:])
        raise SystemExit('FAILED: ' + ' '.join(args[:3]))
    return p

if os.path.exists(BUILD):
    shutil.rmtree(BUILD)
os.makedirs(BUILD)

# 1. 编译资源
run([os.path.join(BT, 'aapt2.exe'), 'compile', '--dir', 'res', '-o',
     os.path.join(BUILD, 'res.zip')])

# 2. 链接资源 + 打包 assets
run([os.path.join(BT, 'aapt2.exe'), 'link',
     '-o', os.path.join(BUILD, 'base.apk'),
     '-I', PLATFORM,
     '--manifest', 'AndroidManifest.xml',
     '-R', os.path.join(BUILD, 'res.zip'),
     '--java', os.path.join(BUILD, 'gen'),
     '--min-sdk-version', '23',
     '--target-sdk-version', '34',
     '-A', ASSETS,
     '--auto-add-overlay'])

# 3. 编译 Java
src_files = []
for r, _, fs in os.walk(os.path.join(PROJ, 'src')):
    src_files += [os.path.join(r, f) for f in fs if f.endswith('.java')]
gen_files = []
for r, _, fs in os.walk(os.path.join(BUILD, 'gen')):
    gen_files += [os.path.join(r, f) for f in fs if f.endswith('.java')]
classes_dir = os.path.join(BUILD, 'classes')
os.makedirs(classes_dir)
run([os.path.join(JDK, 'bin', 'javac.exe'), '-encoding', 'UTF-8',
     '-source', '8', '-target', '8', '-nowarn',
     '-bootclasspath', PLATFORM, '-classpath', PLATFORM,
     '-d', classes_dir] + src_files + gen_files)

# 4. dex
class_files = []
for r, _, fs in os.walk(classes_dir):
    class_files += [os.path.join(r, f) for f in fs if f.endswith('.class')]
dex_out = os.path.join(BUILD, 'dex')
os.makedirs(dex_out)
run([os.path.join(BT, 'd8.bat'), '--release', '--min-api', '23',
     '--lib', PLATFORM, '--output', dex_out] + class_files)

# 5. 把 classes.dex 追加进 apk
with zipfile.ZipFile(os.path.join(BUILD, 'base.apk'), 'a', zipfile.ZIP_DEFLATED) as z:
    if 'classes.dex' in z.namelist():
        raise SystemExit('classes.dex 已存在')
    z.write(os.path.join(dex_out, 'classes.dex'), 'classes.dex')

# 6. 对齐
run([os.path.join(BT, 'zipalign.exe'), '-f', '-p', '4',
     os.path.join(BUILD, 'base.apk'), os.path.join(BUILD, 'aligned.apk')])

# 7. 签名
ks = os.path.join(PROJ, 'kaogong.jks')
if not os.path.exists(ks):
    run([os.path.join(JDK, 'bin', 'keytool.exe'), '-genkeypair', '-keystore', ks,
         '-alias', 'kaogong', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
         '-storepass', 'kaogong', '-keypass', 'kaogong',
         '-dname', 'CN=KaoGong, OU=Personal, O=Personal, L=Beijing, ST=Beijing, C=CN'])

run([os.path.join(BT, 'apksigner.bat'), 'sign',
     '--ks', ks, '--ks-key-alias', 'kaogong',
     '--ks-pass', 'pass:kaogong', '--key-pass', 'pass:kaogong',
     '--out', OUT_APK, os.path.join(BUILD, 'aligned.apk')])

run([os.path.join(BT, 'apksigner.bat'), 'verify', '--print-certs', OUT_APK])
print('\nAPK:', OUT_APK, '%.1f MB' % (os.path.getsize(OUT_APK) / 1024 / 1024))
