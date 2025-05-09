"""Module chính, chứa giao diện và các chức năng chính của ứng dụng."""
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd
from crud import load_scores, generate_student_id, add_student, update_student, delete_student
from other_functions import update_pagination, open_chart_window, show_top_provinces_chart_gui, export_to_excel, show_average_scores

# Khởi tạo ứng dụng
app = tb.Window(themename="cosmo")
app.title("📊 Phân tích điểm thi THPT 2023")
# app.geometry("3000x3000")
app.state("zoomed")


# Biến toàn cục
df = load_scores()
#Số học sinh trên mỗi trang
ROWS_PER_PAGE = 50
current_page = 0
total_rows = 0
total_pages = 0

def auto_save():
    """Hàm tự động lưu dữ liệu vào file scores.csv"""
    df.to_csv("scores.csv", index=False)

def show_page(page):
    """Hàm hiển thị trang dữ liệu trong Treeview"""
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
    """Hàm chuyển đến trang tiếp theo"""
    if current_page < total_pages - 1:
        show_page(current_page + 1)

def prev_page():
    """Hàm chuyển đến trang trước đó"""
    if current_page > 0:
        show_page(current_page - 1)

def confirm_add_hook():
    """Hàm gọi lại sau khi thêm học sinh thành công"""
    global total_rows, total_pages
    total_rows, total_pages = update_pagination(df, ROWS_PER_PAGE)
    show_page(0)
    auto_save()

def confirm_update_hook():
    """Hàm gọi lại sau khi cập nhật học sinh thành công"""
    show_page(current_page)
    auto_save()

def confirm_delete_hook():
    """Hàm gọi lại sau khi xóa học sinh thành công"""
    global total_rows, total_pages
    total_rows, total_pages = update_pagination(df, ROWS_PER_PAGE)
    show_page(0)
    auto_save()


def open_add_window():
    """Hàm mở cửa sổ thêm học sinh"""
    global df
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

    fields = ["Mathematics", "Literature", "Foreign language", "Physics",
              "Chemistry", "Biology", "History", "Geography", "Civic education"]
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
        """Hàm kiểm tra lỗi trước khi thêm học sinh"""
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
            confirm_add_hook()
            form.destroy()
            messagebox.showinfo("✅ Thành công", f"Đã thêm học sinh {sid}.")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    tb.Button(form, text="➕ Xác nhận thêm", bootstyle="success", command=confirm_add).pack(pady=15)

# Hàm mở cửa sổ cập nhật học sinh
def open_update_window():
    """Hàm mở cửa sổ cập nhật học sinh"""
    global df
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
        """Hàm tìm kiếm và điền thông tin học sinh vào form"""
        global df
        student_id = entry_sid.get().strip()
        if student_id not in df["Student ID"].values:
            messagebox.showerror("Lỗi", "Không tìm thấy học sinh.")
            return
        for widget in content_frame.winfo_children():
            widget.destroy()
        student = df[df["Student ID"] == student_id].iloc[0]
        for field in df.columns[1:]:
            tb.Label(content_frame, text=field).pack()
            val = str(student[field])
            entry = tb.Entry(content_frame)
            entry.insert(0, val)
            entry.pack()
            entry_widgets[field] = entry

        def confirm_update():
            global df
            try:
                values = {}
                for k, w in entry_widgets.items():
                    values[k] = float(w.get()) if k != "Foreign language code" else w.get().strip()
                df = update_student(df, student_id, values)
                confirm_update_hook()
                form.destroy()
                messagebox.showinfo("✅ Thành công", f"Đã cập nhật học sinh {student_id}.")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        tb.Button(content_frame, text="💾 Cập nhật", bootstyle="primary", command=confirm_update).pack(pady=10)

    tb.Button(form, text="🔍 Tìm", bootstyle="info", command=fetch_and_fill).pack(pady=5)

