import redis
from django.conf import settings
from supplier.models import Product, SKU

# connect to redis
'''
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)
'''
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self, ID):
        return f"product:{ID}:purchased_with"

    def products_bought(self, purchased_products_IDs):
        for ID_x in purchased_products_IDs:
            for ID_y in purchased_products_IDs:
                if ID_x != ID_y:
                    co_occurence_times = r.get(f"{ID_x}_{ID_y}")
                    if co_occurence_times is None:
                        co_occurence_times = 0
                    r.set(f"{ID_x}_{ID_y}", co_occurence_times + 1)
    
    def get_recommendations(self, product_ID, max_results=6):
    #def get_recommendations(self, product_IDs, max_results=6):
        #product_IDs = [product.ID for product in products]
        #product_IDs = [int(e) for e in product_IDs]
        
        # 1. Retrieval
        sim_val = dict()
        for tmp_key in r.scan_iter(f"{product_ID}_*"):
            key_ = (str(tmp_key).split('_')[-1])[:-1]
            sim_val[key_] = r.get(tmp_key)
            #print(f"key_: {key_}"); print(f"sim_val[key_]: {sim_val[key_]}")

        # 2. Sort
        #sorted(a.items(), key=lambda x:x[1], reverse=True) 
        #[x for x, _ in sorted(a.items(), key=lambda x:x[1])]
        sorted_recommended_IDs = [x for x, _ in sorted(sim_val.items(), key=lambda x:x[1])][:max_results]
        #print(sorted_similar_productIDs)
        
        # 3. Convert productIDs => products (instance of <Product>) => items (containing (1) `SKU`: for field `Picture` (2) `Product`: for field `Name`)  
        recommendations = list()
        #products = Product.objects.filter(ID__in=sorted_recommended_IDs)
        
        for sim_productID in sorted_recommended_IDs:
            item = dict()
            product_obj = Product.objects.filter(ID=sim_productID)[0]
            item.setdefault("product_obj", product_obj)
            item.setdefault("product_name", product_obj.Name)
            item.setdefault("product_price", product_obj.Price)
            item.setdefault("product_picture",  SKU.objects.filter(Product=product_obj)[0].Picture) # Get the first SKU's picture from SKUs with the same SPU
            recommendations.append(item)
        return recommendations

    def clear_purchases(self):
        for ID in Product.objects.values_list("ID", flat=True):
            r.delete(self.get_product_key(ID))