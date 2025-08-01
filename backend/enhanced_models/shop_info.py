# backend/enhanced_models/shop_info.py
"""
Enhanced Shop Info - Preserves original CLI functionality while adding web features
ENHANCED: Added inventory purchasing system with earnings integration
"""
import json
from datetime import datetime
from typing import Dict, List, Optional

class ShopInfoWeb:
    """Enhanced version of original ShopInfo with real-time web capabilities"""
    
    def __init__(self):
        # PRESERVE: Original storage dictionary
        self.storage = {
            "Water": 100000000,
            "Oat Milk": 700,
            "Regular Milk": 800,
            "Almond Milk": 700,
            "Sugar": 100,
            "Coffee Beans": 100,
            "Plain Bagel": 4,
            "Strawberry Cake": 3,
            "Sesameseed Bagel": 4,
            "Honey Bun": 2,
            "Cinnamon Roll": 2,
            "Croissant": 4
        }
        
        # PRESERVE: Web-specific attributes
        self.max_storage = self.storage.copy()  # Track maximum capacity
        self.low_stock_threshold = {
            "Water": 1000000,
            "Oat Milk": 100,
            "Regular Milk": 100,
            "Almond Milk": 100,
            "Sugar": 20,
            "Coffee Beans": 20,
            "Plain Bagel": 1,
            "Strawberry Cake": 1,
            "Sesameseed Bagel": 1,
            "Honey Bun": 1,
            "Cinnamon Roll": 1,
            "Croissant": 1
        }
        
        # NEW: Ingredient purchasing system
        self.ingredient_prices = {
            "Water": 0.001,  # Very cheap since it's in ml
            "Oat Milk": 0.008,  # $5.60 to refill from 0
            "Regular Milk": 0.006,  # $4.80 to refill from 0
            "Almond Milk": 0.009,  # $6.30 to refill from 0
            "Sugar": 0.05,  # $5.00 to refill from 0
            "Coffee Beans": 0.15,  # $15.00 to refill from 0
            "Plain Bagel": 1.50,  # $6.00 to refill from 0
            "Strawberry Cake": 2.00,  # $6.00 to refill from 0
            "Sesameseed Bagel": 1.75,  # $7.00 to refill from 0
            "Honey Bun": 2.50,  # $5.00 to refill from 0
            "Cinnamon Roll": 2.25,  # $4.50 to refill from 0
            "Croissant": 1.50   # $6.00 to refill from 0
        }
        
        self.usage_history = []  # Track ingredient usage over time
        self.restock_log = []   # Track restocking events
        self.purchase_history = []  # Track ingredient purchases
    
    # PRESERVE: Original methods for backward compatibility
    def storagereport(self):
        """Original CLI storage report method"""
        print(f"Water: {self.storage['Water']}ml")
        print(f"Oat Milk: {self.storage['Oat Milk']}ml")
        print(f"Coffee Beans: {self.storage['Coffee Beans']}g")
        print(f"Regular Milk: {self.storage['Regular Milk']}ml")
        print(f"Almond Milk: {self.storage['Almond Milk']}ml")
        print(f"Sugar: {self.storage['Sugar']}g")
        print(f"Plain Bagel: {self.storage['Plain Bagel']}")
        print(f"Strawberry Cake: {self.storage['Strawberry Cake']}")
        print(f"Sesameseed Bagel: {self.storage['Sesameseed Bagel']}")
        print(f"Honey Bun: {self.storage['Honey Bun']}")
        print(f"Cinnamon Roll: {self.storage['Cinnamon Roll']}")
        print(f"Croissant: {self.storage['Croissant']}")
    
    def resource_check(self, ingredients):
        """Original resource checking method"""
        for item, quantity in ingredients.items():
            if quantity > self.storage.get(item, 0):
                print(f"Sorry, we have run out of {item}. Please choose something else.")
                return False
        return True
    
    def coffee_return(self, coffee_order):
        """Original coffee fulfillment method"""
        for item, quantity in coffee_order.ingredients.items():
            if self.storage.get(item, 0) >= quantity:
                self.storage[item] -= quantity
                self._log_usage(item, quantity, 'coffee', coffee_order.coffeeName)
        print(f"Here is your {coffee_order.coffeeName}. Enjoy!")
    
    def food_return(self, food_order):
        """Original food fulfillment method"""
        for item, quantity in food_order.ingredients.items():
            if self.storage.get(item, 0) >= quantity:
                self.storage[item] -= quantity
                self._log_usage(item, quantity, 'food', food_order.food)
        print(f"Here is your {food_order.food}. Enjoy!")
    
    # PRESERVE: Web-specific methods
    def _log_usage(self, item: str, quantity: int, order_type: str, product_name: str):
        """Log ingredient usage for analytics"""
        self.usage_history.append({
            'timestamp': datetime.now().isoformat(),
            'item': item,
            'quantity': quantity,
            'order_type': order_type,
            'product': product_name,
            'remaining': self.storage[item]
        })
    
    def get_real_time_stats(self) -> Dict:
        """Return real-time inventory stats for web dashboard"""
        stats = {}
        
        for item, current_amount in self.storage.items():
            max_amount = self.max_storage[item]
            low_threshold = self.low_stock_threshold[item]
            
            percentage = (current_amount / max_amount) * 100
            status = 'good'
            
            if current_amount <= 0:
                status = 'out'
            elif current_amount <= low_threshold:
                status = 'low'
            elif percentage < 30:
                status = 'warning'
            
            stats[item] = {
                'current': current_amount,
                'max': max_amount,
                'percentage': round(percentage, 1),
                'status': status,
                'low_threshold': low_threshold,
                'unit': self._get_unit(item),
                'price_per_unit': self.ingredient_prices.get(item, 0),
                'refill_cost': self._calculate_refill_cost(item, current_amount)
            }
        
        return stats
    
    def _get_unit(self, item: str) -> str:
        """Get appropriate unit for each ingredient"""
        if item in ["Water", "Oat Milk", "Regular Milk", "Almond Milk"]:
            return "ml"
        elif item in ["Coffee Beans", "Sugar"]:
            return "g"
        else:
            return "units"
    
    def _calculate_refill_cost(self, item: str, current_amount: int) -> float:
        """Calculate cost to refill item to maximum capacity"""
        max_amount = self.max_storage[item]
        needed_amount = max_amount - current_amount
        price_per_unit = self.ingredient_prices.get(item, 0)
        return round(needed_amount * price_per_unit, 2)
    
    # NEW: Inventory purchasing methods
    def can_purchase_refill(self, item: str, player_money: float) -> Dict:
        """Check if player can afford to refill an ingredient"""
        if item not in self.storage:
            return {'can_afford': False, 'reason': 'Invalid item'}
        
        current_amount = self.storage[item]
        max_amount = self.max_storage[item]
        needed_amount = max_amount - current_amount
        
        if needed_amount <= 0:
            return {'can_afford': False, 'reason': 'Already at maximum capacity'}
        
        refill_cost = self._calculate_refill_cost(item, current_amount)
        
        if player_money < refill_cost:
            return {
                'can_afford': False, 
                'reason': f'Not enough money. Need ${refill_cost:.2f}, have ${player_money:.2f}'
            }
        
        return {
            'can_afford': True,
            'cost': refill_cost,
            'needed_amount': needed_amount,
            'current': current_amount,
            'max': max_amount
        }
    
    def purchase_refill(self, item: str, player_money: float) -> Dict:
        """Purchase ingredients to refill to maximum capacity"""
        purchase_check = self.can_purchase_refill(item, player_money)
        
        if not purchase_check['can_afford']:
            return {
                'success': False,
                'message': purchase_check['reason'],
                'money_spent': 0,
                'money_remaining': player_money
            }
        
        # Process the purchase
        cost = purchase_check['cost']
        needed_amount = purchase_check['needed_amount']
        
        # Update inventory
        self.storage[item] = self.max_storage[item]
        
        # Log the purchase
        purchase_record = {
            'timestamp': datetime.now().isoformat(),
            'item': item,
            'amount_purchased': needed_amount,
            'cost': cost,
            'new_total': self.storage[item]
        }
        self.purchase_history.append(purchase_record)
        
        # Log as restock event too
        self.restock_log.append({
            'timestamp': datetime.now().isoformat(),
            'item': item,
            'requested': needed_amount,
            'actual': needed_amount,
            'new_total': self.storage[item],
            'method': 'purchase',
            'cost': cost
        })
        
        return {
            'success': True,
            'message': f'Successfully refilled {item}! Added {needed_amount} {self._get_unit(item)}',
            'money_spent': cost,
            'money_remaining': player_money - cost,
            'item': item,
            'amount_added': needed_amount,
            'new_inventory': self.storage[item]
        }
    
    def get_shopping_list(self, player_money: float) -> List[Dict]:
        """Get list of items that can be purchased with current money"""
        shopping_list = []
        
        for item, current_amount in self.storage.items():
            if current_amount < self.max_storage[item]:
                refill_cost = self._calculate_refill_cost(item, current_amount)
                needed_amount = self.max_storage[item] - current_amount
                
                shopping_list.append({
                    'item': item,
                    'current': current_amount,
                    'max': self.max_storage[item],
                    'needed': needed_amount,
                    'cost': refill_cost,
                    'affordable': player_money >= refill_cost,
                    'priority': 'high' if current_amount <= self.low_stock_threshold[item] else 'low',
                    'unit': self._get_unit(item),
                    'percentage': round((current_amount / self.max_storage[item]) * 100, 1)
                })
        
        # Sort by priority (high first), then by affordability, then by cost
        shopping_list.sort(key=lambda x: (
            x['priority'] != 'high',  # High priority first
            not x['affordable'],      # Affordable first
            x['cost']                 # Cheaper first
        ))
        
        return shopping_list
    
    def get_low_stock_items(self) -> List[Dict]:
        """Get items that are running low and need restocking"""
        low_stock = []
        
        for item, current_amount in self.storage.items():
            threshold = self.low_stock_threshold[item]
            if current_amount <= threshold:
                low_stock.append({
                    'item': item,
                    'current': current_amount,
                    'threshold': threshold,
                    'max': self.max_storage[item],
                    'urgency': 'critical' if current_amount <= 0 else 'low',
                    'refill_cost': self._calculate_refill_cost(item, current_amount),
                    'unit': self._get_unit(item)
                })
        
        return sorted(low_stock, key=lambda x: (x['urgency'] != 'critical', x['current']))
    
    # PRESERVE: Existing web methods (updated with purchase info)
    def get_inventory_alerts(self) -> List[Dict]:
        """Get list of inventory items needing attention"""
        alerts = []
        
        for item, current_amount in self.storage.items():
            if current_amount <= 0:
                alerts.append({
                    'item': item,
                    'level': 'critical',
                    'message': f"{item} is out of stock!",
                    'action': 'restock_immediately',
                    'cost': self._calculate_refill_cost(item, current_amount)
                })
            elif current_amount <= self.low_stock_threshold[item]:
                alerts.append({
                    'item': item,
                    'level': 'warning',
                    'message': f"{item} is running low ({current_amount} {self._get_unit(item)} remaining)",
                    'action': 'restock_soon',
                    'cost': self._calculate_refill_cost(item, current_amount)
                })
        
        return sorted(alerts, key=lambda x: x['level'] == 'critical', reverse=True)
    
    def get_purchase_history(self, days: int = 7) -> List[Dict]:
        """Get recent purchase history"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_purchases = [
            p for p in self.purchase_history 
            if datetime.fromisoformat(p['timestamp']) > cutoff_date
        ]
        
        return sorted(recent_purchases, key=lambda x: x['timestamp'], reverse=True)
    
    def to_json(self) -> str:
        """Convert current state to JSON for web API"""
        return json.dumps({
            'inventory': self.get_real_time_stats(),
            'alerts': self.get_inventory_alerts(),
            'last_updated': datetime.now().isoformat()
        }, indent=2)


# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced functionality
    shop = ShopInfoWeb()
    
    print("=== ORIGINAL CLI FUNCTIONALITY ===")
    shop.storagereport()
    
    # Test purchasing system
    print("\n=== NEW PURCHASING SYSTEM ===")
    player_money = 50.00
    
    # Simulate some usage to create low stock
    shop.storage["Coffee Beans"] = 5  # Low stock
    shop.storage["Plain Bagel"] = 0   # Out of stock
    
    # Get shopping list
    shopping_list = shop.get_shopping_list(player_money)
    print(f"Shopping list with ${player_money}:")
    for item in shopping_list[:3]:  # Show top 3
        affordable = "✅" if item['affordable'] else "❌"
        print(f"{affordable} {item['item']}: ${item['cost']:.2f} (need {item['needed']} {item['unit']})")
    
    # Test purchasing
    print(f"\nTrying to buy Coffee Beans...")
    result = shop.purchase_refill("Coffee Beans", player_money)
    if result['success']:
        print(f"✅ {result['message']}")
        print(f"💰 Money left: ${result['money_remaining']:.2f}")
        player_money = result['money_remaining']
    else:
        print(f"❌ {result['message']}")
    
    # Check alerts
    alerts = shop.get_inventory_alerts()
    print(f"\nInventory alerts: {len(alerts)} items need attention")
    for alert in alerts[:2]:
        print(f"⚠️ {alert['message']} (Cost to refill: ${alert['cost']:.2f})")