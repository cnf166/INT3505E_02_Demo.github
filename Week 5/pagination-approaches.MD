## Phân trang theo Offset/Limit Pagination 

```
@api.route('/books/search')
class BookSearch(Resource):
    @api.doc(params={
        'q': {
            'description': 'Title or author',
            'in': 'query',
            'type': 'string',
            'default': ''
        },
        'offset': {
            'description': 'Starting position (0-based)',
            'in': 'query',
            'type': 'integer',
            'default': 0
        },
        'limit': {
            'description': 'Number of items to return',
            'in': 'query',
            'type': 'integer',
            'default': 10
        }
    })
    @api.marshal_list_with(book_model, code=200, envelope="books")
    def get(self):
        ''' Search books by title or author with offset/limit pagination '''
        search_query = request.args.get('q', '', type=str)
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', 10, type=int)

        query = Book.query
        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_pattern),
                    Book.author.ilike(search_pattern)
                )
            )

        total = query.count()
        books = query.offset(offset).limit(limit).all()
        return {
            'books': books,
            'total': total,
            'offset': offset,
            'limit': limit
        }
```

## Phân trang theo số trang (Page-Based Pagination)

```
@api.route('/books/search')
class BookSearch(Resource):
    @api.doc(params={
        'q': {
            'description': 'Title or author',
            'in': 'query',
            'type': 'string',
            'default': ''
        },
        'page': {
            'description': 'Page number',
            'in': 'query',
            'type': 'integer',
            'default': 1
        },
        'per_page': {
            'description': 'Number of items per page',
            'in': 'query',
            'type': 'integer',
            'default': 10
        }
    })
    @api.marshal_list_with(book_model, code=200, envelope="books")
    def get(self):
        ''' Search books by title or author with page-based pagination '''
        search_query = request.args.get('q', '', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = Book.query
        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_pattern),
                    Book.author.ilike(search_pattern)
                )
            )

        paginated_books = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'books': paginated_books.items,
            'total': paginated_books.total,
            'pages': paginated_books.pages,
            'current_page': paginated_books.page
        }
```

## Phân trang dựa theo con trỏ (Cursor-Based Pagination)

```
@api.route('/books/search')
class BookSearch(Resource):
    @api.doc(params={
        'q': {
            'description': 'Title or author',
            'in': 'query',
            'type': 'string',
            'default': ''
        },
        'cursor': {
            'description': 'Last book ID from previous page',
            'in': 'query',
            'type': 'integer',
            'default': 0
        },
        'limit': {
            'description': 'Number of items to return',
            'in': 'query',
            'type': 'integer',
            'default': 10
        }
    })
    @api.marshal_list_with(book_model, code=200, envelope="books")
    def get(self):
        ''' Search books by title or author with cursor-based pagination '''
        search_query = request.args.get('q', '', type=str)
        cursor = request.args.get('cursor', 0, type=int)
        limit = request.args.get('limit', 10, type=int)

        query = Book.query
        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_pattern),
                    Book.author.ilike(search_pattern)
                )
            )

        if cursor > 0:
            query = query.filter(Book.id > cursor)

        books = query.order_by(Book.id).limit(limit).all()
        total = query.count()
        next_cursor = books[-1].id if books else None

        return {
            'books': books,
            'total': total,
            'next_cursor': next_cursor,
            'limit': limit
        }
```