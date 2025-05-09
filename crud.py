"""Module xử lý chức năng CRUD."""
import pandas as pd
import os

# Đường dẫn đến file CSV chứa điểm số sau khi đã làm sạch
SCORES_FILE = "scores_cleaned.csv"

def load_scores():
    """Tải dữ liệu điểm số từ file CSV."""
    if os.path.exists(SCORES_FILE):
        return pd.read_csv(SCORES_FILE, dtype={"Student ID": str})
    return pd.DataFrame(columns=[
        "Student ID", "Mathematics", "Literature", "Foreign language", "Physics",
        "Chemistry", "Biology", "History", "Geography", "Civic education",
        "Foreign language code"
    ])

def save_scores(df):
    """Lưu dữ liệu điểm số vào file CSV."""
    df.to_csv(SCORES_FILE, index=False)

def validate_scores(values):
    """Kiểm tra tính hợp lệ của điểm số."""
    score_columns = [
        "Mathematics", "Literature", "Foreign language", "Physics",
        "Chemistry", "Biology", "History", "Geography", "Civic education"
    ]
    for key, value in values.items():
        if key in score_columns:
            try:
                score = float(value)
                if not 0 <= score <= 10:
                    raise ValueError(f"Điểm môn {key} phải nằm trong khoảng từ 0 đến 10.")
            except (ValueError, TypeError):
                raise ValueError(f"Điểm môn {key} phải là một số hợp lệ.")
    return True

def generate_student_id(df, ma_so, mode, tail_input=None):
    """Tạo mã học sinh mới dựa trên mã sở và chế độ tự động hoặc thủ công.
    Mã số học sinh có định dạng: [Mã sở] + [6 chữ số].
    + Nếu chế độ là "auto", mã số sẽ tự động tăng dần từ mã số lớn nhất hiện có. Mình mình cần chọn mã sở.
    + Nếu chế độ là "manual", thì mình cần nhập 6 chữ số. """
    #Tự động
    if mode == "auto":
        df_filtered = df[df["Student ID"].str.startswith(ma_so)]
        last_id = df_filtered["Student ID"].str[2:].astype(int).max() if not df_filtered.empty else 0
        tail = str(last_id + 1).zfill(6)
    else:
    # Thủ công
        if not tail_input or len(tail_input) != 6 or not tail_input.isdigit():
            raise ValueError("Vui lòng nhập đúng 6 chữ số.")
        tail = tail_input
    return ma_so + tail

def add_student(df, student_id, values):
    """Thêm học sinh mới vào."""
    #Kiểm tra mã học sinh đã tồn tại chưa
    if student_id in df["Student ID"].values:
        raise ValueError("Mã học sinh đã tồn tại.")
    #Kiểm tra tính hợp lệ của điểm số
    validate_scores(values)
    #Thêm dữ liệu mới vào cuối frame
    df = pd.concat([df, pd.DataFrame([{"Student ID": student_id, **values}])], ignore_index=True)
    save_scores(df)
    return df

def update_student(df, student_id, values):
    """Cập nhật lại điểm của học sinh."""
    if student_id not in df["Student ID"].values:
        raise ValueError("Mã học sinh không tồn tại.")
    validate_scores(values)
    #Thực hiện cập nhật điểm dùng hàm loc() để truy cập vào học sinh cần cập nhật
    for key, val in values.items():
        df.loc[df["Student ID"] == student_id, key] = val
    save_scores(df)
    return df

def delete_student(df, student_id):
    """Xoá học sinh khỏi danh sách."""
    if student_id not in df["Student ID"].values:
        raise ValueError("Mã học sinh không tồn tại.")
    #Lọc theo Boolean để tối ưu hiệu suất
    df = df[df["Student ID"] != student_id]
    save_scores(df)
    return df