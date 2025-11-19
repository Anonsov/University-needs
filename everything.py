# a = [1, [2, [3, 4], 5], 6]
# res = []

# def rec(a):
#     for i in a:
#         if isinstance(i, list):
#             rec(i)
#         elif isinstance(i, int):
#             res.append(i)
            
# rec(a)
# print(res)

# a = input().lower()
# b = input().lower()
# mp1 = {}
# mp2 ={}
# for i in range(len(a)):
#     if a[i] not in mp1:
#         mp1[a[i]] = 1
#     else:
#         mp1[a[i]] += 1
    
#     if b[i] not in mp2:
#         mp2[b[i]] = 1
#     else:
#         mp2[b[i]] += 1
        
# if mp1 == mp2 and len(a) == len(b):
#     print("YES")
# else:
#     print("NO")
        
# # a = input()
# # mp = {}
# # for i in a:
# #     if i not in mp:
# #         mp[i] = 1
# #     else:
# #         mp[i] += 1
# # print(mp)


# a = list(map(int, input().split()))
# i= 0
# l = a[0]
# while i < len(a):
#     if a[i] != l:
#         print(l)
#         break
#     l += 1
# #     i += 1
# a = input()
# l = 0
# r = 1
# n = len(a)
# while l < n and r < n:
#     if a[l] != a[r]:
#         print(a[l])
#         break    
#     l += 2
#     r += 2


# a = input()
# a = "sdjfn sdnfojdsnf osdno fns"
# a = a.split(" ")
# mx = float('-inf')
# res = 0
# for i in :
#     if len(i) > mx:
#         mx = len(i)
#         res = 
# print(a[res])



# a = 1
# b = 0
# n = 5
# for i in range(n - 2):
#     a, b = b + a, a
#     print(a)
    # print(b)
    
    
# a = 46
# b = 16

# def solve(a, b):
#     if b == 0:
#         print(a)
#         # return
#     else:
#         solve(b, a % b)
# solve(a,b)    


# class MyList:
#     def __init__(self, data):
#         self.data = list(data)
#     def __len__(self):
#         return len(self.data)
#     def __getitem__(self, idx):
#         return MyList(self.data[idx])
#     def __contains__(self, item):
#         return item in self.data
#     def __repr__(self):
#         return f"MyList({self.data})"
        
# ml = MyList([10,20,30])
# print(len(ml))
# print(ml[1:])
# print(20 in ml)
        
        
# class CallCounter:
#     def __init__(self):
#         self.count = 0
        
#     def __call__(self, *args, **kwds):
#         self.count += 1
#         return f"called {self.count} times"
    
#     def __int__(self):
#         return self.count
    
#     def __repr__(self):
#         return f"CallCounter({self.count})"
    
# c = CallCounter()
# print(c())
# print(c())
# print(c())
# print(c())
# print(c())
# print(c())


# class Money:
#     rates = {"USD": 1.0, "EUR": 0.9, "GBP": 0.75}

#     def __init__(self, amount, currency):
#         self.amount = float(amount)
#         self.currency = currency.upper()
    
#     def __add__(self, other):
#         if isinstance(other, Money):
#             usd = (self.amount * Money.rates[self.currency]) + (other.amount * Money.rates[other.currency])
#             print("f", (self.amount * Money.rates[self.currency]))
#             print("s",other.amount * Money.rates[other.currency])
#         elif isinstance(other, (int, float)):
#             usd = (self.amount * Money.rates[self.currency]) + (float(other) * Money.rates[self.currency])
#         return Money(usd / Money.rates[self.currency], self.currency)

    
#     def __sub__(self, other):
#         if isinstance(other, Money):
#             usd = self.amount * Money.rates[self.currency] - other.amount * Money.rates[other.currency]
#         elif isinstance(other, (int, float)):
#             usd = self.amount * Money.rates[self.currency] - float(other) * Money.rates[self.currency]
        
#         return Money(usd / Money.rates[self.currency], self.currency)

    
#     def __eq__(self, other):
#         if isinstance(other, Money):
#             return abs(self.amount * Money.rates[self.currency] - other.amount * Money.rates[other.currency]) < 1e-9
#         if isinstance(other, (int, float)):
#             return abs(self.amount - float(other)) < 1e-9
#         return False

#     def __lt__(self, other):
#         if isinstance(other, Money):
#             return (self.amount * Money.rates[self.currency]) < (other.amount * Money.rates[other.currency])
#         if isinstance(other, (int, float)):
#             return self.amount < float(other)
        
#     def __float__(self):
#         return self.amount * Money.rates[self.currency]
    
#     def __repr__(self):
#         return f"Money({self.amount:.2f}, '{self.currency}')"


# m1 = Money(100, "USD")
# m2 = Money(85, "EUR")
# print(m1 > m2)
# print(m1 + m2)
# print(repr(m1))



# class Cart:
#     def __init__(self):
#         self.items = []
#     def __len__(self):
#         return len(self.items)
    
    
#     def __delitem__(self, index):
#         del self.items[index]


#     def add(self, item):
#         self.items.append(item)
    
#     def __str__(self):
#         return f"Cart({self.items})"
    
# cart = Cart()
# cart.add("Apple")
# cart.add("Banana")

# print(len(cart))

# del cart[1]
# print(len(cart))

# del cart[0]

# print(cart)


# class Product:
#     def __init__(self, sku, name, cost_price, selling_price, stock_quantity):
#         self.sku = str(sku)
#         self.name = str(name)
#         self.cost_price = float(cost_price)
#         self.selling_price = float(selling_price)
#         self.stock_quantity = int(stock_quantity)
    
#     def __repr__(self):
#         return (f'Product(sku="{self.sku}", name="{self.name}", '
#                 f'cost_price={self.cost_price:.2f}, selling_price={self.selling_price:.2f}, '
#                 f'stock_quantity={self.stock_quantity})')
    
#     def __str__(self):
#         return f"{self.name} ({self.sku}) - Stock: {self.stock_quantity}"

#     def __eq__(self, other):
#         return self.sku == other.sku

#     def __gt__(self, other):
#         return self.selling_price - self.cost_price > other.selling_price - other.selling_price
    
#     def __lt__(self, other):
#         return self.selling_price - self.cost_price < other.selling_price - other.selling_price
    
#     def __add__(self, other):
#         if self.sku != other.sku:
#             raise ValueError("Different SKUs")
#         return Product(self.sku, 
#                        self.name, 
#                        self.cost_price, 
#                        self.selling_price,
#                        self.stock_quantity + other.stock_quantity)
    
#     def __getitem__(self, key):
#         if key == "margin":
#             return self.selling_price - self.cost_price
#         if key == "roi":
#             return ((self.selling_price - self.cost_price) / self.cost_price) * 100

# mouse = Product("MB-2024", "Ergonomic Mouse", 25.00, 59.99, 50)
# keyboard = Product("KB-2023", "Mechanical Keyboard", 45.00, 129.99, 25)
# print(mouse)
# print(mouse > keyboard)
# print(f"ROI: {mouse['roi']}%")



