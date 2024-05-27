from main import redis, Product
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                # result[1] -> Second elemtent of the results array
                # result[1][0] -> First element on that array
                # result[1][0][1] -> the order inside the second element
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                    print(product)
                except:
                    # When an error happens the an stream is send out
                    # to the payment service so the order status 
                    # can change to refunded
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)