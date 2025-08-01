# backend/enhanced_models/bakery_item.py
"""
Enhanced Bakery Item - Preserves original CLI functionality while adding web features
"""
import json
from datetime import datetime

class BakeryItemWeb:
    """Enhanced version of original BakeryItem with web-ready features"""
    def __init__(self, food, price, plainbagels, strawberrycake, sesbagel, honeybun, cinnamonroll, croissant):
        # PRESERVE: Original attributes exactly as they were
        self.food = food
        self.price = price
        self.ingredients = {
            "Plain Bagel": plainbagels,
            "Strawberry Cake": strawberrycake,
            "Sesameseed Bagel": sesbagel,
            "Honey Bun": honeybun,
            "Cinnamon Roll": cinnamonroll,
            "Croissant": croissant
        }
        
        # NEW: Web-specific attributes
        self.prep_time = self._calculate_prep_time()
        self.category = self._get_category()
        self.dietary_info = self._get_dietary_info()
        self.description = self._generate_description()
        self.popularity_score = self._calculate_popularity()
        self.warming_required = self._needs_warming()
    
    def _calculate_prep_time(self):
        """Calculate preparation time based on item type"""
        prep_times = {
            "Plain Bagel": 60,      # Slice and toast
            "Strawberry Cake": 30,   # Just plate
            "Sesameseed Bagel": 60,  # Slice and toast
            "Honey Bun": 45,        # Warm slightly
            "Cinnamon Roll": 90,    # Warm and glaze
            "Croissant": 75         # Warm and prepare
        }
        return prep_times.get(self.food, 45)
    
    def _get_category(self):
        """Categorize the bakery item"""
        if "bagel" in self.food.lower():
            return "bagels"
        elif "cake" in self.food.lower():
            return "desserts"
        elif "bun" in self.food.lower() or "roll" in self.food.lower():
            return "pastries"
        elif "croissant" in self.food.lower():
            return "pastries"
        else:
            return "specialty"
    
    def _get_dietary_info(self):
        """Get dietary information for web display"""
        info = {
            "vegetarian": True,  # All bakery items are vegetarian
            "vegan": False,      # Most contain dairy/eggs
            "gluten_free": False, # All contain wheat
            "nut_free": True     # No nuts in these items
        }
        
        # Special cases
        if "sesame" in self.food.lower():
            info["allergens"] = ["sesame", "gluten"]
        else:
            info["allergens"] = ["gluten", "dairy", "eggs"]
            
        return info
    
    def _generate_description(self):
        """Generate appealing description for web display"""
        descriptions = {
            "Plain Bagel": "Freshly baked bagel, toasted to perfection. Simple and satisfying.",
            "Strawberry Cake": "Moist vanilla cake layered with fresh strawberry filling and cream.",
            "Sesameseed Bagel": "Traditional bagel topped with toasted sesame seeds for extra flavor.",
            "Honey Bun": "Sweet, soft pastry glazed with golden honey. A morning favorite.",
            "Cinnamon Roll": "Warm, spiral pastry with cinnamon sugar filling and sweet glaze.",
            "Croissant": "Buttery, flaky French pastry with golden, crispy layers."
        }
        return descriptions.get(self.food, "Delicious bakery item made fresh daily.")
    
    def _calculate_popularity(self):
        """Calculate popularity score for recommendations (1-10)"""
        # Based on typical bakery popularity and price point
        popularity = {
            "Plain Bagel": 8,      # Classic choice
            "Croissant": 7,        # Popular but pricier
            "Cinnamon Roll": 9,    # Very popular
            "Strawberry Cake": 6,  # Dessert item
            "Sesameseed Bagel": 7, # Good alternative
            "Honey Bun": 5         # Less common
        }
        return popularity.get(self.food, 5)
    
    def _needs_warming(self):
        """Check if item should be warmed before serving"""
        warm_items = ["Honey Bun", "Cinnamon Roll", "Croissant"]
        return self.food in warm_items
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.food.lower().replace(' ', '_'),
            'name': self.food,
            'price': self.price,
            'ingredients': self.ingredients,
            'prep_time': self.prep_time,
            'category': self.category,
            'description': self.description,
            'dietary_info': self.dietary_info,
            'popularity_score': self.popularity_score,
            'warming_required': self.warming_required,
            'image_url': f"/static/images/bakery/{self.category}.jpg"
        }
    
    def get_preparation_steps(self):
        """Get step-by-step preparation for mini-games"""
        steps = {
            "Plain Bagel": [
                {"action": "slice", "duration": 10, "description": "Slice bagel in half"},
                {"action": "toast", "duration": 45, "description": "Toast until golden brown"},
                {"action": "serve", "duration": 5, "description": "Place on plate"}
            ],
            "Strawberry Cake": [
                {"action": "slice", "duration": 15, "description": "Cut perfect slice"},
                {"action": "plate", "duration": 10, "description": "Place on dessert plate"},
                {"action": "garnish", "duration": 5, "description": "Add finishing touches"}
            ],
            "Cinnamon Roll": [
                {"action": "warm", "duration": 60, "description": "Warm in oven"},
                {"action": "glaze", "duration": 20, "description": "Apply fresh glaze"},
                {"action": "serve", "duration": 10, "description": "Serve while warm"}
            ]
        }
        
        # Default steps for items not specifically defined
        default_steps = [
            {"action": "prepare", "duration": 20, "description": f"Prepare {self.food}"},
            {"action": "warm", "duration": 25, "description": "Warm if needed"},
            {"action": "serve", "duration": 5, "description": "Present to customer"}
        ]
        
        return steps.get(self.food, default_steps)


