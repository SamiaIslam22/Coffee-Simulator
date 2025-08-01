# backend/enhanced_models/coffee_menu.py
"""
Enhanced Coffee Menu - Preserves original CLI functionality while adding web features
"""
import json
from datetime import datetime

class MenulistWeb:
    """Enhanced version of original Menulist with web-ready features"""
    def __init__(self, coffeeName, water, oatmilk, almondmilk, regmilk, coffeebeans, sugar, price):
        # Preserve original attributes
        self.coffeeName = coffeeName
        self.ingredients = {
            "Water": water,
            "Regular Milk": regmilk,
            "Oat Milk": oatmilk,
            "Almond Milk": almondmilk,
            "Coffee Beans": coffeebeans,
            "Sugar": sugar
        }
        self.price = price
        
        # NEW: Web-specific attributes
        self.prep_time = self._calculate_prep_time()
        self.complexity = self._calculate_complexity()
        self.category = self._get_category()
        self.description = self._generate_description()
    
    def _calculate_prep_time(self):
        """Calculate preparation time based on drink complexity"""
        base_time = 30  # Base 30 seconds
        
        # Add time for milk preparation
        total_milk = self.ingredients["Regular Milk"] + self.ingredients["Oat Milk"] + self.ingredients["Almond Milk"]
        if total_milk > 0:
            base_time += 45  # Steaming milk takes extra time
        
        # Espresso shots take time
        if self.ingredients["Coffee Beans"] > 20:
            base_time += 30  # Extra shot
        
        # Large sizes take longer
        if "large" in self.coffeeName.lower():
            base_time += 15
            
        return base_time
    
    def _calculate_complexity(self):
        """Determine drink complexity for mini-games (1-5 scale)"""
        complexity = 1
        
        # Check for milk steaming
        total_milk = self.ingredients["Regular Milk"] + self.ingredients["Oat Milk"] + self.ingredients["Almond Milk"]
        if total_milk > 0:
            complexity += 2
        
        # Espresso complexity
        if self.ingredients["Coffee Beans"] > 20:
            complexity += 1
        
        # Cappuccino has more foam complexity
        if "cappuccino" in self.coffeeName.lower():
            complexity += 1
            
        return min(complexity, 5)
    
    def _get_category(self):
        """Categorize the coffee type"""
        name_lower = self.coffeeName.lower()
        if "latte" in name_lower:
            return "latte"
        elif "cappuccino" in name_lower:
            return "cappuccino"
        elif "expresso" in name_lower:
            return "espresso"
        else:
            return "specialty"
    
    def _generate_description(self):
        """Generate appealing description for web display"""
        descriptions = {
            "latte": "Smooth espresso with steamed milk and a light foam layer",
            "cappuccino": "Rich espresso topped with thick, creamy foam",
            "espresso": "Pure, concentrated coffee shot with rich crema",
            "specialty": "Our signature coffee creation"
        }
        
        size = "Large" if "large" in self.coffeeName.lower() else "Medium"
        milk_type = ""
        
        if self.ingredients["Oat Milk"] > 0:
            milk_type = " with creamy oat milk"
        elif self.ingredients["Almond Milk"] > 0:
            milk_type = " with smooth almond milk"
        elif self.ingredients["Regular Milk"] > 0:
            milk_type = " with fresh dairy milk"
        
        temperature = "hot" if "ice" not in self.coffeeName.lower() else "iced"
        
        return f"{size} {temperature} {descriptions[self.category]}{milk_type}"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.coffeeName.lower().replace(' ', '_'),
            'name': self.coffeeName,
            'price': self.price,
            'ingredients': self.ingredients,
            'prep_time': self.prep_time,
            'complexity': self.complexity,
            'category': self.category,
            'description': self.description,
            'image_url': f"/static/images/coffee/{self.category}.jpg"
        }
    
    def get_mini_game_config(self):
        """Return configuration for coffee-making mini-games"""
        return {
            'espresso_timing': {
                'target_time': 25 + (self.complexity * 2),
                'tolerance': 3
            },
            'milk_steaming': {
                'target_temp': 65,
                'target_foam': 'light' if 'latte' in self.coffeeName.lower() else 'thick',
                'time_limit': 45
            },
            'pour_precision': {
                'pattern_required': self.complexity >= 3,
                'speed_bonus': True
            }
        }


