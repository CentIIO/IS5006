
def rbs_get_customer_attributes(type):
    if type >= 0.8:
        quality_tolerance = 0.8
        price_tolerance = 300
        sentiment_tolerance = 0.8
        ratio = 0.8
    elif type >= 0.6:
        quality_tolerance = 0.7
        price_tolerance = 200
        sentiment_tolerance = 0.6
        ratio = 0.6
    elif type >= 0.4:
        quality_tolerance = 0.5
        price_tolerance = 100
        sentiment_tolerance = 0.4
        ratio = 0.4
    else:
        quality_tolerance = 0.3
        price_tolerance = 50
        sentiment_tolerance = 0.2
        ratio = 0.2
    return quality_tolerance, price_tolerance, sentiment_tolerance, ratio

