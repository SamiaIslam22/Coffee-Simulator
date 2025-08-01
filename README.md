<img width="1274" height="878" alt="image" src="https://github.com/user-attachments/assets/d5368ff8-22c7-4d5c-9be7-b048a446a41f" />

# ☕ Coffee Simulator - From CLI to Web Game

**A Journey of Growth: Transforming My First Python Project into an Interactive Web Experience**

---

## 🎯 Project Overview

This Coffee Simulator represents more than just a coding project—it's a testament to growth, learning, and the sentimental value of our programming journey. What started as a simple command-line interface (CLI) application during my freshman year has evolved into a fully interactive web-based game.

### The Story Behind the Code

This coffee shop simulator was my very first Python project during my freshman year of college. It was a simple terminal-based application where everything happened through text - you'd see menu options in the terminal, select items by typing numbers, and watch text responses scroll by. Basic classes, simple input/output, and a lot of trial and error.

Now, as I'm in my senior year, I wanted to transform this precious piece of my programming journey. I know this might seem like a silly project, or maybe not as robust as regular Python projects that others might build. But this holds precious memories of my youth that I want to hold onto and make better.

It's not about building the most complex system. It's about showing that it doesn't matter if the starting point feels so small and insignificant. What matters is how you grow and make it better - day by day, month by month, and for me, semester by semester.

What started as 200 lines of basic Python with simple `input()` and `print()` statements has evolved into a full-stack web application with real-time inventory management, customer AI, and interactive gameplay. But every coffee option, every bakery item, every piece of business logic from that original freshman project is still here, preserved and enhanced.

---

## 🎮 How to Play

### Getting Started

1. **Launch the Game**
   - Visit the main page and click "Let's Play!"
   - The game loads with a pixel art coffee shop environment
   - You'll see your earnings, customer count, rating, and target in the top-left corner

2. **Serving Customers**
   - Click the "🚶‍♂️ Call Next Customer" button to spawn a new customer
   - Watch as they walk to your counter following an L-shaped path
   - When they arrive, they'll show a speech bubble with their order and preferred payment method
   - Click on the customer to open the order menu

3. **Taking Orders**
   
   **For Coffee Drinks:**
   - Step 1: Choose "☕ Coffee Drinks"
   - Step 2: Select drink type (Latte, Cappuccino, or Espresso)
   - Step 3: Choose temperature (Hot or Iced)
   - Step 4: Pick size (Medium or Large)
   - Step 5: Select milk type (Regular, Oat, or Almond) - *Skip for Espresso*
   - Step 6: Choose payment method (Cash or Card)
   
   **For Bakery Items:**
   - Step 1: Choose "🥐 Bakery Items"
   - Step 2: Select from 6 bakery options (Plain Bagel, Strawberry Cake, etc.)
   - Step 3: Choose payment method (Cash or Card)

4. **Payment Processing**
   - **Cash**: No additional fees
   - **Card**: 1.5% processing fee added to the total
   - Match the customer's preferred payment method for maximum satisfaction!

5. **Customer Satisfaction**
   - Get the order exactly right → Customer shows 👍 reaction, you get tips and rating boost
   - Wrong order or payment method → Customer shows 👎 reaction, rating decreases
   - Serve quickly → Better tips and satisfaction
   - Take too long → Customer leaves unhappy

### Game Mechanics

**Inventory Management:**
- Click "📦 Inventory" to view and manage your stock
- Ingredients are consumed with each order
- Buy refills using your earnings when stock runs low
- Low stock items are highlighted with alerts

**Progressive Targets:**
- Start with a $100 earnings target
- Each target achieved unlocks the next level ($200, $300, etc.)
- Track your progress with the progress bar

**Rating System:**
- Start at 100% rating
- Good service increases rating
- Poor service or slow orders decrease rating
- Maintain high ratings for better customer tips

**Controls:**
- **Space**: Call next customer
- **I**: Toggle inventory panel
- **Escape**: Close menus/panels
- **Click customers**: Take their orders

---

## 🛠️ Technical Architecture

### Backend (Python Flask)
```
coffee-shop-web-game/
├── backend/
│   ├── app.py                     # Main Flask application
│   └── enhanced_models/           # Enhanced versions of original classes
│       ├── coffee_menu.py         # 26 coffee variations
│       ├── bakery_item.py         # 6 bakery items
│       ├── shop_info.py           # Real-time inventory system
│       └── money_machine.py       # Payment processing & analytics
```

### Frontend (Web Technologies)
- **HTML5 Canvas**: Pixel art game rendering
- **WebSocket**: Real-time updates between client and server
- **Responsive Design**: Works on desktop and mobile
- **Custom Pixel Art**: Enhanced with optional custom sprites

### Original CLI Code (Preserved)
```
original/
├── main.py                # Original CLI application
├── CoffeeMenuItem.py      # Original coffee menu (26 items)
├── bakeryItem.py         # Original bakery menu (6 items)
├── moneyMachine.py       # Original payment system
└── shop.py               # Original inventory management
```

---

## 🎯 Game Features

### Core Gameplay
- **Pixel Coffee Shop**: You're the barista behind the counter
- **AI Customers**: Walk up and place realistic orders
- **Sequential Service**: One customer at a time for focused gameplay
- **Real-time Inventory**: Ingredients decrease as you serve
- **Dynamic Pricing**: Card payments include processing fees
- **Customer AI**: Each customer has patience, preferences, and reactions

