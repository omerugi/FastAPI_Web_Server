import logging
import threading
import time

import uvicorn
from fastapi import FastAPI, Path, Response, status
import requests
from Modules import DataService, Order

data = DataService()
app = FastAPI()
log = logging.getLogger()


@app.get("/")
def get_info():
    api = "https://tenbis-static.azureedge.net/restaurant-menu/19156_en"
    response = requests.get(api)
    json_url = response.json()["categoriesList"]
    return json_url


@app.get("/drinks", status_code=200)
def get_drinks():
    return data.get_all_drinks()


@app.get("/drink/{drink_id}", status_code=200)
def get_drink(response: Response, drink_id: str):
    try:
        return data.get_drink_by_id(drink_id)
    except Exception:
        log.error(f"drink with id {drink_id} is not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details": f"drink with id {drink_id} is not found"}


@app.get("/pizzas", status_code=200)
def get_pizzas():
    return data.get_all_pizzas()


@app.get("/pizza/{pizza_id}", status_code=200)
def get_pizza(response: Response, pizza_id: str):
    try:
        return data.get_pizza_by_id(pizza_id)
    except Exception:
        log.error(f"drink with id {pizza_id} is not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details": f"pizza with id {pizza_id} is not found"}


@app.get("/desserts", status_code=200)
def get_desserts():
    return data.get_all_desserts()


@app.get("/dessert/{dessert_id}", status_code=200)
def get_dessert(response: Response,
                dessert_id: str):
    try:
        return data.get_dessert_by_id(dessert_id)
    except Exception:
        log.error(f"drink with id {dessert_id} is not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details": f"dessert with id {dessert_id} is not found"}


@app.post("/order", status_code=200)
def post_order(response: Response, order: Order):
    try:
        total_price = data.get_total_order_price(order)
        return {"Total price": total_price}
    except Exception:
        log.error(f"One or more id's are not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details": f"One or more id's are not found"}


'''
This method will work on a thread and every 24h will update the new data from the API
'''

def th_update_data():
    while True:
        data.conf_prod()
        time.sleep(86400)


if __name__ == "__main__":
    th = threading.Thread(target=th_update_data)
    th.start()
    uvicorn.run(app)
