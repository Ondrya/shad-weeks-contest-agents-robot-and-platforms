import sys
from collections import deque

def solve():
    # Быстрое чтение всех входных данных
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))

    # Массив доступных позиций (платформ)
    # 0 и n всегда доступны (старт и финиш)
    valid = [False] * (n + 1)
    valid[0] = True
    valid[n] = True
    
    for _ in range(k):
        valid[int(next(iterator))] = True

    # 1. Прямой BFS: минимальное количество прыжков от 0 до каждой точки
    dist_f = [-1] * (n + 1)
    dist_f[0] = 0
    q = deque([0])
    
    while q:
        u = q.popleft()
        for v in (u + 1, u + 2):
            if v <= n and valid[v] and dist_f[v] == -1:
                dist_f[v] = dist_f[u] + 1
                q.append(v)

    # Если до n добраться невозможно
    if dist_f[n] == -1:
        print(-1)
        return

    min_jumps = dist_f[n]

    # 2. Обратный BFS: минимальное количество прыжков от каждой точки до n
    dist_b = [-1] * (n + 1)
    dist_b[n] = 0
    q = deque([n])
    
    while q:
        u = q.popleft()
        for v in (u - 1, u - 2):
            if v >= 0 and valid[v] and dist_b[v] == -1:
                dist_b[v] = dist_b[u] + 1
                q.append(v)

    # 3. Жадное восстановление лексикографически минимального пути
    path = []
    cur = 0
    while cur < n:
        # Пробуем прыгнуть на 1, затем на 2 (для лексикографической минимальности)
        for jump in (1, 2):
            nxt = cur + jump
            if nxt <= n and valid[nxt] and dist_b[nxt] != -1:
                # Проверяем, лежит ли переход на кратчайшем пути
                if dist_f[cur] + 1 + dist_b[nxt] == min_jumps:
                    path.append(str(jump))
                    cur = nxt
                    break  # Берём первый подходящий вариант (1 < 2)

    print(min_jumps)
    print("".join(path))

if __name__ == "__main__":
    solve()