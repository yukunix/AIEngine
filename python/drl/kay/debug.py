from drl.kay.config import Config

def action_policy(buy_quantity, portfolio, config):
    stock_price = portfolio['current_stock_price']
    fund = portfolio['fund']
    stock_quantity = portfolio['stock_quantity']
    if buy_quantity > 0:
        if buy_quantity * stock_price > fund:
            quantity_max = fund / stock_price
            for action in config.actions[::-1]:
                if action <= quantity_max:
                    buy_quantity = action
        return buy_quantity
    elif buy_quantity < 0:
        if -buy_quantity > stock_quantity:
            for action in config.actions:
                if -action <= stock_quantity:
                    buy_quantity = action
        return buy_quantity
    else:
        return 0



def main():
    config = Config()
    portfolio = {'current_stock_price': 10, 'stock_quantity': 0, 'fund': 12323, 'total':200000}
    print(action_policy(10000, portfolio, config))
    print(action_policy(-10000, portfolio, config))

if __name__ == '__main__':
    main()