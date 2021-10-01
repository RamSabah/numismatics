


def fak_recursiv(n):# n = 0
    if(n == 0): # n = 0
        return 1
    else:
        fak = n * fak_recursiv(n-1)
        return fak

print(fak_recursiv(5))

# 120