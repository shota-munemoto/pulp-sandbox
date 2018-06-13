from server import db


# 職員
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


# 日付
class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


# 勤務
class Kinmu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


# グループ
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


# グループに所属する職員
class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    member_id = db.Column(
        db.Integer, db.ForeignKey('member.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('group_id', 'member_id'), )


# 連続禁止勤務並び
class RenzokuKinshiKinmu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sequence_id = db.Column(db.Integer, nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)


# 日付の勤務にグループから割り当てる職員数の下限
class C1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    min_number_of_assignments = db.Column(db.Integer, nullable=False)


# 日付の勤務にグループから割り当てる職員数の上限
class C2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    max_number_of_assignments = db.Column(db.Integer, nullable=False)


# 職員の勤務の割り当て数の下限
class C3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey('member.id'), nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    min_number_of_assignments = db.Column(db.Integer, nullable=False)


# 職員の勤務の割り当て数の上限
class C4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey('member.id'), nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    max_number_of_assignments = db.Column(db.Integer, nullable=False)


# 勤務の連続日数の下限
class C5(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    min_number_of_days = db.Column(db.Integer, nullable=False)


# 勤務の連続日数の上限
class C6(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    max_number_of_days = db.Column(db.Integer, nullable=False)


# 勤務の間隔日数の下限
class C7(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    min_number_of_days = db.Column(db.Integer, nullable=False)


# 勤務の間隔日数の上限
class C8(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
    max_number_of_days = db.Column(db.Integer, nullable=False)


# 職員の日付に割り当てる勤務
class C9(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey('member.id'), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)


# 職員の日付に割り当てない勤務
class C10(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey('member.id'), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=False)
    kinmu_id = db.Column(db.Integer, db.ForeignKey('kinmu.id'), nullable=False)
