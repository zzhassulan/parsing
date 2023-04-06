import json
import csv
import requests
from bs4 import BeautifulSoup

urls = "https://health-diet.ru/table_calorie/"
header = {
    "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320"
}

# RESPONSE GET SITE__________________________________

response = requests.get(url=urls, headers=header)
src = response.text
# print(src)

with open("core/index.html", "w") as responseFILE:
    responseFILE.write(src)

# _______________________________________________-

# mzr-tc-group-item-href

with open("core/index.html", "r") as responseFILE:
    src = responseFILE.read()

soup = BeautifulSoup(src, "lxml")
all_titles = soup.find_all("a", class_="mzr-tc-group-item-href")

all_cotigories_dict = {}

print(all_titles)
for item in all_titles:
    item_title = item.text
    item_url = "https://health-diet.ru" + item.get("href")
    # print(item_title)
    # print(item_url)

    all_cotigories_dict[item_title] = item_url

with open("core/all_cotigories_dict.json", "w", encoding="UTF-8") as SaveCatigories:
    json.dump(all_cotigories_dict, SaveCatigories, indent=4, ensure_ascii=False)
# _________________________________________________________________

with open("core/all_cotigories_dict.json", "r") as READJSON:
    all_cotigories = json.load(READJSON)

iterable_count = int(len(all_cotigories)) - 1
count = 0
for cotegory_name, cotegory_url in all_cotigories.items():
    rep = [",", " ", "-", "'", "(", ")"]
    for item_rep in rep:
        if item_rep in cotegory_name:
            cotegory_name = cotegory_name.replace(item_rep, "_")

    response = requests.get(url=cotegory_url, headers=header)
    src = response.text

    with open(f"core/{count}_{cotegory_name}.html", "w") as file:
        file.write(src)
    
    with open(f"core/{count}_{cotegory_name}.html", "r") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    
    # Собираем загаловки таблицы
    table_header = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    # mzr-tc-group-table
    product = table_header[0].text
    colories = table_header[1].text
    priteins = table_header[2].text
    fats = table_header[3].text
    carbohydrates = table_header[4].text

    with open(f"core/{count}_{cotegory_name}.csv", "w", encoding="UTF-8") as CsvFile:
        writer = csv.writer(CsvFile)

        writer.writerow(
            (
                product,
                colories,
                priteins,
                fats,
                carbohydrates
            )
        )
    product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []

    for item in product_data:
        product_tds = item.find_all("td")

        product_name = product_tds[0].find("a").text
        product_calories = product_tds[1].text
        product_priteins = product_tds[2].text
        product_fats = product_tds[3].text
        product_carbohydrates = product_tds[4].text

        product_info.append(
            {
                'name': product_name,
                'calories': product_calories,
                'priteins': product_priteins,
                'fats': product_fats,
                'carbohydrates': product_carbohydrates,
            }
        )

        with open(f"core/{count}_{cotegory_name}.csv", "a", encoding="UTF-8") as CsvFile:
            writer = csv.writer(CsvFile)

            writer.writerow(
                (
                    product_name,
                    product_calories,
                    product_priteins,
                    product_fats,
                    product_carbohydrates,
                )
            )
    with open(f"core/{count}_{cotegory_name}.json", "w", encoding="UTF-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
    
    count += 1
    print(f"# Итерация {count}. {cotegory_name} Записан...")
    iterable_count = iterable_count - 1
    if iterable_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итерации: {iterable_count}")