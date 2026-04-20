from django.core.cache import cache

def invalidate_product_cache():
    version = cache.get("product_version", 1)
    cache.set("product_version", version + 1)