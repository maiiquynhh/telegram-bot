# downloader
Bot Telegram tự động tải các file zip và rar từ group hoặc channel telegram

1. Tạo bot và lấy token từ BotFather
2. Cho bot join vào group hoặc channel
3. Thay đổi các cấu hình trong source code
- TOKEN = "BOT_TOKEN" 
- MINIO_ENDPOINT = "localhost:9000"
- MINIO_ACCESS_KEY = "MINIO_ACCESS_KEY"
- MINIO_SECRET_KEY = "MINIO_SECRET_KEY"
- MINIO_BUCKET_NAME = "downloader-bot"
- API_ID = API_ID 
- API_HASH = "API_HASH"

Các chức năng của bot
- Tự động tải xuống các file zip và rar được gửi đến group hoặc channel và lưu về Minio và folder của source code
- Kiểm tra các file bị trùng lặp: 
  - Nếu file có cùng tên và dung lượng: bot phản hồi file đã tồn tại
  - Nếu file khác dung lượng thì tải xuống với cấu trúc:"tên + dung lượng file" và phản hồi tải thành công

