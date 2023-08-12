# Telegram bot download file
Bot Telegram tự động tải các file zip và rar từ group hoặc channel telegram

- file bot_folder.py: lưu các file về 1 folder
- file bot_minio.py: lưu các file trên Minio

1. Tạo bot và lấy token từ BotFather
2. Cho bot join vào group hoặc channel
3. Cấu hình trong file .env
- TOKEN = "BOT_TOKEN" 
- MINIO_ENDPOINT = "localhost:9000"
- MINIO_ACCESS_KEY = "MINIO_ACCESS_KEY"
- MINIO_SECRET_KEY = "MINIO_SECRET_KEY"
- MINIO_BUCKET_NAME = "downloader-bot"
- API_ID = API_ID 
- API_HASH = "API_HASH"

Các chức năng của bot
- Tự động tải xuống các file zip và rar được gửi đến group hoặc channel và lưu về Minio hoặc folder
- Bot xử lý nhiều file cùng 1 lúc và tải được các file có dung lượng lớn
- Kiểm tra các file bị trùng lặp: 
  - Nếu file có cùng tên và dung lượng: bot phản hồi file đã tồn tại
  - Nếu file khác dung lượng thì tải xuống với cấu trúc:"tên + dung lượng file" và phản hồi tải thành công

Nhiều file được gửi sẽ được xử lý riêng, file nặng sẽ download lâu hơn:
<img src="https://github.com/maiiquynhh/telegram-bot/issues/1#issue-1847615024">
<img src="https://github.com/maiiquynhh/telegram-bot/issues/2#issue-1847620362"> 

File log khi có file được gửi đến
<img src="https://github.com/maiiquynhh/telegram-bot/issues/3#issue-1847620765">






