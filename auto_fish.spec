# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['auto_fish.py'],
    pathex=['.'],
    binaries=[
        ('C:\\Windows\\System32\\libomp140.x86_64.dll', '.'),  # Add libomp140.x86_64.dll
    ],
    datas=[
        ('easyocr_models/*', 'easyocr_models'),  # Include EasyOCR models
    ],
    hiddenimports=[
        'torch',
        'torch._C',
        'torchvision',
        'torchvision.models',
        'torchvision.transforms',
        'torchvision.datasets',
        'PIL._imaging',  # Add Pillow imaging
        'cv2',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Add torch DLLs explicitly
binaries = [
    ('.venv\\Lib\\site-packages\\torch\\lib\\c10.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\caffe2_nvrtc.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\fbgemm.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\nvrtc.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\nvrtc-builtins.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\torch_cuda.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\torch_cpu.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\torch.dll', 'torch\\lib', 'BINARY'),
    ('.venv\\Lib\\site-packages\\torch\\lib\\torch_python.dll', 'torch\\lib', 'BINARY'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='auto_fish',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries + binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='auto_fish'
)
