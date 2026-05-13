param(
    [string]$OutputDir = "portable"
)

$ErrorActionPreference = 'Stop'

python -m pip install --upgrade pip pyinstaller certifi
python build_password_ninja_icon.py
& "portable/build-portable-icon.ps1"
pyinstaller --noconfirm --onedir --windowed --name PasswordNinjaPortable --icon assets/password_ninja_portable.ico password_ninja_gui.py

if (Test-Path $OutputDir) {
    Remove-Item $OutputDir -Recurse -Force
}

New-Item -ItemType Directory -Force $OutputDir | Out-Null
Copy-Item -Recurse dist/PasswordNinjaPortable/* $OutputDir/
Compress-Archive -Path "$OutputDir/*" -DestinationPath "PasswordNinja-Portable-Windows.zip" -Force
