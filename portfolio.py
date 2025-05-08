# IH#5 Forgiveness – can remove a stock; nothing permanent
# IH#6 Guidance    – always prints next command prompt

from dataclasses import dataclass, field  
from api import StockAPI  

@dataclass  
class Portfolio:  
    owner: str  
    starting_cash: float = 10_000.00  # Add starting_cash parameter  
    positions: dict[str, int] = field(default_factory=dict)  

    # -------------- domain actions --------------  
    def add(self, symbol: str, qty: int = 1) -> None:  
        """Add stocks to the portfolio."""  
        self.positions[symbol] = self.positions.get(symbol, 0) + qty  
        print(f"Added {qty} × {symbol} to your portfolio.")  
        self.display()  # Display updated portfolio immediately  

    def remove(self, symbol: str) -> None:  
        """Remove stocks from the portfolio."""  
        if symbol in self.positions:  
            self.positions.pop(symbol)  
            print(f"Removed {symbol} from your portfolio.")  
        else:  
            print(f"{symbol} not found in your portfolio.")  
        self.display()  # Display updated portfolio immediately  

    def value(self) -> float:  
        """Calculate the total value of the portfolio including cash."""  
        total = self.starting_cash  # Start with the starting cash  
        for sym, qty in self.positions.items():  
            price = StockAPI.get_quote(sym)  
            total += price * qty  
        return round(total, 2)  

    def display(self) -> None:  
        """Display the contents and value of the portfolio."""  
        print(f"\n{self.owner}'s Portfolio")  
        print("-" * 30)  
        for sym, qty in self.positions.items():  
            price = StockAPI.get_quote(sym)  
            print(f"{sym:<6}  {qty:>3}  @ ${price:>8.2f}  = ${price * qty:>8.2f}")  
        print("-" * 30)  
        print(f"Total value: ${self.value():.2f}\n")  
        
        # Ensure the command prompt appears after every display  
        print("> Type next command:")