class CoffeeMenuWeb:
    """Enhanced version of original CoffeeMenu with web capabilities"""
    
    def __init__(self):
        # Preserve all original menu items but use enhanced class
        self.menu = [
            MenulistWeb(coffeeName="medium regularmilk hot latte", water=160, regmilk=110, oatmilk=0, almondmilk=0, coffeebeans=14, sugar=2, price=4.50),
            MenulistWeb(coffeeName="medium oatmilk hot latte", water=160, oatmilk=110, regmilk=0, almondmilk=0, coffeebeans=14, sugar=2, price=4.70),
            MenulistWeb(coffeeName="medium almondmilk hot latte", water=160, almondmilk=110, oatmilk=0, regmilk=0, coffeebeans=14, sugar=2, price=4.70),
            MenulistWeb(coffeeName="medium regularmilk ice latte", water=170, regmilk=80, oatmilk=0, almondmilk=0, coffeebeans=14, sugar=2, price=4.50),
            MenulistWeb(coffeeName="medium oatmilk ice latte", water=170, oatmilk=80, regmilk=0, almondmilk=0, coffeebeans=14, sugar=2, price=4.70),
            MenulistWeb(coffeeName="medium almondmilk ice latte", water=170, almondmilk=80, oatmilk=0, regmilk=0, coffeebeans=14, sugar=2, price=4.70),
            MenulistWeb(coffeeName="large regularmilk hot latte", water=200, regmilk=150, oatmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.50),
            MenulistWeb(coffeeName="large oatmilk hot latte", water=200, oatmilk=150, regmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.70),
            MenulistWeb(coffeeName="large almondmilk hot latte", water=200, almondmilk=150, oatmilk=0, regmilk=0, coffeebeans=24, sugar=3, price=5.70),
            MenulistWeb(coffeeName="large regularmilk ice latte", water=210, regmilk=110, oatmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.50),
            MenulistWeb(coffeeName="large oatmilk ice latte", water=210, oatmilk=110, regmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.70),
            MenulistWeb(coffeeName="large almondmilk ice latte", water=210, almondmilk=110, oatmilk=0, regmilk=0, coffeebeans=24, sugar=3, price=5.70),
            MenulistWeb(coffeeName="medium hot expresso", water=50, regmilk=0, oatmilk=0, almondmilk=0, sugar=2, coffeebeans=24, price=4.70),
            MenulistWeb(coffeeName="large hot expresso", water=50, regmilk=0, oatmilk=0, almondmilk=0, sugar=3, coffeebeans=24, price=5.70),
            MenulistWeb(coffeeName="medium regularmilk hot cappuccino", water=200, regmilk=50, oatmilk=0, almondmilk=0, coffeebeans=18, sugar=2, price=4.70),
            MenulistWeb(coffeeName="medium oatmilk hot cappuccino", water=200, oatmilk=50, regmilk=0, almondmilk=0, coffeebeans=18, sugar=2, price=4.90),
            MenulistWeb(coffeeName="medium almondmilk hot cappuccino", water=200, almondmilk=50, oatmilk=0, regmilk=0, coffeebeans=18, sugar=2, price=4.90),
            MenulistWeb(coffeeName="medium regularmilk ice cappuccino", water=210, regmilk=50, oatmilk=0, almondmilk=0, coffeebeans=18, sugar=2, price=4.70),
            MenulistWeb(coffeeName="medium oatmilk ice cappuccino", water=210, oatmilk=50, regmilk=0, almondmilk=0, coffeebeans=18, sugar=2, price=4.90),
            MenulistWeb(coffeeName="medium almondmilk ice cappuccino", water=210, almondmilk=50, oatmilk=0, regmilk=0, coffeebeans=18, sugar=2, price=4.90),
            MenulistWeb(coffeeName="large regularmilk hot cappuccino", water=250, regmilk=70, oatmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.70),
            MenulistWeb(coffeeName="large oatmilk hot cappuccino", water=250, oatmilk=70, regmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.90),
            MenulistWeb(coffeeName="large almondmilk hot cappuccino", water=250, almondmilk=70, oatmilk=0, regmilk=0, coffeebeans=24, sugar=3, price=5.90),
            MenulistWeb(coffeeName="large regularmilk ice cappuccino", water=260, regmilk=50, oatmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.70),
            MenulistWeb(coffeeName="large oatmilk ice cappuccino", water=260, oatmilk=50, regmilk=0, almondmilk=0, coffeebeans=24, sugar=3, price=5.90),
            MenulistWeb(coffeeName="large almondmilk ice cappuccino", water=260, almondmilk=50, oatmilk=0, regmilk=0, coffeebeans=24, sugar=3, price=5.90),
        ]
    
    # PRESERVE: Original method for backward compatibility
    def coffee(self):
        """Original CLI display method"""
        given_option = ""
        for item in self.menu:
            given_option += f"☕{item.coffeeName} ${item.price:.2f}☕ \n"
        return given_option
    
    # PRESERVE: Original find method
    def find_coffee(self, orderName):
        """Original CLI search method"""
        for item in self.menu:
            if item.coffeeName.lower() == orderName.lower():
                return item
        return None
    
    # NEW: Web-specific methods
    def get_menu_json(self):
        """Return menu as JSON for web API"""
        return json.dumps([item.to_dict() for item in self.menu], indent=2)
    
    def get_menu_by_category(self):
        """Group menu items by category for web display"""
        categories = {}
        for item in self.menu:
            category = item.category
            if category not in categories:
                categories[category] = []
            categories[category].append(item.to_dict())
        return categories
    
    def get_featured_items(self, count=3):
        """Get featured menu items for homepage"""
        # Sort by complexity and price for featured selection
        featured = sorted(self.menu, key=lambda x: (x.complexity, x.price), reverse=True)[:count]
        return [item.to_dict() for item in featured]
    
    def search_menu(self, query):
        """Enhanced search for web interface"""
        results = []
        query_lower = query.lower()
        
        for item in self.menu:
            # Search in name, category, and description
            if (query_lower in item.coffeeName.lower() or 
                query_lower in item.category.lower() or 
                query_lower in item.description.lower()):
                results.append(item.to_dict())
        
        return results
    
    def get_coffee_by_id(self, coffee_id):
        """Find coffee by web-friendly ID"""
        for item in self.menu:
            if item.coffeeName.lower().replace(' ', '_') == coffee_id:
                return item
        return None
    def get_coffee_by_id_enhanced(self, coffee_id):
        """Enhanced coffee finding with multiple matching strategies"""
        print(f"🔍 Looking for coffee with ID: '{coffee_id}'")
        
        # Strategy 1: Exact ID match (web-friendly format)
        for item in self.menu:
            item_id = item.coffeeName.lower().replace(' ', '_')
            if item_id == coffee_id:
                print(f"✅ Found exact ID match: {item.coffeeName}")
                return item
        
        # Strategy 2: Exact name match
        for item in self.menu:
            if item.coffeeName.lower() == coffee_id.lower():
                print(f"✅ Found exact name match: {item.coffeeName}")
                return item
        
        # Strategy 3: Name with underscores converted to spaces
        search_name = coffee_id.replace('_', ' ')
        for item in self.menu:
            if item.coffeeName.lower() == search_name.lower():
                print(f"✅ Found underscore-converted match: {item.coffeeName}")
                return item
        
        # Strategy 4: Component-based fuzzy matching
        search_components = coffee_id.lower().replace('_', ' ').split()
        for item in self.menu:
            item_name_lower = item.coffeeName.lower()
            matches = sum(1 for component in search_components if component in item_name_lower)
            if matches >= len(search_components) - 1:  # Allow 1 missing component
                print(f"✅ Found fuzzy match: {item.coffeeName} (matched {matches}/{len(search_components)} components)")
                return item
        
        print(f"❌ No match found for '{coffee_id}'")
        print(f"📋 Available items: {[item.coffeeName for item in self.menu[:5]]}...")  # Show first 5 for debugging
        return None
    def get_preparation_queue(self, orders):
        """Optimize preparation order for efficiency"""
        # Sort orders by preparation time and complexity
        return sorted(orders, key=lambda x: (x['prep_time'], x['complexity']))


# Example usage and testing
if __name__ == "__main__":
    # Test backward compatibility
    coffee_menu = CoffeeMenuWeb()
    
    # Original CLI functionality still works
    print("=== ORIGINAL CLI FUNCTIONALITY ===")
    print(coffee_menu.coffee())
    
    found_item = coffee_menu.find_coffee("medium oatmilk hot latte")
    if found_item:
        print(f"Found: {found_item.coffeeName} - ${found_item.price}")
    
    # New web functionality
    print("\n=== NEW WEB FUNCTIONALITY ===")
    print("Featured Items:")
    for item in coffee_menu.get_featured_items():
        print(f"- {item['name']}: {item['description']}")
    
    print(f"\nMenu Categories: {list(coffee_menu.get_menu_by_category().keys())}")
    
    search_results = coffee_menu.search_menu("latte")
    print(f"\nSearch 'latte' found {len(search_results)} results")