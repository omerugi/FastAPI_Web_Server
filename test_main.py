from fastapi.testclient import TestClient
import requests
from main import app

client = TestClient(app)
response_api = requests.get("https://tenbis-static.azureedge.net/restaurant-menu/19156_en")
json_url = response_api.json()["categoriesList"]


def drinks_from_api():
    for i in json_url:
        if i["categoryName"] == "Drinks":
            return i["dishList"]


def pizzas_from_api():
    for i in json_url:
        if i["categoryName"] == "Pizzas":
            return i["dishList"]


def desserts_from_api():
    for i in json_url:
        if i["categoryName"] == "Desserts":
            return i["dishList"]


def test_status_code_drinks():
    response = client.get("/drinks")
    assert (response.status_code == 200)


def test_all_drinks():
    response = client.get("/drinks")
    all_drinks = response.json()
    ans_from_api = drinks_from_api()
    assert (len(all_drinks) == len(ans_from_api))

    for i, j in zip(all_drinks, ans_from_api):
        assert (all_drinks[i]["dishId"] == j["dishId"])
        assert (all_drinks[i]["dishName"] == j["dishName"])
        assert (all_drinks[i]["dishDescription"] == j["dishDescription"])
        assert (all_drinks[i]["dishPrice"] == j["dishPrice"])


def test_drink_by_id():
    valid_drink_codes = ["2055846", "2055838", "2055839", "2055840"]
    name_set = ["Green Power", "Coca-Cola", "Cola Zero", "diet Coke"]
    price_set = [16.0, 12.0, 12.0, 12.0]
    for i in range(len(valid_drink_codes)):
        response = client.get(f"/drink/{valid_drink_codes[i]}")
        assert (response.status_code == 200)
        response_json = response.json()
        assert (name_set[i] == response_json["dishName"])
        assert (price_set[i] == response_json["dishPrice"])

    invalid_drink_codes = ["0", "33", "hey"]
    for i in range(len(invalid_drink_codes)):
        response = client.get(f"/drink/{invalid_drink_codes[i]}")
        assert (response.status_code == 404)
        assert (response.json() == {"details": f"drink with id {invalid_drink_codes[i]} is not found"})


def test_status_code_pizzas():
    response = client.get("/pizzas")
    assert (response.status_code == 200)


def test_all_pizzas():
    response = client.get("/pizzas")
    all_pizzas = response.json()
    ans_from_api = pizzas_from_api()
    assert (len(all_pizzas) == len(ans_from_api))

    for i, j in zip(all_pizzas, ans_from_api):
        assert (all_pizzas[i]["dishId"] == j["dishId"])
        assert (all_pizzas[i]["dishName"] == j["dishName"])
        assert (all_pizzas[i]["dishDescription"] == j["dishDescription"])
        assert (all_pizzas[i]["dishPrice"] == j["dishPrice"])


def test_pizza_by_id():
    valid_pizza_codes = ["2055830", "2055831", "2055832", "2055833"]
    name_set = ["Margarita", "Pongy", "Calabria", "Goat cheese and arugula"]
    description_set = ["Italian tomato sauce, mozzarella and olive oil Frmgno",
                       "Italian tomato sauce, mushrooms, mozzarella, olive oil, parsley and Frmgno",
                       "Italian tomato sauce, mozzarella and spicy chili peppers, kalamata olives Aorogno and Frmgno",
                       "Italian tomato sauce, mozzarella and goat cheese arugula and Frmgno"]
    price_set = [50.0, 55.0, 55.0, 55.0]
    for i in range(len(valid_pizza_codes)):
        response = client.get(f"/pizza/{valid_pizza_codes[i]}")
        assert (response.status_code == 200)
        response_json = response.json()
        assert (name_set[i] == response_json["dishName"])
        assert (description_set[i] == response_json["dishDescription"])
        assert (price_set[i] == response_json["dishPrice"])

    invalid_drink_codes = ["0", "33", "hey"]
    for i in range(len(invalid_drink_codes)):
        response = client.get(f"/pizza/{invalid_drink_codes[i]}")
        assert (response.status_code == 404)
        assert (response.json() == {"details": f"pizza with id {invalid_drink_codes[i]} is not found"})


def test_status_code_desserts():
    response = client.get("/desserts")
    assert (response.status_code == 200)


def test_all_desserts():
    response = client.get("/desserts")
    all_pizzas = response.json()
    ans_from_api = desserts_from_api()
    assert (len(all_pizzas) == len(ans_from_api))

    for i, j in zip(all_pizzas, ans_from_api):
        assert (all_pizzas[i]["dishId"] == j["dishId"])
        assert (all_pizzas[i]["dishName"] == j["dishName"])
        assert (all_pizzas[i]["dishDescription"] == j["dishDescription"])
        assert (all_pizzas[i]["dishPrice"] == j["dishPrice"])


def test_dessert_by_id():
    valid_dessert_codes = ["2055835", "2055836", "2055837"]
    name_set = ["Tiramisu", "Cheesecake crumbs (no sugar added)", "Tart The Wanderer"]
    price_set = [29, 29, 27]
    for i in range(len(valid_dessert_codes)):
        response = client.get(f"/dessert/{valid_dessert_codes[i]}")
        assert (response.status_code == 200)
        response_json = response.json()
        assert (name_set[i] == response_json["dishName"])
        assert (price_set[i] == response_json["dishPrice"])

    invalid_drink_codes = ["0", "33", "hey"]
    for i in range(len(invalid_drink_codes)):
        response = client.get(f"/dessert/{invalid_drink_codes[i]}")
        assert (response.status_code == 404)
        assert (response.json() == {"details": f"dessert with id {invalid_drink_codes[i]} is not found"})


def test_order():
    order = {
        "drinks": ["2055846", "2055838", "2055839", "2055840"],
        "desserts": ["2055835", "2055836", "2055837"],
        "pizzas": ["2055830", "2055831", "2055832", "2055833"]
    }
    sum_order = 16.0 + 12.0 + 12.0 + 12.0 + 29 + 29 + 27 + 50.0 + 55.0 + 55.0 + 55.0
    response = client.post("/order", json=order)
    assert (response.status_code == 200)
    response_json = response.json()
    assert (response_json['Total price'] == sum_order)

    order = {
        "drinks": ["2055838", "2055839", "2055840"],
        "desserts": ["2055835", "2055836", "2055837"],
        "pizzas": ["2055830", "2055832"]
    }
    sum_order = 12.0 + 12.0 + 12.0 + 29 + 29 + 27 + 50.0 + 55.0
    response = client.post("/order", json=order)
    assert (response.status_code == 200)
    response_json = response.json()
    assert (response_json['Total price'] == sum_order)

    order = {
        "drinks": ["2055838", "2055839", "2055840"],
        "desserts": ["2055835", "2055836", "2055837"],
        "pizzas": ["2055830", "2055832", "2"]
    }
    response = client.post("/order", json=order)
    assert (response.status_code == 404)
    response_json = response.json()
    assert (response_json == {"details": f"One or more id's are not found"})
