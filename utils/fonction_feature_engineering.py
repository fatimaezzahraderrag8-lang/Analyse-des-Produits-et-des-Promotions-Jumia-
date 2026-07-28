def price_category(price):

    if price < 500:
        return "Low"
    elif price < 2000:
        return "Medium"
    else:
        return "High"

def popularity(ratings):

    if ratings < 100:
        return "Low"
    elif ratings < 500:
        return "Medium"
    else:
        return "High"
    
def seller_level(score):

    if score < 60:
        return "Low"
    elif score < 90:
        return "Medium"
    else:
        return "High"