import operator
import pulp
from server import models


def solve():
    # 職員mの集合。
    members = models.Member.query.all()
    M = [member.id for member in members]
    # 日付dの集合。
    dates = models.Date.query.order_by(models.Date.name.asc()).all()
    D = [date.id for date in dates]
    # 勤務kの集合。
    kinmus = models.Kinmu.query.all()
    K = [kinmu.id for kinmu in kinmus]
    # グループgの集合。
    groups = models.Group.query.all()
    G = [group.id for group in groups]
    # グループgに所属する職員mの集合。
    group_members = models.GroupMember.query.all()
    GM = {
        group.id: [
            group_member.member_id for group_member in group_members
            if group_member.group_id == group.id
        ]
        for group in groups
    }
    # 連続禁止勤務並びの集合。
    renzoku_kinshi_kinmus = models.RenzokuKinshiKinmu.query.all()
    P = [[
        renzoku_kinshi_kinmu.kinmu_id for renzoku_kinshi_kinmu in sorted(
            renzoku_kinshi_kinmus, key=operator.attrgetter('sequence_number'))
        if renzoku_kinshi_kinmu.sequence_id == sequence_id
    ] for sequence_id in list(
        set(renzoku_kinshi_kinmu.sequence_id
            for renzoku_kinshi_kinmu in renzoku_kinshi_kinmus))]

    # 日付dの勤務kにグループgから割り当てる職員数の下限。
    c1s = models.C1.query.all()
    c1 = {
        date_id: {
            kinmu_id: {
                r.group_id: r.min_number_of_assignments
                for r in c1s if r.date_id == date_id and r.kinmu_id == kinmu_id
            }
            for kinmu_id in list(
                set(r.kinmu_id
                    for r in [r for r in c1s if r.date_id == date_id]))
        }
        for date_id in list(set(r.date_id for r in c1s))
    }
    # 日付dの勤務kにグループgから割り当てる職員数の上限。
    c2s = models.C2.query.all()
    c2 = {
        date_id: {
            kinmu_id: {
                r.group_id: r.max_number_of_assignments
                for r in c2s if r.date_id == date_id and r.kinmu_id == kinmu_id
            }
            for kinmu_id in list(
                set(r.kinmu_id
                    for r in [r for r in c2s if r.date_id == date_id]))
        }
        for date_id in list(set(r.date_id for r in c2s))
    }
    # 職員sの勤務kの割り当て数の下限。
    c3s = models.C3.query.all()
    c3 = {
        member_id: {
            r.kinmu_id: r.min_number_of_assignments
            for r in c3s if r.member_id == member_id
        }
        for member_id in list(set(r.member_id for r in c3s))
    }
    # 職員sの勤務kの割り当て数の上限。
    c4s = models.C4.query.all()
    c4 = {
        member_id: {
            r.kinmu_id: r.max_number_of_assignments
            for r in c4s if r.member_id == member_id
        }
        for member_id in list(set(r.member_id for r in c4s))
    }
    # 勤務kの連続日数の下限。
    c5s = models.C5.query.all()
    c5 = {r.kinmu_id: r.min_number_of_days for r in c5s}
    # 勤務kの連続日数の上限。
    c6s = models.C6.query.all()
    c6 = {r.kinmu_id: r.max_number_of_days for r in c6s}
    # 勤務kの間隔日数の下限。
    c7s = models.C7.query.all()
    c7 = {r.kinmu_id: r.min_number_of_days for r in c7s}
    # 勤務kの間隔日数の上限。
    c8s = models.C8.query.all()
    c8 = {r.kinmu_id: r.max_number_of_days for r in c8s}
    # 職員sの日付dに割り当てる勤務k。
    c9s = models.C9.query.all()
    c9 = {
        member_id:
        {r.date_id: r.kinmu_id
         for r in c9s in r.member_id == member_id}
        for member_id in list(set(r.member_id for r in c9s))
    }
    # 職員sの日付dに割り当てない勤務k。
    c10s = models.C10.query.all()
    c10 = {
        member_id: {r.date_id: r.kinmu_id
                    for r in c10s in r.member_id}
        for member_id in list(set(r.member_id for r in c10s))
    }

    # 決定変数。
    # 職員mの日付dに勤務kが割り当てられているとき1。
    x = pulp.LpVariable.dicts('x', (M, D, K), 0, 1, pulp.LpBinary)

    problem = pulp.LpProblem('Scheduling', pulp.LpMinimize)

    # 目的関数。
    problem += sum(c1[d][k][g] - sum(x[m][d][k] for m in GM[g])
                   for d in D if d in c1
                   for k in K if k in c1[d]
                   for g in G if g in c1[d][k]) + \
        sum(sum(x[m][d][k] for m in GM[g]) - c2[d][k][g]
            for d in D if d in c2
            for k in K if k in c2[d]
            for g in G if g in c2[d][k])

    # 各職員mの各日dに割り当てる勤務の数は1。
    for m in M:
        for d in D:
            problem += sum([x[m][d][k] for k in K]) == 1, ''

    for d in D:
        if d not in c1:
            continue
        for k in K:
            if k not in c1[d]:
                continue
            for g in G:
                if g not in c1[d][k]:
                    continue
                problem += sum(x[m][d][k] for m in GM[g]) >= c1[d][k][g], ''
    for d in D:
        if d not in c2:
            continue
        for k in K:
            if k not in c2[d]:
                continue
            for g in G:
                if g not in c2[d][k]:
                    continue
                problem += sum(x[m][d][k] for m in GM[g]) <= c2[d][k][g], ''

    for m in M:
        if m not in c3:
            continue
        for k in K:
            if k not in c3[m]:
                continue
            problem += sum(x[m][d][k] for d in D) >= c3[m][k]
    for m in M:
        if m not in c4:
            continue
        for k in K:
            if k not in c4[m]:
                continue
            problem += sum(x[m][d][k] for d in D) <= c4[m][k]

    for m in M:
        for k in K:
            if k not in c5:
                continue
            for d in D:
                if str(int(d) - c5[k]) not in D:
                    continue
                problem += sum(x[m][str(int(d) - i)][k]
                               for i in range(0, c5[k] + 1)) >= c5[k]
    for m in M:
        for k in K:
            if k not in c6:
                continue
            for d in D:
                if str(int(d) - c6[k]) not in D:
                    continue
                problem += sum(x[m][str(int(d) - i)][k]
                               for i in range(0, c6[k] + 1)) <= c6[k]

    for m in M:
        for k in K:
            if k not in c7:
                continue
            for d in D:
                for i in range(2, c7[k] + 1):
                    if str(int(d) - i) not in D:
                        continue
                    problem += x[m][str(int(d) - i)][k] - \
                        sum(x[m][str(int(d) - j)][k] for j in range(1, i)) + \
                        x[m][d][k] <= 1
    for m in M:
        for k in K:
            if k not in c8:
                continue
            for d in D:
                if str(int(d) - c8[k]) not in D:
                    continue
                problem += sum(x[m][str(int(d) - i)][k]
                               for i in range(0, c8[k] + 1)) >= 1

    for m in M:
        if m not in c9:
            continue
        for d in D:
            if d not in c9[m]:
                continue
            for k in K:
                if k not in c9[m][d]:
                    continue
                problem += x[m][d][k] == 1
    for m in M:
        if m not in c10:
            continue
        for d in D:
            if d not in c10[m]:
                continue
            for k in K:
                if k not in c10[m][d]:
                    continue
                problem += x[m][d][k] == 0

    for m in M:
        for p in P:
            l = len(p) - 1
            for d in D:
                if str(int(d) - l) not in D:
                    continue
                problem += sum(x[m][str(int(d) - l + i)][p[i]]
                               for i in range(0, l + 1)) <= l

    problem.writeLP('scheduling.lp')

    with open('scheduling.txt', 'w') as f:
        solved = False
        while True:
            problem.solve()
            print("Status:", pulp.LpStatus[problem.status])
            if pulp.LpStatus[problem.status] != 'Optimal':
                return solved
            solved = True
            lm = max(len(member.name) for member in members)
            f.write(' ' * lm + '|' +
                    ''.join([date.name[-1:] for date in dates]) + '|\n')
            f.write('-' * lm + '+' + ('-' * len(D)) + '+\n')
            for member in members:
                f.write(member.name.rjust(lm) + '|')
                for d in D:
                    for kinmu in kinmus:
                        if x[member.id][d][kinmu.id].value() == 1:
                            f.write(kinmu.name)
                            break
                f.write('|\n')
            f.write('-' * lm + '+' + ('-' * len(D)) + '+\n')
            problem += sum(x[m][d][k] for m in M for d in D for k in K
                           if x[m][d][k].value() == 1) <= len(M) * len(D) - 1
            return solved
