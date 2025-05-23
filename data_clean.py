import pandas as pd

# Đọc dữ liệu và giữ nguyên số 0 ở đầu mã học sinh
# Ép kiểu dữ liệu cho cột "Student ID" thành kiểu chuỗi để không bị mất số 0
df = pd.read_csv(r"scores.csv", dtype={"Student ID": str})

# Thay thế các giá trị NaN (Not a Number bằng 0), trừ cột mã ngoại ngữ nếu cần giữ rỗng
cols_to_fill = df.columns.drop(["Student ID", "Foreign language code"])
df[cols_to_fill] = df[cols_to_fill].fillna(0)

# Lưu lại file mới
df.to_csv(r"scores_cleaned.csv", index=False)

