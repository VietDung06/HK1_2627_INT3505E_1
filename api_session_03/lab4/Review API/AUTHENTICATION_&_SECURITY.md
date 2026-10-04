08: AUTHENTICATION & SECURITY 

A. Kiến thức bài học

Tiêu chí 08: AUTHENTICATION & SECURITY:

    -Token gửi ở Header: Token bảo mật phải được truyền thông qua HTTP Header (ví dụ: Authorization: Bearer <token>), tuyệt đối không gửi qua URL query string (vì URL token sẽ bị ghi lại ở server access log, browser history, header Referer...).

    -Rate Limit rõ ràng: API phải phản hồi thông tin Rate Limit rõ ràng và có thông điệp hướng dẫn khi bị vượt quá ngưỡng.

B. Phân tích & Đánh giá Discord REST API

    1.Cơ chế Xác thực (Authentication):

        -Discord API bắt buộc xác thực qua HTTP Header với định dạng:
            +Dành cho Bot: Authorization: Bot <token>
            +Dành cho OAuth2 (User Access Token): Authorization: Bearer <token>

        -Discord không cho phép và nghiêm cấm việc truyền token thông qua URL query parameter (ví dụ: ?token=...).

        -Đánh giá: Đạt chuẩn rất tốt so với nguyên tắc thiết kế bảo mật của slide.

    2.Cơ chế Kiểm soát Tốc độ (Rate Limiting):

        -Discord áp dụng cơ chế Rate Limit rất chi tiết (per-route, global, gateway).

        -Server gửi kèm các HTTP response header để client chủ động theo dõi:
            +X-RateLimit-Limit: Số lượng request tối đa.
            +X-RateLimit-Remaining: Số request còn lại trong window.
            +X-RateLimit-Reset: Thời gian reset limit (Epoch seconds).
            +X-RateLimit-Bucket: Định danh cho bucket chứa route đó.

        -Khi client bị giới hạn (vượt quá rate limit), Discord trả về mã lỗi 429 Too Many Requests kèm header Retry-After (tính theo giây/mili giây) và response body chi tiết chứa retry_after.

        -Đánh giá: Hoàn toàn khớp với chuẩn HTTP Status Code 429 và Retry-After header trong slide bài giảng.

C. KẾT LUẬN VỀ MẶT HẠN CHẾ TRONG TIÊU CHÍ 08 CỦA DISCORD API:

    -Kết luận: Thiếu Idempotency Key cho các tác vụ quan trọng (Write Actions): Mặc dù bảo mật xác thực và rate-limit rất tốt, Discord API thiếu cơ chế Idempotency-Key header cho các phương thức POST hoặc PATCH tạo/thực hiện giao dịch (ví dụ: gửi tin nhắn, mua quà tặng/nitro, mua Sticker). Khi gặp sự cố chập chờn mạng làm request retry tự động, việc thiếu Idempotency Key khiến bot hoặc ứng dụng dễ gặp tình trạng gửi trùng tin nhắn nhiều lần hoặc thực hiện hành động dư thừa trên hệ thống.

