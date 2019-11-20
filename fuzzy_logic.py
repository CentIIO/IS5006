#fuzzy logic needs to be improved

def fuzzy_get_customer_tolerance(type):
    if type > 0.9:
        quality_tolerance = 0.9
        price_tolerance = 0.9
        sentiment_tolerance = 0.9
    elif type > 0.7:
        quality_tolerance = 0.7
        price_tolerance = 0.7
        sentiment_tolerance = 0.7
    elif type > 0.5:
        quality_tolerance = 0.5
        price_tolerance = 0.5
        sentiment_tolerance = 0.5
    else:
        quality_tolerance = 0.3
        price_tolerance = 0.3
        sentiment_tolerance = 0.3
    return quality_tolerance, price_tolerance, sentiment_tolerance
