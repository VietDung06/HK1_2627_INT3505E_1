**BÁO CÁO AUDIT PUBLIC API: GITHUB REST API (v3)**

**1. Tổng quan về API**

- **Tên API:** GitHub REST API v3
- **Base URL:** [https://api.github.com](https://api.github.com)
- **Mục đích:** Cung cấp các thao tác tương tác với dữ liệu trên GitHub (Users, Repositories, Issues, Pull Requests,...).
- **Định dạng dữ liệu:** JSON (application/json)

**2. Bảng tổng hợp Audit 5 Endpoints**

|**STT**|**Endpoint**|**Method**|**Status Code chính**|**Đánh giá RESTful**|
| :- | :- | :- | :- | :- |
|**1**|/users/{username}|GET|200 OK, 404 Not Found|**Đạt** (Danh từ, safe/idempotent)|
|**2**|/users/{username}/repos|GET|200 OK, 404 Not Found|**Đạt** (Lồng nhau thể hiện quan hệ)|
|**3**|/user/repos|POST|201 Created, 422 Unprocessable Entity|**Đạt** (Có header Location, dùng 201)|
|**4**|/repos/{owner}/{repo}|PATCH|200 OK, 400 Bad Request|**Đạt** (Sử dụng đúng nghĩa Partial Update)|
|**5**|/repos/{owner}/{repo}|DELETE|204 No Content, 403 Forbidden|**Đạt** (Phương thức DELETE chuẩn, 204 No Content)|

**3. Chi tiết Audit từng Endpoint**

**Endpoint 1: Lấy thông tin công khai của người dùng**

- **URI:** GET /users/{username}
- **HTTP Method:** GET
- **Mục đích:** Truy vấn thông tin profile của một người dùng cụ thể.
- **HTTP Status Codes:**
  - 200 OK: Lấy thông tin thành công.
  - 404 Not Found: Không tìm thấy username tương ứng.
- **Headers quan trọng:**
  - *Request Headers:*
    - Accept: application/vnd.github+json
    - Authorization: Bearer <token> *(tùy chọn)*
  - *Response Headers:*
    - Content-Type: application/json; charset=utf-8
    - X-RateLimit-Limit: Giới hạn số lượng request.
    - X-RateLimit-Remaining: Số request còn lại trong cửa sổ thời gian.
    - ETag: Mã băm hỗ trợ caching (Conditional GET).
- **Đánh giá RESTful:** **CÓ (Chuẩn RESTful)**
  - **URI làm gốc:** Định danh tài nguyên bằng danh từ /users/{username}, không dùng động từ (không dùng /getUserInfo).
  - **Tính chất HTTP Method:** Phương thức GET đạt tính **Safe** (không làm thay đổi dữ liệu trên server) và **Idempotent** (gọi 1 lần hay n lần cho cùng kết quả).

**Endpoint 2: Lấy danh sách Repositories của một người dùng**

- **URI:** GET /users/{username}/repos
- **HTTP Method:** GET
- **Mục đích:** Truy vấn tập hợp các kho lưu trữ (repository) thuộc sở hữu của người dùng.
- **HTTP Status Codes:**
  - 200 OK: Trả về danh sách repository (mảng JSON).
  - 404 Not Found: Không tìm thấy người dùng.
- **Headers quan trọng:**
  - *Request Headers:*
    - Accept: application/vnd.github+json
  - *Response Headers:*
    - Content-Type: application/json; charset=utf-8
    - Link: [https://api.github.com/user/582772/repos?page=2](https://api.github.com/user/582772/repos?page=2); rel="next", <...>; rel="last" *(dùng cho phân trang - Pagination)*
- **Đánh giá RESTful:** **CÓ (Chuẩn RESTful)**
  - **Quan hệ tài nguyên (Sub-resource):** Thiết kế dạng /users/{username}/repos thể hiện rõ mối quan hệ sở hữu 1-N (User sở hữu Repositories).
  - **Phân trang (HATEOAS):** Header Link cung cấp đường dẫn tới trang tiếp theo/trang cuối, tuân thủ nguyên lý HATEOAS trong REST.

**Endpoint 3: Tạo một Repository mới cho tài khoản đăng nhập**

- **URI:** POST /user/repos
- **HTTP Method:** POST
- **Mục đích:** Tạo một kho lưu trữ mới cho người dùng hiện tại (xác thực qua Token).
- **HTTP Status Codes:**
  - 201 Created: Tạo tài nguyên thành công.
  - 401 Unauthorized: Chưa xác thực/Token không hợp lệ.
  - 422 Unprocessable Entity: Dữ liệu đầu vào không hợp lệ (ví dụ: trùng tên repo).
- **Headers quan trọng:**
  - *Request Headers:*
    - Authorization: Bearer <token> *(bắt buộc)*
    - Content-Type: application/json
  - *Response Headers:*
    - Location: [https://api.github.com/repos/](https://api.github.com/repos/){owner}/{repo\_name}
    - Content-Type: application/json; charset=utf-8
- **Đánh giá RESTful:** **CÓ (Chuẩn RESTful)**
  - **Sử dụng Status Code chuẩn:** Trả về 201 Created thay vì 200 OK chung chung khi tạo mới thành công.
  - **Điều hướng tài nguyên:** Response kèm theo Header Location chứa liên kết trực tiếp tới tài nguyên vừa tạo.

**Endpoint 4: Cập nhật thông tin một Repository**

- **URI:** PATCH /repos/{owner}/{repo}
- **HTTP Method:** PATCH
- **Mục đích:** Cập nhật một hoặc một số trường thuộc tính của Repository (ví dụ: đổi tên, sửa description, bật/tắt private).
- **HTTP Status Codes:**
  - 200 OK: Cập nhật thành công và trả về thông tin repo mới.
  - 307 Temporary Redirect: Đã đổi tên repo thành công và đường dẫn cũ chuyển hướng.
  - 403 Forbidden: Không có quyền sửa repo.
  - 404 Not Found: Không tìm thấy repo.
- **Headers quan trọng:**
  - *Request Headers:*
    - Authorization: Bearer <token>
    - Content-Type: application/json
  - *Response Headers:*
    - Content-Type: application/json; charset=utf-8
- **Đánh giá RESTful:** **CÓ (Chuẩn RESTful)**
  - **Phân biệt PUT và PATCH:** Sử dụng đúng phương thức PATCH cho hành vi "cập nhật từng phần" (partial update) thay vì bắt buộc gửi lại toàn bộ đối tượng như PUT.

**Endpoint 5: Xóa một Repository**

- **URI:** DELETE /repos/{owner}/{repo}
- **HTTP Method:** DELETE
- **Mục đích:** Xóa vĩnh viễn kho lưu trữ khỏi hệ thống.
- **HTTP Status Codes:**
  - 204 No Content: Xóa thành công, phản hồi không chứa body.
  - 403 Forbidden: Không đủ quyền xóa.
  - 404 Not Found: Không tìm thấy kho lưu trữ.
- **Headers quan trọng:**
  - *Request Headers:*
    - Authorization: Bearer <token>
  - *Response Headers:*
    - X-RateLimit-Remaining
- **Đánh giá RESTful:** **CÓ (Chuẩn RESTful)**
  - **Phản hồi rỗng chuẩn mực:** Trả về mã status 204 No Content thể hiện thao tác thành công và không cần gửi lại dữ liệu thừa trong Response Body.
  - **Tính chất HTTP Method:** Phương thức DELETE mang tính Idempotent (gọi xóa 1 tài nguyên nhiều lần thì kết quả sau lần đầu vẫn là tài nguyên đó không còn tồn tại).

**4. Kết luận Đánh giá Chung**

API của GitHub v3 là một ví dụ mẫu mực về thiết kế RESTful Architecture với các điểm mạnh vượt trội:

1. **Chuẩn hóa URI:** Sử dụng danh từ dạng số nhiều (/users, /repos), thể hiện rõ quan hệ cha-con thông qua cấu trúc đường dẫn.
1. **HTTP Methods đúng ngữ nghĩa:** Áp dụng đầy đủ GET, POST, PATCH, DELETE chính xác theo mục đích thao tác.
1. **HTTP Status Codes phong phú:** Phản ánh đúng trạng thái xử lý (200, 201, 204, 401, 403, 404, 422).
1. **Tận dụng HTTP Headers:** Quản lý Rate Limit, Caching (ETag), Pagination (Link) và tài nguyên mới tạo (Location) chuyên nghiệp thông qua Headers.

