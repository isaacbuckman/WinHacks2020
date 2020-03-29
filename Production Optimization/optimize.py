import math, copy

def use_resources(resources, materials):
    for material in materials:
        if resources[material] < materials[material]:
            return False, resources
    resources = {resource: amt - materials.get(resource, 0) for resource, amt in resources.items()}
    return True, resources


def maximize_value(prev_resources, product_info, prev_products, lookup_table):
    if str((prev_resources, prev_products)) in lookup_table: return lookup_table[str((prev_resources, prev_products))]
    potential_values = []
    for product in prev_products:
        products = copy.copy(prev_products)
        can_make_product, resources = use_resources(prev_resources, product_info[product]['materials'])
        if can_make_product:
            products[product] += 1
            value, products, resources = maximize_value(resources, product_info, products, lookup_table)
            value = product_info[product]['value'] * (1/math.log(products[product] + 1)) + value
        else:
            value = 0
        potential_values.append((value, products, resources))
    print(potential_values)
    result = max(potential_values)
    lookup_table[str((prev_resources, prev_products))] = result
    return result


def main(resources, product_info):
    products = {product: 0 for product in product_info}
    lookup_table = {}
    return maximize_value(resources, product_info, products, lookup_table)

if __name__ == '__main__':
    # resources = {
    #     'strap': 100,
    #     'mask': 30,
    #     'staple': 350,
    #     'buckle': 25
    # }
    resources = {
        'strap': 300,
        'mask': 100,
        'staple': 600,
        'buckle': 20
    }
    product_info = {
        'N95': {
            'materials': {
                'strap': 1,
                'mask': 1,
                'staple': 2
            },
            'value': 10
        },
        'belt': {
            'materials': {
                'strap': 2,
                'staple': 3,
                'buckle': 1
            },
            'value': 3
        },
        'belt2': {
            'materials': {
                'strap': 3,
                'staple': 3,
                'buckle': 2
            },
            'value': 7
        }
    }
    value, products, resources = main(resources, product_info)
    print(value)
    print(products)
    print(resources)
