print(min(map(int,input().split()) if int(input()) else [0],key=lambda t:(abs(t),-t)))
