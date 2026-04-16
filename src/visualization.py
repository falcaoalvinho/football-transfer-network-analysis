import matplotlib.pyplot as plt

COLORS = [

"#FF0000",
"#FF4D00",
"#FF9900",
"#FFE600",
"#CCFF00",
"#80FF00",
"#33FF00",
"#00FF1A",
"#00FF66",
"#00FFB3",
"#00FFFF",
"#00B3FF",
"#0066FF",
"#001AFF",
"#3300FF",
"#8000FF",
"#CC00FF",
"#FF00E6",
"#FF0099"
]

def dict_to_histogram(data_set: dict, bins: int,) -> None:
    data_list = [(key, value) for key, value in data_set.items()]

    values, columns, bars = plt.hist(data_list, bins=bins, edgecolor="black")
    plt.bar_label(bars, fontsize=10, color="black")
    plt.title("Distribuição das Centralidades dos Vértices")
    plt.xlabel("Centralidade dos Vértices")
    plt.show()