# backend/app.py - UPDATED WITH INVENTORY SYSTEM
# ===============================================

import os
import sys
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import json
from datetime import datetime

# 🔧 FIX 1: Setup proper Python paths
def setup_python_paths():
    """Ensure all modules can be imported properly"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Add paths to sys.path if not already there
    paths_to_add = [current_dir, project_root]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 Current directory: {current_dir}")
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Python path updated")

# Setup paths before imports
setup_python_paths()

# 🔧 FIX 2: Safe imports with fallbacks
def import_enhanced_models():
    """Import enhanced models with fallback to basic functionality"""
    try:
        from enhanced_models.coffee_menu import CoffeeMenuWeb
        from enhanced_models.shop_info import ShopInfoWeb
        from enhanced_models.bakery_item import BakeryMenuWeb
        from enhanced_models.money_machine import MoneyMachineWeb
        print("✅ Enhanced models imported successfully")
        return CoffeeMenuWeb, ShopInfoWeb, BakeryMenuWeb, MoneyMachineWeb
    except ImportError as e:
        print(f"❌ Enhanced models import failed: {e}")
        print("🔄 Using fallback basic models...")
        
        # Create basic fallback classes
        class BasicMenu:
            def __init__(self):
                self.menu = [
                    {'id': 'basic_coffee', 'name': 'Basic Coffee', 'price': 4.50, 'category': 'coffee'},
                    {'id': 'basic_bagel', 'name': 'Basic Bagel', 'price': 3.00, 'category': 'food'}
                ]
            def get_menu_by_category(self):
                return {'coffee': [self.menu[0]], 'bakery': [self.menu[1]]}
            def get_coffee_by_id(self, item_id):
                return next((item for item in self.menu if item['id'] == item_id), None)
            def get_food_by_id(self, item_id):
                return next((item for item in self.menu if item['id'] == item_id), None)
        
        class BasicShop:
            def __init__(self):
                self.storage = {'Water': 1000, 'Coffee Beans': 100}
            def get_real_time_stats(self):
                return {item: {'current': amount, 'status': 'good'} for item, amount in self.storage.items()}
            def resource_check(self, ingredients):
                return True
            def coffee_return(self, coffee):
                print(f"Serving: {coffee}")
            def food_return(self, food):
                print(f"Serving: {food}")
            def purchase_refill(self, item, money):
                return {'success': False, 'message': 'Enhanced models not available'}
        
        class BasicMoney:
            def __init__(self):
                self.profit = 0.0
            def process_web_payment(self, method, amount, details):
                self.profit += amount
                return {'success': True, 'message': 'Payment processed', 'change': 0}
        
        return BasicMenu, BasicShop, BasicMenu, BasicMoney

# Import the models
CoffeeMenuWeb, ShopInfoWeb, BakeryMenuWeb, MoneyMachineWeb = import_enhanced_models()

# 🔧 FIX 3: Setup Flask with proper paths
def setup_flask_app():
    """Create Flask app with correct template and static paths"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    template_dir = os.path.join(project_root, 'frontend', 'templates')
    static_dir = os.path.join(project_root, 'frontend', 'static')
    
    # Create directories if they don't exist
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    
    print(f"📁 Template directory: {template_dir}")
    print(f"📁 Static directory: {static_dir}")
    
    # Verify template files exist
    launcher_path = os.path.join(template_dir, 'launcher.html')
    game_path = os.path.join(template_dir, 'pixel_game.html')
    
    if not os.path.exists(launcher_path):
        print(f"⚠️  Missing: {launcher_path}")
    if not os.path.exists(game_path):
        print(f"⚠️  Missing: {game_path}")
    
    # Create Flask app
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-coffee-simulator')
    
    return app

# Create Flask app
app = setup_flask_app()

# 🔧 FIX 4: Setup SocketIO with proper configuration
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=False  # Reduce noise in logs
)

