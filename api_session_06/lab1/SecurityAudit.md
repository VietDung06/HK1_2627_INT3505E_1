# Security Audit Report - Social Network API

Dưới đây là danh sách 6 điểm nguy cơ rò rỉ thông tin và lỗ hổng bảo mật phổ biến cần kiểm tra và khắc phục đối với API xác thực & bài viết:

### 1. Phân quyền cấp đối tượng bị lỗi (Broken Object Level Authorization - BOLA / API1:2023)
* **Mô tả nguy cơ**: Endpoint `GET /posts/{id}` trả về thông tin bài viết chỉ dựa vào `id`. Nếu không kiểm tra xem bài viết có ở chế độ riêng tư (Private/Friends-only) hay không, bất kỳ người dùng đã đăng nhập nào cũng có thể đổi `{id}` để đọc bài viết riêng tư của người khác.
* **Biện pháp khắc phục**: Kiểm tra quyền sở hữu và chính sách hiển thị bài viết (Ownership & Privacy Check) ở tầng logic ứng dụng trước khi trả dữ liệu.

### 2. Lưu trữ Token ở Frontend không an toàn (XSS Lead to Token Theft / API Security BCP)
* **Mô tả nguy cơ**: Việc lưu `access_token` hoặc `refresh_token` ở `localStorage` hoặc `sessionStorage` trên ứng dụng Web khiến bất kỳ mã JavaScript độc hại nào (XSS) cũng có thể truy cập `document.localStorage` để lấy trộm token.
* **Biện pháp khắc phục**: Đổi cơ chế lưu trữ Refresh Token sang `HttpOnly`, `Secure`, `SameSite` Cookie trên Trình duyệt để ngăn JavaScript truy cập.

### 3. Đưa thông tin nhạy cảm vào JWT Payload (PII Leakage)
* **Mô tả nguy cơ**: JWT Payload chỉ được Base64URL encode chứ không mã hóa. Nếu đưa thông tin cá nhân (PII) như `email`, `phone_number`, `password_hash` vào claims của JWT, kẻ tấn công hoặc bên thứ ba có thể đọc được toàn bộ thông tin này dễ dàng.
* **Biện pháp khắc phục**: Chỉ đưa các thông tin nhận dạng tối thiểu (như `sub`: user_id, `roles`, `scopes`) vào JWT Payload. Không lưu thông tin nhạy cảm.

### 4. Thiếu giới hạn tần suất yêu cầu (Lack of Rate Limiting / API2:2023 - Credential Stuffing)
* **Mô tả nguy cơ**: Endpoint `POST /auth/login` nếu không được rate-limit sẽ dễ bị tấn công dò vét mật khẩu (Brute-force) hoặc Credential Stuffing.
* **Biện pháp khắc phục**: Cấu hình Rate Limiting (ví dụ: tối đa 5 lần thử/phút cho mỗi IP/Email) và áp dụng cơ chế khóa tạm thời.

### 5. Rò rỉ thông tin qua Thông báo Lỗi (Verbose Error Messages / Username Enumeration)
* **Mô tả nguy cơ**: Khi đăng nhập thất bại, API trả về thông báo chi tiết như `"Email không tồn tại"` hoặc `"Mật khẩu không đúng"`. Kẻ tấn công có thể lợi dụng điều này để thu thập danh sách email người dùng tồn tại trong hệ thống.
* **Biện pháp khắc phục**: Trả về thông báo lỗi chung cho cả 2 trường hợp sai email/password: `"Invalid email or password"` (Status Code 401).

### 6. Chấp nhận Thuật toán JWT yếu hoặc `alg: none` (Algorithm Confusion / API2:2023)
* **Mô tả nguy cơ**: Khi verify JWT, nếu server không giới hạn thuật toán (allowlist) mà tin hoàn toàn vào header `alg` do client gửi lên, kẻ tấn công có thể sửa `alg` thành `none` hoặc tráo đổi giữa HS256 và RS256 để bypass kiểm tra chữ ký.
* **Biện pháp khắc phục**: Cấu hình cứng danh sách thuật toán hợp lệ (Allowlist `["HS256"]` hoặc `["RS256"]`) tại tầng kiểm tra JWT.