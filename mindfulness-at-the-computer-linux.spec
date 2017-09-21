# -*- mode: python -*-

block_cipher = None


a = Analysis(['mindfulness-at-the-computer.py'],
             pathex=['/home/sunyata/PycharmProjects/mindfulness-at-the-computer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

# Adding the user_files directory
user_files_dir_str = "user_files"
a.datas += Tree('./' + user_files_dir_str, prefix=user_files_dir_str, excludes=['*.db'])
# -documentation: https://pythonhosted.org/PyInstaller/advanced-topics.html#the-tree-class

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mindfulness-at-the-computer',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='mindfulness-at-the-computer')
