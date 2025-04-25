import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
import os
from crud import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


app = tb.Window(themename="cosmo")
app.title("📊 Phân tích điểm thi THPT 2023")
app.geometry("3000x3000")
# Load dữ liệu
df = load_scores()

ROWS_PER_PAGE = 50
current_page = 0

def update_pagination():
    global total_rows, total_pages
    total_rows = len(df)
    total_pages = (total_rows + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

def show_page(page):
    global current_page
    current_page = page
    tree.delete(*tree.get_children())
    start = page * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE
    sorted_df = df.sort_values(by="Student ID")
    page_data = sorted_df.iloc[start:end]

    for _, row in page_data.iterrows():
        tree.insert("", "end", values=list(row))
    lbl_page.config(text=f"Trang {current_page + 1} / {total_pages}")

def next_page():
    if current_page < total_pages - 1:
        show_page(current_page + 1)

def prev_page():
    if current_page > 0:
        show_page(current_page - 1)
# === Thêm dữ liệu ===
def open_add_window():
    form = tb.Toplevel(app)
    form.title("➕ Thêm học sinh")
    form.geometry("700x560")
    form.resizable(False, False)

    tb.Label(form, text="Chọn mã sở GDĐT:", font=("Segoe UI", 10, "bold")).pack(pady=5)
    ma_so_df = pd.read_csv("ma_so_ten_so_gddt.csv", dtype={"Mã sở": str})
    ma_so_dict = dict(zip(ma_so_df["Tên sở GDĐT"], ma_so_df["Mã sở"]))
    combo_so = tb.Combobox(form, values=list(ma_so_dict.keys()), bootstyle="info")
    combo_so.pack(pady=5)

    tb.Label(form, text="Cách tạo mã học sinh:").pack()
    mode = tb.StringVar(value="auto")
    entry_tail = tb.Entry(form)

    def toggle_entry_tail_state():
        if mode.get() == "auto":
            entry_tail.config(state="disabled")
        else:
            entry_tail.config(state="normal")

    tb.Radiobutton(form, text="Tự động", variable=mode, value="auto", command=toggle_entry_tail_state).pack(anchor="w", padx=10)
    tb.Radiobutton(form, text="Tự nhập 6 số cuối", variable=mode, value="manual", command=toggle_entry_tail_state).pack(anchor="w", padx=10)

    tb.Label(form, text="Nhập 6 số cuối:").pack()
    entry_tail.pack(pady=5)
    toggle_entry_tail_state()


    fields = [
        "Mathematics", "Literature", "Foreign language", "Physics",
        "Chemistry", "Biology", "History", "Geography", "Civic education"
    ]
    entries = {}
    input_frame = tb.Frame(form)
    input_frame.pack(pady=10)

    cols_per_row = 3
    for i in range(0, len(fields), cols_per_row):
        row_frame = tb.Frame(input_frame)
        row_frame.pack(pady=5)
        for field in fields[i:i + cols_per_row]:
            field_frame = tb.Frame(row_frame)
            field_frame.pack(side="left", padx=10)
            tb.Label(field_frame, text=field).pack()
            entry = tb.Entry(field_frame, width=12)
            entry.pack()
            entries[field] = entry

    lang_code_combo = tb.Combobox(form, values=[
        "N1 - Tiếng Anh", "N2 - Tiếng Nga", "N3 - Tiếng Pháp",
        "N4 - Tiếng Trung Quốc", "N5 - Tiếng Đức",
        "N6 - Tiếng Nhật", "N7 - Tiếng Hàn"
    ], bootstyle="secondary")
    lang_code_combo.pack(pady=5)
    lang_code_combo.set("N1 - Tiếng Anh")  


    def confirm_add():
        global df
        try:
            ten_so = combo_so.get()
            if ten_so not in ma_so_dict:
                messagebox.showerror("Lỗi", "Vui lòng chọn mã sở.")
                return
            ma_so = ma_so_dict[ten_so]
            tail = entry_tail.get().zfill(6) if mode.get() == "manual" else None
            sid = generate_student_id(df, ma_so, mode.get(), tail)

            values = {key: float(entries[key].get().strip() or 0) for key in fields}
            lang_code = lang_code_combo.get().split(" - ")[0].strip()
            values["Foreign language code"] = lang_code

            df = add_student(df, sid, values)
            update_pagination()
            form.destroy()
            show_page(0)
            messagebox.showinfo("✅ Thành công", f"Đã thêm học sinh {sid}.")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    tb.Button(form, text="➕ Xác nhận thêm", bootstyle="success", command=confirm_add).pack(pady=15)
# === Cập nhật dữ liệu ===
def open_update_window():
    form = tb.Toplevel(app)
    form.title("✏️ Cập nhật học sinh")
    form.geometry("500x500")

    tb.Label(form, text="Nhập mã học sinh (Student ID):").pack(pady=5)
    entry_sid = tb.Entry(form)
    entry_sid.pack(pady=5)

    content_frame = tb.Frame(form)
    content_frame.pack(pady=10)
    entry_widgets = {}

    def fetch_and_fill():
        sid = entry_sid.get().strip()
        if sid not in df["Student ID"].values:
            messagebox.showerror("Lỗi", "Không tìm thấy học sinh.")
            return
        for widget in content_frame.winfo_children():
            widget.destroy()
        student = df[df["Student ID"] == sid].iloc[0]
        for field in df.columns[1:]:  # bỏ Student ID
            tb.Label(content_frame, text=field).pack()
            val = str(student[field])
            entry = tb.Entry(content_frame)
            entry.insert(0, val)
            entry.pack()
            entry_widgets[field] = entry

        def confirm_update():
            try:
                values = {}
                for k, w in entry_widgets.items():
                    values[k] = float(w.get()) if k != "Foreign language code" else w.get().strip()
                global df
                df = update_student(df, sid, values)
                show_page(current_page)
                form.destroy()
                messagebox.showinfo("✅ Thành công", f"Đã cập nhật học sinh {sid}.")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        tb.Button(content_frame, text="💾 Cập nhật", bootstyle="primary", command=confirm_update).pack(pady=10)

    tb.Button(form, text="🔍 Tìm", bootstyle="info", command=fetch_and_fill).pack(pady=5)

# === Xóa 1 dữ liệu ===
def open_delete_window():
    form = tb.Toplevel(app)
    form.title("🗑️ Xoá học sinh")
    form.geometry("400x200")

    tb.Label(form, text="Nhập mã học sinh:").pack(pady=5)
    entry_sid = tb.Entry(form)
    entry_sid.pack(pady=5)

    def confirm_delete():
        sid = entry_sid.get().strip()
        try:
            global df
            df = delete_student(df, sid)
            update_pagination()
            show_page(0)
            form.destroy()
            messagebox.showinfo("✅ Đã xoá", f"Học sinh {sid} đã bị xoá.")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    tb.Button(form, text="🗑️ Xoá", bootstyle="danger", command=confirm_delete).pack(pady=10)

# === Bảng dữ liệu ===
frame = tb.Frame(app, padding=10)
frame.pack(fill=BOTH, expand=True)

tree = tb.Treeview(frame, columns=list(df.columns), show="headings", bootstyle="info")
for col in df.columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

vsb = tb.Scrollbar(frame, orient=VERTICAL, command=tree.yview, bootstyle="round")
hsb = tb.Scrollbar(frame, orient=HORIZONTAL, command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

vsb.pack(side=RIGHT, fill=Y)
hsb.pack(side=BOTTOM, fill=X)
tree.pack(side=LEFT, fill=BOTH, expand=True)
# === Biểu đồ ===


def plot_score_distribution(subject):
    if subject == "Foreign language":
        data = df[(df["Foreign language code"] == "N1") & (df["Foreign language"] >= 0.5)]["Foreign language"]
        title = "Phổ điểm môn Tiếng Anh (Mã N1)"
    else:
        data = df[df[subject] >= 0.5][subject]
        title = f"Phổ điểm môn {subject}"

   
    bins = [round(x * 0.25, 2) for x in range(0, 41)]  

    counts = pd.cut(data, bins=bins, right=True, include_lowest=True).value_counts().sort_index()

    labels = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in counts.index]
    values = counts.values

    plt.figure(figsize=(14, 6))
    bars = plt.bar(labels, values, edgecolor="black")

    for bar, count in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count),
                 ha='center', va='bottom', fontsize=8, rotation=90)

    plt.title(f"{title} - THPT 2023", fontsize=14)
    plt.xlabel("Khoảng điểm", fontsize=12)
    plt.ylabel("Số lượng thí sinh", fontsize=12)
    plt.xticks(rotation=90)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()




