# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['src/gui.py'],
    pathex=['.'],
    binaries=[
        ("src/meety/static/icons/*.png", "meety/static/icons"),
    ],
    datas=[
        ("src/meety/static/config/*.yaml", "meety/static/config"),
        ("src/meety/gui/static/*.css", "meety/gui/static"),
    ],
    hiddenimports=['colorama'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(
    a.pure,
	a.zipped_data,
    cipher=block_cipher
)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="meety",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False
)
coll = COLLECT(
    exe,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='meety',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)