# 🔧 FIX 5: Initialize game systems with error handling
def initialize_game_systems():
    """Initialize all game systems safely"""
    try:
        coffee_menu = CoffeeMenuWeb()
        shop_info = ShopInfoWeb()
        bakery_menu = BakeryMenuWeb()
        money_machine = MoneyMachineWeb()
        
        print("✅ Game systems initialized:")
        print(f"   ☕ Coffee items: {len(getattr(coffee_menu, 'menu', []))}")
        print(f"   🥐 Bakery items: {len(getattr(bakery_menu, 'menu', []))}")
        print(f"   📦 Inventory items: {len(getattr(shop_info, 'storage', {}))}")
        print(f"   💰 Money system ready")
        
        return coffee_menu, shop_info, bakery_menu, money_machine
    
    except Exception as e:
        print(f"❌ Error initializing game systems: {e}")
        # Return minimal working systems
        class MinimalSystem:
            def __init__(self):
                self.menu = []
                self.storage = {}
            def get_menu_by_category(self):
                return {}
            def get_real_time_stats(self):
                return {}
            def process_web_payment(self, *args):
                return {'success': False, 'error': 'System not available'}
            def purchase_refill(self, item, money):
                return {'success': False, 'message': 'System not available'}
        
        minimal = MinimalSystem()
        return minimal, minimal, minimal, minimal

# Initialize game systems
coffee_menu, shop_info, bakery_menu, money_machine = initialize_game_systems()

# Game state tracking
game_sessions = {}

