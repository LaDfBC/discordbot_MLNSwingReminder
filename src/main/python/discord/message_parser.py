def parse_timeframe(content):
    parts = content.split(' ')

    if len(parts) != 3:
        return [], "Improperly formatted message! Proper usage: <command> <number> <unit> such as !notify-player 2 hours"

    try:
        time_multiplier = int(parts[1])
        time_units = parts[2]
    except ArithmeticError:
        return [], "Failed to parse number " + parts[1]

    return time_multiplier