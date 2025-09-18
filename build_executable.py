#!/usr/bin/env python3
"""
Executable Builder for Vedic Astrology Calculator
Creates standalone executables using PyInstaller for multiple platforms
"""

import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict

class ExecutableBuilder:
    def __init__(self):
        self.platform_info = {
            'os': platform.system().lower(),
            'arch': platform.machine().lower(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}"
        }
        self.build_dir = Path('dist')
        self.work_dir = Path('build')
        
    def install_pyinstaller(self) -> bool:
        """Install PyInstaller if not available"""
        try:
            import PyInstaller
            return True
        except ImportError:
            print("📦 Installing PyInstaller...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install PyInstaller")
                return False
    
    def create_pyinstaller_spec(self) -> Path:
        """Create PyInstaller spec file for the application"""
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Application information
app_name = 'VedicAstrologyCalculator'
main_script = 'main.py'

# Platform-specific configurations
if sys.platform.startswith('win'):
    icon_file = 'assets/icon.ico' if Path('assets/icon.ico').exists() else None
    exe_extension = '.exe'
elif sys.platform == 'darwin':
    icon_file = 'assets/icon.icns' if Path('assets/icon.icns').exists() else None
    exe_extension = ''
else:  # Linux and other Unix-like
    icon_file = 'assets/icon.png' if Path('assets/icon.png').exists() else None
    exe_extension = ''

# Data files to include
datas = [
    ('static', 'static'),
    ('ephe', 'ephe'),
]

# Hidden imports for dynamic imports
hiddenimports = [
    'uvicorn',
    'fastapi',
    'pydantic',
    'swisseph',
    'pytz',
    'bcrypt',
    'sqlite3',
    'json',
    'datetime',
    'urllib.request',
    'urllib.parse',
    'urllib.error',
]

# Binaries and libraries
binaries = []

# Excluded modules to reduce size
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
    'jupyter',
    'IPython',
    'sphinx',
    'pytest',
    'setuptools',
]

a = Analysis(
    [main_script],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name + exe_extension,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)

# macOS App Bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=app_name + '.app',
        icon=icon_file,
        bundle_identifier='com.vedicastrology.calculator',
        version='1.0.0',
        info_plist={
            'CFBundleDisplayName': 'Vedic Astrology Calculator',
            'CFBundleGetInfoString': 'Vedic Astrology Calculator v1.0.0',
            'CFBundleIdentifier': 'com.vedicastrology.calculator',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
        },
    )
'''
        
        spec_file = Path('vedic_astrology.spec')
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        return spec_file
    
    def build_executable(self) -> bool:
        """Build the executable using PyInstaller"""
        if not self.install_pyinstaller():
            return False
        
        print("🔨 Building executable...")
        
        # Clean previous builds
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)
        
        # Create PyInstaller spec
        spec_file = self.create_pyinstaller_spec()
        
        # Build executable
        try:
            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--clean',
                '--noconfirm',
                str(spec_file)
            ]
            
            # Platform-specific optimizations
            if self.platform_info['os'] == 'windows':
                # Windows-specific options
                cmd.extend(['--win-private-assemblies'])
            elif self.platform_info['os'] == 'darwin':
                # macOS-specific options
                cmd.extend(['--windowed'])
            
            subprocess.run(cmd, check=True)
            
            print("✅ Executable built successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build executable: {e}")
            return False
    
    def create_installer(self) -> bool:
        """Create platform-specific installer"""
        if self.platform_info['os'] == 'windows':
            return self._create_windows_installer()
        elif self.platform_info['os'] == 'darwin':
            return self._create_macos_installer()
        else:
            return self._create_linux_package()
    
    def _create_windows_installer(self) -> bool:
        """Create Windows MSI installer using WiX or NSIS"""
        print("📦 Creating Windows installer...")
        
        # Check if NSIS is available
        nsis_path = shutil.which('makensis')
        if not nsis_path:
            print("⚠️  NSIS not found, skipping installer creation")
            print("   Install NSIS from https://nsis.sourceforge.io/")
            return False
        
        # Create NSIS script
        nsis_script = self._create_nsis_script()
        
        try:
            subprocess.run([nsis_path, str(nsis_script)], check=True)
            print("✅ Windows installer created!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to create Windows installer")
            return False
    
    def _create_macos_installer(self) -> bool:
        """Create macOS DMG installer"""
        print("📦 Creating macOS DMG installer...")
        
        app_path = self.build_dir / 'VedicAstrologyCalculator.app'
        dmg_path = self.build_dir / 'VedicAstrologyCalculator.dmg'
        
        if not app_path.exists():
            print("❌ App bundle not found")
            return False
        
        try:
            # Create DMG
            cmd = [
                'hdiutil', 'create',
                '-srcfolder', str(app_path),
                '-format', 'UDZO',
                '-fs', 'HFS+',
                '-volname', 'Vedic Astrology Calculator',
                str(dmg_path)
            ]
            
            subprocess.run(cmd, check=True)
            print("✅ macOS DMG created!")
            return True
            
        except subprocess.CalledProcessError:
            print("❌ Failed to create DMG")
            return False
    
    def _create_linux_package(self) -> bool:
        """Create Linux packages (AppImage, DEB, RPM)"""
        print("📦 Creating Linux packages...")
        
        # Create AppImage
        if self._create_appimage():
            print("✅ AppImage created!")
        
        # Create DEB package
        if self._create_deb_package():
            print("✅ DEB package created!")
        
        return True
    
    def _create_appimage(self) -> bool:
        """Create AppImage for Linux"""
        try:
            # This is a simplified version - full AppImage creation is complex
            print("📦 AppImage creation requires appimagetool")
            print("   Download from https://github.com/AppImage/AppImageKit")
            return False
        except Exception:
            return False
    
    def _create_deb_package(self) -> bool:
        """Create DEB package for Debian/Ubuntu"""
        try:
            # This would require creating debian/ directory structure
            print("📦 DEB package creation requires debian packaging tools")
            return False
        except Exception:
            return False
    
    def _create_nsis_script(self) -> Path:
        """Create NSIS installer script for Windows"""
        nsis_content = '''!define APPNAME "Vedic Astrology Calculator"
