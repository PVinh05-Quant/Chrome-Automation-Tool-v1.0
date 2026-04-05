# 🚀 Chrome Automation Tool v1.0

**Chrome Automation Tool v1.0** là một hệ thống tự động hóa trình duyệt web mạnh mẽ, đa luồng và linh hoạt được viết bằng Python. Công cụ này cho phép bạn quản lý nhiều hàng đợi người dùng (profile), tự động cấu hình proxy, sắp xếp cửa sổ thông minh trên màn hình và thực thi các kịch bản tương tác web phức tạp thông qua cấu hình JSON hoàn toàn tự động.

## 🌟 Tính năng nổi bật

* **Chạy Đa Luồng (Multiprocessing):** Hỗ trợ chạy song song nhiều tiến trình trình duyệt cùng lúc thông qua `multiprocessing`. Tối ưu hóa thời gian thực thi cho lượng lớn tài khoản.
* **Quản Lý Cửa Sổ Thông Minh:** Tự động tính toán độ phân giải màn hình (thông qua `tkinter`) để chia lưới và sắp xếp các cửa sổ Chrome sao cho không bị trùng lặp, giúp dễ dàng theo dõi.
* **Hỗ Trợ Proxy Cấp Cao:** Tích hợp `seleniumwire` cho phép sử dụng Proxy có xác thực (Authentication) (HTTP/HTTPS) một cách dễ dàng, chia đều proxy cho từng tài khoản dựa trên mã định danh.
* **Bypass Anti-Bot Cơ Bản:** Vô hiệu hóa cờ tự động hóa (`AutomationControlled`, `enable-automation`), loại bỏ logs không cần thiết và giả mạo User-Agent để trình duyệt trông tự nhiên hơn.
* **Quản Lý Tài Nguyên Hệ Thống:** Tích hợp `psutil` để theo dõi CPU và RAM. Tự động tạm dừng việc tạo tiến trình mới nếu tài nguyên vượt quá ngưỡng cấu hình (ví dụ: >90%), chống crash máy.
* **Hỗ Trợ Tiện Ích Mở Rộng (.crx):** Tự động tải tất cả các file extension `.crx` có trong thư mục `extensions/` vào từng profile Chrome.
* **Hệ Thống Kịch Bản (Scripting) Linh Hoạt:** Đọc kịch bản từ file `kich_ban.json`. Hỗ trợ vô số hành động: điều hướng, click, điền form, cuộn trang, vòng lặp, xử lý alert, thao tác với dropdown, và thực thi JavaScript.
* **Hai Chế Độ Hoạt Động:**
    * **Tự Động (Auto):** Chạy tự động hoàn toàn 100% theo kịch bản.
    * **Tương Tác (Interactive):** Khởi tạo trình duyệt, nạp profile/proxy và giữ nguyên cửa sổ để người dùng tự thao tác thủ công.

---

## 📁 Cấu trúc thư mục dự án

```text
Chrome Automation Tool v1.0/
│
├── main.py                     # Trạm điều khiển trung tâm (Entry point)
│
├── modules/                    # Chứa mã nguồn cốt lõi
│   ├── che_do_tuong_tac.py     # Module giữ trình duyệt mở cho thao tác thủ công
│   ├── chrome_utils.py         # Tiện ích cấu hình Chrome Options & Extensions
│   ├── khoi_tao_trinh_duyet.py # Module cài đặt ChromeDriver, Proxy, User-Agent
│   ├── kiem_tra_tai_nguyen.py  # Giám sát RAM & CPU hệ thống
│   ├── quan_ly_man_hinh.py     # Module tính toán và sắp xếp lưới cửa sổ
│   ├── thuc_thi_kich_ban.py    # Engine chính: phân tích & chạy các bước kịch bản JSON
│   ├── trinh_tai_du_lieu.py    # Module nạp dữ liệu từ CSV, JSON
│   └── extensions/             # (Tùy chọn) Thư mục chứa các file extension .crx
│
└── data/                       # Dữ liệu đầu vào
    ├── cau_hinh.json           # File cấu hình tổng của hệ thống
    ├── danh_sach_nguoi_dung.csv# Chứa thông tin tài khoản/người dùng
    ├── danh_sach_proxy.csv     # Chứa danh sách proxy
    └── kich_ban.json           # File định nghĩa các bước tự động hóa
```

---

## ⚙️ Yêu cầu hệ thống (Prerequisites)

