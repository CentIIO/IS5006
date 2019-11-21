# IS5006
MAS with Logging Features


Install Dependecies:
```python
pip install names
```
###MAS system features:
* multiple products
* multiple sellers
* multiple buyers
* google sheet update
* gmail sending ability

###Product features:
* __accessories__. It is a list which is other product. For example, iPhoneX and iPhoneX_case are individual product, and iPhoneX_case is iPhoneX's accessory.
When customer decide to bug the product, he will have chance to buy its accessory.
* __release_date__ and __initial_amount__. It means this product is not available at the start and will enter the market at a specific date (tick) with initial amount of inventory.
* __reproduce_period__ and __reproduce_amount__. If product is too popular, it can be sold out. And customer can not buy it when inventory is 0. Inventory will be filled again with specific amount every specific period.

###Seller features:
* CEO will update product price based on latest sales history
* CEO will decide each product's advertisement type

###Buyer features:
* different buyer type will have different quality/sentiment/price tolerance.
* can buy multiple products.
* will check accessory if decide buy product.
* will not finish buying if quality/sentiment/price tolerance is not satisfied.
* will not buy if wallet is less than product price.
