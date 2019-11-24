
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

def rbs_CEO_decide_new_price_budget(product, saleshistory, profithistory, adbudget):
    sales1,sales2,sales3 = saleshistory[-3],saleshistory[-2],saleshistory[-1]
    profit1, profit2, profit3 = profithistory[-3], profithistory[-2], profithistory[-1]
    newadvbudget = adbudget
    newprice = product.price

    if sales3 > sales2 and sales2 > sales1 and profit3 > profit2 and profit2 > profit1:
        # sales +, +. profile +, +.
        newadvbudget = adbudget
        newprice = product.price*1.4
    elif sales3 < sales2 and sales2 < sales1 and profit3 < profit2 and profit2 < profit1:
        # sales -, -. profile -, -.
        newadvbudget = 1.5 * adbudget
        newprice = product.price * 0.5
    elif sales3 < sales2 and sales2 > sales1 and profit3 < profit2 and profit2 > profit1:
        # sales +, -. profile +, -.
        newadvbudget = 1.2*adbudget
        newprice = product.price*0.8
    elif sales3 > sales2 and sales2 > sales1 and profit3 < profit2 and profit2 < profit1:
        # sales +, +. profile -, -.
        newadvbudget = 0.8*adbudget
        newprice = product.price*1.2
    elif sales3 < sales2 and sales2 < sales1 and profit3 > profit2 and profit2 > profit1:
        # sales -, -. profile +, +.
        newadvbudget = 1.5*adbudget
        newprice = product.price*1.4
    elif sales3 > sales2 and sales2 < sales1 and profit3 > profit2 and profit2 < profit1:
        # sales -, +. profile -, +.
        newadvbudget = adbudget
        newprice = product.price*1.2
    else:
        pass

    return newprice, newadvbudget