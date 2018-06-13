from server import db, models

db.create_all()

member_names = [str(n + 1) for n in range(50)]
date_names = [str(n + 1) for n in range(31)]
working_kinmu_names = ['a', 'b', 'c', 'd', 'e']
holiday_kinmu_names = [' ']
kinmu_names = holiday_kinmu_names + working_kinmu_names
group_names = ['A', 'B', 'C', 'D', 'E']
group_member_names = {
    'A': member_names[0:10],
    'B': member_names[10:20],
    'C': member_names[20:30],
    'D': member_names[30:40],
    'E': member_names[40:50]
}
renzoku_kinshi_kinmu_names = [['e', 'a']]

db.session.add_all([models.Member(name=name) for name in member_names])
db.session.add_all([models.Date(name=name) for name in date_names])
db.session.add_all([models.Kinmu(name=name) for name in kinmu_names])
db.session.add_all([models.Group(name=name) for name in group_names])
db.session.commit()
members = models.Member.query.all()
dates = models.Date.query.all()
kinmus = models.Kinmu.query.all()
working_kinmus = [
    kinmu for kinmu in kinmus if kinmu.name in working_kinmu_names
]
holiday_kinmus = [
    kinmu for kinmu in kinmus if kinmu.name in holiday_kinmu_names
]
groups = models.Group.query.all()
db.session.add_all([
    models.GroupMember(group_id=group.id, member_id=member.id)
    for group_name, member_names in group_member_names.items()
    for group in groups if group.name == group_name
    for member_name in member_names for member in members
    if member.name == member_name
])
db.session.add_all([
    models.RenzokuKinshiKinmu(
        sequence_id=i, sequence_number=j, kinmu_id=kinmu.id)
    for i, names in enumerate(renzoku_kinshi_kinmu_names)
    for j, name in enumerate(names) for kinmu in kinmus if kinmu.name == name
])
db.session.add_all([
    models.C1(
        date_id=date.id,
        kinmu_id=kinmu.id,
        group_id=group.id,
        min_number_of_assignments=1) for date in dates
    for kinmu in working_kinmus for group in groups
])
db.session.add_all([
    models.C2(
        date_id=date.id,
        kinmu_id=kinmu.id,
        group_id=group.id,
        max_number_of_assignments=2) for date in dates
    for kinmu in working_kinmus for group in groups
])
db.session.add_all([
    models.C3(
        member_id=member.id, kinmu_id=kinmu.id, min_number_of_assignments=10)
    for member in members for kinmu in holiday_kinmus
])
db.session.add_all([
    models.C6(kinmu_id=kinmu.id, max_number_of_days=2) for kinmu in kinmus
    if kinmu.name == 'e'
])
db.session.add_all([
    models.C7(kinmu_id=kinmu.id, min_number_of_days=2) for kinmu in kinmus
    if kinmu.name == ' '
])
db.session.add_all([
    models.C8(kinmu_id=kinmu.id, max_number_of_days=3) for kinmu in kinmus
    if kinmu.name == ' '
])
db.session.commit()