# Hàm mở cửa sổ xóa học sinh
def open_delete_window():
    """Hàm mở cửa sổ xóa học sinh"""
    global df
    form = tb.Toplevel(app)
    form.title("🗑️ Xoá học sinh")
    form.geometry("400x200")

    tb.Label(form, text="Nhập mã học sinh:").pack(pady=5)
    entry_sid = tb.Entry(form)
    entry_sid.pack(pady=5)

    def confirm_delete():
        global df
        student_id = entry_sid.get().strip()
        if not messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa học sinh với mã {student_id}?"):
            return
        try:
            df = delete_student(df, student_id)
            confirm_delete_hook()
            form.destroy()
            messagebox.showinfo("✅ Đã xoá", f"Học sinh {student_id} đã bị xoá.")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    tb.Button(form, text="🗑️ Xoá", bootstyle="danger", command=confirm_delete).pack(pady=10)

# Tìm kiếm nhanh
def search_student():
    """Hàm tìm kiếm học sinh theo mã học sinh"""
    global df
    keyword = entry_search.get().strip()
    if not keyword:
        messagebox.showerror("Lỗi", "Vui lòng nhập từ khoá để tìm.")
        return
    filtered = df[df["Student ID"].astype(str).str.contains(keyword)]
    if filtered.empty:
        messagebox.showinfo("Thông báo", "Không tìm thấy học sinh phù hợp.")
        return
    tree.delete(*tree.get_children())
    for _, row in filtered.iterrows():
        tree.insert("", "end", values=list(row))
    lbl_page.config(text=f"Kết quả tìm kiếm: {len(filtered)} học sinh")

# Treeview
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

# Điều hướng
nav_frame = tb.Frame(app)
nav_frame.pack()
btn_prev = tb.Button(nav_frame, text="← Trang trước", command=prev_page)
btn_prev.grid(row=0, column=0, padx=10)
lbl_page = tb.Label(nav_frame, text="", font=("Segoe UI", 10, "bold"))
lbl_page.grid(row=0, column=1, padx=10)
btn_next = tb.Button(nav_frame, text="Trang sau →", command=next_page)
btn_next.grid(row=0, column=2, padx=10)

# Thao tác
action_frame = tb.Frame(app, padding=10)
action_frame.pack()
tb.Button(action_frame, text="➕ Thêm", width=15, bootstyle="success", command=open_add_window).grid(row=0, column=0, padx=10)
tb.Button(action_frame, text="✏️ Sửa", width=15, bootstyle="warning", command=open_update_window).grid(row=0, column=1, padx=10)
tb.Button(action_frame, text="🗑️ Xoá", width=15, bootstyle="danger", command=open_delete_window).grid(row=0, column=2, padx=10)
tb.Button(action_frame, text="📊 Biểu đồ", width=15, bootstyle="secondary", command=lambda: open_chart_window(app, df)).grid(row=0, column=3, padx=10)
tb.Button(action_frame, text="🏆 Top điểm 10", width=15, bootstyle="info", command=lambda: show_top_provinces_chart_gui(app, df)).grid(row=0, column=4, padx=10)
tb.Button(action_frame, text="💾 Xuất Excel", width=15, bootstyle="success", command=lambda: export_to_excel(df)).grid(row=0, column=5, padx=10)
tb.Button(action_frame, text="📈 Thống kê", width=15, bootstyle="primary", command=lambda: show_average_scores(app, df)).grid(row=0, column=6, padx=10)

# Tìm kiếm
tb.Label(action_frame, text="🔎 Tìm HS:").grid(row=1, column=0, pady=10)
entry_search = tb.Entry(action_frame)
entry_search.grid(row=1, column=1)
tb.Button(action_frame, text="Tìm", bootstyle="info", command=search_student).grid(row=1, column=2, padx=5)

# Khởi động
if __name__ == "__main__":
    total_rows, total_pages = update_pagination(df, ROWS_PER_PAGE)
    show_page(0)
    app.mainloop()