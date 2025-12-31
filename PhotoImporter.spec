# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['photo_importer.py'],
    pathex=[],
    binaries=[],
    datas=[('app_icon.jpg', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PhotoImporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.jpg'],
)
app = BUNDLE(
    exe,
    name='PhotoImporter.app',
    icon='app_icon.jpg',
    bundle_identifier='com.danielgarcia.photoimporter',
    info_plist={
        'CFBundleShortVersionString': '1.1.0',
        'CFBundleVersion': '1.1.0',
    }
)