def open_chart_window():
    chart_win = tb.Toplevel(app)
    chart_win.title("📊 Xem phổ điểm")
    chart_win.geometry("300x180")

    tb.Label(chart_win, text="Chọn môn:", font=("Segoe UI", 10, "bold")).pack(pady=10)
    subjects = {
        "Toán": "Mathematics",
        "Văn": "Literature",
        "Tiếng Anh (N1)": "Foreign language"
    }
    combo_subject = tb.Combobox(chart_win, values=list(subjects.keys()), bootstyle="info")
    combo_subject.pack()

    def confirm_plot():
        key = combo_subject.get()
        if key not in subjects:
            messagebox.showerror("Lỗi", "Vui lòng chọn môn hợp lệ.")
            return
        subject_col = subjects[key]
        chart_win.destroy()
        plot_score_distribution(subject_col)

    tb.Button(chart_win, text="📈 Hiện biểu đồ", bootstyle="primary", command=confirm_plot).pack(pady=10)

#====Top tỉnh/thành có nhiều thí sinh đạt điểm 10.==
def show_top_provinces_chart_gui():
    global df

    # Tạo cửa sổ mới
    chart_win = tb.Toplevel(app)
    chart_win.title("🏆 Top tỉnh có nhiều thí sinh đạt điểm 10")
    chart_win.geometry("1000x600")

    # Tạo mã sở từ Student ID
    df["Mã sở"] = df["Student ID"].astype(str).str[:2]

    # Xác định môn thi
    mon_thi = [
        "Mathematics", "Literature", "Foreign language",
        "Physics", "Chemistry", "Biology",
        "History", "Geography", "Civic education"
    ]

    # Học sinh có ít nhất 1 môn đạt 10 điểm
    df["Có điểm 10"] = df[mon_thi].apply(lambda row: any(score == 10 for score in row), axis=1)

    # Đếm số HS có điểm 10 theo Mã sở
    top_scores = df[df["Có điểm 10"]].groupby("Mã sở").size()

    # Nối với bảng tên sở
    ma_so_df = pd.read_csv("ma_so_ten_so_gddt.csv", dtype={"Mã sở": str})
    merged = pd.DataFrame({"Mã sở": top_scores.index, "Số HS": top_scores.values})
    merged = merged.merge(ma_so_df, on="Mã sở")

    top10 = merged.sort_values("Số HS", ascending=False).head(10)

    # Tạo Figure
    fig = Figure(figsize=(10, 5), dpi=100)
    ax = fig.add_subplot(111)

    bars = ax.bar(top10["Tên sở GDĐT"], top10["Số HS"], color="dodgerblue", edgecolor="black")

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 10, int(yval), ha='center', va='bottom', fontsize=9)

    ax.set_title("Top tỉnh thành có nhiều thí sinh có điểm 10", fontsize=14)
    ax.set_ylabel("Số học sinh", fontsize=12)
    ax.set_xticklabels(top10["Tên sở GDĐT"], rotation=30, ha="right")

    # Hiển thị Figure trong Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# === Điều hướng trang ===