Dự án yêu cầu Python 3.10+ và các thư viện sau:

* `selenium` (Điều khiển trình duyệt)
* `selenium-wire` (Xử lý proxy authentication)
* `webdriver-manager` (Tự động tải ChromeDriver tương thích)
* `psutil` (Quản lý tài nguyên phần cứng)

Cài đặt nhanh các thư viện bằng lệnh:
```bash
pip install selenium selenium-wire webdriver-manager psutil
```

---

## 📝 Hướng dẫn cấu hình dữ liệu (`data/`)

### 1. File cấu hình hệ thống: `cau_hinh.json`
File này quản lý cách tool hoạt động.
```json
{
    "su_dung_che_do_tuong_tac": false,      // Chuyển sang true nếu muốn tự thao tác tay
    "url_khoi_dau_tuong_tac": "https://google.com", 
    "so_luong_tien_trinh_song_song": 1,     // Số lượng luồng chạy đồng thời
    "su_dung_profile_rieng": false,         // Lưu cache/cookie riêng biệt cho từng user
    "thu_muc_profiles": "profiles",         // Tên thư mục lưu data user
    "su_dung_proxy": false,                 // Bật/tắt việc dùng proxy
    "kiem_tra_tai_nguyen": false,           // Bật/tắt giám sát phần cứng
    "cpu_toi_da": 90,                       // Ngưỡng CPU (%) để tool tạm dừng
    "ram_toi_da": 90,                       // Ngưỡng RAM (%) để tool tạm dừng
    "sap_xep_cua_so": {
        "so_cot_mong_muon": 1,              // Số cột hiển thị trên màn hình
        "so_dong_mong_muon": 1,             // Số dòng hiển thị
        "chieu_rong_mong_muon": 505,        // Fix cứng chiều rộng cửa sổ
        "chieu_cao_mong_muon": 400,         // Fix cứng chiều cao cửa sổ
        "khoang_cach_giua_cac_cua_so": 3,
        "bu_tru_chieu_cao_tieu_de": 80
    }
}
```

### 2. Danh sách người dùng: `danh_sach_nguoi_dung.csv`
Định nghĩa thông tin các tài khoản. Cột `ma_dinh_danh` là bắt buộc để mapping với proxy và thư mục profile.
```csv
ma_dinh_danh,email,mat_khau
1,user01@example.com,pass123
2,user02@example.com,pass456
```

### 3. Danh sách Proxy: `danh_sach_proxy.csv`
*Lưu ý: Chỉ hoạt động nếu `su_dung_proxy` trong cấu hình là `true`.*
```csv
ma_dinh_danh,dia_chi_ip,cong,ten_dang_nhap,mat_khau,giao_thuc
1,103.82.X.X,44871,my_user,my_pass,http
```

---

## 🤖 Hướng dẫn viết Kịch bản (Scripting) - `kich_ban.json`

File `kich_ban.json` là một mảng (array) chứa các bước (object). Công cụ hỗ trợ rất nhiều hành động (action) khác nhau:

### Khai báo Bộ chọn (Selectors)
Hỗ trợ 4 loại: `"ID"`, `"NAME"`, `"XPATH"`, `"CSS_SELECTOR"`.

### Các hành động (hanh_dong) được hỗ trợ:

**1. Điều hướng web (`dieu_huong`)**
```json
{ "buoc": 1, "hanh_dong": "dieu_huong", "gia_tri": "https://www.google.com" }
```

**2. Tạm dừng (`cho` / `tam_dung_tu_dong`)**
Tạm dừng tĩnh:
```json
{ "buoc": 2, "hanh_dong": "cho", "gia_tri": 3 }
```
Tạm dừng ngẫu nhiên:
```json
{ 
  "buoc": 2, 
  "hanh_dong": "cho", 
  "gia_tri": { "loai": "so_thuc_ngau_nhien", "nho_nhat": 1, "lon_nhat": 3.5 } 
}
```

**3. Điền thông tin (`dien_thong_tin`)**
Nhập dữ liệu vào form.
```json
{
  "buoc": 3,
  "hanh_dong": "dien_thong_tin",
  "loai_bo_chon": "NAME",
  "gia_tri_bo_chon": "q",
  "gia_tri_nhap": "Selenium Python" 
}
```

**4. Nhấn chuột (`nhan_chuot`)**
```json
{
  "buoc": 4,
  "hanh_dong": "nhan_chuot",
  "loai_bo_chon": "XPATH",
  "gia_tri_bo_chon": "//button[@id='submit']"
}
```

