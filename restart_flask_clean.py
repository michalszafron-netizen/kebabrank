# restart_flask_clean.py - Force clean restart of Flask app
import os
import sys
import time
import signal
import psutil
from dotenv import load_dotenv

load_dotenv()

def kill_flask_processes():
    """Forcefully kill all Flask processes and their children"""
    killed = 0
    processes = []
    
    # First pass - collect all Flask processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'ppid']):
        try:
            if proc.info['name'] in ['python', 'python.exe', 'python3']:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('app.py' in arg or 'flask' in arg.lower() for arg in cmdline):
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Second pass - kill processes starting from children
    processes.sort(key=lambda p: p.info['ppid'], reverse=True)
    
    for proc in processes:
        try:
            print(f"🔫 Killing process tree for PID {proc.info['pid']}")
            parent = psutil.Process(proc.info['pid'])
            children = parent.children(recursive=True)
            
            # Kill children first
            for child in children:
                try:
                    child.kill()
                    killed += 1
                except:
                    continue
            
            # Then kill parent
            parent.kill()
            killed += 1
        except:
            continue
    
    if killed > 0:
        print(f"✅ Killed {killed} processes in total")
        return True
    
    print("ℹ️ No Flask processes found running")
    return True

def clear_python_cache():
    """Clear Python cache files"""
    cache_dirs = ['__pycache__', '.pytest_cache']
    cache_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip venv and .git directories
        if 'venv' in root or '.git' in root:
            continue
            
        # Remove __pycache__ directories
        for cache_dir in cache_dirs:
            if cache_dir in dirs:
                cache_path = os.path.join(root, cache_dir)
                print(f"🗑️ Removing cache directory: {cache_path}")
                import shutil
                shutil.rmtree(cache_path, ignore_errors=True)
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                print(f"🗑️ Removing cache file: {file_path}")
                os.remove(file_path)

def start_flask():
    """Start Flask app with robust process management"""
    import socket
    import subprocess
    import time
    
    port = 5000
    max_retries = 3
    retry_delay = 3
    
    print(f"\n🚀 Starting Flask app on port {port}...")
    
    for attempt in range(max_retries):
        # Check/kill existing processes
        kill_flask_processes()
        time.sleep(2)
        
        # Verify port is available
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
        except socket.error:
            print(f"❌ Port {port} still in use (attempt {attempt + 1}/{max_retries})")
            continue
            
        # Start Flask with explicit environment
        try:
            flask_env = os.environ.copy()
            flask_env['FLASK_ENV'] = 'development'
            flask_env['FLASK_APP'] = 'app.py'
            
            # Start Flask directly with explicit host/port
            proc = subprocess.Popen(
                ['python', 'app.py'],
                env=flask_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait and check if process is still running
            time.sleep(3)
            if proc.poll() is not None:  # Process ended
                stdout, stderr = proc.communicate()
                print(f"❌ Flask failed to start")
                if stderr:
                    print(f"Error output:\n{stderr}")
                continue
            
            # Verify server started
            try:
                with socket.create_connection(('localhost', port), timeout=5):
                    print(f"✅ Flask successfully started on http://localhost:{port}")
                    print(f"   Process PID: {proc.pid}")
                    return True
            except (socket.timeout, ConnectionRefusedError) as e:
                proc.terminate()
                print(f"⚠️ Flask didn't start properly (attempt {attempt + 1}/{max_retries})")
                print(f"   Error: {str(e)}")
                continue
                
        except Exception as e:
            print(f"❌ Failed to start Flask: {str(e)}")
            continue
    
    print(f"❌ Failed to start Flask after {max_retries} attempts")
    return False

if __name__ == "__main__":
    print("🔄 Flask Clean Restart Tool")
    print("=" * 50)
    
    try:
        # Step 1: Kill existing processes
        print("\nSTEP 1: Killing existing Flask processes...")
        if not kill_flask_processes():
            print("❌ Failed to kill processes")
            sys.exit(1)
        print("✅ Process killing complete")
        
        # Step 2: Clear cache
        print("\nSTEP 2: Clearing Python cache...")
        clear_python_cache()
        print("✅ Cache clearing complete")
        
        # Step 3: Start Flask
        print("\nSTEP 3: Starting Flask server...")
        print("=" * 50)
        success = start_flask()
        
        if not success:
            print("\n❌ CRITICAL: Failed to start Flask server")
            sys.exit(1)
        print("\n✅ Flask server started successfully")
            
    except Exception as e:
        print(f"\n❌ UNHANDLED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