nav_frame = tb.Frame(app)
nav_frame.pack()

btn_prev = tb.Button(nav_frame, text="← Trang trước", command=prev_page)
btn_prev.grid(row=0, column=0, padx=10)

lbl_page = tb.Label(nav_frame, text="", font=("Segoe UI", 10, "bold"))
lbl_page.grid(row=0, column=1, padx=10)

btn_next = tb.Button(nav_frame, text="Trang sau →", command=next_page)
btn_next.grid(row=0, column=2, padx=10)

# === Thao tác ===
action_frame = tb.Frame(app, padding=10)
action_frame.pack()
# Các nút sửa, xoá sẽ thêm sau
tb.Button(action_frame, text="➕ Thêm", width=15, bootstyle="success", command=open_add_window).grid(row=0, column=0, padx=10)
tb.Button(action_frame, text="✏️ Sửa", width=15, bootstyle="warning", command=open_update_window).grid(row=0, column=1, padx=10)
tb.Button(action_frame, text="🗑️ Xoá", width=15, bootstyle="danger", command=open_delete_window).grid(row=0, column=2, padx=10)
tb.Button(action_frame, text="📊 Biểu đồ", width=15, bootstyle="secondary", command=open_chart_window).grid(row=0, column=3, padx=10)
tb.Button(action_frame, text="🏆 Top điểm 10", width=15, bootstyle="info", command=show_top_provinces_chart_gui).grid(row=0, column=4, padx=10)




update_pagination()
show_page(0)
app.mainloop()
