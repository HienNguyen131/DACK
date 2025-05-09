import pandas as pd

# Đọc dữ liệu và giữ nguyên số 0 ở đầu mã học sinh
df = pd.read_csv(r"D:\ltrinhPython\DACK\scores.csv", dtype={"Student ID": str})

# Thay thế các giá trị NaN bằng 0, trừ cột mã ngoại ngữ nếu cần giữ rỗng
cols_to_fill = df.columns.drop(["Student ID", "Foreign language code"])
df[cols_to_fill] = df[cols_to_fill].fillna(0)
# Lưu lại file mới
df.to_csv(r"D:\ltrinhPython\DACK\scores_filled.csv", index=False)

# Lọc học sinh có điểm môn Toán bằng 0
toan_0 = df[df["Literature"] == 0]

# In ra console
print("📢 Danh sách học sinh có điểm môn Toán = 0:")
print(toan_0[["Student ID", "Literature"]])
print(f"Tổng số học sinh: {len(toan_0)}")