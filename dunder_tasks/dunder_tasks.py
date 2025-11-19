# TASK 1
class Product:
    def __init__(self, sku, name, cost_price, selling_price, stock_quantity):
        self.sku = str(sku)
        self.name = str(name)
        self.cost_price = float(cost_price)
        self.selling_price = float(selling_price)
        self.stock_quantity = int(stock_quantity)
    
    def __repr__(self):
        return (f'Product(sku="{self.sku}", name="{self.name}", '
                f'cost_price={self.cost_price:.2f}, selling_price={self.selling_price:.2f}, '
                f'stock_quantity={self.stock_quantity})')
    
    def __str__(self):
        return f"{self.name} ({self.sku}) - Stock: {self.stock_quantity}"

    def __eq__(self, other):
        return self.sku == other.sku

    def __gt__(self, other):
        return self.selling_price - self.cost_price > other.selling_price - other.selling_price
    
    def __lt__(self, other):
        return self.selling_price - self.cost_price < other.selling_price - other.selling_price
    
    def __add__(self, other):
        if self.sku != other.sku:
            raise ValueError("Different SKUs")
        return Product(self.sku, 
                       self.name, 
                       self.cost_price, 
                       self.selling_price,
                       self.stock_quantity + other.stock_quantity)
    
    def __getitem__(self, key):
        if key == "margin":
            return self.selling_price - self.cost_price
        if key == "roi":
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100

mouse = Product("MB-2024", "Ergonomic Mouse", 25.00, 59.99, 50)
keyboard = Product("KB-2023", "Mechanical Keyboard", 45.00, 129.99, 25)
print(mouse)
print(mouse > keyboard)
print(f"ROI: {mouse['roi']}%")




# TASK 2
class SalesOrder:
    def __init__(self, order_id, customer_id):
        self.order_id = str(order_id)
        self.customer_id = str(customer_id)
        self.items = []

    def __len__(self):
        return sum(int(it.get('quantity', 0)) for it in self.items)


    def __contains__(self, product):
        for it in self.items:
            p = it.get('product')
            if p == product:
                return True
            if isinstance(product, str):
                sku = getattr(p, 'sku', None)
                if sku == product or str(p) == product:
                    return True
        return False
    
    def __iadd__(self, other):
        if isinstance(other, tuple):
            product, qty = other
        else:
            product, qty = other, 1
            
        qty = int(qty)

        for it in self.items:
            if it['product'] == product:
                it['quantity'] += qty
                break
        else:
            self.items.append({'product': product, 'quantity': qty})
        return self
        
    def __bool__(self):
        return len(self) > 0
    
order_101 = SalesOrder("ORDER-101", "CUST-55")
order_101 += "mouse"
order_101 += "keyboard"

print(len(order_101))
print("mouse" in order_101)



# TASK 3
class Product:
    def __init__(self, sku, name, cost_price, selling_price, stock_quantity):
        self.sku = str(sku)
        self.name = str(name)
        try:
            self.cost_price = float(cost_price)
            self.selling_price = float(selling_price)
            self.stock_quantity = int(stock_quantity)
        except (TypeError, ValueError):
            raise ValueError("Invalid numeric values for price or stock_quantity")
        if self.cost_price < 0 or self.selling_price < 0 or self.stock_quantity < 0:
            raise ValueError("cost_price, selling_price and stock_quantity must be non-negative")

    def __repr__(self):
        return (f'Product(sku="{self.sku}", name="{self.name}", '
                f'cost_price={self.cost_price:.2f}, selling_price={self.selling_price:.2f}, '
                f'stock_quantity={self.stock_quantity})')

    def __str__(self):
        return f"{self.name} ({self.sku}) - Stock: {self.stock_quantity}"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.sku == other.sku

    def margin(self):
        return self.selling_price - self.cost_price

    def __gt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.margin() > other.margin()

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.margin() < other.margin()

    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        if self.sku != other.sku:
            raise ValueError("Cannot add products with different SKUs")
        if self.name != other.name:
            raise ValueError("Cannot merge products: differing names for same SKU")
        return Product(self.sku, self.name, self.cost_price, self.selling_price,
                       self.stock_quantity + other.stock_quantity)

    def __getitem__(self, key):
        if key == "margin":
            return self.margin()
        if key == "roi":
            if self.cost_price == 0:
                return float("inf")
            return (self.margin() / self.cost_price) * 100
        raise KeyError(f"Unknown metric: {key}")


class SalesOrder:
    def __init__(self, order_id, customer_id):
        self.order_id = str(order_id)
        self.customer_id = str(customer_id)
        
        self.items = []

    def __len__(self):
        return sum(int(it.get('quantity', 0)) for it in self.items)

    def __contains__(self, product):
        for it in self.items:
            p = it.get('product')
            if isinstance(product, Product):
                if p == product:
                    return True
            else:
                sku = getattr(p, 'sku', None)
                if sku == str(product) or str(p) == str(product):
                    return True
        return False

    def __iadd__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            product, qty = other
        else:
            product, qty = other, 1

        if not isinstance(product, Product):
            raise TypeError("SalesOrder accepts Product instances only")

        qty = int(qty)
        if qty <= 0:
            raise ValueError("quantity must be a positive integer")

        for it in self.items:
            if it.get('product') == product:
                it['quantity'] = int(it.get('quantity', 0)) + qty
                break
        else:
            self.items.append({'product': product, 'quantity': qty})
        return self

    def __bool__(self):
        return len(self) > 0

p_mouse = Product("MB-2024", "Ergonomic Mouse", 25.00, 59.99, 50)
p_kbd = Product("KB-2023", "Mechanical Keyboard", 45.00, 129.99, 25)

order = SalesOrder("ORDER-101", "CUST-55")
order += p_mouse
order += (p_kbd, 2)

print(len(order))          
print(p_mouse in order)     
if order:
    print("Order is fulfillable")
print("Margin:", p_mouse["margin"])
print("ROI:", p_mouse["roi"])