**5. Lấy Text và lưu biến tạm (`lay_text`)**
```json
{
  "buoc": 5,
  "hanh_dong": "lay_text",
  "loai_bo_chon": "ID",
  "gia_tri_bo_chon": "result-stats",
  "khoa_luu_text": "ket_qua_tim_kiem" // Có thể tái sử dụng biến này bằng {ket_qua_tim_kiem} ở bước khác
}
```

**6. Thao tác Dropdown (`chon_dropdown`)**
Hỗ trợ `chon_theo`: `"text"`, `"value"`, hoặc `"index"`.
```json
{
  "buoc": 6,
  "hanh_dong": "chon_dropdown",
  "loai_bo_chon": "ID",
  "gia_tri_bo_chon": "dropdown",
  "chon_theo": "value",
  "gia_tri_chon": "2"
}
```

**7. Cuộn trang (`cuon_trang`)**
Hỗ trợ các loại cuộn: `"xuong"` (cuối trang), `"len"` (đầu trang), `"den_phan_tu"`, và `"theo_pixel"`.
```json
{
  "buoc": 7,
  "hanh_dong": "cuon_trang",
  "loai_cuon": "xuong"
}
```

**8. Xử lý Alert (`xu_ly_alert`)**
Hỗ trợ hành động: `"chap_nhan"`, `"huy_bo"`, `"nhap_text"`.
```json
{
  "buoc": 8,
  "hanh_dong": "xu_ly_alert",
  "hanh_dong_alert": "chap_nhan"
}
```

**9. Chuyển đổi Tab/Cửa sổ (`chuyen_cua_so`)**
Hỗ trợ chuyển đích: `"moi_nhat"` (tab mới mở), `"dau_tien"`, `"theo_tieu_de"`.
```json
{
  "buoc": 9,
  "hanh_dong": "chuyen_cua_so",
  "dich": "moi_nhat"
}
```

**10. Vòng lặp phức tạp (`vong_lap`)**
Cho phép lặp lại một chuỗi hành động, có hỗ trợ điều kiện dừng sớm (Break).
```json
{
  "buoc": 10,
  "hanh_dong": "vong_lap",
  "lap_toi_da": 3,
  "dieu_kien_dung": {
    "loai_bo_chon": "XPATH",
    "gia_tri_bo_chon": "//h2[text()='Success']",
    "loai_kiem_tra": "ton_tai"
  },
  "buoc_con": [
    {
      "buoc": "10.1",
      "hanh_dong": "cuon_trang",
      "loai_cuon": "theo_pixel",
      "x": 0, "y": 500
    },
    {
      "buoc": "10.2",
      "hanh_dong": "cho",
      "gia_tri": 1
    }
  ]
}
```

---

## 🚀 Cách chạy chương trình

Sau khi đã thiết lập xong các file trong thư mục `data/`, mở Terminal / Command Prompt tại thư mục gốc của dự án và chạy lệnh:

```bash
python main.py
```

* **Nếu `su_dung_che_do_tuong_tac` = `true`:** Hệ thống sẽ mở từng profile lên, áp dụng proxy và dừng lại chờ bạn ấn phím `Enter` trong terminal cho mỗi lượt. Khi làm việc xong, nhấn Enter một lần nữa để đóng hàng loạt.
* **Nếu `su_dung_che_do_tuong_tac` = `false`:** Hệ thống sẽ tự động điều phối các luồng (Workers) và chạy tự động hoàn toàn tuân theo file `kich_ban.json`.

---

## 🛠 Xử lý lỗi (Troubleshooting) & Logs

* Hệ thống được thiết lập log ở chế độ `INFO` với định dạng thời gian rõ ràng để dễ theo dõi các tiến trình.
* Log của `selenium` và `seleniumwire` được thiết lập ở mức `CRITICAL` để tránh spam màn hình console.
* Nếu tài nguyên máy bị báo quá tải ("Tài nguyên hệ thống cao! Đang tạm dừng..."), hãy kiểm tra và giảm biến `so_luong_tien_trinh_song_song` xuống trong file cấu hình.

---
👨‍💻 Tác giả & Liên hệ
Dự án được lên ý tưởng, phát triển và tối ưu hóa bởi:

Dev: PVinh + AI

Email Liên Hệ: ppvinh151@gmail.com#   C h r o m e - A u t o m a t i o n - T o o l - v 1 . 0  
 