import csv
import timeit
from BTrees.OOBTree import OOBTree

def load_data_from_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            })
    return data

def add_item_to_tree(tree, item):
    tree[item["ID"]] = {"Name": item["Name"], "Category": item["Category"], "Price": item["Price"]}

def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = {"Name": item["Name"], "Category": item["Category"], "Price": item["Price"]}

def range_query_tree(tree, min_price, max_price):
    return [value for _, value in tree.items(min_price, max_price)]

def range_query_dict(dictionary, min_price, max_price):
    return [value for value in dictionary.values() if min_price <= value["Price"] <= max_price]

def main():
    data = load_data_from_csv("generated_items_data.csv")

    tree = OOBTree()
    dictionary = {}

    for item in data:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    min_price = 50.0
    max_price = 150.0

    tree_time = timeit.timeit(lambda: range_query_tree(tree, min_price, max_price), number=100)
    
    dict_time = timeit.timeit(lambda: range_query_dict(dictionary, min_price, max_price), number=100)
    
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()