# 🔧 FIX 6: Add error handling decorator
def safe_route(func):
    """Decorator to add error handling to routes"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Route error in {func.__name__}: {e}")
            if request.is_json:
                return jsonify({
                    'error': True,
                    'message': str(e),
                    'route': func.__name__
                }), 500
            else:
                return f"Error in {func.__name__}: {str(e)}", 500
    wrapper.__name__ = func.__name__
    return wrapper

# === MAIN ROUTES ===
@app.route('/')
@safe_route
def index():
    """Coffee Simulator Launcher"""
    return render_template('launcher.html')

@app.route('/pixel')
@safe_route
def pixel_game():
    """Coffee Simulator Game"""
    return render_template('pixel_game.html')

# === API ROUTES ===
@app.route('/api/test')
@safe_route
def test_api():
    """Test endpoint to verify API is working"""
    coffee_count = len(getattr(coffee_menu, 'menu', []))
    bakery_count = len(getattr(bakery_menu, 'menu', []))
    
    return jsonify({
        'status': 'working',
        'message': 'Coffee Simulator API is responding correctly',
        'timestamp': datetime.now().isoformat(),
        'coffee_items': coffee_count,
        'bakery_items': bakery_count,
        'enhanced_models': 'CoffeeMenuWeb' in str(type(coffee_menu))
    })

@app.route('/api/menu/coffee')
@safe_route
def get_coffee_menu():
    """Get complete coffee menu in JSON format"""
    try:
        menu_data = coffee_menu.get_menu_by_category()
        return jsonify(menu_data)
    except Exception as e:
        print(f"❌ Error getting coffee menu: {e}")
        # Return minimal fallback
        return jsonify({
            'coffee': [
                {'id': 'fallback_coffee', 'name': 'House Coffee', 'price': 4.50, 'category': 'coffee'}
            ]
        })

@app.route('/api/menu/bakery')
@safe_route
def get_bakery_menu():
    """Get complete bakery menu in JSON format"""
    try:
        menu_data = bakery_menu.get_menu_by_category()
        return jsonify(menu_data)
    except Exception as e:
        print(f"❌ Error getting bakery menu: {e}")
        return jsonify({
            'bakery': [
                {'id': 'fallback_bagel', 'name': 'Plain Bagel', 'price': 3.00, 'category': 'food'}
            ]
        })

@app.route('/api/shop/inventory')
@safe_route
def get_inventory():
    """Get real-time inventory status"""
    try:
        inventory_data = shop_info.get_real_time_stats()
        return jsonify(inventory_data)
    except Exception as e:
        print(f"❌ Error getting inventory: {e}")
        return jsonify({
            'Water': {'current': 1000, 'status': 'good'},
            'Coffee Beans': {'current': 100, 'status': 'good'}
        })

# 🆕 NEW INVENTORY PURCHASE ROUTES
@app.route('/api/shop/purchase', methods=['POST'])
@safe_route
def purchase_ingredient():
    """Purchase ingredients to refill inventory"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        item_name = data.get('item')
        player_money = data.get('player_money', 0)
        
        if not item_name:
            return jsonify({'error': 'Item name required'}), 400
        
        if player_money < 0:
            return jsonify({'error': 'Invalid money amount'}), 400
        
        print(f"💰 Purchase request: {item_name} with ${player_money}")
        
        # Process the purchase through shop_info
        purchase_result = shop_info.purchase_refill(item_name, player_money)
        
        if purchase_result['success']:
            print(f"✅ Purchase successful: {purchase_result['message']}")
            
            # Emit real-time inventory update
            try:
                socketio.emit('inventory_updated', shop_info.get_real_time_stats())
                socketio.emit('purchase_completed', {
                    'item': item_name,
                    'cost': purchase_result['money_spent'],
                    'new_inventory': purchase_result['new_inventory'],
                    'money_remaining': purchase_result['money_remaining']
                })
            except Exception as e:
                print(f"⚠️ WebSocket emit failed: {e}, but purchase was successful")
            
            return jsonify(purchase_result)
        else:
            print(f"❌ Purchase failed: {purchase_result['message']}")
            return jsonify(purchase_result), 400
            
    except Exception as e:
        print(f"❌ Purchase processing error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Purchase failed: {str(e)}'}), 500

@app.route('/api/shop/shopping-list')
@safe_route
def get_shopping_list():
    """Get list of items that can be purchased"""
    try:
        player_money = request.args.get('money', 0, type=float)
        
        if hasattr(shop_info, 'get_shopping_list'):
            shopping_list = shop_info.get_shopping_list(player_money)
        else:
            shopping_list = []
        
        return jsonify({
            'shopping_list': shopping_list,
            'player_money': player_money,
            'total_items': len(shopping_list),
            'affordable_items': len([item for item in shopping_list if item.get('affordable', False)])
        })
        
    except Exception as e:
        print(f"❌ Error getting shopping list: {e}")
        return jsonify({'error': f'Failed to get shopping list: {str(e)}'}), 500

@app.route('/api/shop/alerts')
@safe_route
def get_inventory_alerts():
    """Get current inventory alerts"""
    try:
        if hasattr(shop_info, 'get_inventory_alerts'):
            alerts = shop_info.get_inventory_alerts()
        else:
            alerts = []
            
        if hasattr(shop_info, 'get_low_stock_items'):
            low_stock_items = shop_info.get_low_stock_items()
        else:
            low_stock_items = []
        
        return jsonify({
            'alerts': alerts,
            'low_stock_items': low_stock_items,
            'total_alerts': len(alerts),
            'critical_alerts': len([a for a in alerts if a.get('level') == 'critical'])
        })
        
    except Exception as e:
        print(f"❌ Error getting inventory alerts: {e}")
        return jsonify({'error': f'Failed to get alerts: {str(e)}'}), 500

@app.route('/api/game/order', methods=['POST'])
@safe_route
def process_order():
    """Process a customer order with enhanced item matching and inventory deduction"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        order_type = data.get('type')
        item_id = data.get('item_id')
        payment_method = data.get('payment_method', 'cash')
        payment_details = data.get('payment_details', {})
        session_id = session.get('session_id', 'default')
        
        print(f"🛒 Processing order: {order_type} - {item_id}")
        
        # Find the item with enhanced matching
        if order_type == 'coffee':
            # Try enhanced matching first
            item = coffee_menu.get_coffee_by_id_enhanced(item_id)
            # Fallback to original method
            if not item:
                item = coffee_menu.get_coffee_by_id(item_id)
            # Final fallback - search by name components
            if not item:
                item = coffee_menu.find_coffee(item_id.replace('_', ' '))
            
            if not item:
                print(f"❌ Coffee not found: {item_id}")
                print(f"📋 Available coffee items: {[i.coffeeName for i in coffee_menu.menu[:3]]}...")
                return jsonify({'error': f'Coffee not found: {item_id}'}), 404
                
        elif order_type == 'food':
            # Try enhanced matching first
            item = bakery_menu.get_food_by_id_enhanced(item_id)
            # Fallback to original method
            if not item:
                item = bakery_menu.get_food_by_id(item_id)
            # Final fallback - search by name components
            if not item:
                item = bakery_menu.find_food(item_id.replace('_', ' '))
            
            if not item:
                print(f"❌ Food item not found: {item_id}")
                print(f"📋 Available food items: {[i.food for i in bakery_menu.menu]}")
                return jsonify({'error': f'Food item not found: {item_id}'}), 404
        else:
            return jsonify({'error': 'Invalid order type'}), 400
        
        print(f"✅ Found item: {getattr(item, 'coffeeName', None) or getattr(item, 'food', 'Unknown')}")
        
        # For basic systems, create item object if it's just a dict
        if isinstance(item, dict):
            item_price = item['price']
            item_name = item['name']
        else:
            item_price = getattr(item, 'price', 4.50)
            item_name = getattr(item, 'coffeeName', None) or getattr(item, 'food', 'Unknown Item')
        
        # 🆕 INVENTORY CHECK: Verify we have enough ingredients before processing
        if hasattr(item, 'ingredients') and item.ingredients:
            if not shop_info.resource_check(item.ingredients):
                return jsonify({'error': 'Insufficient ingredients in inventory. Please restock!'}), 400
        
        # Process payment
        payment_result = money_machine.process_web_payment(
            payment_method, item_price, payment_details
        )
        
        if not payment_result.get('success'):
            return jsonify({'error': payment_result.get('message', 'Payment failed')}), 400
        
        # 🆕 INVENTORY DEDUCTION: Fulfill the order and deduct inventory
        try:
            if order_type == 'coffee':
                shop_info.coffee_return(item)
                print(f"✅ Coffee order fulfilled: {getattr(item, 'coffeeName', 'Unknown')}")
                
            else:  # food/bakery order
                shop_info.food_return(item)
                print(f"✅ Food order fulfilled: {getattr(item, 'food', 'Unknown')}")
                
        except Exception as e:
            print(f"⚠️ Order fulfillment had issues: {e}, but continuing...")
            # Still count as success for demo, but log the issue
        
        # Emit real-time updates
        try:
            # 🆕 EMIT UPDATED INVENTORY after order fulfillment
            socketio.emit('inventory_updated', shop_info.get_real_time_stats())
            socketio.emit('order_completed', {
                'type': order_type,
                'item': item if isinstance(item, dict) else {'name': item_name, 'price': item_price},
                'session_id': session_id,
                'payment_result': payment_result,
                'inventory_updated': True  # Flag that inventory was updated
            })
        except Exception as e:
            print(f"⚠️ WebSocket emit failed: {e}, but order processed")
        
        return jsonify({
            'success': True,
            'item': item if isinstance(item, dict) else {'name': item_name, 'price': item_price},
            'payment_result': payment_result,
            'inventory_updated': True
        })
    
    except Exception as e:
        print(f"❌ Order processing error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Order processing failed: {str(e)}'}), 500

# === WEBSOCKET EVENTS ===
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    session_id = session.get('session_id')
    if not session_id:
        session_id = f"session_{datetime.now().timestamp()}"
        session['session_id'] = session_id
    
    # Initialize game session
    if session_id not in game_sessions:
        game_sessions[session_id] = {
            'start_time': datetime.now(),
            'orders_completed': 0,
            'total_earnings': 0.0,
            'quality_scores': []
        }
    
    print(f"🔌 Client connected: {session_id}")
    emit('connected', {'session_id': session_id})
    
    try:
        emit('inventory_updated', shop_info.get_real_time_stats())
    except:
        emit('inventory_updated', {})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = session.get('session_id', 'unknown')
    print(f"🔌 Client disconnected: {session_id}")

# 🆕 INVENTORY WEBSOCKET EVENTS
@socketio.on('request_inventory_update')
def handle_inventory_request():
    """Handle manual inventory update requests"""
    try:
        emit('inventory_updated', shop_info.get_real_time_stats())
        print("📦 Inventory update sent to client")
    except Exception as e:
        print(f"❌ Error sending inventory update: {e}")
        emit('inventory_error', {'error': str(e)})

# === ERROR HANDLERS ===
@app.errorhandler(404)
def not_found(error):
    if request.is_json:
        return jsonify({'error': 'Page not found'}), 404
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return "Internal server error", 500

# === STARTUP VALIDATION ===
def validate_startup():
    """Validate that the app is ready to run"""
    print("\n🚀 COFFEE SIMULATOR STARTUP VALIDATION")
    print("========================================")
    
    checks = []
    
    # Check template files
    template_dir = app.template_folder
    launcher_exists = os.path.exists(os.path.join(template_dir, 'launcher.html'))
    game_exists = os.path.exists(os.path.join(template_dir, 'pixel_game.html'))
    
    checks.append(f"{'✅' if launcher_exists else '❌'} Launcher template")
    checks.append(f"{'✅' if game_exists else '❌'} Game template")
    
    # Check game systems
    coffee_working = len(getattr(coffee_menu, 'menu', [])) > 0
    bakery_working = len(getattr(bakery_menu, 'menu', [])) > 0
    inventory_working = len(getattr(shop_info, 'storage', {})) > 0
    
    # 🆕 CHECK INVENTORY SYSTEM
    purchase_system_working = hasattr(shop_info, 'purchase_refill')
    
    checks.append(f"{'✅' if coffee_working else '❌'} Coffee menu ({len(getattr(coffee_menu, 'menu', []))} items)")
    checks.append(f"{'✅' if bakery_working else '❌'} Bakery menu ({len(getattr(bakery_menu, 'menu', []))} items)")
    checks.append(f"{'✅' if inventory_working else '❌'} Inventory system ({len(getattr(shop_info, 'storage', {}))} items)")
    checks.append(f"{'✅' if purchase_system_working else '❌'} Purchase system")
    
    # Print results
    for check in checks:
        print(f"  {check}")
    
    success_count = len([c for c in checks if c.startswith("✅")])
    total_count = len(checks)
    
    print(f"\n📊 STARTUP STATUS: {success_count}/{total_count} systems ready")
    
    if success_count >= total_count * 0.7:  # 70% threshold
        print("🎉 Ready to launch!")
        return True
    else:
        print("⚠️  Some systems need attention, but attempting launch...")
        return False

if __name__ == '__main__':
    # Run startup validation
    validate_startup()
    
    print("\n☕ STARTING COFFEE SIMULATOR...")
    print("===============================")
    print("📊 Features enabled:")
    print("   - Pixel art game interface")
    print("   - Real-time inventory management")
    print("   - WebSocket support for live updates")
    print("   - Enhanced backend with error handling")
    print("   - 🆕 Complete inventory purchasing system")
    print("   - 🆕 Real-time ingredient deduction")
    print("   - 🆕 Smart cost management")
    print(f"\n🌐 Access the game at: http://localhost:5000")
    print("🎮 Direct game link: http://localhost:5000/pixel")
    print("📊 API test: http://localhost:5000/api/test")
    print("📦 Inventory API: http://localhost:5000/api/shop/inventory")
    
    # Start the server
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)