### Business Management
- **Progressive Targets**: $100 → $200 → $300 → ... keep growing!
- **Inventory Purchasing**: Use earnings to restock ingredients
- **Performance Tracking**: Customers served, hourly rate, satisfaction
- **Real-time Alerts**: Know when supplies are running low

### Enhanced Experience
- **Custom Sprites**: Optional customer and environment images
- **Pixel Art Fallbacks**: Beautiful pixel art when images aren't available
- **Smooth Animations**: Customer movement, reactions, and UI transitions
- **Audio-Visual Feedback**: Success sounds, visual celebrations

---

## 📊 Menu System

### Coffee Menu (26 Variations)
**Lattes:**
- Medium/Large × Hot/Iced × Regular/Oat/Almond Milk = 12 variations
- Prices: $4.50-$5.70 (premium milk +$0.20)

**Cappuccinos:**
- Medium/Large × Hot/Iced × Regular/Oat/Almond Milk = 12 variations  
- Prices: $4.70-$5.90 (premium milk +$0.20)

**Espresso:**
- Medium/Large × Hot only = 2 variations
- Prices: $4.70-$5.70

### Bakery Menu (6 Items)
- Plain Bagel: $3.00
- Strawberry Cake: $4.00
- Sesameseed Bagel: $3.50
- Honey Bun: $4.00
- Cinnamon Roll: $3.70
- Croissant: $3.00

### Inventory System (12 Ingredients)
**Liquids:** Water, Regular Milk, Oat Milk, Almond Milk
**Solids:** Coffee Beans, Sugar
**Bakery:** All 6 bakery items individually tracked

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Quick Start
```bash
# Clone the repository
git clone [your-repo-url]
cd coffee-shop-web-game

# Install dependencies
pip install flask flask-socketio

# Run the application
python run.py

# Access the game
# Main page: http://localhost:5000
# Direct game: http://localhost:5000/pixel
```

### Development Setup
```bash
# Install additional dev dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python run.py
```

---

## 🎨 Customization

### Adding Custom Images
Place images in `frontend/static/images/`:
- `cafe.png` - Coffee shop background
- `worker.png` - Barista sprite
- `customer1.png` through `customer9.png` - Customer sprites
- `like.png` / `hate.png` - Reaction emojis

Images are optional - the game uses beautiful pixel art fallbacks!

### Modifying Game Balance
Edit values in the enhanced model files:
- **Prices**: `coffee_menu.py` and `bakery_item.py`
- **Inventory**: `shop_info.py` (starting amounts, costs)
- **Customer Patience**: `pixel_game.html` (maxWaitTime)
- **Target Progression**: `pixel_game.html` (targetIncrement)

---

## 📈 Educational Value

### Programming Concepts Demonstrated
- **Object-Oriented Programming**: Classes, inheritance, encapsulation
- **Web Development**: Flask, WebSockets, HTML5 Canvas
- **API Design**: RESTful endpoints, JSON data exchange
- **Real-time Systems**: WebSocket communication
- **Game Development**: Animation loops, state management
- **Business Logic**: Inventory management, payment processing

### Skills Showcase
- **Full-Stack Development**: Backend Python + Frontend JavaScript
- **Problem Solving**: Transforming CLI to web interface
- **Code Evolution**: Maintaining backward compatibility
- **Documentation**: Comprehensive README and code comments
- **UI/UX Design**: Intuitive game interface

---

## 🏆 Achievement Highlights

### Technical Accomplishments
- ✅ **100% Backward Compatibility**: Original CLI code preserved and functional
- ✅ **Modern Web Architecture**: Professional Flask application structure  
- ✅ **Real-time Capabilities**: WebSocket integration for live features
- ✅ **Clean Code Evolution**: Enhanced classes maintain original interfaces
- ✅ **API-First Design**: RESTful endpoints for all functionality

### Game Development
- ✅ **Custom Pixel Art Engine**: HTML5 Canvas with retro graphics
- ✅ **AI Customer System**: Autonomous customer behavior and ordering
- ✅ **Real-time Gameplay**: Live inventory updates and score tracking
- ✅ **Intuitive UX**: Simple click-to-play mechanics
- ✅ **Performance Optimized**: Smooth 60fps animation and rendering

---

## 💡 The Philosophy

Growth isn't about abandoning where you started. It's about taking those precious first steps and building something beautiful on that foundation. Because sometimes the most meaningful progress isn't about starting over - it's about taking what you built with young, eager hands and making it shine.

Every developer has that one project that represents their beginning. This coffee shop simulator is mine. When I look at the original code now, I can see every struggle, every small victory, every moment when something finally worked after hours of debugging.

Transforming it into this web game isn't just about showcasing technical skills - it's about honoring that journey. It's about taking something that meant the world to freshman me and showing how much I've grown, while keeping the heart of what made it special in the first place.

---

## 🤝 Contributing

This project is primarily a personal portfolio piece, but suggestions and improvements are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Share your own "first project" transformation stories
- Contribute pixel art or sprites

---

## 📄 License

### ✅ LICENSE.txt (Creative Commons NonCommercial)
Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For full license text: https://creativecommons.org/licenses/by-nc/4.0/

© 2025 Samia Islam. Licensed under CC BY-NC 4.0.

---

## 🙏 Acknowledgments

- **Freshman Me**: For writing that first magical CLI coffee shop
- **Coffee**: For inspiring both the original project and late-night coding sessions
- **The Programming Community**: For teaching that every expert was once a beginner
- **ASCII Art Credit**: Original coffee shop ASCII art by ccw@aloha.com

---

*From 200 lines of freshman Python to a full-stack web game - because every great journey starts with a single `print("Hello, World!")`* ☕✨
