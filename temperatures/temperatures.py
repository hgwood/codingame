ntemperatures = int(input())
temperatures = list(map(int, input().split())) if ntemperatures else [0]
print(min(temperatures, key=lambda t: (abs(t), -t, t)))
