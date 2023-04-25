from data import db_session
from data.posts import Post
from data.users import User
from data.comments import Comment
import datetime


db_session.global_init("db/users.db")
db_sess = db_session.create_session()

# user = User()
# user.name = "Пользователь 1"
# user.surname = "asd"
# user.nickname = "afdas"
# user.email = "email@email.ru"
# user.birthday = datetime.datetime.now()
# db_sess.add(user)
# db_sess.commit()
#
# post = Post()
# post.likes = 1
# post.post_text = "fsdfds"
# post.post_picture = "dasdas"
# post.comments_number = 123
# post.place = "adfsad"
# post.user_id = 1
# post.modified_date = datetime.datetime.now()
# db_sess.add(post)
# db_sess.commit()
#
# comment = Comment()
# comment.likes = 1
# comment.comment_text = "adasdas"
# comment.user_id = 1
# comment.post_id = 1
# comment.modified_date = datetime.datetime.now()
# db_sess.add(comment)
# db_sess.commit()

gu = db_sess.query(Post).first()
print(gu.comments[0].comment_text)
