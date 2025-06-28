# SouthVietnamLottery
## Quy trình trích xuất thông tin
### Bước 1: Cào dữ liệu (Data Scraping)
- **Nguồn dữ liệu:**

    https://www.minhngoc.net.vn/ket-qua-xo-so/mien-nam.html
    table.bkqmiennam[0]

    https://supabase.com/dashboard/project/kqnomikuczplckuqcybu/database/schemas

- **Công cụ cào dữ liệu:**

    ***Python:*** Sử dụng thư viện Selenium để cào dữ liệu từ các trang web.

    ***Tần suất:*** 17:00 hằng ngày.

    ***Thông tin cần thu thập:***

    Kết quả các giải (từ giải đặc biệt đến giải tám).
    Ngày quay số, tỉnh quay số.

- **Lập lịch:** Sử dụng Apache Airflow trên Server

``` Thực hiện ```

1. Cài đặt Airflow (Python 3.8.10)

```shell
pip install markupsafe==2.1.3
pip install apache-airflow==2.6.3
pip install selenium webdriver-manager
pip uninstall pendulum -y
pip install pendulum==2.1.2
pip install flask-session==0.5.0
pip install connexion==2.14.2
set AIRFLOW_HOME=D:\Work\Master\SouthVietnamLottery\airflow
airflow db init
```

Mở file airflow.cfg thêm dòng `use_symlinks = False`
vào:
```
[logging]
use_symlinks = False
```

Tạo tài khoản admin
```
airflow users create --username admin --firstname Admin --lastname "" --role Admin --email example@xyz.com
```
Chạy Airflow
```
airflow webserver -p 8080
```

2. Viết DAG cho cào dữ liệu

- Viết module cao dữ liệu
- 

### Bước 2: Lưu trữ dữ liệu (Data Storage)
Loại cơ sở dữ liệu:
Cơ sở dữ liệu quan hệ (RDBMS): MySQL, PostgreSQL để lưu trữ dữ liệu có cấu trúc (kết quả xổ số, ngày quay, tỉnh).
Cơ sở dữ liệu NoSQL: MongoDB nếu dữ liệu có cấu trúc linh hoạt hoặc cần lưu trữ dữ liệu thô (raw data).
Data Lake: Sử dụng S3 (AWS) hoặc Google Cloud Storage để lưu trữ dữ liệu thô dưới dạng JSON, CSV.
Cấu trúc bảng (ví dụ cho MySQL):
Bảng results:
id: Khóa chính.
draw_date: Ngày quay số.
province: Tỉnh quay số.
special_prize, first_prize, ..., eighth_prize: Kết quả các giải.
Bảng loto:
id: Khóa chính.
draw_date: Ngày quay số.
province: Tỉnh quay số.
number: Số loto (2 chữ số cuối của các giải).
Backup và bảo mật:
Sao lưu định kỳ dữ liệu.
Mã hóa dữ liệu nhạy cảm (nếu có).
Đảm bảo quyền truy cập được kiểm soát.
Bước 3: ETL (Extract, Transform, Load)
Extract: Trích xuất dữ liệu từ cơ sở dữ liệu thô hoặc file JSON/CSV.
Transform:
Làm sạch dữ liệu:
Xử lý giá trị thiếu, trùng lặp.
Chuẩn hóa định dạng (ví dụ: ngày tháng, tên tỉnh).
Tính toán bổ sung:
Tần suất xuất hiện của các con số (theo giải, theo tỉnh, theo thời gian).
Phân tích số đầu/đuôi, cặp số, chu kỳ lặp.
Xác định các số “nóng” (xuất hiện nhiều) và “lạnh” (xuất hiện ít).
Tích hợp dữ liệu:
Gộp dữ liệu từ nhiều tỉnh, nhiều ngày.
Tạo các chỉ số thống kê (ví dụ: tỷ lệ xuất hiện của số chẵn/lẻ, số lớn/nhỏ).
Load:
Lưu dữ liệu đã xử lý vào một data warehouse (như Redshift, BigQuery) hoặc cơ sở dữ liệu phân tích (như PostgreSQL).
Tạo các bảng tổng hợp (aggregate tables) để tối ưu hóa truy vấn báo cáo.
Công cụ ETL:
Apache Airflow: Lập lịch và quản lý pipeline ETL.
Python (Pandas): Xử lý và biến đổi dữ liệu.
Talend hoặc Pentaho: Nếu cần công cụ ETL giao diện đồ họa.
Bước 4: Reporting
Công cụ báo cáo:
Power BI, Tableau, hoặc Looker: Tạo dashboard tương tác.
Python (Matplotlib, Seaborn): Tạo báo cáo tĩnh hoặc biểu đồ tùy chỉnh.
Google Data Studio: Nếu cần giải pháp miễn phí và dễ sử dụng.
Các loại báo cáo:
Báo cáo tĩnh: Báo cáo hàng tuần/tháng về tần suất số, xu hướng số.
Dashboard tương tác:
Bộ lọc theo tỉnh, ngày, giải.
Biểu đồ tần suất số, biểu đồ nhiệt (heatmap) cho các cặp số.
Dự đoán xu hướng dựa trên lịch sử (sử dụng mô hình thống kê đơn giản).
Phân phối báo cáo:
Gửi email tự động (sử dụng Airflow hoặc cron jobs).
Xuất file PDF/Excel.
Cung cấp API để truy cập báo cáo từ ứng dụng bên thứ ba.

