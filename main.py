#!/usr/bin/env python3  
"""  
CLI front-end for the API-Stock-Trader bot  

• First shows a simple Login / Register / Quit menu (uses AuthManager).  
• After a successful login, it starts a text REPL so the user can  
  fetch prices, buy/sell, and view a tiny in-memory portfolio.  
"""  

from datetime import datetime  
from auth import AuthManager  
from api import StockAPI  
from portfolio import Portfolio  

# ───────────────────────────────────── ASCII banner ──────────────────────────  
BANNER = r"""  
            _   _                                                    
            | | | | __ _ _ __  _ __  _   _                            
            | |_| |/ _` | '_ \| '_ \| | | |                           
            |  _  | (_| | |_) | |_) | |_| |                           
            |_| |_|\__,_| .__/| .__/ \__, |                           
            ___        |_|   |_|    |___/                    _       
            |_ _|_ ____   _____  ___| |_ _ __ ___   ___ _ __ | |_ ___ 
            | || '_ \ \ / / _ \/ __| __| '_ ` _ \ / _ \ '_ \| __/ __|
            | || | | \ V /  __/\__ \ |_| | | | | |  __/ | | | |_\__ \
            |___|_| |_|\_/ \___||___/\__|_| |_| |_|\___|_| |_|\__|___/ 

                   B  E  G  I  N   I  N  V  E  S  T  I  N  G  
"""  

# ───────────────────────────────────── helper screens ────────────────────────  
def show_help() -> None:  
    print(  
        """  
COMMANDS  
  price  <TICKER>           Get the latest price  
  buy    <TICKER> <QTY>     Simulate purchase  
  sell   <TICKER> <QTY>     Simulate sell  
  portfolio                 Show current holdings + cash  
  about                     Learn what this is  
  help                      Show this list again  
  quit                      Exit the program  
"""  
    )  


def about() -> None:  
    print(  
        """  
ABOUT  
This console app is a Milestone-1 demo for CS-361.  It wraps a tiny  
StockAPI micro-service plus an in-memory Portfolio so we can interact  
live in the terminal—just like the Affurmnations example your professor  
showed, but for stock-trading instead of pet affirmations.  
"""  
    )  


# ─────────────────────────── trading REPL (after login) ──────────────────────  
def trade_cli(portfolio: Portfolio) -> None:  
    print(BANNER)  # Print the ASCII banner  
    print("Welcome,", portfolio.owner)  
    print("Today is", datetime.now().strftime("%b %d, %Y – %I:%M %p"))  
    print("Type help to see commands.\n")  

    while True:  
        try:  
            raw = input("> ").strip()  
        except (EOFError, KeyboardInterrupt):  
            print("\nBye!")  
            break  

        if not raw:  
            continue  

        parts = raw.split()  
        cmd = parts[0].lower()  

        # ───────────── core commands ─────────────  
        if cmd in ("q", "quit", "exit"):  
            print("Bye!")  
            break  

        elif cmd == "help":  
            show_help()  

        elif cmd == "about":  
            about()  

        elif cmd == "portfolio":  
            print(portfolio)  
  

        elif cmd == "price" and len(parts) == 2:  
            ticker = parts[1].upper()  
            price = StockAPI.get_quote(ticker)  
            if price is None:  
                print(f"⚠️  {ticker}: price unavailable right now.")  
            else:  
                print(f"{ticker}: ${price:,.2f}")  

        elif cmd == "buy" and len(parts) == 3:  
            ticker, qty_txt = parts[1].upper(), parts[2]  
            if not qty_txt.isdigit():  
                print("Quantity must be a whole number.")  
                continue  
            qty = int(qty_txt)  
            price = StockAPI.get_quote(ticker)  
            if price is None:  
                print("Cannot buy: live price unavailable.")  
                continue  
            portfolio.buy(ticker, qty, price)  

        elif cmd == "sell" and len(parts) == 3:  
            ticker, qty_txt = parts[1].upper(), parts[2]  
            if not qty_txt.isdigit():  
                print("Quantity must be a whole number.")  
                continue  
            qty = int(qty_txt)  
            price = StockAPI.get_quote(ticker)  
            if price is None:  
                print("Cannot sell: live price unavailable.")  
                continue  
            portfolio.sell(ticker, qty, price)  

        else:  
            print("Unknown command. Type  help  to list options.")  

        print("-" * 40)  # polite gap so the screen doesn’t scroll too fast  


# ───────────────────────────────────── top-level flow ────────────────────────  
def main() -> None:  
    print("Welcome to API-Stock-Trader-Bot – check prices & track a tiny portfolio.")  
    auth = AuthManager()  
    user = None  

    while not user:  
        choice = input("\n[L]ogin  [R]egister  [Q]uit : ").lower()  
        if choice == "l":  
            user = auth.login()  
        elif choice == "r":  
            user = auth.register()  
        elif choice == "q":  
            print("See you next time!")  
            return  

    # start the investing REPL  
    portfolio = Portfolio(owner=user, starting_cash=10_000.00)  
    trade_cli(portfolio)  


if __name__ == "__main__":  
    main()