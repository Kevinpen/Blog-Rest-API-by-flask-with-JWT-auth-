from flask import jsonify, abort
from flask_restful import Resource, reqparse,fields, marshal
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

list_route = '/blogapi/v1.0/blogs'
item_route = '/blogapi/v1.0/blogs/<int:id>'

blogs = [
    {
      "author": "Kevin",
      "content": "Write experiences, thoughts...",
      "id": 1,
      "title": "Blog Guide"
    },
    {
      "author": "Emma",
      "content": "Get creative, practice, practice, ",
      "id": 2,
      "title": "Programming Python"
    },
    {
      "author": "Oliver",
      "content": "Common misconceptions",
      "id": 3,
      "title": "Mistakes to Avoid"
    },
    {
      "author": "Mike",
      "content": "",
      "id": 4,
      "title": "Best Books"
    },
    {
      "author": "John",
      "content": "",
      "id": 5,
      "title": "Product Review"
    }
  ]

blog_fields = {
    'title': fields.String,
    'content': fields.String,
    'author': fields.String,
    'uri': fields.Url('blog')
}

class BlogListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True,
                                   help='No Blog title provided',
                                   location='json')
        self.parser.add_argument('content', type=str, default="",
                                   location='json')
        self.parser.add_argument('author', type=str, default="",
                                   location='json')
        super(BlogListAPI, self).__init__()
    
    def get(self):
        return {'blogs': [marshal(blog, blog_fields) for blog in blogs]}

    def post(self):
        args = self.parser.parse_args()
        blog = {
            'id': blogs[-1]['id'] + 1 if len(blogs) > 0 else 1,
            'title': args['title'],
            'content': args['content'],
            'author': args['author']
        }
        blogs.append(blog)
        return {'blog': marshal(blog, blog_fields)}, 201

class BlogItemAPI(Resource):
    @jwt_required
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, location='json')
        self.parser.add_argument('content', type=str, location='json')
        self.parser.add_argument('author', type=str, location='json')
        super(BlogItemAPI, self).__init__()

    def get(self, id):
        blog = [blog for blog in blogs if blog['id'] == id]
        if len(blog) == 0:
            abort(404)
        return {'blog': marshal(blog[0], blog_fields)}

    def put(self, id):
        blog = [blog for blog in blogs if blog['id'] == id]
        if len(blog) == 0:
            abort(404)
        blog = blog[0]
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                blog[k] = v

    def delete(self, id):
        blog = [blog for blog in blogs if blog['id'] == id]
        if len(blog) == 0:
            abort(404)
        blogs.remove(blog[0])
        return {'Deleted': True}