2. Ý tưởng phân tích và báo cáo kết quả xổ số miền Nam
Dưới đây là một số ý tưởng cụ thể để tạo ra các báo cáo phân tích hấp dẫn và hữu ích:
Ý tưởng 1: Phân tích tần suất số
Mô tả: Xác định các con số xuất hiện nhiều nhất và ít nhất trong một khoảng thời gian (1 tháng, 3 tháng, 1 năm).
Báo cáo:
Biểu đồ cột hiển thị tần suất xuất hiện của từng số (00-99).
Heatmap cho cặp số (ví dụ: 23-45 có xuất hiện cùng nhau thường xuyên không).
So sánh tần suất giữa các tỉnh (ví dụ: TP.HCM vs. Đồng Nai).
Ứng dụng: Giúp người chơi nhận diện các số “nóng” hoặc “lạnh” để tham khảo.
Ý tưởng 2: Phân tích số đầu/đuôi
Mô tả: Phân tích tần suất xuất hiện của các số đầu (chữ số hàng chục) và số đuôi (chữ số hàng đơn vị).
Báo cáo:
Biểu đồ tròn cho tỷ lệ xuất hiện của các số đầu (0-9).
Biểu đồ dòng (line chart) theo thời gian để theo dõi xu hướng số đuôi.
Báo cáo các cặp đầu-đuôi phổ biến (ví dụ: đầu 2-đuôi 3).
Ứng dụng: Hỗ trợ người chơi tập trung vào các cặp đầu-đuôi có khả năng xuất hiện cao.
Ý tưởng 3: Phân tích chu kỳ và xu hướng
Mô tả: Xác định chu kỳ lặp của các con số hoặc các giải (ví dụ: số 45 có xu hướng xuất hiện lại sau 7 ngày).
Báo cáo:
Biểu đồ chu kỳ (cycle chart) cho các số hoặc cặp số.
Dự đoán đơn giản dựa trên xu hướng lịch sử (sử dụng trung bình động hoặc hồi quy tuyến tính).
Báo cáo các số “trễ” (chưa xuất hiện trong thời gian dài).
Ứng dụng: Cung cấp thông tin cho người chơi về thời điểm một số có thể “trở lại”.
Ý tưởng 4: So sánh giữa các tỉnh
Mô tả: Phân tích sự khác biệt về kết quả xổ số giữa các tỉnh miền Nam.
Báo cáo:
Biểu đồ so sánh tần suất số giữa các tỉnh.
Bảng xếp hạng các tỉnh có tỷ lệ xuất hiện số chẵn/lẻ, lớn/nhỏ.
Heatmap cho sự tương đồng về kết quả giữa các tỉnh.
Ứng dụng: Giúp người chơi hiểu đặc điểm riêng của từng tỉnh.
Ý tưởng 5: Phân tích theo giải
Mô tả: Tập trung vào các giải cụ thể (đặc biệt, nhất, nhì, v.v.) để tìm xu hướng.
Báo cáo:
Tần suất số trong giải đặc biệt theo thời gian.
Phân tích các cặp số liên tiếp trong giải đặc biệt (ví dụ: 123456 -> 12-34-56).
So sánh đặc điểm số trong giải đặc biệt vs. các giải khác.
Ứng dụng: Hỗ trợ người chơi tập trung vào các giải có giá trị cao.
Ý tưởng 6: Ứng dụng học máy (nâng cao)
Mô tả: Sử dụng các mô hình học máy để dự đoán hoặc tìm mẫu trong dữ liệu xổ số.
Phương pháp:
Mô hình hồi quy hoặc phân loại để dự đoán số tiếp theo (dù xổ số là ngẫu nhiên, nhưng có thể tìm các mẫu thống kê).
Phân cụm (clustering) để nhóm các ngày quay số có đặc điểm tương đồng.
Báo cáo:
Biểu đồ dự đoán xác suất xuất hiện của các số.
Báo cáo các mẫu tiềm năng (nếu có).
Lưu ý: Cần nhấn mạnh rằng xổ số là ngẫu nhiên, và các dự đoán chỉ mang tính tham khảo.

3. Một số lưu ý thực tế
Tính pháp lý: Đảm bảo tuân thủ các quy định về cờ bạc và xổ số tại Việt Nam. Tránh quảng bá công cụ này như một phương pháp “chắc chắn thắng”.
Tính ngẫu nhiên: Xổ số là trò chơi ngẫu nhiên, nên các báo cáo chỉ nên cung cấp thông tin tham khảo, không nên đưa ra lời hứa hẹn về kết quả.
Giao diện thân thiện: Nếu phát triển sản phẩm cho người dùng cuối, hãy tạo giao diện đơn giản, dễ sử dụng, với các bộ lọc (theo tỉnh, ngày, giải) và biểu đồ trực quan.
Tối ưu hóa chi phí: Sử dụng các công cụ mã nguồn mở (Python, PostgreSQL, Apache Airflow) để giảm chi phí triển khai.

4. Ví dụ dashboard mẫu
Bộ lọc:
Chọn tỉnh (TP.HCM, Đồng Nai, Cần Thơ, v.v.).
Chọn khoảng thời gian (1 tuần, 1 tháng, 1 năm).
Chọn loại giải (đặc biệt, nhất, loto, v.v.).
Biểu đồ:
Biểu đồ cột: Tần suất số (00-99).
Heatmap: Tần suất cặp số.
Biểu đồ đường: Xu hướng số đầu/đuôi theo thời gian.
Bảng dữ liệu:
Danh sách các số “nóng” và “lạnh”.
Các số “trễ” (chưa xuất hiện lâu).
Tóm tắt kết quả theo tỉnh.
