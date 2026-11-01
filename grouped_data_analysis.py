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

with open("urban_climate.csv", "r", newline="", encoding="utf-8") as file:
    data = list(csv.DictReader(file))

attributes = ["temperature_celsius", "humidity_percent", "precipitation_mm"]

# Group records by city
city_groups = {}
for row in data:
    city = row["city"]
    if city not in city_groups:
        city_groups[city] = []
    city_groups[city].append(row)

for city, rows in city_groups.items():
    print("\\n--------------------------------")
    print("City:", city)
    print("Frequency:", len(rows))
    for column in attributes:
        values = read_numeric_column(rows, column)
        q1, q2, q3, iqr = get_quartiles(values)
        print("\\nAttribute:", column)
        print("Mean:", get_mean(values))
        print("Mode:", get_mode(values))
        print("Median:", get_median(values))
        print("Sample variance:", get_variance(values))
        print("Sample standard deviation:", get_standard_deviation(values))
        print("IQR:", iqr)
