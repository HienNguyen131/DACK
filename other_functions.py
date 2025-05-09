"""Module chứa các hàm hỗ trợ để vẽ biểu đồ và thống kê dữ liệu cho ứng dụng.
Gồm vẽ biểu đồ hình hộp, biểu đồ cột, thống kê điểm trung binh, xuất dữ liệu ra file excel, tính toán số trang,
xếp hạng các tỉnh có nhiều thí sinh đạt điểm 10."""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import ttkbootstrap as tb
from tkinter import messagebox
import os

def update_pagination(df, rows_per_page):
    """Hàm tính số trang để hiển thị"""
    #Tính tổng số hàm có trong dataset
    total_rows = len(df)
    #Tính tổng số trang
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page
    return total_rows, total_pages

def plot_score_distribution(subject, df):
    """Hàm vẽ biểu đồ phân bố điểm cho một môn học cụ thể"""
    #Khi chọn ngoại ngữ, do có nhiều loại ngoại ngữ nên nhóm chỉ xét theo mã N1 là Tiếng Anh.
    #Lọc dữ liệu lần nữa là do theo theo khối nên sẽ có môn ngoài khối thì sẽ không thi hoặc bỏ thi gì đó,
    #nên sẽ không liệt kê, vậy nên sẽ chỉ xét có điểm thi tối thiểu là 0.25, điểm 1 câu trắc nghiệm.
    if subject == "Foreign language":
        data = df[(df["Foreign language code"] == "N1") & (df["Foreign language"] >= 0.25)]["Foreign language"]
        title = "Phổ điểm môn Tiếng Anh (Mã N1)"
    else:
        data = df[df[subject] > 0.25][subject]
        title = f"Phổ điểm môn {subject}"
    bins = [round(x * 0.25, 2) for x in range(0, 41)]
    counts = pd.cut(data, bins=bins, right=True, include_lowest=True).value_counts().sort_index()
    labels = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in counts.index]
    values = counts.values
    plt.figure(figsize=(14, 6), num=title)
    #Biểu đồ cột
    bars = plt.bar(labels, values, edgecolor="black")
    for bar, count in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count),
                 ha='center', va='bottom', fontsize=8, rotation=90)
    plt.title(f"{title} - THPT 2023", fontsize=14)
    plt.xlabel("Khoảng điểm")
    plt.ylabel("Số lượng thí sinh")
    plt.xticks(rotation=90)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

def plot_boxplot(subject, df):
    """Hàm vẽ biểu đồ hộp cho một môn học cụ thể"""
    if subject == "Foreign language":
        data = df[(df["Foreign language code"] == "N1") & (df["Foreign language"] >= 0.5)]["Foreign language"]
        title = "Phổ điểm môn Tiếng Anh (Mã N1)"
    else:
        data = df[df[subject] >= 0.25][subject]
        title = f"Phổ điểm môn {subject}"

    # Tính toán thống kê
    avg = data.mean()
    median = data.median()
    min_score = data.min()
    max_score = data.max()
    std_dev = data.std()
    count = len(data)

    # Tạo biểu đồ
    fig, ax = plt.subplots(figsize=(10, 6), num=title)  # Điều chỉnh kích thước để có không gian cho bảng bên cạnh
    ax.boxplot(data, vert=True, patch_artist=True)
    ax.set_title(f"Phân bố điểm môn {subject}", fontsize=14)
    ax.set_ylabel("Điểm")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    #Bảng thống kê điểm
    stats_data = [
        ["Số lượng", f"{count}"],
        ["Trung bình", f"{avg:.2f}"],
        ["Trung vị", f"{median:.2f}"],
        ["Min", f"{min_score:.2f}"],
        ["Max", f"{max_score:.2f}"],
        ["Độ lệch chuẩn", f"{std_dev:.2f}"]
    ]
    table = plt.table(cellText=stats_data,
                      colLabels=["Thông tin", "Giá trị"],
                      cellLoc='center',
                      colLoc='center',
                      loc='right')
    table.scale(1, 1.5)  
    plt.subplots_adjust(right=0.75)  
    plt.tight_layout()
    plt.show()

def open_chart_window(app, df):
    """Hàm mở cửa sổ vẽ biểu đồ"""
    chart_win = tb.Toplevel(app)
    chart_win.title("📊 Xem biểu đồ")
    chart_win.geometry("300x250")
    chart_win.resizable(False, False)

    tb.Label(chart_win, text="Chọn môn:", font=("Segoe UI", 10, "bold")).pack(pady=10)
    # Danh sách các môn học để chọn vẽ biểu đổ
    subjects = {
    "Toán": "Mathematics",
    "Văn": "Literature",
    "Tiếng Anh (N1)": "Foreign language",
    "Vật lý": "Physics",
    "Hóa học": "Chemistry",
    "Sinh học": "Biology",
    "Lịch sử": "History",
    "Địa lý": "Geography",
    "Giáo dục công dân": "Civic education"}
    #Combobox để chọn môn học
    combo_subject = tb.Combobox(chart_win, values=list(subjects.keys()), bootstyle="info")
    combo_subject.pack(pady=5)

    tb.Label(chart_win, text="Chọn loại biểu đồ:", font=("Segoe UI", 10, "bold")).pack(pady=10)
    chart_type = tb.StringVar(value="Bar")
    #Radiobutton để chọn loại biểu đồ
    tb.Radiobutton(chart_win, text="Biểu đồ cột", variable=chart_type, value="Bar").pack(anchor="w", padx=10)
    tb.Radiobutton(chart_win, text="Biểu đồ hộp", variable=chart_type, value="Box").pack(anchor="w", padx=10)

    def confirm_plot():
        """Hàm xác nhận và vẽ biểu đồ"""
        key = combo_subject.get()
        if key not in subjects and chart_type.get() == "Bar":
            messagebox.showerror("Lỗi", "Vui lòng chọn môn hợp lệ.")
            return
        chart_win.destroy()
        if chart_type.get() == "Bar":
            subject_col = subjects[key]
            plot_score_distribution(subject_col, df)
        else:
            subject_col = subjects[key]
            plot_boxplot(subject_col,df)

    tb.Button(chart_win, text="📈 Hiện biểu đồ", bootstyle="primary", command=confirm_plot).pack(pady=15)

