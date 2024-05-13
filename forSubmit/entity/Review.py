from csit314.app import db
from csit314.entity.User import User, Role
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    author_userid = db.Column(db.String(50), db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    @classmethod
    def createReview(cls, details: dict, agent_id: int) -> bool:
        # details에서 author_userid를 가져옵니다. 이는 로그인한 사용자의 userid를 의미합니다.
        author_userid = details.get('author_userid')

        # User 테이블에서 해당 userid를 가진 사용자가 BUYER 또는 SELLER 역할을 가지고 있는지 확인합니다.
        valid_user = User.query.filter_by(id=author_userid, role=Role.BUYER.value).first() \
               or User.query.filter_by(id=author_userid, role=Role.SELLER.value).first()
        if not valid_user:
            return False  # BUYER 또는 SELLER 역할이 아니면 생성 불가능

        # 필수 필드가 모두 details에 포함되어 있는지 확인합니다.
        required_fields = ['content', 'rating']
        if not all(field in details for field in required_fields):
            return False  # 필수 필드 누락

        # 새 리뷰를 생성합니다. agent_id를 포함하여 생성
        new_review = cls(**details, agent_id=agent_id, create_date=datetime.now())
        db.session.add(new_review)
        db.session.commit()
        return True


