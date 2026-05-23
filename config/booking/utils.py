


TAX_RATE = 0.18
CONVENIENCE_RATE=0.10
# DELIVERY_CHARGE= 0


def calculate_amount_for_items(items):
    
    total_rent = 0
    total_deposit =0
    item_breakdown =[]
    
    for item in items:
        
        product =item['product']
        qty = item['quantity']
        days = (item['end'] - item['start']).days
        
        rent = product.price_per_day * days * qty
        deposit = product.security_deposit * qty
        
        total_rent +=rent
        total_deposit += deposit
        
        item_breakdown.append({
            'product_id':    product.id,
            'product_title': product.title,
            'days':          days,
            'quantity':      qty,
            'rent':          rent,
            'deposit':       deposit,
        })
    tax = round(total_rent * TAX_RATE,2)
    convenience = round(total_deposit*CONVENIENCE_RATE,2)
    
    if total_rent > 35000:
        delivery = 0
    elif total_rent > 20000:
        delivery = 200
    elif total_rent > 10000:
        delivery = 100
    else:
        delivery = 500

    
    grand_total = total_rent + total_deposit + tax + convenience + delivery
    
    return {
        'items':item_breakdown,
        'rent':total_rent,
        'deposit':total_deposit,
        'tax':tax,
        'convenience':convenience,
        'delivery':delivery,
        'grand_total':grand_total
    }
        

def calculate_amount_from_reservations(reservations):
    """Adapter — converts saved Reservation objects into items and reuses the same function."""
    items = [
        {
            'product':    r.product,
            'quantity':   r.quantity,
            'start':      r.start_date,
            'end':        r.end_date,
        }
        for r in reservations
    ]
    return calculate_amount_for_items(items)