import csv

def manual_sort(values):
    # Merge sort to arrange values without using sorted().
    if len(values) <= 1:
        return values[:]
    middle = len(values) // 2
    left = manual_sort(values[:middle])
    right = manual_sort(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def get_mean(values):
    total = 0
    for value in values:
        total += value
    return total / len(values)


def get_median(values):
    data = manual_sort(values)
    n = len(data)
    if n % 2 == 0:
        return (data[n // 2 - 1] + data[n // 2]) / 2
    return data[n // 2]


def get_mode(values):
    frequency = {}
    for value in values:
        frequency[value] = frequency.get(value, 0) + 1
    highest = max(frequency.values())
    if highest == 1:
        return "No mode"
    modes = []
    for value in frequency:
        if frequency[value] == highest:
            modes.append(value)
    return modes


def get_variance(values):
    mean = get_mean(values)
    total = 0
    for value in values:
        total += (value - mean) ** 2
    if len(values) < 2:
        return 0
    return total / (len(values) - 1)


def get_standard_deviation(values):
    return get_variance(values) ** 0.5


def get_quartiles(values):
    data = manual_sort(values)
    n = len(data)
    q2 = get_median(data)
    if n % 2 == 0:
        lower = data[:n // 2]
        upper = data[n // 2:]
    else:
        lower = data[:n // 2]
        upper = data[n // 2 + 1:]
    q1 = get_median(lower)
    q3 = get_median(upper)
    return q1, q2, q3, q3 - q1


def read_numeric_column(rows, column):
    values = []
    for row in rows:
        try:
            values.append(float(row[column]))
        except (ValueError, TypeError, KeyError):
            pass
    return values

# Read the CSV file from the same folder as this program.
with open("urban_climate.csv", "r", newline="", encoding="utf-8") as file:
    data = list(csv.DictReader(file))

print("Total records:", len(data))

# Frequency of each city
city_frequency = {}
for row in data:
    city = row["city"]
    city_frequency[city] = city_frequency.get(city, 0) + 1

print("\\nFrequency of cities:")
for city, count in city_frequency.items():
    print(city, ":", count)

# Statistics for temperature, humidity and precipitation
attributes = ["temperature_celsius", "humidity_percent", "precipitation_mm"]

for column in attributes:
    values = read_numeric_column(data, column)
    print("\\nAttribute:", column)
    print("Frequency:", len(values))
    print("Mean:", get_mean(values))
    print("Median:", get_median(values))
    print("Mode:", get_mode(values))

# Optional city-wise temperature calculation
while True:
    city_name = input("\\nEnter a city name (or type exit): ")
    if city_name.lower() == "exit":
        break
    city_values = []
    for row in data:
        if row["city"].lower() == city_name.lower():
            try:
                city_values.append(float(row["temperature_celsius"]))
            except (ValueError, TypeError):
                pass
    if city_values:
        print("Mean:", get_mean(city_values))
        print("Median:", get_median(city_values))
        print("Mode:", get_mode(city_values))
    else:
        print("City not found.")
