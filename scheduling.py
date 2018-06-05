import pulp
import pandas as pd

# 職員sの集合。
staffs = pd.read_csv('./data/staffs.csv', dtype={'職員名': str})
S = [r['職員名'] for _, r in staffs.iterrows()]
# 日dの集合。
days = pd.read_csv('./data/days.csv', dtype={'日付': str})
D = [r['日付'] for _, r in days.iterrows()]
# 土曜日dの集合。
H = [d for d in D if (int(d) - 5) % 7 == 0]
# 勤務kの集合。
kinmus = pd.read_csv('./data/kinmus.csv', dtype={'勤務名': str})
K = [r['勤務名'] for _, r in kinmus.iterrows()]
# グループgの集合。
groups = pd.read_csv('./data/groups.csv', dtype={'グループ名': str})
G = [r['グループ名'] for _, r in groups.iterrows()]
# グループgに所属する職員sの集合。
staff_groups = pd.read_csv(
    './data/staff_groups.csv', dtype={
        'グループ名': str,
        '職員名': str
    })
SG = {
    g: [r['職員名'] for _, r in staffs.iterrows()]
    for g, staffs in staff_groups.groupby('グループ名')
}
# 連続禁止勤務並びの集合。
renzoku_kinshi_kinmus = pd.read_csv(
    './data/renzoku_kinshi_kinmus.csv',
    dtype={
        '並びID': int,
        '勤務名': str,
        '並び順': int
    })
P = [[r['勤務名'] for _, r in kinmus.sort_values(by='並び順').iterrows()]
     for _, kinmus in renzoku_kinshi_kinmus.groupby('並びID')]

# 日dの勤務kにグループgから割り当てる職員数の下限。
c1_df = pd.read_csv(
    './data/c1.csv',
    dtype={
        '日付': str,
        '勤務名': str,
        'グループ名': str,
        '割り当て職員数下限': int
    })
c1 = {
    d: {
        k: {r['グループ名']: r['割り当て職員数下限']
            for _, r in groups.iterrows()}
        for k, groups in kinmus.groupby('勤務名')
    }
    for d, kinmus in c1_df.groupby('日付')
}
# 日dの勤務kにグループgから割り当てる職員数の上限。
c2_df = pd.read_csv(
    './data/c2.csv',
    dtype={
        '日付': str,
        '勤務名': str,
        'グループ名': str,
        '割り当て職員数上限': int
    })
c2 = {
    d: {
        k: {r['グループ名']: r['割り当て職員数上限']
            for _, r in groups.iterrows()}
        for k, groups in kinmus.groupby('勤務名')
    }
    for d, kinmus in c2_df.groupby('日付')
}
# 職員sの勤務kの割り当て数の下限。
c3_df = pd.read_csv(
    './data/c3.csv', dtype={
        '職員名': str,
        '勤務名': str,
        '割り当て数下限': int
    })
c3 = {
    s: {r['勤務名']: r['割り当て数下限']
        for _, r in kinmus.iterrows()}
    for s, kinmus in c3_df.groupby('職員名')
}
# 職員sの勤務kの割り当て数の上限。
c4_df = pd.read_csv(
    './data/c4.csv', dtype={
        '職員名': str,
        '勤務名': str,
        '割り当て数上限': int
    })
c4 = {
    s: {r['勤務名']: r['割り当て数上限']
        for _, r in kinmus.iterrows()}
    for s, kinmus in c4_df.groupby('職員名')
}
# 勤務kの連続日数の下限。
c5_df = pd.read_csv('./data/c5.csv', dtype={'勤務名': str, '連続日数下限': int})
c5 = {r['勤務名']: r['連続日数下限'] for _, r in c5_df.iterrows()}
# 勤務kの連続日数の上限。
c6_df = pd.read_csv('./data/c6.csv', dtype={'勤務名': str, '連続日数上限': int})
c6 = {r['勤務名']: r['連続日数上限'] for _, r in c6_df.iterrows()}
# 勤務kの間隔日数の下限。
c7_df = pd.read_csv('./data/c7.csv', dtype={'勤務名': str, '間隔日数下限': int})
c7 = {r['勤務名']: r['間隔日数下限'] for _, r in c7_df.iterrows()}
# 勤務kの間隔日数の上限。
c8_df = pd.read_csv('./data/c8.csv', dtype={'勤務名': str, '間隔日数上限': int})
c8 = {r['勤務名']: r['間隔日数上限'] for _, r in c8_df.iterrows()}
# 職員sの土日休暇回数の下限。
c9_df = pd.read_csv('./data/c9.csv', dtype={'職員名': str, '土日休暇回数下限': int})
c9 = {r['職員名']: r['土日休暇回数下限'] for _, r in c9_df.iterrows()}
# 職員sの土日休暇回数の上限。
c10_df = pd.read_csv('./data/c10.csv', dtype={'職員名': str, '土日休暇回数上限': int})
c10 = {r['職員名']: r['土日休暇回数上限'] for _, r in c10_df.iterrows()}
# 職員sの日dに割り当てる勤務k。
c11_df = pd.read_csv(
    './data/c11.csv', dtype={
        '職員名': str,
        '日付': str,
        '割り当て勤務名': str
    })
c11 = {
    s: {r['日付']: r['割り当て勤務名']
        for _, r in kinmus.iterrows()}
    for s, kinmus in c11_df.groupby('職員名')
}
# 職員sの日dに割り当てない勤務k。
c12_df = pd.read_csv(
    './data/c12.csv', dtype={
        '職員名': str,
        '日付': str,
        '割り当てない勤務名': str
    })
c12 = {
    s: {r['日付']: r['割り当てない勤務名']
        for _, r in kinmus.iterrows()}
    for s, kinmus in c12_df.groupby('職員名')
}

# 決定変数。
# 職員sの日dに勤務kが割り当てられているとき1。
x = pulp.LpVariable.dicts('x', (S, D, K), 0, 1, pulp.LpBinary)
# 職員sに土曜日dから始まる土日休暇が割り当てられているとき1。
y = pulp.LpVariable.dicts('y', (S, H), 0, 1, pulp.LpBinary)

problem = pulp.LpProblem('Scheduling', pulp.LpMinimize)

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
        print("Status:", pulp.LpStatus[problem.status])
        if pulp.LpStatus[problem.status] != 'Optimal':
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
