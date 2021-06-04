from flask_restful import fields

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