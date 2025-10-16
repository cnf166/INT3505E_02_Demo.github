-- Demo Data Modelling -
Bước 1: Xác Định Thực thể và Thuộc tính

Book (Sách): Đại diện cho từng cuốn sách.

book_id (PK, INT): Mã sách (tự động tăng).
title (VARCHAR(255)): Tiêu đề sách.
publication_year (INT): Năm xuất bản.
publisher (VARCHAR(100)): Nhà xuất bản.
copies_available (INT): Số bản có sẵn.
total_copies (INT): Tổng số bản.

Author (Tác Giả): Lưu thông tin tác giả.

author_id (PK, INT): Mã tác giả.
name (VARCHAR(100)): Tên tác giả.
bio (TEXT): Tiểu sử ngắn (tùy chọn).

Category (Thể Loại): Phân loại sách.

category_id (PK, INT): Mã thể loại.
name (VARCHAR(50)): Tên thể loại (ví dụ: "Khoa học", "Văn học").

Member (Độc Giả/Thành Viên): Người dùng thư viện.

member_id (PK, INT): Mã thành viên.
name (VARCHAR(100)): Tên.
email (VARCHAR(100)): Email.
phone (VARCHAR(20)): Số điện thoại.
address (VARCHAR(255)): Địa chỉ.
join_date (DATE): Ngày đăng ký.
membership_type (VARCHAR(50)): Loại thành viên (ví dụ: "Sinh viên", "Giáo viên").

Loan (Mượn Sách): Theo dõi giao dịch mượn/trả.

loan_id (PK, INT): Mã mượn.
book_id (FK, INT): Mã sách.
member_id (FK, INT): Mã thành viên.
loan_date (DATE): Ngày mượn.
due_date (DATE): Ngày hạn trả.
return_date (DATE): Ngày trả thực tế (NULL nếu chưa trả).
fine_amount (DECIMAL(10,2)): Phạt quá hạn (tính động).

Book_Author (Bảng trung gian cho many-to-many giữa Book và Author).

book_id (FK, INT).
author_id (FK, INT).
PK: (book_id, author_id).

Book_Category (Bảng trung gian cho many-to-many giữa Book và Category).

book_id (FK, INT).
category_id (FK, INT).
PK: (book_id, category_id).

Bước 2: Xác Định Relationships

Book và Author: Many-to-Many (một sách có nhiều tác giả, một tác giả viết nhiều sách) → Sử dụng bảng Book_Author.
Book và Category: Many-to-Many (một sách thuộc nhiều thể loại, một thể loại có nhiều sách) → Sử dụng bảng Book_Category.
Member và Loan: One-to-Many (một thành viên mượn nhiều sách, một giao dịch mượn thuộc một thành viên).
Book và Loan: One-to-Many (một sách được mượn nhiều lần, một giao dịch mượn chỉ một sách). Lưu ý: Nếu cho phép mượn nhiều sách cùng lúc, có thể cần bảng Loan_Item tương tự như OrderItem.

Bước 4: Implement Schema trong SQL

USE library_db;

-- Table Author
CREATE TABLE Author (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bio TEXT
);

-- Table Category
CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table Book
CREATE TABLE Book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    publication_year INT,
    publisher VARCHAR(100),
    copies_available INT DEFAULT 1,
    total_copies INT DEFAULT 1
);

-- Table Book_Author (Many-to-Many)
CREATE TABLE Book_Author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE
);

-- Table Book_Category (Many-to-Many)
CREATE TABLE Book_Category (
    book_id INT,
    category_id INT,
    PRIMARY KEY (book_id, category_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE
);

-- Table Member
CREATE TABLE Member (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    join_date DATE DEFAULT CURRENT_DATE,
    membership_type VARCHAR(50)
);

-- Table Loan
CREATE TABLE Loan (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    loan_date DATE DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (book_id) REFERENCES Book(book_id) ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE RESTRICT
);
