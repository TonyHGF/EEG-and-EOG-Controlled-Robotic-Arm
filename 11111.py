# read data from 1.txt



xs = []

with open('1.txt', 'r') as f:
    for line in f:
        xs.append(float(line.strip()))

print(len(xs))

print(min(xs))

# import matplotlib.pyplot as plt

# plt.plot(xs[1500:2000])
# plt.ylim(-200,200)
# plt.show()