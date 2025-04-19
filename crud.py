import pandas as pd
import os

SCORES_FILE = "scores_filled.csv"

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
    df = pd.concat([df, pd.DataFrame([{"Student ID": sid, **values}])], ignore_index=True)
    save_scores(df)
    return df
def update_student(df, sid, values):
    if sid not in df["Student ID"].values:
        raise ValueError("Mã học sinh không tồn tại.")
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

def delete_multiple_students(df, sid_list):
    not_found = [sid for sid in sid_list if sid not in df["Student ID"].values]
    if not_found:
        raise ValueError(f"Mã không tồn tại: {', '.join(not_found)}")
    df = df[~df["Student ID"].isin(sid_list)]
    save_scores(df)
    return df
