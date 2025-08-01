#!/usr/bin/env python3
"""
Coffee Shop Web Game - Application Entry Point
UPDATED: Enhanced import handling and deployment optimization
"""
import os
import sys

def setup_import_paths():
    """Setup import paths to find app.py in various configurations"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define all possible locations where app.py might be
    search_paths = [
        current_dir,                                    # Same directory as run.py
        os.path.join(current_dir, 'backend'),          # backend subdirectory
        os.path.join(current_dir, '..', 'backend'),    # parent/backend
        os.path.join(current_dir, 'src'),              # src subdirectory
        os.path.join(current_dir, 'app'),              # app subdirectory
    ]
    
    print("🔍 Searching for app.py...")
    print(f"📁 Starting from: {current_dir}")
    
    for path in search_paths:
        app_file = os.path.join(path, 'app.py')
        if os.path.exists(app_file):
            print(f"✅ Found app.py at: {app_file}")
            # Add this path to Python's import path
            if path not in sys.path:
                sys.path.insert(0, path)
            return path, True
    
    # If not found, show directory structure for debugging
    print("❌ app.py not found in any expected location")
    print("📁 Current directory structure:")
    try:
        for root, dirs, files in os.walk(current_dir):
            level = root.replace(current_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith(('.py', '.html', '.txt')):
                    print(f"{subindent}{file}")
            if level > 2:  # Limit depth
                break
    except Exception:
        print("   Could not scan directory structure")
    
    return None, False

def import_flask_app(app_location):
    """Import Flask app with multiple fallback methods"""
    
    # Method 1: Standard import
    try:
        print("🔄 Method 1: Standard import...")
        from app import app, socketio
        print("✅ Standard import successful")
        return app, socketio, True
    except ImportError as e:
        print(f"⚠️ Standard import failed: {e}")
    
    # Method 2: Direct file import using importlib
    if app_location:
        try:
            print("🔄 Method 2: Direct file import...")
            import importlib.util
            app_file = os.path.join(app_location, 'app.py')
            
            spec = importlib.util.spec_from_file_location("app_module", app_file)
            app_module = importlib.util.module_from_spec(spec)
            sys.modules["app_module"] = app_module
            spec.loader.exec_module(app_module)
            
            app = getattr(app_module, 'app', None)
            socketio = getattr(app_module, 'socketio', None)
            
            if app and socketio:
                print("✅ Direct file import successful")
                return app, socketio, True
            else:
                print("⚠️ app.py found but missing 'app' or 'socketio' variables")
                
        except Exception as e:
            print(f"⚠️ Direct file import failed: {e}")
    
    # Method 3: Try backend.app import
    try:
        print("🔄 Method 3: Backend module import...")
        from backend.app import app, socketio
        print("✅ Backend module import successful")
        return app, socketio, True
    except ImportError as e:
        print(f"⚠️ Backend module import failed: {e}")
    
    print("❌ All import methods failed")
    return None, None, False

def get_deployment_config():
    """Get optimized configuration for different deployment platforms"""
    # Port configuration
    port = int(os.environ.get('PORT', 5000))
    
    # Detect deployment platform
    deployment_platform = None
    is_production = False
    
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        deployment_platform = "Railway"
        is_production = True
    elif os.environ.get('RENDER'):
        deployment_platform = "Render"
        is_production = True
    elif os.environ.get('DYNO'):
        deployment_platform = "Heroku"
        is_production = True
    elif os.environ.get('FLASK_ENV') == 'production':
        deployment_platform = "Production"
        is_production = True
    else:
        deployment_platform = "Local Development"
        is_production = False
    
    config = {
        'port': port,
        'host': '0.0.0.0',
        'debug': not is_production,
        'use_reloader': not is_production,
        'is_production': is_production,
        'platform': deployment_platform
    }
    
    return config

def print_startup_banner(config):
    """Print detailed startup information"""
    print("\n" + "☕" * 20)
    print("   COFFEE SHOP WEB GAME")
    print("   From CLI to Web - A Journey")
    print("☕" * 20)
    
    print(f"\n🌐 Platform: {config['platform']}")
    
    if config['is_production']:
        print("🚀 PRODUCTION DEPLOYMENT")
        print(f"   Port: {config['port']}")
        print("   Debug: OFF")
        print("   Reloader: OFF")
        print("   Host: 0.0.0.0 (public)")
    else:
        print("🔧 LOCAL DEVELOPMENT")
        print(f"   URL: http://localhost:{config['port']}")
        print(f"   Game: http://localhost:{config['port']}/pixel")
        print(f"   API Test: http://localhost:{config['port']}/api/test")
        print(f"   Debug: {'ON' if config['debug'] else 'OFF'}")
    
    print("\n🎮 Features Available:")
    print("   ☕ 26 Coffee drink combinations")
    print("   🥐 6 Fresh bakery items")
    print("   📦 Real-time inventory management")
    print("   💰 Ingredient purchasing system")
    print("   🎯 Progressive target system")
    print("   📱 Mobile-responsive design")
    print("   ⚡ WebSocket real-time updates")
    print("   🎨 Pixel art game interface")
    
    print(f"\n🚀 Starting {config['platform']} server...")
    print("=" * 50)

def show_troubleshooting():
    """Show troubleshooting information if startup fails"""
    print("\n" + "🆘" * 20)
    print("   TROUBLESHOOTING GUIDE")
    print("🆘" * 20)
    
    print("\n📋 Common Solutions:")
    print("1. 📁 File Structure Check:")
    print("   Make sure your project looks like this:")
    print("   your-project/")
    print("   ├── run.py")
    print("   ├── backend/")
    print("   │   └── app.py")
    print("   └── requirements.txt")
    
    print("\n2. 🔧 Quick Fixes:")
    print("   • Run: cd backend && python app.py")
    print("   • Or move app.py to same folder as run.py")
    print("   • Check that backend/app.py exists")
    
    print("\n3. 📦 Dependencies:")
    print("   • pip install flask flask-socketio")
    print("   • pip install -r requirements.txt")
    
    print("\n4. 🚀 For Deployment:")
    print("   • This error won't happen on Railway/Render")
    print("   • They handle paths automatically")
    print("   • Just push to GitHub and deploy!")

def main():
    """Enhanced main function with comprehensive error handling"""
    print("🚀 Coffee Shop Web Game - Starting Up...")
    
    # Step 1: Setup import paths
    app_location, found = setup_import_paths()
    
    # Step 2: Import Flask app
    app, socketio, import_success = import_flask_app(app_location)
    
    if not import_success:
        print("\n❌ Failed to import Flask application")
        show_troubleshooting()
        
        # Last resort: try running app.py directly if it exists
        if app_location:
            app_file = os.path.join(app_location, 'app.py')
            print(f"\n🔄 Last resort: Running {app_file} directly...")
            try:
                os.chdir(app_location)
                os.system('python app.py')
            except Exception as e:
                print(f"❌ Direct execution failed: {e}")
        
        sys.exit(1)
    
    # Step 3: Get deployment configuration
    config = get_deployment_config()
    
    # Step 4: Print startup information
    print_startup_banner(config)
    
    # Step 5: Start the server
    try:
        socketio.run(
            app,
            host=config['host'],
            port=config['port'],
            debug=config['debug'],
            use_reloader=config['use_reloader'],
            allow_unsafe_werkzeug=config['is_production']
        )
    except KeyboardInterrupt:
        print("\n\n👋 Coffee shop closed by user. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        if config['debug']:
            import traceback
            traceback.print_exc()
        
        print("\n💡 Try these fixes:")
        print("   • Check if port is already in use")
        print("   • Run: lsof -i :5000 (to check port usage)")
        print("   • Try a different port: PORT=8000 python run.py")
        
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)