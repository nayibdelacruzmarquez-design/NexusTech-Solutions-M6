# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Definir archivos de recursos estáticos que deben incluirse en el build
# Formato: (Ruta_Origen, Ruta_Destino_En_Exe)
added_files = [
    ('resources', 'resources'),
    ('pyscript', 'pyscript'),
    ('docs', 'docs'),
]

a = Analysis(
    ['src/main.py'],  # Punto de entrada correcto dentro de src/
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'sqlite3',
        'src.core.signals',
        'src.data.database',
        'src.data.api_client',
        'src.utils.threads',
        'src.utils.resource_path',
        'src.gui.main_window',
        'src.gui.widgets.custom_charts',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NexusTech_Solutions',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para que sea una app de ventana GUI sin consola negra de fondo
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='resources/icons/app_icon.ico', # Descomenta si tienes un icono .ico
)