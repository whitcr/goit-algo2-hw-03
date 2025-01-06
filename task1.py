import networkx as nx
from collections import defaultdict

def create_network():
    G = nx.DiGraph()
    
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    
    return G, edges

def analyze_network(G, edges):
    # Аналіз потоків від терміналів через склади до магазинів
    terminal_flows = defaultdict(int)
    warehouse_flows = defaultdict(int)
    store_flows = defaultdict(int)
    
    # Розрахунок максимального потоку для кожного магазину
    for edge in edges:
        if edge[1].startswith("Магазин"):
            store = edge[1]
            warehouse = edge[0]
            capacity = edge[2]
            
            # Знаходимо максимальний потік до конкретного магазину
            flow_value, flow_dict = nx.maximum_flow(G, "Термінал 1", store)
            flow_value2, flow_dict2 = nx.maximum_flow(G, "Термінал 2", store)
            
            store_flows[store] = flow_value + flow_value2
            warehouse_flows[warehouse] += min(capacity, flow_value + flow_value2)
            
            # Додаємо потоки до терміналів
            if flow_value > 0:
                terminal_flows["Термінал 1"] += flow_value
            if flow_value2 > 0:
                terminal_flows["Термінал 2"] += flow_value2

    return terminal_flows, warehouse_flows, store_flows

def main():
    G, edges = create_network()
    terminal_flows, warehouse_flows, store_flows = analyze_network(G, edges)
    
    print("\n1. Аналіз потоків через термінали:")
    print("-" * 50)
    for terminal, flow in sorted(terminal_flows.items()):
        print(f"{terminal}: {flow} одиниць")
    
    print("\n2. Аналіз пропускної здатності маршрутів:")
    print("-" * 50)
    for u, v, capacity in sorted(edges, key=lambda x: x[2]):
        print(f"{u} -> {v}: {capacity} одиниць")
    
    print("\n3. Аналіз отримання товарів магазинами:")
    print("-" * 50)
    for store, flow in sorted(store_flows.items(), key=lambda x: x[1]):
        print(f"{store}: {flow} одиниць")
    
    print("\n4. Аналіз вузьких місць мережі:")
    print("-" * 50)
    bottlenecks = [(u, v, c) for u, v, c in edges if c <= 10]
    for u, v, capacity in sorted(bottlenecks, key=lambda x: x[2]):
        print(f"Вузьке місце: {u} -> {v} (пропускна здатність: {capacity} одиниць)")

if __name__ == "__main__":
    main()
    
    
# 1. Які термінали забезпечують найбільший потік товарів до магазинів?
# Обидва термінали забезпечують однаковий потік - по 130 одиниць 

# 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?
# Найменшу пропускну здатність має маршрут Склад 4, Магазин 13, 5 одиниць

# Ці обмеження створюють "вузькі місця" у системі та обмежують загальний потік товарів до відповідних магазинів.

# 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання?

# Магазини з найменшим отриманням товарів:
# Магазин 13, 5 одиниць
# Магазин 2, 11, 14, по 10 одиниць

# Постачання можна збільшити шляхом більшення пропускної здатності прямих маршрутів до цих магазинів

# 4. Чи є вузькі місця, які можна усунути для покращення ефективності логістичної мережі?
# Основні вузькі місця:
# Критичне вузьке місце: Склад 4, Магазин 13, 5 одиниць
# Системне вузьке місце: Термінал 2, Склад 2, 10 одиниць, яке обмежує загальну пропускну здатність для всіх магазинів, що обслуговуються через Склад 2