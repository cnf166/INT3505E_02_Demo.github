# Hệ Thống Quản Lý Thư Viện (Library Management System)

## Mô Tả

Demo cho data modelling cho hệ thống thư viện quản lý.

## Kiến Trúc Database

### Entities (Thực thể)

#### 1. Book (Sách)
Lưu trữ thông tin về sách trong thư viện.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `book_id` | INT (PK) | Mã sách (tự động tăng) |
| `title` | VARCHAR(255) | Tiêu đề sách |
| `isbn` | VARCHAR(13) | Mã ISBN (duy nhất) |
| `publication_year` | INT | Năm xuất bản |
| `publisher` | VARCHAR(100) | Nhà xuất bản |
| `copies_available` | INT | Số bản có sẵn để mượn |
| `total_copies` | INT | Tổng số bản trong thư viện |

#### 2. Author (Tác Giả)
Lưu trữ thông tin tác giả.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `author_id` | INT (PK) | Mã tác giả (tự động tăng) |
| `name` | VARCHAR(100) | Tên tác giả |
| `bio` | TEXT | Tiểu sử ngắn (tùy chọn) |

#### 3. Category (Thể Loại)
Phân loại sách theo thể loại.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `category_id` | INT (PK) | Mã thể loại (tự động tăng) |
| `name` | VARCHAR(50) | Tên thể loại (duy nhất) |

#### 4. Member (Thành Viên)
Lưu trữ thông tin độc giả/người dùng thư viện.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `member_id` | INT (PK) | Mã thành viên (tự động tăng) |
| `name` | VARCHAR(100) | Tên thành viên |
| `email` | VARCHAR(100) | Email (duy nhất) |
| `phone` | VARCHAR(20) | Số điện thoại |
| `address` | VARCHAR(255) | Địa chỉ |
| `join_date` | DATE | Ngày đăng ký (mặc định: ngày hiện tại) |
| `membership_type` | VARCHAR(50) | Loại thành viên (VD: "Sinh viên", "Giáo viên") |

#### 5. Loan (Mượn Sách)
Theo dõi các giao dịch mượn/trả sách.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `loan_id` | INT (PK) | Mã giao dịch mượn (tự động tăng) |
| `book_id` | INT (FK) | Mã sách được mượn |
| `member_id` | INT (FK) | Mã thành viên mượn sách |
| `loan_date` | DATE | Ngày mượn (mặc định: ngày hiện tại) |
| `due_date` | DATE | Ngày hạn trả |
| `return_date` | DATE | Ngày trả thực tế (NULL nếu chưa trả) |
| `fine_amount` | DECIMAL(10,2) | Số tiền phạt quá hạn |

#### 6. Book_Author (Bảng trung gian)
Liên kết many-to-many giữa Book và Author.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `book_id` | INT (FK) | Mã sách |
| `author_id` | INT (FK) | Mã tác giả |

**Primary Key**: (`book_id`, `author_id`)

#### 7. Book_Category (Bảng trung gian)
Liên kết many-to-many giữa Book và Category.

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `book_id` | INT (FK) | Mã sách |
| `category_id` | INT (FK) | Mã thể loại |

**Primary Key**: (`book_id`, `category_id`)

## Relationships (Mối quan hệ - Liên kết)

```
Book ←→ Author (Many-to-Many via Book_Author)
Book ←→ Category (Many-to-Many via Book_Category)
Member → Loan (One-to-Many)
Book → Loan (One-to-Many)
```

### Chi tiết Relationships

- **Book ↔ Author**: Một sách có thể có nhiều tác giả, một tác giả có thể viết nhiều sách
- **Book ↔ Category**: Một sách có thể thuộc nhiều thể loại, một thể loại chứa nhiều sách
- **Member → Loan**: Một thành viên có thể mượn nhiều lần, mỗi giao dịch mượn thuộc về một thành viên
- **Book → Loan**: Một sách có thể được mượn nhiều lần, mỗi giao dịch mượn chỉ gồm một sách

#### Implement schema trong SQL.
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
```

[Thông tin liên hệ của bạn]
