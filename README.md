# 📌 Giới thiệu Dự án

Đây là dự án cuối kỳ của môn **Lập Trình Python** với đề tài: **"Ứng dụng các thư viện xử lý dữ liệu của Python để phân tích điểm thi THPT Quốc gia năm 2023"**. Dự án sử dụng tập dữ liệu từ [🎓 Vietnamese National HS Graduation Exam 2023 💯](https://www.kaggle.com/datasets/duongtruongbinh/vietnamese-national-high-school-graduation-exam).

## Mục tiêu
- Phân tích và trực quan hóa dữ liệu điểm thi THPT Quốc gia 2023.
- Xây dựng ứng dụng với giao diện người dùng để hỗ trợ quản lý và phân tích dữ liệu.

## Chức năng chính
- **Đọc dữ liệu**: Tải dữ liệu thô từ file CSV.
- **Làm sạch dữ liệu**: Sử dụng Pandas để xử lý dữ liệu thiếu, chuẩn hóa định dạng và loại bỏ bất thường.
- **Quản lý dữ liệu**: Thực hiện các thao tác [CRUD](https://vi.wikipedia.org/wiki/CRUD) (Create, Read, Update, Delete) trên tập dữ liệu.
- **Trực quan hóa**: Vẽ biểu đồ (biểu đồ cột, phân tán, histogram, v.v.) bằng Matplotlib để mô tả các đặc trưng của dữ liệu.
- **Giao diện người dùng**: Xây dựng giao diện thân thiện với người dùng bằng Tkinter và ttkbootstrap.

## Công nghệ sử dụng
- **Ngôn ngữ**: Python 3.x
- **Thư viện**: Pandas, Matplotlib, ttkbootstrap
- **IDE đề xuất**: VSCode, PyCharm

## Đội ngũ thực hiện
Sinh viên thực hiện:
- [Nguyễn Thanh Hiền - 22110137](https://github.com/HienNguyen131)
- [Phan Thanh Thiện - 22110234](https://github.com/ThienPhan2004)
- [Bùi Lê Anh Tân - 22110223](https://github.com/blatenka)

---

# 🚀 Cài đặt

### Yêu cầu
- **Python**: Phiên bản 3.8 trở lên. Tải tại [python.org](https://www.python.org).
- **Hệ điều hành**: Windows, macOS, hoặc Linux.

### Cài đặt thư viện
Cài đặt các thư viện cần thiết bằng lệnh:
```bash
pip install ttkbootstrap pandas matplotlib
```

### Clone repository
Sao chép mã nguồn về máy:
```bash
git clone https://github.com/HienNguyen131/DACK.git
cd DACK
```

### Chạy chương trình
Chạy file chính của dự án:
```bash
python main.py
```

---

# 📖 Hướng dẫn sử dụng
1. **Chuẩn bị dữ liệu**: Đảm bảo file CSV chứa dữ liệu điểm thi được đặt trong thư mục dự án hoặc chỉ định đường dẫn chính xác trong mã nguồn.
2. **Khởi chạy ứng dụng**: Chạy file `main.py` để mở giao diện Tkinter.
3. **Tương tác**:
   - Sử dụng các nút chức năng để thực hiện CRUD.
   - Xem biểu đồ trực quan qua mục "Trực quan hóa".
4. **Lưu ý**: Kiểm tra dữ liệu đầu vào để tránh lỗi khi phân tích.

# 📜 Giấy phép
Dự án được phát hành dưới [MIT License](https://opensource.org/licenses/MIT).