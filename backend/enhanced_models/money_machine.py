# backend/enhanced_models/money_machine.py
"""
Enhanced Money Machine - Preserves original CLI functionality while adding web features
"""
import json
from datetime import datetime
from typing import List, Dict, Optional

class MoneyMachineWeb:
    """Enhanced version of original MoneyMachine with web-ready features"""
    
    def __init__(self):
        # PRESERVE: Original attributes
        self.currency = "$"
        self.profit = 0.0
        
        # NEW: Web-specific attributes
        self.transaction_history = []
        self.daily_earnings = {}
        self.payment_methods_used = {"cash": 0, "card": 0}
        self.tips_collected = 0.0
        self.shift_start_time = datetime.now()
        self.target_earnings = 100.0  # Daily target
    
    # PRESERVE: Original methods for backward compatibility
    def profit_report(self):
        """Original CLI profit report method"""
        print(f"Money: {self.currency}{self.profit}")
    
    def insert_cash(self, amount):
        """Original cash payment method with enhanced logging"""
        try:
            cash_input = float(input(f"Insert {self.currency}{amount:.2f} in cash: "))
            
            if cash_input >= amount:
                change = cash_input - amount
                self.profit += amount
                
                # NEW: Log the transaction
                self._log_transaction("cash", amount, cash_input, change, True)
                
                print(f"Thank you! Here's your change: {self.currency}{change:.2f}")
                return True
            else:
                print("Insufficient cash. Please insert the correct amount.")
                self._log_transaction("cash", amount, cash_input, 0, False)
                return False
                
        except ValueError:
            print("Invalid cash amount entered.")
            return False
    
    def add_card(self, amount):
        """Original card payment method with enhanced logging"""
        while True:
            try:
                card_number = int(input("Enter your card number: "))
            except ValueError:
                print("Invalid card number.")
                continue
            
            try:
                card_balance = float(input("Enter your card balance: "))
            except ValueError:
                print("Invalid card balance")
                continue
            
            if card_balance >= amount:
                self.profit += amount
                remaining_balance = card_balance - amount
                
                # NEW: Log the transaction
                self._log_transaction("card", amount, card_balance, 0, True, card_number)
                
                print(f"Payment successful. Remaining card balance: {self.currency}{remaining_balance:.2f}")
                return True
            else:
                print("Insufficient card balance. Please use a different payment method.")
                self._log_transaction("card", amount, card_balance, 0, False, card_number)
                return False
    
    # NEW: Web-specific methods
    def _log_transaction(self, payment_method: str, amount: float, 
                        input_amount: float, change: float, success: bool, 
                        card_number: Optional[int] = None):
        """Log transaction details for analytics"""
        transaction = {
            'timestamp': datetime.now().isoformat(),
            'payment_method': payment_method,
            'amount': amount,
            'input_amount': input_amount,
            'change': change,
            'success': success,
            'card_number': str(card_number)[-4:] if card_number else None  # Last 4 digits only
        }
        
        self.transaction_history.append(transaction)
        
        if success:
            self.payment_methods_used[payment_method] += 1
            
            # Track daily earnings
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in self.daily_earnings:
                self.daily_earnings[today] = 0.0
            self.daily_earnings[today] += amount
    
    def process_web_payment(self, payment_method: str, amount: float, 
                           payment_details: Dict) -> Dict:
        """Process payment from web interface"""
        success = False
        message = ""
        change = 0.0
        tip = payment_details.get('tip', 0.0)
        total_amount = amount + tip
        
        if payment_method == "cash":
            cash_given = payment_details.get('cash_amount', 0.0)
            if cash_given >= total_amount:
                change = cash_given - total_amount
                self.profit += amount
                if tip > 0:
                    self.tips_collected += tip
                success = True
                message = f"Payment successful! Change: {self.currency}{change:.2f}"
            else:
                message = f"Insufficient cash. Need {self.currency}{total_amount:.2f}, got {self.currency}{cash_given:.2f}"
            
            self._log_transaction("cash", amount, cash_given, change, success)
            
        elif payment_method == "card":
            # Simulate card processing
            card_number = payment_details.get('card_number', '1234')
            
            # In real app, you'd integrate with payment processor
            # For demo, we'll simulate successful payment
            if len(str(card_number)) >= 4:  # Basic validation
                self.profit += amount
                if tip > 0:
                    self.tips_collected += tip
                success = True
                message = "Card payment successful!"
            else:
                message = "Invalid card number"
            
            self._log_transaction("card", amount, total_amount, 0, success, int(card_number))
        
        # Calculate quality bonus if provided
        quality_bonus = payment_details.get('quality_bonus', 0.0)
        if success and quality_bonus > 0:
            self.profit += quality_bonus
            message += f" Quality bonus: {self.currency}{quality_bonus:.2f}"
        
        return {
            'success': success,
            'message': message,
            'change': change,
            'tip': tip,
            'total_earned': amount + tip + quality_bonus,
            'transaction_id': len(self.transaction_history)
        }
    
    def get_earnings_summary(self) -> Dict:
        """Get comprehensive earnings summary for web dashboard"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_earnings = self.daily_earnings.get(today, 0.0)
        
        # Calculate hourly rate
        hours_worked = (datetime.now() - self.shift_start_time).total_seconds() / 3600
        hourly_rate = self.profit / max(hours_worked, 0.1)  # Avoid division by zero
        
        # Calculate progress toward target
        target_progress = (today_earnings / self.target_earnings) * 100
        
        return {
            'total_profit': self.profit,
            'today_earnings': today_earnings,
            'tips_collected': self.tips_collected,
            'hours_worked': round(hours_worked, 2),
            'hourly_rate': round(hourly_rate, 2),
            'target_earnings': self.target_earnings,
            'target_progress': round(target_progress, 1),
            'transactions_today': len([t for t in self.transaction_history 
                                     if t['timestamp'].startswith(today)]),
            'payment_methods': self.payment_methods_used.copy(),
            'currency': self.currency
        }
    
    def get_transaction_history(self, days: int = 7) -> List[Dict]:
        """Get recent transaction history"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_transactions = [
            t for t in self.transaction_history 
            if datetime.fromisoformat(t['timestamp']) > cutoff_date
        ]
        
        return sorted(recent_transactions, key=lambda x: x['timestamp'], reverse=True)
    
    def get_daily_breakdown(self, days: int = 7) -> Dict:
        """Get daily earnings breakdown for charts"""
        from datetime import timedelta
        
        breakdown = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            breakdown[date] = self.daily_earnings.get(date, 0.0)
        
        return dict(sorted(breakdown.items()))
    
    def get_payment_analytics(self) -> Dict:
        """Get payment method analytics"""
        successful_transactions = [t for t in self.transaction_history if t['success']]
        
        if not successful_transactions:
            return {'cash_percentage': 0, 'card_percentage': 0, 'total_transactions': 0}
        
        cash_count = len([t for t in successful_transactions if t['payment_method'] == 'cash'])
        card_count = len([t for t in successful_transactions if t['payment_method'] == 'card'])
        total = len(successful_transactions)
        
        return {
            'cash_percentage': round((cash_count / total) * 100, 1),
            'card_percentage': round((card_count / total) * 100, 1),
            'total_transactions': total,
            'cash_transactions': cash_count,
            'card_transactions': card_count,
            'average_transaction': round(self.profit / max(total, 1), 2)
        }
    
    def add_tip(self, amount: float, source: str = "web") -> bool:
        """Add tip from customer"""
        if amount > 0:
            self.tips_collected += amount
            
            # Log tip as special transaction
            tip_transaction = {
                'timestamp': datetime.now().isoformat(),
                'payment_method': 'tip',
                'amount': amount,
                'input_amount': amount,
                'change': 0,
                'success': True,
                'source': source
            }
            self.transaction_history.append(tip_transaction)
            return True
        return False
    
    def set_shift_target(self, target: float):
        """Set earnings target for current shift"""
        self.target_earnings = target
    
    def reset_shift(self):
        """Reset for new shift (keeps historical data)"""
        self.shift_start_time = datetime.now()
        # Note: We don't reset profit or history for continuity
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics for gamification"""
        successful_transactions = [t for t in self.transaction_history if t['success']]
        
        metrics = {
            'total_customers_served': len(successful_transactions),
            'average_order_value': round(self.profit / max(len(successful_transactions), 1), 2),
            'tips_percentage': round((self.tips_collected / max(self.profit, 1)) * 100, 1),
            'efficiency_score': min(100, len(successful_transactions) * 2),  # Simple efficiency calculation
            'customer_satisfaction': 85 + min(15, self.tips_collected)  # Simulated satisfaction based on tips
        }
        
        return metrics
    
    def to_json(self) -> str:
        """Convert current state to JSON for web API"""
        return json.dumps({
            'earnings_summary': self.get_earnings_summary(),
            'payment_analytics': self.get_payment_analytics(),
            'performance_metrics': self.get_performance_metrics(),
            'recent_transactions': self.get_transaction_history(1),  # Today only
            'last_updated': datetime.now().isoformat()
        }, indent=2)


# Example usage and testing
if __name__ == "__main__":
    # Test backward compatibility
    money_machine = MoneyMachineWeb()
    
    print("=== ORIGINAL CLI FUNCTIONALITY ===")
    money_machine.profit_report()
    
    # Simulate some transactions for testing web features
    print("\n=== SIMULATING TRANSACTIONS ===")
    
    # Simulate web payments
    payment1 = money_machine.process_web_payment("card", 4.50, {
        'card_number': '1234567890123456',
        'tip': 1.0,
        'quality_bonus': 0.5
    })
    print(f"Payment 1: {payment1['message']}")
    
    payment2 = money_machine.process_web_payment("cash", 3.00, {
        'cash_amount': 5.00,
        'tip': 0.5
    })
    print(f"Payment 2: {payment2['message']}")
    
    # Test new web functionality
    print("\n=== NEW WEB FUNCTIONALITY ===")
    summary = money_machine.get_earnings_summary()
    print(f"Total Profit: {summary['currency']}{summary['total_profit']}")
    print(f"Tips Collected: {summary['currency']}{summary['tips_collected']}")
    print(f"Hourly Rate: {summary['currency']}{summary['hourly_rate']}")
    print(f"Target Progress: {summary['target_progress']}%")
    
    analytics = money_machine.get_payment_analytics()
    print(f"Payment Split: {analytics['cash_percentage']}% cash, {analytics['card_percentage']}% card")
    
    metrics = money_machine.get_performance_metrics()
    print(f"Customers Served: {metrics['total_customers_served']}")
    print(f"Customer Satisfaction: {metrics['customer_satisfaction']}%")