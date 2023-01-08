import csv

file= open("myfala.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

data.sort()
for num, spot in enumerate(data):
    a = num + 1
    spot.insert(0, a)

with open('myfala_sorted.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)