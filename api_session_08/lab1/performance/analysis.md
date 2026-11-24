# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s | 17 | 0.00% | 4.80 |
| B | 50 | 5 | 60s | 39 | 0.14% | 23.21 |
| C | 200 | 50 | 30s | 350 | 0.11% | 93.38 |

1. Kịch bản nào p95 cao nhất? Vì sao?
    **Kịch bản C** có p95 cao nhất: **350 ms**, so với 17 ms ở A và 39 ms ở B.
    Khi tăng lên 200 users, throughput tăng lên 93.38 RPS nhưng CPU/SQLite và Flask
    development server phải xử lý nhiều request đồng thời hơn, làm hàng đợi và
    tail latency tăng.

2.Endpoint nào fail rate tăng theo user? Nguyên nhân?
    `GET /books?year={year}` có failure rate cao nhất theo endpoint: 0.94% ở B
    (2/213) và 0.77% ở C (3/390). Đây là các lỗi **client-side** do Locust chủ
    động gọi `response.failure("Simulated 500 client-side failure")` mỗi request
    tìm kiếm thứ 100; server vẫn trả HTTP 200. Không có HTTP 500 thật trong các
    lần chạy này.

3. Đạt SLO p95 < 300ms không? Đề xuất CI gate
    A và B đạt SLO giả định p95 < 300 ms; C không đạt với p95 350 ms. Kết quả
    chỉ phản ánh một máy cá nhân chạy Flask development server + SQLite, dữ liệu
    và thời lượng nhỏ, không đại diện cho production. Ngoài ra, C có failure giả
    lập nên exit code của Locust là 1 dù test vẫn tạo được HTML report.

Bonus: Pool size = 5 thì 200 user đồng thời bị gì? Test bằng Locust thế nào?
    Để kiểm chứng pool giới hạn 5, cấu hình SQLAlchemy pool size bằng 5 trong
    một bản chạy riêng, giữ nguyên users/spawn rate và chạy lại A/B/C. So sánh
    p95, RPS, timeout và số lỗi với baseline; xem log server để xác định chờ
    connection pool thay vì nhầm với lỗi ứng dụng. Có thể chạy thêm các mức
    pool 5, 20 và mặc định, lặp mỗi kịch bản ít nhất 3 lần rồi lấy median/p95.

