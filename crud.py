import pandas as pd
import os

# Đường dẫn đến file lưu trữ dữ liệu điểm số
SCORES_FILE = "D:/PythonProgrammingFinalProject/DACK/scores_filled.csv"

def load_scores():
    if os.path.exists(SCORES_FILE):
        return pd.read_csv(SCORES_FILE, dtype={"Student ID": str})
    return pd.DataFrame(columns=[
        "Student ID", "Mathematics", "Literature", "Foreign language", "Physics",
        "Chemistry", "Biology", "History", "Geography", "Civic education",
        "Foreign language code"
    ])

def save_scores(df):
    df.to_csv(SCORES_FILE, index=False)

def validate_scores(values):
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
    if mode == "auto":
        df_filtered = df[df["Student ID"].str.startswith(ma_so)]
        last_id = df_filtered["Student ID"].str[2:].astype(int).max() if not df_filtered.empty else 0
        tail = str(last_id + 1).zfill(6)
    else:
        if not tail_input or len(tail_input) != 6 or not tail_input.isdigit():
            raise ValueError("Vui lòng nhập đúng 6 chữ số.")
        tail = tail_input
    return ma_so + tail

def add_student(df, sid, values):
    if sid in df["Student ID"].values:
        raise ValueError("Mã học sinh đã tồn tại.")
    validate_scores(values)
    df = pd.concat([df, pd.DataFrame([{"Student ID": sid, **values}])], ignore_index=True)
    save_scores(df)
    return df

def update_student(df, sid, values):
    if sid not in df["Student ID"].values:
        raise ValueError("Mã học sinh không tồn tại.")
    validate_scores(values)
    for key, val in values.items():
        df.loc[df["Student ID"] == sid, key] = val
    save_scores(df)
    return df

def delete_student(df, sid):
    if sid not in df["Student ID"].values:
        raise ValueError("Mã học sinh không tồn tại.")
    df = df[df["Student ID"] != sid]
    save_scores(df)
    return df