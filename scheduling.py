from pulp import *

# 職員sの集合。
S = [str(i + 1) for i in range(50)]
# 日dの集合。
D = [str(i + 1) for i in range(31)]
# 土曜日dの集合。
H = [d for d in D if (int(d) - 5) % 7 == 0]
# 勤務kの集合。
K = [' ', 'a', 'b', 'c', 'd', 'e']
# グループgの集合。
G = ['A', 'B', 'C', 'D', 'E']
# グループgに所属する職員sの集合。
SG = {'A': S[0:10], 'B': S[10:20], 'C': S[20:30], 'D': S[30:40], 'E': S[40:50]}
# 連続禁止勤務並びの集合。
P = [['e', 'a']]

# 日dの勤務kにグループgから割り当てる職員数の下限。
c1 = {
    d: {
        'a': {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1,
            'E': 1
        },
        'b': {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1,
            'E': 1
        },
        'c': {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1,
            'E': 1
        },
        'd': {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1,
            'E': 1
        },
        'e': {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1,
            'E': 1
        }
    }
    for d in D
}
# 日dの勤務kにグループgから割り当てる職員数の上限。
c2 = {
    d: {
        'a': {
            'A': 2,
            'B': 2,
            'C': 2,
            'D': 2,
            'E': 2
        },
        'b': {
            'A': 2,
            'B': 2,
            'C': 2,
            'D': 2,
            'E': 2
        },
        'c': {
            'A': 2,
            'B': 2,
            'C': 2,
            'D': 2,
            'E': 2
        },
        'd': {
            'A': 2,
            'B': 2,
            'C': 2,
            'D': 2,
            'E': 2
        },
        'e': {
            'A': 2,
            'B': 2,
            'C': 2,
            'D': 2,
            'E': 2
        }
    }
    for d in D
}
# 職員sの勤務kの割り当て数の下限。
c3 = {s: {' ': 10} for s in S}
# 職員sの勤務kの割り当て数の上限。
c4 = {s: {} for s in S}
# 勤務kの連続日数の下限。
c5 = {}
# 勤務kの連続日数の上限。
c6 = {'e': 2}
# 勤務kの間隔日数の下限。
c7 = {' ': 2}
# 勤務kの間隔日数の上限。
c8 = {' ': 3}
# 職員sの土日休暇回数の下限。
c9 = {s: 1 for s in S}
# 職員sの土日休暇回数の上限。
c10 = {}
# 日dの職員sに割り当てる勤務k。
c11 = {}
# 日dの職員sに割り当てない勤務k。
c12 = {}

# 決定変数。
# 職員sの日dに勤務kが割り当てられているとき1。
x = LpVariable.dicts('x', (S, D, K), 0, 1, LpBinary)
# 職員sに土曜日dから始まる土日休暇が割り当てられているとき1。
y = LpVariable.dicts('y', (S, H), 0, 1, LpBinary)

problem = LpProblem('Scheduling', LpMinimize)

# 目的関数。
problem += sum(c1[d][k][g] - sum(x[s][d][k] for s in SG[g])
               for d in D if d in c1
               for k in K if k in c1[d]
               for g in G if g in c1[d][k]) + \
    sum(sum(x[s][d][k] for s in SG[g]) - c2[d][k][g]
        for d in D if d in c2
        for k in K if k in c2[d]
        for g in G if g in c2[d][k])

# 各職員sの各日dに割り当てる勤務の数は1。
for s in S:
    for d in D:
        problem += sum([x[s][d][k] for k in K]) == 1, ''

for d in D:
    if d not in c1:
        continue
    for k in K:
        if k not in c1[d]:
            continue
        for g in G:
            if g not in c1[d][k]:
                continue
            problem += sum(x[s][d][k] for s in SG[g]) >= c1[d][k][g], ''
for d in D:
    if d not in c2:
        continue
    for k in K:
        if k not in c2[d]:
            continue
        for g in G:
            if g not in c2[d][k]:
                continue
            problem += sum(x[s][d][k] for s in SG[g]) <= c2[d][k][g], ''

for s in S:
    if s not in c3:
        continue
    for k in K:
        if k not in c3[s]:
            continue
        problem += sum(x[s][d][k] for d in D) >= c3[s][k]
for s in S:
    if s not in c4:
        continue
    for k in K:
        if k not in c4[s]:
            continue
        problem += sum(x[s][d][k] for d in D) <= c4[s][k]

for s in S:
    for k in K:
        if k not in c5:
            continue
        for d in D:
            if str(int(d) - c5[k]) not in D:
                continue
            problem += sum(x[s][str(int(d) - i)][k]
                           for i in range(0, c5[k] + 1)) >= c5[k]
for s in S:
    for k in K:
        if k not in c6:
            continue
        for d in D:
            if str(int(d) - c6[k]) not in D:
                continue
            problem += sum(x[s][str(int(d) - i)][k]
                           for i in range(0, c6[k] + 1)) <= c6[k]

for s in S:
    for k in K:
        if k not in c7:
            continue
        for d in D:
            for i in range(2, c7[k] + 1):
                if str(int(d) - i) not in D:
                    continue
                problem += x[s][str(int(d) - i)][k] - \
                    sum(x[s][str(int(d) - j)][k] for j in range(1, i)) + \
                    x[s][d][k] <= 1
for s in S:
    for k in K:
        if k not in c8:
            continue
        for d in D:
            if str(int(d) - c8[k]) not in D:
                continue
            problem += sum(x[s][str(int(d) - i)][k]
                           for i in range(0, c8[k] + 1)) >= 1

for s in S:
    if s in c9:
        problem += sum(y[s][d] for d in H) >= c9[s]
    if s in c10:
        problem += sum(y[s][d] for d in H) <= c10[s]
    for d in H:
        problem += 2 * y[s][d] - x[s][d][' '] - x[s][str(int(d) + 1)][' '] <= 0
        problem += y[s][d] - x[s][d][' '] - x[s][str(int(d) + 1)][' '] >= -1

for s in S:
    if s not in c11:
        continue
    for d in D:
        if d not in c11[s]:
            continue
        for k in K:
            if k not in c11[s][d]:
                continue
            problem += x[s][d][k] == 1
for s in S:
    if s not in c12:
        continue
    for d in D:
        if d not in c12[s]:
            continue
        for k in K:
            if k not in c12[s][d]:
                continue
            problem += x[s][d][k] == 0

for s in S:
    for p in P:
        l = len(p) - 1
        for d in D:
            if str(int(d) - l) not in D:
                continue
            problem += sum(x[s][str(int(d) - l + i)][p[i]]
                           for i in range(0, l + 1)) <= l

problem.writeLP('scheduling.lp')

with open('scheduling.txt', 'w') as f:
    while True:
        problem.solve()
        print("Status:", LpStatus[problem.status])
        if LpStatus[problem.status] != 'Optimal':
            break
        ls = max(len(s) for s in S)
        f.write(' ' * ls + '|' + ''.join([d[-1:] for d in D]) + '|\n')
        f.write('-' * ls + '+' + ('-' * len(D)) + '+\n')
        for s in S:
            f.write(s.rjust(ls) + '|')
            for d in D:
                for k in K:
                    if x[s][d][k].value() == 1:
                        f.write(k)
                        break
            f.write('|\n')
        f.write('-' * ls + '+' + ('-' * len(D)) + '+\n')
        problem += sum(x[s][d][k] for s in S for d in D for k in K
                       if x[s][d][k].value() == 1) <= len(S) * len(D) - 1
        break
