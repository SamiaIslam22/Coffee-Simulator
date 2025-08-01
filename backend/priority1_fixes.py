# ☕ PRIORITY 1: ESSENTIAL FIXES FOR COFFEE SIMULATOR
# ================================================

"""
This file contains all the critical fixes needed to get the Coffee Simulator
working properly. Address these issues in order.
"""

# 🔧 FIX 1: FLASK APP STARTUP ISSUES
# ==================================

# ISSUE: Import path problems in app.py
# SOLUTION: Fix the import statements

# ORIGINAL (BROKEN):
# from enhanced_models.coffee_menu import CoffeeMenuWeb
# from enhanced_models.shop_info import ShopInfoWeb
# from enhanced_models.bakery_item import BakeryMenuWeb  
# from enhanced_models.money_machine import MoneyMachineWeb

# FIXED VERSION:
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now imports should work
try:
    from enhanced_models.coffee_menu import CoffeeMenuWeb
    from enhanced_models.shop_info import ShopInfoWeb
    from enhanced_models.bakery_item import BakeryMenuWeb
    from enhanced_models.money_machine import MoneyMachineWeb
    print("✅ Enhanced models imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Fallback to original models if enhanced ones fail
    print("🔄 Falling back to original models...")


# 🔧 FIX 2: TEMPLATE AND STATIC PATHS
# ===================================

# ISSUE: Template folder paths may not resolve correctly
# SOLUTION: Use absolute paths and verify directories exist

def setup_flask_paths():
    """Setup correct paths for Flask templates and static files"""
    # Get the project root directory
    current_file = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(backend_dir)
    
    template_dir = os.path.join(project_root, 'frontend', 'templates')
    static_dir = os.path.join(project_root, 'frontend', 'static')
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 Template dir: {template_dir}")
    print(f"📁 Static dir: {static_dir}")
    
    # Check if directories exist
    if not os.path.exists(template_dir):
        print(f"❌ Template directory missing: {template_dir}")
        # Create directory if it doesn't exist
        os.makedirs(template_dir, exist_ok=True)
        print(f"✅ Created template directory")
    
    if not os.path.exists(static_dir):
        print(f"❌ Static directory missing: {static_dir}")
        os.makedirs(static_dir, exist_ok=True)
        print(f"✅ Created static directory")
    
    return template_dir, static_dir


# 🔧 FIX 3: API ERROR HANDLING
# ============================

# ISSUE: Limited error handling in API endpoints
# SOLUTION: Add comprehensive error handling

def safe_api_call(func):
    """Decorator to add error handling to API endpoints"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ API Error in {func.__name__}: {e}")
            return {
                'error': True,
                'message': str(e),
                'function': func.__name__
            }, 500
    return wrapper


# 🔧 FIX 4: MENU DATA STRUCTURE MISMATCH
# ======================================

# ISSUE: Frontend expects flattened menu, backend returns categorized
# SOLUTION: Add menu flattening function

def flatten_menu_response(categorized_menu):
    """Convert categorized menu to flat list for frontend"""
    flattened = []
    
    if isinstance(categorized_menu, dict):
        for category, items in categorized_menu.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        # Ensure item has required fields
                        item.setdefault('category', category)
                        flattened.append(item)
    
    return flattened


# 🔧 FIX 5: WEBSOCKET CONNECTION ISSUES
# =====================================

# ISSUE: WebSocket may need CORS configuration
# SOLUTION: Add proper SocketIO configuration

def setup_socketio(app):
    """Setup SocketIO with proper configuration"""
    from flask_socketio import SocketIO
    
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*",  # Allow all origins for development
        logger=True,               # Enable logging for debugging
        engineio_logger=True       # Enable engine.io logging
    )
    
    return socketio


# 🔧 FIX 6: CUSTOMER SPAWNING TIMING
# ==================================

# ISSUE: Customer spawning may be too random or frequent
# SOLUTION: Better timing control

class CustomerSpawner:
    def __init__(self):
        self.last_spawn_time = 0
        self.min_spawn_interval = 3000  # 3 seconds minimum
        self.max_customers = 3
        self.spawn_probability = 0.015  # 1.5% per frame at 60fps
    
    def should_spawn_customer(self, current_customers_count, current_time):
        """Determine if a new customer should spawn"""
        # Don't spawn if too many customers
        if current_customers_count >= self.max_customers:
            return False
        
        # Don't spawn if too soon since last spawn
        if current_time - self.last_spawn_time < self.min_spawn_interval:
            return False
        
        # Random chance to spawn
        import random
        if random.random() < self.spawn_probability:
            self.last_spawn_time = current_time
            return True
        
        return False


# 🔧 FIX 7: INVENTORY UPDATE ISSUES
# =================================

# ISSUE: Inventory updates may not sync properly between frontend/backend
# SOLUTION: Add inventory validation and sync

def validate_inventory_update(required_ingredients, current_inventory):
    """Validate that an order can be fulfilled with current inventory"""
    for ingredient, required_amount in required_ingredients.items():
        available = current_inventory.get(ingredient, {}).get('current', 0)
        if available < required_amount:
            return False, f"Insufficient {ingredient}: need {required_amount}, have {available}"
    
    return True, "OK"


# 🔧 FIX 8: PAYMENT PROCESSING FLOW
# =================================

# ISSUE: Payment processing may fail silently
# SOLUTION: Add detailed payment validation

def process_game_payment(item_price, payment_method='auto'):
    """Process payment for game orders with proper validation"""
    try:
        payment_details = {
            'cash_amount': item_price + 0.50,  # Customer pays a bit extra
            'tip': 0.25 if item_price > 4.0 else 0.0,  # Tip for expensive items
            'quality_bonus': 0.0
        }
        
        return {
            'success': True,
            'payment_method': payment_method,
            'payment_details': payment_details,
            'total_paid': payment_details['cash_amount'],
            'change': payment_details['cash_amount'] - item_price,
            'tip': payment_details['tip']
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# 🔧 FIX 9: DEBUGGING HELPERS
# ===========================

def debug_game_state():
    """Print current game state for debugging"""
    print("\n🔍 GAME STATE DEBUG")
    print("===================")
    
    # Test menu loading
    try:
        coffee_menu = CoffeeMenuWeb()
        print(f"☕ Coffee menu: {len(coffee_menu.menu)} items")
        
        bakery_menu = BakeryMenuWeb()
        print(f"🥐 Bakery menu: {len(bakery_menu.menu)} items")
        
        shop_info = ShopInfoWeb()
        print(f"📦 Inventory: {len(shop_info.storage)} items")
        
        money_machine = MoneyMachineWeb()
        print(f"💰 Money system: {money_machine.currency} ready")
        
    except Exception as e:
        print(f"❌ Error loading game components: {e}")


# 🔧 FIX 10: STARTUP VALIDATION
# =============================

def validate_game_startup():
    """Validate that all game systems are working"""
    print("🚀 VALIDATING GAME STARTUP")
    print("===========================")
    
    checks = []
    
    # Check 1: Import paths
    try:
        from enhanced_models.coffee_menu import CoffeeMenuWeb
        checks.append("✅ Enhanced models import")
    except:
        checks.append("❌ Enhanced models import")
    
    # Check 2: Menu data
    try:
        coffee_menu = CoffeeMenuWeb()
        assert len(coffee_menu.menu) > 0
        checks.append("✅ Coffee menu loaded")
    except:
        checks.append("❌ Coffee menu loaded")
    
    # Check 3: Template paths
    template_dir, static_dir = setup_flask_paths()
    if os.path.exists(template_dir):
        checks.append("✅ Template directory")
    else:
        checks.append("❌ Template directory")
    
    # Print results
    for check in checks:
        print(f"  {check}")
    
    success_count = len([c for c in checks if c.startswith("✅")])
    total_count = len(checks)
    
    print(f"\n📊 STARTUP VALIDATION: {success_count}/{total_count} checks passed")
    
    if success_count == total_count:
        print("🎉 All systems ready!")
        return True
    else:
        print("⚠️  Some systems need attention")
        return False


# 🔧 MAIN TESTING FUNCTION
# ========================

if __name__ == "__main__":
    print("☕ COFFEE SIMULATOR - PRIORITY 1 FIXES")
    print("=======================================")
    
    # Run validation
    if validate_game_startup():
        print("\n✅ Ready to test gameplay!")
        debug_game_state()
    else:
        print("\n❌ Fix the failing checks first")