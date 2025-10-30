import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from library_api.models.book_create import BookCreate  # noqa: E501
from library_api.models.book_search_response import BookSearchResponse  # noqa: E501
from library_api.models.book_update import BookUpdate  # noqa: E501
from library_api.models.create_book201_response import CreateBook201Response  # noqa: E501
from library_api.models.delete_book200_response import DeleteBook200Response  # noqa: E501
from library_api.models.error import Error  # noqa: E501
from library_api.models.get_books200_response import GetBooks200Response  # noqa: E501
from library_api import util


def create_book(body):  # noqa: E501
    """Create a new book

    Tạo một cuốn sách mới # noqa: E501

    :param book_create: 
    :type book_create: dict | bytes

    :rtype: Union[CreateBook201Response, Tuple[CreateBook201Response, int], Tuple[CreateBook201Response, int, Dict[str, str]]
    """
    book_create = body
    if connexion.request.is_json:
        book_create = BookCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_book(id):  # noqa: E501
    """Delete a book

    Xóa sách theo ID # noqa: E501

    :param id: Book ID
    :type id: int

    :rtype: Union[DeleteBook200Response, Tuple[DeleteBook200Response, int], Tuple[DeleteBook200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_book_by_id(id):  # noqa: E501
    """Get a book by id

    Lấy thông tin sách theo ID # noqa: E501

    :param id: Book ID
    :type id: int

    :rtype: Union[CreateBook201Response, Tuple[CreateBook201Response, int], Tuple[CreateBook201Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_books():  # noqa: E501
    """Get all books

    Lấy danh sách tất cả các sách # noqa: E501


    :rtype: Union[GetBooks200Response, Tuple[GetBooks200Response, int], Tuple[GetBooks200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def search_books(q=None, page=None, per_page=None):  # noqa: E501
    """Search books by title or author with pagination

    Tìm kiếm sách theo tiêu đề hoặc tác giả với phân trang # noqa: E501

    :param q: Search query for title or author
    :type q: str
    :param page: Page number
    :type page: int
    :param per_page: Number of items per page
    :type per_page: int

    :rtype: Union[BookSearchResponse, Tuple[BookSearchResponse, int], Tuple[BookSearchResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def update_book(id, body):  # noqa: E501
    """Update a book

    Cập nhật thông tin sách # noqa: E501

    :param id: Book ID
    :type id: int
    :param book_update: 
    :type book_update: dict | bytes

    :rtype: Union[CreateBook201Response, Tuple[CreateBook201Response, int], Tuple[CreateBook201Response, int, Dict[str, str]]
    """
    book_update = body
    if connexion.request.is_json:
        book_update = BookUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