!define COMPANYNAME "Vedic Astrology"
!define DESCRIPTION "Professional Vedic Astrology Calculator"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

RequestExecutionLevel admin

InstallDir "$PROGRAMFILES\\${COMPANYNAME}\\${APPNAME}"

Name "${APPNAME}"
OutFile "VedicAstrologyCalculator-Setup.exe"

Page directory
Page instfiles

Section "install"
    SetOutPath $INSTDIR
    File /r "dist\\VedicAstrologyCalculator\\*.*"
    
    # Create uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    # Start Menu
    CreateDirectory "$SMPROGRAMS\\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\VedicAstrologyCalculator.exe"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    # Desktop shortcut
    CreateShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\VedicAstrologyCalculator.exe"
    
    # Registry
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$INSTDIR\\VedicAstrologyCalculator.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
SectionEnd

Section "uninstall"
    Delete "$INSTDIR\\*.*"
    RMDir /r "$INSTDIR"
    
    Delete "$SMPROGRAMS\\${COMPANYNAME}\\*.*"
    RMDir "$SMPROGRAMS\\${COMPANYNAME}"
    
    Delete "$DESKTOP\\${APPNAME}.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"
SectionEnd
'''
        
        nsis_file = Path('installer.nsi')
        with open(nsis_file, 'w') as f:
            f.write(nsis_content)
        
        return nsis_file
    
    def create_startup_executable(self) -> bool:
        """Create a simple startup executable that launches the web server"""
        startup_content = '''#!/usr/bin/env python3
"""
Startup launcher for Vedic Astrology Calculator
Launches the FastAPI server and opens browser
"""

import sys
import os
import time
import threading
import webbrowser
import subprocess
from pathlib import Path

def launch_server():
    """Launch the FastAPI server"""
    try:
        # Change to application directory
        app_dir = Path(__file__).parent
        os.chdir(app_dir)
        
        # Launch uvicorn server
        cmd = [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '5000']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return process
    except Exception as e:
        print(f"Failed to launch server: {e}")
        return None

def open_browser():
    """Open web browser after server starts"""
    time.sleep(3)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

def main():
    print("🕉️  Starting Vedic Astrology Calculator...")
    
    # Launch server in background
    server_process = launch_server()
    if not server_process:
        input("Press Enter to exit...")
        return
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("✅ Server started at http://localhost:5000")
    print("🌐 Opening web browser...")
    print("\\n💡 Press Ctrl+C to stop the server")
    
    try:
        # Wait for server process
        server_process.wait()
    except KeyboardInterrupt:
        print("\\n🛑 Stopping server...")
        server_process.terminate()
        
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
'''
        
        startup_file = Path('startup.py')
        with open(startup_file, 'w') as f:
            f.write(startup_content)
        
        return True
    
    def build_all(self) -> bool:
        """Build executable and installer"""
        print("🏗️  Starting build process...")
        
        # Create startup script
        self.create_startup_executable()
        
        # Build executable
        if not self.build_executable():
            return False
        
        # Create installer
        if not self.create_installer():
            print("⚠️  Installer creation failed, but executable is available")
        
        # Show results
        self._show_build_results()
        
        return True
    
    def _show_build_results(self):
        """Show build results and instructions"""
        print("\\n🎉 Build Process Complete!")
        print("=" * 50)
        
        if self.build_dir.exists():
            print(f"📁 Build files: {self.build_dir}")
            
            # List created files
            for item in self.build_dir.iterdir():
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"   📄 {item.name} ({size_mb:.1f} MB)")
                elif item.is_dir():
                    print(f"   📁 {item.name}/")
        
        print("\\n📝 Distribution Instructions:")
        print("1. Test the executable on target platforms")
        print("2. Bundle with the ephe/ directory for ephemeris data")
        print("3. Include static/ directory for web interface")
        print("4. Provide installation instructions")
        
        print("\\n🚀 Usage:")
        if self.platform_info['os'] == 'windows':
            print("   Windows: Run VedicAstrologyCalculator.exe")
        elif self.platform_info['os'] == 'darwin':
            print("   macOS: Open VedicAstrologyCalculator.app")
        else:
            print("   Linux: ./VedicAstrologyCalculator")

def main():
    """Main entry point"""
    builder = ExecutableBuilder()
    success = builder.build_all()
    
    if not success:
        print("❌ Build failed!")
        sys.exit(1)
    
    print("✅ Build successful!")

if __name__ == "__main__":
    main()