def show_top_provinces_chart_gui(app, df):
    """Hàm vẽ biểu đồ xép hạng các tỉnh có nhiều thí sinh đạt điểm 10"""
    chart_win = tb.Toplevel(app)
    chart_win.title("🏆 Top tỉnh có nhiều thí sinh đạt điểm 10")
    chart_win.geometry("1000x600")
    df["Mã sở"] = df["Student ID"].astype(str).str[:2]
    #Lọc lấy mã sở
    mon_thi = ["Mathematics", "Literature", "Foreign language", "Physics", "Chemistry",
               "Biology", "History", "Geography", "Civic education"]
    df["Có điểm 10"] = df[mon_thi].apply(lambda row: any(score == 10 for score in row), axis=1)
    top_scores = df[df["Có điểm 10"]].groupby("Mã sở").size()
    ma_so_df = pd.read_csv("ma_so_ten_so_gddt.csv", dtype={"Mã sở": str})
    merged = pd.DataFrame({"Mã sở": top_scores.index, "Số HS": top_scores.values})
    merged = merged.merge(ma_so_df, on="Mã sở")
    top10 = merged.sort_values("Số HS", ascending=False).head(10)
    fig = Figure(figsize=(10, 5), dpi=100)
    ax = fig.add_subplot(111)
    bars = ax.bar(top10["Tên sở GDĐT"], top10["Số HS"], color="dodgerblue", edgecolor="black")
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 10, int(yval), ha='center', va='bottom')
    ax.set_title("Top tỉnh thành có nhiều thí sinh có điểm 10", fontsize=14)
    ax.set_ylabel("Số học sinh")
    ax.set_xticklabels(top10["Tên sở GDĐT"], rotation=30, ha="right")
    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def export_to_excel(df):
    base_dir = ""
    filepath = os.path.join(base_dir, "diem_thi_thpt_2023_xuat.xlsx")
    df.to_excel(filepath, index=False)
    messagebox.showinfo("✅ Xuất thành công", f"Dữ liệu đã được lưu vào {filepath}")

def show_average_scores(app, df):
    """Hàm hiển thị thống kê điểm trung bình cho các môn học"""
    stats_win = tb.Toplevel(app)
    stats_win.title("📈 Thống kê điểm trung bình")
    stats_win.geometry("800x400")
    stats_win.resizable(False, False)

    # Tiêu đề
    tb.Label(stats_win, text="Thống kê điểm thi THPT 2023", font=("Segoe UI", 12, "bold")).pack(pady=10)

    # Khung chứa tiêu đề cột
    header_frame = tb.Frame(stats_win)
    header_frame.pack(fill="x", padx=10)
    headers = ["Môn", "Trung bình", "Cao nhất", "Thấp nhất", "Tỷ lệ ≥ 5.0"]
    for col, header in enumerate(headers):
        tb.Label(header_frame, text=header, font=("Segoe UI", 10, "bold"), width=15).grid(row=0, column=col, padx=5)

    # Khung chứa dữ liệu
    data_frame = tb.Frame(stats_win)
    data_frame.pack(fill="x", padx=10, pady=5)

    score_columns = [
        "Mathematics", "Literature", "Foreign language", "Physics",
        "Chemistry", "Biology", "History", "Geography", "Civic education"
    ]
    for row, col in enumerate(score_columns, start=1):
        mean_score = df[col].mean()
        max_score = df[col].max()
        min_score = df[col].min()
        pass_rate = (df[col] >= 5.0).mean() * 100

        display_mean = f"{mean_score:.2f}" if not pd.isna(mean_score) else "Chưa có dữ liệu"
        display_max = f"{max_score:.2f}" if not pd.isna(max_score) else "Chưa có dữ liệu"
        display_min = f"{min_score:.2f}" if not pd.isna(min_score) else "Chưa có dữ liệu"
        display_pass = f"{pass_rate:.1f}%" if not pd.isna(pass_rate) else "Chưa có dữ liệu"

        tb.Label(data_frame, text=col, font=("Segoe UI", 10), width=15).grid(row=row, column=0, padx=5, pady=2)
        tb.Label(data_frame, text=display_mean, font=("Segoe UI", 10), width=15).grid(row=row, column=1, padx=5, pady=2)
        tb.Label(data_frame, text=display_max, font=("Segoe UI", 10), width=15).grid(row=row, column=2, padx=5, pady=2)
        tb.Label(data_frame, text=display_min, font=("Segoe UI", 10), width=15).grid(row=row, column=3, padx=5, pady=2)
        tb.Label(data_frame, text=display_pass, font=("Segoe UI", 10), width=15).grid(row=row, column=4, padx=5, pady=2)

    # Tổng số học sinh
    tb.Label(stats_win, text=f"Tổng số học sinh: {len(df)}", font=("Segoe UI", 10, "bold")).pack(pady=15)

    # Nút Đóng
    tb.Button(stats_win, text="Đóng", bootstyle="secondary", command=stats_win.destroy).pack(pady=10)