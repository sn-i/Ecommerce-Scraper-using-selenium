import csv

class Data:
    def __init__(self):
        pass

    def store_data(self, data, filename="scraped_data.csv"):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Product Name", "Price", "Availability"])
            writer.writerows(data)
        print(f"Data has been saved to {filename}")

    def read_data(self, filename="scraped_data.csv"):
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
            return data
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return []
