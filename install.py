#!/usr/bin/env python3
"""
Universal Installer for Vedic Astrology Calculator
Automatically detects platform and chooses optimal installation method
"""

import os
import sys
import platform
import subprocess
import json
import shutil
import urllib.request
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class UniversalInstaller:
    def __init__(self):
        self.platform_info = self._detect_platform()
        self.package_managers = self._detect_package_managers()
        self.container_tools = self._detect_container_tools()
        self.web_servers = self._detect_web_servers()
        self.replit_env = self._detect_replit_environment()
        self.cloudpanel_env = self._detect_cloudpanel_environment()
        
    def _detect_platform(self) -> Dict:
        """Detect operating system and architecture"""
        return {
            'os': platform.system().lower(),
            'arch': platform.machine().lower(),
            'version': platform.version(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'is_admin': self._check_admin_privileges(),
            'is_container': self._detect_container_environment()
        }
    
    def _check_admin_privileges(self) -> bool:
        """Check if running with administrator/root privileges"""
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows
            try:
                import ctypes
                # Windows-specific check
                if hasattr(ctypes, 'windll'):
                    return bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore
                return False
            except (ImportError, AttributeError):
                return False
    
    def _detect_container_environment(self) -> bool:
        """Detect if running inside a container"""
        container_indicators = [
            '/.dockerenv',
            '/run/.containerenv',
            os.environ.get('KUBERNETES_SERVICE_HOST'),
            os.environ.get('container') == 'podman'
        ]
        return any(indicator for indicator in container_indicators if indicator)
    
    def _detect_package_managers(self) -> Dict[str, bool]:
        """Detect available Python package managers"""
        managers = {}
        tools = ['uv', 'pip', 'conda', 'mamba', 'poetry', 'pipenv', 'pdm']
        
        for tool in tools:
            managers[tool] = shutil.which(tool) is not None
            
        # Special case for pip - might be available as python -m pip
        if not managers['pip']:
            try:
                subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                             capture_output=True, check=True)
                managers['pip'] = True
            except subprocess.CalledProcessError:
                pass
                
        return managers
    
    def _detect_container_tools(self) -> Dict[str, bool]:
        """Detect available containerization tools"""
        tools = ['docker', 'podman', 'nerdctl']
        return {tool: shutil.which(tool) is not None for tool in tools}
    
    def _detect_web_servers(self) -> Dict[str, bool]:
        """Detect available web servers"""
        servers = ['nginx', 'apache2', 'httpd', 'caddy']
        return {server: shutil.which(server) is not None for server in servers}
    
    def _detect_replit_environment(self) -> Dict[str, any]:
        """Detect Replit-specific environment details"""
        replit_indicators = {
            'is_replit': bool(os.getenv('REPLIT_DEV_DOMAIN')),
            'replit_domain': os.getenv('REPLIT_DEV_DOMAIN'),
            'repl_id': os.getenv('REPL_ID'),
            'repl_owner': os.getenv('REPL_OWNER'),
            'repl_slug': os.getenv('REPL_SLUG'),
            'has_nixos': os.path.exists('/etc/os-release') and 'nixos' in open('/etc/os-release', 'r').read().lower() if os.path.exists('/etc/os-release') else False
        }
        return replit_indicators
    
    def _detect_cloudpanel_environment(self) -> Dict[str, any]:
        """Detect CloudPanel environment and configuration"""
        cloudpanel_indicators = {
            'is_cloudpanel': any([
                os.path.exists('/usr/local/cloudpanel'),
                os.path.exists('/home/cloudpanel'),
                shutil.which('clp') is not None,
                os.path.exists('/etc/cloudpanel')
            ]),
            'has_nginx': shutil.which('nginx') is not None,
            'has_uwsgi': shutil.which('uwsgi') is not None,
            'has_systemd': shutil.which('systemctl') is not None,
            'site_user_pattern': self._detect_site_user_pattern(),
            'python_versions': self._detect_available_python_versions()
        }
        return cloudpanel_indicators
    
    def _detect_site_user_pattern(self) -> Optional[str]:
        """Detect CloudPanel site user pattern"""
        try:
            # Check for typical CloudPanel site directory structure
            home_dirs = [d for d in os.listdir('/home') if d.startswith('site-')]
            if home_dirs:
                return home_dirs[0]
        except (OSError, PermissionError):
            pass
        return None
    
    def _detect_available_python_versions(self) -> List[str]:
        """Detect available Python versions"""
        versions = []
        for version in ['python3.11', 'python3.10', 'python3.9', 'python3.8', 'python3', 'python']:
            if shutil.which(version):
                versions.append(version)
        return versions
    
    def _run_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run command with error handling"""
        try:
            return subprocess.run(command, capture_output=True, text=True, check=check)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {' '.join(command)}")
            print(f"Error: {e.stderr}")
            if check:
                raise
            # Return a CompletedProcess object for consistency
            return subprocess.CompletedProcess(command, e.returncode, e.stdout, e.stderr)
    
    def _download_file(self, url: str, destination: Path) -> None:
        """Download file with progress indicator"""
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, destination)
    
    def get_optimal_installation_method(self) -> str:
        """Determine the best installation method for this environment"""
        # Container environments - prefer pip for stability
        if self.platform_info['is_container']:
            if self.package_managers['pip']:
                return 'pip_native'
            elif self.package_managers['uv']:
                return 'uv_native'
                
        # Development environments - prefer uv or poetry
        if self.package_managers['uv']:
            return 'uv_venv'
        elif self.package_managers['poetry']:
            return 'poetry'
        
        # Containerization available - prefer Docker for isolation
        if self.container_tools['docker']:
            return 'docker'
        elif self.container_tools['podman']:
            return 'podman'
            
        # Fallback to pip
        if self.package_managers['pip']:
            return 'pip_venv'
            
        return 'binary_download'
    
    def install_via_podman(self) -> bool:
        """Install using Podman (same as Docker)"""
        print("🚀 Installing via Podman...")
        try:
            # Create Dockerfile if it doesn't exist
            if not Path('Dockerfile').exists():
                self._create_dockerfile()
            
            # Build Podman image
            self._run_command(['podman', 'build', '-t', 'vedic-astrology-calc', '.'])
            
            # Create podman-compose file (similar to docker-compose)
            self._create_podman_compose()
            
            print("✅ Podman installation complete!")
            print("Run: podman run -p 5000:5000 vedic-astrology-calc")
            return True
        except Exception as e:
            print(f"❌ Podman installation failed: {e}")
            return False
    
    def install_via_uv_native(self) -> bool:
        """Install using uv without virtual environment (container-friendly)"""
        print("🚀 Installing via uv (native)...")
        try:
            # Install dependencies using uv
            self._run_command(['uv', 'sync', '--no-dev'])
            
            print("✅ Installation complete!")
            print("Run: uv run uvicorn main:app --host 0.0.0.0 --port 5000")
            return True
        except Exception as e:
            print(f"❌ uv native installation failed: {e}")
            return False
    
    def install_via_uv_venv(self) -> bool:
        """Install using uv with virtual environment"""
        print("🚀 Installing via uv (virtual environment)...")
        try:
            # Sync dependencies
            self._run_command(['uv', 'sync'])
            
            # Create startup script
            self._create_startup_script('uv')
            
            print("✅ Installation complete!")
            print("Run: ./start.sh (Linux/Mac) or start.bat (Windows)")
            return True
        except Exception as e:
            print(f"❌ uv venv installation failed: {e}")
            return False
    
    def install_via_poetry(self) -> bool:
        """Install using Poetry"""
        print("🚀 Installing via Poetry...")
        try:
            # Convert pyproject.toml to poetry format if needed
            self._ensure_poetry_compatibility()
            
            # Install dependencies
            self._run_command(['poetry', 'install'])
            
            # Create startup script
            self._create_startup_script('poetry')
            
            print("✅ Installation complete!")
            print("Run: poetry run uvicorn main:app --host 0.0.0.0 --port 5000")
            return True
        except Exception as e:
            print(f"❌ Poetry installation failed: {e}")
            return False
    
    def install_via_pip_native(self) -> bool:
        """Install using pip without virtual environment (container-friendly)"""
        print("🚀 Installing via pip (native)...")
        try:
            # Install the project and dependencies
            self._run_command([sys.executable, '-m', 'pip', 'install', '.'])
            
            print("✅ Installation complete!")
            print("Run: python -m uvicorn main:app --host 0.0.0.0 --port 5000")
            return True
        except Exception as e:
            print(f"❌ pip native installation failed: {e}")
            return False
    
    def install_via_pip_venv(self) -> bool:
        """Install using pip with virtual environment"""
        print("🚀 Installing via pip (virtual environment)...")
        try:
            # Create virtual environment
            venv_path = Path('.venv')
            self._run_command([sys.executable, '-m', 'venv', str(venv_path)])
            
            # Activate virtual environment and install
            if self.platform_info['os'] == 'windows':
                pip_path = venv_path / 'Scripts' / 'pip'
                python_path = venv_path / 'Scripts' / 'python'
            else:
                pip_path = venv_path / 'bin' / 'pip'
                python_path = venv_path / 'bin' / 'python'
            
            # Install the project and dependencies
            self._run_command([str(pip_path), 'install', '.'])
            
            # Create startup script
            self._create_startup_script('pip', python_path)
            
            print("✅ Installation complete!")
            print("Run: ./start.sh (Linux/Mac) or start.bat (Windows)")
            return True
        except Exception as e:
            print(f"❌ pip venv installation failed: {e}")
            return False
    
    def install_via_docker(self) -> bool:
        """Install using Docker"""
        print("🚀 Installing via Docker...")
        try:
            # Create Dockerfile if it doesn't exist
            if not Path('Dockerfile').exists():
                self._create_dockerfile()
            
            # Build Docker image
            self._run_command(['docker', 'build', '-t', 'vedic-astrology-calc', '.'])
            
            # Create docker-compose file
            self._create_docker_compose()
            
            print("✅ Docker installation complete!")
            print("Run: docker-compose up")
            print("Or: docker run -p 5000:5000 vedic-astrology-calc")
            return True
        except Exception as e:
            print(f"❌ Docker installation failed: {e}")
            return False
    
    def install_via_binary_download(self) -> bool:
        """Download and install pre-built binary"""
        print("🚀 Installing via binary download...")
        print("❌ Binary downloads not yet implemented")
        print("Please install Python and pip, then try again")
        return False
    
    def _extract_dependencies_from_pyproject(self) -> List[str]:
        """Extract dependencies from pyproject.toml"""
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib  # type: ignore
            except ImportError:
                # Fallback - return known dependencies
                return [
                    'fastapi>=0.116.1',
                    'uvicorn>=0.35.0',
                    'pydantic>=2.11.9',
                    'pyswisseph>=2.10.3.2',
                    'pytz>=2025.2',
                    'bcrypt>=4.3.0',
                    'requests>=2.32.5'
                ]
        
        try:
            with open('pyproject.toml', 'rb') as f:
                data = tomllib.load(f)
            return data.get('project', {}).get('dependencies', [])
        except Exception:
            return []
    
    def _ensure_poetry_compatibility(self) -> None:
        """Ensure pyproject.toml is compatible with Poetry"""
        # Poetry compatibility is complex - for now, just check if poetry section exists
        pass
    
    def _create_startup_script(self, method: str, python_path: Optional[Path] = None) -> None:
        """Create platform-appropriate startup scripts"""
        if self.platform_info['os'] == 'windows':
            self._create_windows_startup_script(method, python_path)
        else:
            self._create_unix_startup_script(method, python_path)
    
    def _create_unix_startup_script(self, method: str, python_path: Optional[Path] = None) -> None:
        """Create Unix startup script"""
        script_content = "#!/bin/bash\n\n"
        
        if method == 'uv':
            script_content += "source .venv/bin/activate\n"
            script_content += "python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload\n"
        elif method == 'poetry':
            script_content += "poetry run uvicorn main:app --host 0.0.0.0 --port 5000 --reload\n"
        elif method == 'pip' and python_path:
            script_content += f"source .venv/bin/activate\n"
            script_content += "python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload\n"
        
        with open('start.sh', 'w') as f:
            f.write(script_content)
        os.chmod('start.sh', 0o755)
    
    def _create_windows_startup_script(self, method: str, python_path: Optional[Path] = None) -> None:
        """Create Windows startup script"""
        script_content = "@echo off\n\n"
        
        if method == 'uv':
            script_content += "call .venv\\Scripts\\activate.bat\n"
            script_content += "python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload\n"
        elif method == 'poetry':
            script_content += "poetry run uvicorn main:app --host 0.0.0.0 --port 5000 --reload\n"
        elif method == 'pip' and python_path:
            script_content += "call .venv\\Scripts\\activate.bat\n"
            script_content += "python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload\n"
        
        with open('start.bat', 'w') as f:
            f.write(script_content)
    
    def _create_dockerfile(self) -> None:
        """Create optimized multi-stage Dockerfile"""
        dockerfile_content = '''# Multi-stage Dockerfile for Vedic Astrology Calculator
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Set UV environment path for consistency
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \\
    ca-certificates \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy virtual environment from base stage
COPY --from=base /app/.venv /app/.venv

# Copy application code
COPY --chown=app:app . .

# Create ephe directory and set permissions
RUN mkdir -p ephe data && chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \\
    CMD curl -f http://localhost:5000/ || exit 1

# Start application
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
'''
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile_content)
    
    def _create_docker_compose(self) -> None:
        """Create docker-compose.yml for easy deployment"""
        compose_content = '''version: '3.8'

services:
  vedic-astrology:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./ephe:/app/ephe:ro
      - astrology_db:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  astrology_db:
'''
        with open('docker-compose.yml', 'w') as f:
            f.write(compose_content)
    
    def _create_podman_compose(self) -> None:
        """Create podman-compose.yml for easy deployment"""
        compose_content = '''version: '3.8'

services:
  vedic-astrology:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=production
      - DATA_DIR=/app/data
    volumes:
      - ./ephe:/app/ephe:ro
      - astrology_db:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  astrology_db:
'''
        with open('podman-compose.yml', 'w') as f:
            f.write(compose_content)
    
    def display_system_info(self) -> None:
        """Display detected system information"""
        print("🔍 System Detection Results:")
        print(f"Operating System: {self.platform_info['os'].title()}")
        print(f"Architecture: {self.platform_info['arch']}")
        print(f"Python Version: {self.platform_info['python_version']}")
        print(f"Admin Privileges: {'Yes' if self.platform_info['is_admin'] else 'No'}")
        print(f"Container Environment: {'Yes' if self.platform_info['is_container'] else 'No'}")
        
        print("\n📦 Available Package Managers:")
        for manager, available in self.package_managers.items():
            status = "✅" if available else "❌"
            print(f"{status} {manager}")
        
        print("\n🐳 Available Container Tools:")
        for tool, available in self.container_tools.items():
            status = "✅" if available else "❌"
            print(f"{status} {tool}")
    
    def install(self) -> bool:
        """Main installation method"""
        print("🎯 Universal Installer for Vedic Astrology Calculator")
        print("=" * 60)
        
        self.display_system_info()
        
        method = self.get_optimal_installation_method()
        print(f"\n🚀 Optimal installation method: {method}")
        
        # Map methods to functions
        method_map = {
            'uv_native': self.install_via_uv_native,
            'uv_venv': self.install_via_uv_venv,
            'poetry': self.install_via_poetry,
            'pip_native': self.install_via_pip_native,
            'pip_venv': self.install_via_pip_venv,
            'docker': self.install_via_docker,
            'podman': self.install_via_podman,
            'binary_download': self.install_via_binary_download
        }
        
        # Try optimal method first
        if method in method_map:
            try:
                if method_map[method]():
                    return True
            except Exception as e:
                print(f"⚠️ {method} failed: {e}")
        
        # Try fallback methods in order of reliability
        print("\n🔄 Trying fallback methods...")
        fallback_order = ['pip_venv', 'pip_native', 'uv_venv', 'docker', 'binary_download']
        
        for fallback_method in fallback_order:
            if fallback_method != method and fallback_method in method_map:
                print(f"Trying {fallback_method}...")
                try:
                    if method_map[fallback_method]():
                        return True
                except Exception as e:
                    print(f"⚠️ {fallback_method} failed: {e}")
                    continue
        
        print("❌ All installation methods failed!")
        return False

def main():
    """Main entry point"""
    installer = UniversalInstaller()
    success = installer.install()
    
    if success:
        print("\n🎉 Installation successful!")
        print("\n📝 Next steps:")
        print("1. The Vedic Astrology Calculator is now ready to use")
        print("2. Access the web interface at http://localhost:5000")
        print("3. API documentation at http://localhost:5000/docs")
        print("4. Admin panel at http://localhost:5000/admin")
    else:
        print("\n💡 Manual installation:")
        print("1. Install Python 3.11+")
        print("2. Install uv: pip install uv")
        print("3. Run: uv sync")
        print("4. Run: uv run uvicorn main:app --host 0.0.0.0 --port 5000")
        sys.exit(1)

if __name__ == "__main__":
    main()