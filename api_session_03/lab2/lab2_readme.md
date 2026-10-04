Request tới http://127.0.0.1:5000/resources/999 trả về error 404 do không tìm thấy data
![alt text](1.png)

Body có type, title, detail, status, instance, KHÔNG lộ stack trace
![alt text](2.png)

Nếu thiếu Accept hoặc client gửi Accept: application/json, vẫn trả problem+json cho lỗi API
![alt text](3.png)

Nếu gặp exception chưa bắt, trả 500 với message trung tính và log chi tiết server-side
![alt text](4.png)
