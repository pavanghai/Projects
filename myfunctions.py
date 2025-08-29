from datetime import datetime, timedelta


def nth_weekday(weekday: str, n: int):
    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    
    if weekday.lower() not in weekdays or n < 1:
        raise ValueError("Invalid weekday or n. Use ('mon', 'tue', ..., 'sun') and n > 0")
    
    today = datetime.today()
    target_weekday = weekdays.index(weekday.lower())  # Get weekday index (0=Monday, ..., 6=Sunday)
    days_until_target = (target_weekday - today.weekday()) % 7  # Days to next target weekday
    first_occurrence = today + timedelta(days=days_until_target)  # First upcoming target weekday
    nth_occurrence = first_occurrence + timedelta(weeks=n-1)  # Get nth occurrence
    
    return nth_occurrence.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD


def generate_strike_prices(last_price, step, count):
    """
    Generates a list of strike prices based on the given last price, step size, and count.
    
    The list will contain:
    - ITM (In The Money) strikes below the ATM (At The Money) strike,
    - ATM strike in the middle (for odd count),
    - OTM (Out of The Money) strikes above the ATM strike.
    
    Parameters:
    last_price (float): The last traded price of the stock.
    step (int): The step size for the strike prices.
    count (int): The total number of strike prices to return, which must be a positive integer.

    Returns:
    list: A list of strike prices with the specified count. The list will be centered around the ATM strike.
    """
    atm_strike = round(last_price / step) * step
    half_count = count // 2
    strikes = [atm_strike + (i * step) for i in range(-half_count, half_count + 1)]
    return strikes if count % 2 else strikes[1:]  # Remove ATM for even count

# Example usage
for i in range(1, 20):
    print(generate_strike_prices(22397, 50, i))

# print(generate_strike_prices(22397, 50, 6))  # [22300, 22350, 22400, 22450, 22500, 22550]
# print(generate_strike_prices(22397, 50, 7))  # [22250, 22300, 22350, 22400, 22450, 22500, 22550]