class BakeryMenuWeb:
    """Enhanced version of original BakeryMenu with web capabilities"""
    
    def __init__(self):
        # PRESERVE: All original menu items but use enhanced class
        self.menu = [
            BakeryItemWeb(food="Plain Bagel", price=3.00, plainbagels=1, strawberrycake=0, sesbagel=0, honeybun=0, cinnamonroll=0, croissant=0),
            BakeryItemWeb(food="Strawberry Cake", price=4.00, plainbagels=0, strawberrycake=1, sesbagel=0, honeybun=0, cinnamonroll=0, croissant=0),
            BakeryItemWeb(food="Sesameseed Bagel", price=3.50, plainbagels=0, strawberrycake=0, sesbagel=1, honeybun=0, cinnamonroll=0, croissant=0),
            BakeryItemWeb(food="Honey Bun", price=4.00, plainbagels=0, strawberrycake=0, sesbagel=0, honeybun=1, cinnamonroll=0, croissant=0),
            BakeryItemWeb(food="Cinnamon Roll", price=3.70, plainbagels=0, strawberrycake=0, sesbagel=0, honeybun=0, cinnamonroll=2, croissant=0),
            BakeryItemWeb(food="Croissant", price=3.00, plainbagels=0, strawberrycake=0, sesbagel=0, honeybun=0, cinnamonroll=0, croissant=1),
        ]
    
    # PRESERVE: Original method for backward compatibility
    def find_food(self, orderName):
        """Original CLI search method"""
        for item in self.menu:
            if item.food.lower() == orderName.lower():
                return item
        return None
    
    # NEW: Web-specific methods
    def get_menu_display(self):
        """Get formatted menu for CLI display (preserves original format)"""
        menu_text = ""
        for item in self.menu:
            menu_text += f" {item.food} (${item.price:.2f}) \n"
        return menu_text
    
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
    
    def get_popular_items(self, count=3):
        """Get most popular bakery items"""
        popular = sorted(self.menu, key=lambda x: x.popularity_score, reverse=True)[:count]
        return [item.to_dict() for item in popular]
    
    def get_quick_items(self):
        """Get items that can be prepared quickly"""
        quick_items = [item for item in self.menu if item.prep_time <= 60]
        return [item.to_dict() for item in quick_items]
    
    def search_menu(self, query):
        """Enhanced search for web interface"""
        results = []
        query_lower = query.lower()
        
        for item in self.menu:
            # Search in name, category, and description
            if (query_lower in item.food.lower() or 
                query_lower in item.category.lower() or 
                query_lower in item.description.lower()):
                results.append(item.to_dict())
        
        return results
    
    def get_food_by_id(self, food_id):
        """Find food by web-friendly ID"""
        for item in self.menu:
            if item.food.lower().replace(' ', '_') == food_id:
                return item
        return None
    def get_food_by_id_enhanced(self, food_id):
        """Enhanced food finding with multiple matching strategies"""
        print(f"🔍 Looking for food with ID: '{food_id}'")
        
        # Strategy 1: Exact ID match (web-friendly format)
        for item in self.menu:
            item_id = item.food.lower().replace(' ', '_')
            if item_id == food_id:
                print(f"✅ Found exact ID match: {item.food}")
                return item
        
        # Strategy 2: Exact name match
        for item in self.menu:
            if item.food.lower() == food_id.lower():
                print(f"✅ Found exact name match: {item.food}")
                return item
        
        # Strategy 3: Name with underscores converted to spaces
        search_name = food_id.replace('_', ' ')
        for item in self.menu:
            if item.food.lower() == search_name.lower():
                print(f"✅ Found underscore-converted match: {item.food}")
                return item
        
        # Strategy 4: Component-based fuzzy matching
        search_components = food_id.lower().replace('_', ' ').split()
        for item in self.menu:
            item_name_lower = item.food.lower()
            matches = sum(1 for component in search_components if component in item_name_lower)
            if matches >= len(search_components) - 1:  # Allow 1 missing component
                print(f"✅ Found fuzzy match: {item.food} (matched {matches}/{len(search_components)} components)")
                return item
        
        print(f"❌ No match found for '{food_id}'")
        print(f"📋 Available items: {[item.food for item in self.menu]}")
        return None
    def get_dietary_filtered_menu(self, dietary_restrictions):
        """Filter menu by dietary restrictions"""
        filtered = []
        
        for item in self.menu:
            dietary_info = item.dietary_info
            suitable = True
            
            # Check each restriction
            for restriction in dietary_restrictions:
                if restriction == 'vegetarian' and not dietary_info.get('vegetarian', False):
                    suitable = False
                    break
                elif restriction == 'vegan' and not dietary_info.get('vegan', False):
                    suitable = False
                    break
                elif restriction == 'gluten_free' and not dietary_info.get('gluten_free', False):
                    suitable = False
                    break
            
            if suitable:
                filtered.append(item.to_dict())
        
        return filtered
    
    def get_preparation_queue(self, orders):
        """Optimize preparation order for efficiency"""
        # Sort by warming requirement first, then by prep time
        return sorted(orders, key=lambda x: (not x.get('warming_required', False), x.get('prep_time', 0)))


# Example usage and testing
if __name__ == "__main__":
    # Test backward compatibility
    bakery_menu = BakeryMenuWeb()
    
    print("=== ORIGINAL CLI FUNCTIONALITY ===")
    print("Menu Display:")
    print(bakery_menu.get_menu_display())
    
    found_item = bakery_menu.find_food("Plain Bagel")
    if found_item:
        print(f"Found: {found_item.food} - ${found_item.price}")
    
    # New web functionality
    print("\n=== NEW WEB FUNCTIONALITY ===")
    print("Popular Items:")
    for item in bakery_menu.get_popular_items():
        print(f"- {item['name']}: {item['description']}")
    
    print(f"\nMenu Categories: {list(bakery_menu.get_menu_by_category().keys())}")
    
    search_results = bakery_menu.search_menu("bagel")
    print(f"\nSearch 'bagel' found {len(search_results)} results")
    
    quick_items = bakery_menu.get_quick_items()
    print(f"Quick preparation items: {len(quick_items)}")