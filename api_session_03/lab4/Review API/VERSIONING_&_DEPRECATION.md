09: VERSIONING & DEPRECATION

A. Kiến thức bài học

Tiêu chí 09: VERSIONING & DEPRECATION:

    -Versioning từ ngày đầu: API phải tích hợp Version Prefix (tiền tố phiên bản) trực tiếp vào URL ngay từ thiết kế ban đầu (ví dụ: /api/v1/...).

    -Lộ trình Deprecation rõ ràng: Có chính sách, tài liệu hướng dẫn chuyển đổi và thông báo ngừng hỗ trợ phiên bản cũ rõ ràng để tránh breaking change cho client.

B. Phân tích & Đánh giá Discord REST API

    1.Cấu trúc Versioning (Đánh số phiên bản):

        -Discord triển khai phiên bản công khai dưới dạng Path Versioning:

            +Base URL: [https://discord.com/api/v](https://discord.com/api/v){version} (Ví dụ hiện tại là [https://discord.com/api/v10](https://discord.com/api/v10)).

        -Các API request không truyền version mặc định sẽ chuyển về API version mặc định (Discord khuyên luôn khai báo rõ version trong URL).

        -Đánh giá: Đạt chuẩn. Việc đặt version prefix /v10 ngay trên path giúp client dễ dàng xác định phiên bản đang làm việc.

    2.Chính sách Deprecation (Ngừng hỗ trợ):

        -Discord duy trì tài liệu công khai lịch sử danh sách các phiên bản (API Versions status):

            +Available: Phiên bản khả dụng.
            +Deprecated: Phiên bản không khuyến khích sử dụng, ngừng cập nhật tính năng mới.
            +Discontinued: Phiên bản đã đóng hoàn toàn (Client gọi vào sẽ nhận lỗi 400 hoặc 404).

        -Discord đưa ra mốc thời gian chuyển giao khá rõ ràng cho lập trình viên khi nâng cấp từ v6, v8, v9, v10.

        -Đánh giá: Đạt chuẩn. Giúp phát triển ứng dụng bền vững, tránh tình trạng ứng dụng của bên thứ ba bị dừng đột ngột (Client breakage).

C. KẾT LUẬN VỀ MẶT HẠN CHẾ TRONG TIÊU CHÍ 09 CỦA DISCORD API:

    -Kết luận: Khả năng thương lượng phiên bản linh hoạt (Content Negotiation / Header Versioning) và Deprecation Header còn hạn chế:

        +Discord chỉ hỗ trợ duy nhất Path Versioning (/api/v10/users). Thiếu sự hỗ trợ cho Header-based Versioning (ví dụ: Accept-Version hoặc X-API-Version), điều này ép buộc lập trình viên phải thay đổi cứng URL ở mọi endpoint khi nâng cấp phiên bản.

        +Khi một endpoint hoặc một field cụ thể chuẩn bị bị loại bỏ (Deprecate), Discord chủ yếu đưa thông tin lên trang Documentation thay vì trả về HTTP Header Sunset hoặc Deprecation chuẩn RFC trực tiếp trong API response. Điều này khiến lập trình viên khó tự động hóa việc bắt cảnh báo ứng dụng đang dùng tính năng sắp bị khai tử thông qua log của ứng dụng.
