
def rbs_get_customer_attributes(type):
    if type >= 0.8:
        quality_tolerance = 0.8
        price_tolerance = 300
        sentiment_tolerance = 0.8
        ratio = 0.6
    elif type >= 0.6:
        quality_tolerance = 0.7
        price_tolerance = 200
        sentiment_tolerance = 0.6
        ratio = 0.08
    elif type >= 0.4:
        quality_tolerance = 0.5
        price_tolerance = 100
        sentiment_tolerance = 0.4
        ratio = 0.06
    else:
        quality_tolerance = 0.3
        price_tolerance = 50
        sentiment_tolerance = 0.2
        ratio = 0.02
    return quality_tolerance, price_tolerance, sentiment_tolerance, ratio

def rbs_get_product_newamount(product,amtinInv):

    if amtinInv <= product.quantity *0.2:
        newamount = 1.2* product.quantity
    elif amtinInv <= product.quantity *0.4:
        newamount = 1.0 * product.quantity
    elif amtinInv <= product.quantity *0.6:
        newamount = 0.8 * product.quantity
    else:
        newamount = amtinInv
    return newamount