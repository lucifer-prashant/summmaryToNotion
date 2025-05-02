import PyInstaller.__main__
import os
import sys
import time
import subprocess
import psutil  

def kill_existing_process():
    """Find and kill any existing GlobalIntegrator processes"""
    exe_name = "GlobalIntegrator.exe"
    print(f"Checking for running instances of {exe_name}")
    
    try:
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == exe_name:
                print(f"Found running process: {proc.info}")
                try:
                    proc.terminate()
                    print(f"Terminated process with PID {proc.info['pid']}")
                    killed = True
                    time.sleep(1)  
                    
                    if proc.is_running():
                        print(f"Process still running, force killing PID {proc.info['pid']}")
                        proc.kill()
                        time.sleep(1)
                except Exception as e:
                    print(f"Failed to terminate process: {e}")
        
        return killed
    except Exception as e:
        print(f"Error while checking for existing processes: {e}")
        return False

def build_executable():
    """Build the executable with PyInstaller"""
    kill_existing_process()
    
    exe_path = os.path.join('dist', 'GlobalIntegrator.exe')
    if os.path.exists(exe_path):
        try:
            print(f"Removing existing executable: {exe_path}")
            os.remove(exe_path)
            time.sleep(1)  
        except Exception as e:
            print(f"Failed to remove existing executable: {e}")
            return False
    
    print("Starting executable build process")
    
    pyinstaller_args = [
        'global_integ.py',
        '--onefile',
        '--windowed',
        '--name=GlobalIntegrator',
        '--add-data=token.json;.',
        '--add-data=credentials.json;.',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=pystray._win32',
        '--hidden-import=pystray._base',
    ]
    
    if os.path.exists('icon.ico'):
        pyinstaller_args.append('--icon=icon.ico')
        print("Using custom icon.ico")
    else:
        print("No icon.ico found - building without custom icon")
    
    print(f"PyInstaller args: {pyinstaller_args}")
    
    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print("Executable built successfully!")
        return True
    except Exception as e:
        print(f"Error building executable: {e}")
        return False

def run_application():
    """Run the main application"""
    exe_path = os.path.join('dist', 'GlobalIntegrator.exe')
    
    if not os.path.exists(exe_path):
        print("Executable not found. Building first...")
        if not build_executable():
            print("Failed to build executable")
            return
    
    try:
        print(f"Starting application: {exe_path}")
        subprocess.call([exe_path])
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    print("Script started")
    
    try:
        import psutil
    except ImportError:
        print("psutil not found, attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            import psutil
            print("Successfully installed psutil")
        except Exception as e:
            print(f"Failed to install psutil: {e}")
            sys.exit(1)
    
    try:
        import pystray
    except ImportError:
        print("pystray not found, attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray"])
            print("Successfully installed pystray")
        except Exception as e:
            print(f"Failed to install pystray: {e}")
    
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not found, attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("Successfully installed Pillow")
        except Exception as e:
            print(f"Failed to install Pillow: {e}")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--build':
        build_executable()
    else:
        killed = kill_existing_process()
        if killed:
            print("Killed existing processes, waiting before starting new instance")
            time.sleep(2)  
        
        run_application()