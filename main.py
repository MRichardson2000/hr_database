from create_csv import create_csv
from queries import find_performance_averages


def main():
    data = find_performance_averages()
    headers = list(data[0].keys() if data else [])
    create_csv(data, "highest_paid_employees", headers)


if __name__ == "__main__":
    main()
