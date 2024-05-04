# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ytm_oauth.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/prawwtocol/.local/share/virtualenvs/ytm-to-itunes-r8RrihgR/lib/python3.12/site-packages/ytmusicapi/locales/en/LC_MESSAGES/base.mo', 'ytmusicapi/locales/en/LC_MESSAGES')],

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
    name='ytm_oauth',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
