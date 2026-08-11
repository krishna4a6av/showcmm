from tabulate import tabulate

def display_table(data: list[tuple[str, int]]) -> None:
    table = [[cmd, count] for cmd, count in data]
    print(tabulate(table, headers=["commands", "number"]))
