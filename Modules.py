import requests
import logging
from pydantic import BaseModel

'''
This class represents an order from a user
'''


class Order(BaseModel):
    drinks: list = []
    desserts: list = []
    pizzas: list = []


'''
This class stores the data coming from the API
'''


class DataService:

    def __init__(self):
        self.prod_details = {}
        self.api_conf = "https://tenbis-static.azureedge.net/restaurant-menu/19156_en"
        self.log = logging.getLogger()
        self.prod_list = ["Drinks", "Pizzas", "Desserts"]
        self.prod_info = ["dishId", "dishName", "dishDescription", "dishPrice"]
        self.conf_prod()  # Active this at init to get all the data from the API

    '''
    This method will take data from the API based on a list of categories ("prod_list")
    and store them in a dictionary where:
    - The key is the product's category name.
    - The value will be all the items from that category.
    ** Note: this will be a thread that will update the dictionary every 24 hours (86400 seconds).
    '''

    def conf_prod(self):
        # The response from the API
        response = requests.get(self.api_conf)
        # Format as json and retrieves the list of all the categories
        json_url = response.json()["categoriesList"]
        for i in json_url:
            prod_cat = i["categoryName"]
            # Find only the categories in json_url that match those in "prod_list"
            if prod_cat in self.prod_list:
                temp = {}
                for j in i["dishList"]:
                    # Each dish is added to a dictionary where - key = DishId, value = details from "prod_info"
                    temp[str(j["dishId"])] = {key: j[key] for key in self.prod_info}
                # Store it in a dic where - key = product category, value = dictionary of products in category
                self.prod_details[prod_cat] = temp
                self.log.info("Updated category: ", prod_cat)
                print("Updated category: ", prod_cat)

    '''
    Retrieves all the drinks available in the restaurant
    '''

    def get_all_drinks(self):
        return self.prod_details["Drinks"]

    '''
    Retrieves a drink based on a DishId
    '''

    def get_drink_by_id(self, drink_id):
        return self.get_all_drinks()[drink_id]

    '''
    Retrieves all the pizzas available in the restaurant
    '''

    def get_all_pizzas(self):
        return self.prod_details["Pizzas"]

    '''
    Retrieves a pizza based on a DishId
    '''

    def get_pizza_by_id(self, pizza_id):
        return self.get_all_pizzas()[pizza_id]

    '''
    Retrieves all the desserts available in the restaurant
    '''

    def get_all_desserts(self):
        return self.prod_details["Desserts"]

    '''
    Retrieves a dessert based on a DishId
    '''

    def get_dessert_by_id(self, dessert_id):
        return self.get_all_desserts()[dessert_id]

    '''
    Receives an Order obj - list of id's from each category. and return the sum value of all the products ordered
    '''

    def get_total_order_price(self, order):
        total_price = 0
        for i in order.drinks:
            total_price += self.get_drink_by_id(i)["dishPrice"]
        for j in order.pizzas:
            total_price += self.get_pizza_by_id(j)["dishPrice"]
        for q in order.desserts:
            total_price += self.get_dessert_by_id(q)["dishPrice"]
        return total_price
