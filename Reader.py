import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import re
import base64

current_filename = ""
konami_code_sequence = []

def decode(base64_message):
    try:
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
    except Exception as e:
        return f"Error decoding Base64: {str(e)}"

konami_code = decode('VXAgVXAgRG93biBEb3duIExlZnQgUmlnaHQgTGVmdCBSaWdodCBiIGE=').split(' ')
love_message = decode('VG9pIHlldSBtb3Qgbmd1b2kgdGVuIE4=')

def extract_number_from_filename(filename):
    match = re.search(r"\d+(\.\d+)?", filename)
    if match:
        return float(match.group())
    return float('inf')

def display_txt_files():
    txt_files = [file for file in os.listdir('Vol') if file.endswith('.txt')]
    if not txt_files:
        messagebox.showinfo("Thông báo", "Không có file .txt trong thư mục.")
        return

    txt_files = sorted(txt_files, key=extract_number_from_filename)
    files_list.delete(0, tk.END)
    for txt_file in txt_files:
        filename = os.path.splitext(txt_file)[0]  # Loại bỏ đuôi .txt
        files_list.insert(tk.END, filename)

def load_selected_file(event=None):
    global current_filename
    selected_index = files_list.curselection()
    if not selected_index:
        return

    filename = files_list.get(selected_index)
    try:
        with open(f"Vol/{filename}.txt", 'r', encoding='utf-8') as file:  # Thêm mã hóa 'utf-8' khi đọc file
            content = file.read()
        text_editor.delete(1.0, tk.END)
        text_editor.insert(tk.END, content)
        current_filename = filename
    except FileNotFoundError:
        messagebox.showinfo("Thông báo", "File không tồn tại.")

def save_current_file(event=None):
    global current_filename
    if not current_filename:
        messagebox.showinfo("Thông báo", "Hãy chọn một file hoặc tạo mới trước khi lưu.")
        return

    new_content = text_editor.get(1.0, tk.END)
    with open(f"Vol/{current_filename}.txt", 'w', encoding='utf-8') as file:  # Thay đổi mã hóa thành 'utf-8'
        file.write(new_content)
    messagebox.showinfo("Thông báo", f"Nội dung của {current_filename}.txt đã được lưu.")
    display_txt_files()  # Hiển thị danh sách file lại sau khi lưu

def create_new_txt_file():
    global current_filename
    new_filename = simpledialog.askstring("Tạo file mới", "Nhập tên file mới:")
    if new_filename is not None and new_filename.strip():
        filename = f"Vol/{new_filename}"
        with open(f"{filename}.txt", 'x') as file:
            file.write("")
        current_filename = new_filename
        messagebox.showinfo("Thông báo", f"File {filename}.txt đã được tạo.")
        display_txt_files()

def delete_selected_file():
    selected_index = files_list.curselection()
    if not selected_index:
        messagebox.showinfo("Thông báo", "Hãy chọn một file để xóa.")
        return

    filename = files_list.get(selected_index)
    if messagebox.askokcancel("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa {filename}.txt?"):
        try:
            os.remove(f"Vol/{filename}.txt")
            messagebox.showinfo("Thông báo", f"File {filename}.txt đã được xóa.")
            display_txt_files()
        except FileNotFoundError:
            messagebox.showinfo("Thông báo", "File không tồn tại.")
        except Exception as e:
            messagebox.showinfo("Thông báo", f"Lỗi xóa file: {e}")

def on_key(event):
    global konami_code_sequence

    key = event.keysym
    konami_code_sequence.append(key)
    if konami_code_sequence[-len(konami_code):] == konami_code:
        messagebox.showinfo("Thông báo", love_message)
        konami_code_sequence = []  # Reset the sequence after showing the message

def set_cursor_white(event=None):
    # Đặt màu trắng cho con trỏ
    text_editor.tag_configure("white_cursor", background="white")
    text_editor.config(insertbackground="white")

def set_line_spacing(event=None):
    # Đặt line spacing
    text_editor.tag_configure("line_space", spacing=15)

def rename_selected_file():
    global current_filename
    selected_index = files_list.curselection()
    if not selected_index:
        messagebox.showinfo("Thông báo", "Hãy chọn một file để đổi tên.")
        return

    old_filename = files_list.get(selected_index)
    new_filename = simpledialog.askstring("Đổi tên file", "Nhập tên mới:", initialvalue=old_filename)
    if new_filename is not None and new_filename.strip():
        old_file_path = f"Vol/{old_filename}.txt"
        new_file_path = f"Vol/{new_filename}.txt"

        try:
            os.rename(old_file_path, new_file_path)
            messagebox.showinfo("Thông báo", f"File {old_filename}.txt đã được đổi tên thành {new_filename}.txt.")
            current_filename = new_filename
            display_txt_files()
        except FileExistsError:
            messagebox.showinfo("Thông báo", f"File {new_filename}.txt đã tồn tại. Vui lòng chọn tên khác.")
        except FileNotFoundError:
            messagebox.showinfo("Thông báo", "File không tồn tại.")
        except Exception as e:
            messagebox.showinfo("Thông báo", f"Lỗi đổi tên file: {e}")

def refresh_files_list():
    display_txt_files()

def button_hover(event):
    event.widget.config(background="#1e90ff")

def button_leave(event):
    event.widget.config(background="#272727")
    
root = tk.Tk()
root.title("Status Sheep")
root.geometry("800x600")
# Tạo theme và font
style = ttk.Style(root)
style.theme_use("clam")  # Chọn theme, có thể thay bằng "clam", "alt", "default", "classic", "vista", "xpnative"
style.configure(".", font=('Segoe UI', 12), foreground='white', background='#272727')  # Cấu hình font và màu cho tất cả các widget

frame_top = ttk.Frame(root)
frame_top.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

files_list = tk.Listbox(frame_top, width=40, height=10, selectmode=tk.SINGLE, font=('Segoe UI', 12), foreground='white', background='#272727')
files_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_buttons = ttk.Frame(frame_top)
frame_buttons.pack(side=tk.LEFT, padx=10)

btn_new = ttk.Button(frame_buttons, text="New File", command=create_new_txt_file, style='my.TButton')
btn_new.pack(pady=5)
btn_new.bind("<Enter>", button_hover)
btn_new.bind("<Leave>", button_leave)

btn_delete = ttk.Button(frame_buttons, text="Delete", command=delete_selected_file, style='my.TButton')
btn_delete.pack(pady=5)
btn_delete.bind("<Enter>", button_hover)
btn_delete.bind("<Leave>", button_leave)

btn_rename = ttk.Button(frame_buttons, text="Rename", command=rename_selected_file, style='my.TButton')
btn_rename.pack(pady=5)
btn_rename.bind("<Enter>", button_hover)
btn_rename.bind("<Leave>", button_leave)

btn_refresh = ttk.Button(frame_buttons, text="Refresh", command=refresh_files_list, style='my.TButton')
btn_refresh.pack(pady=5)
btn_refresh.bind("<Enter>", button_hover)
btn_refresh.bind("<Leave>", button_leave)

# Định nghĩa style cho button
style.configure('my.TButton', font=('Segoe UI', 12), foreground='black', background='#1e90ff', padding=10)

frame_bottom = ttk.Frame(root)
frame_bottom.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

text_editor = tk.Text(frame_bottom, wrap=tk.WORD, font=('Segoe UI', 12), foreground='white', background='#272727')
text_editor.pack(fill=tk.BOTH, expand=True)

text_editor.bind("<Control-s>", save_current_file)  # Bắt sự kiện gõ Ctrl + S để lưu

files_list.bind("<ButtonRelease-1>", load_selected_file)  # Binding sự kiện click vào item trong list để hiển thị nội dung

root.bind("<FocusIn>", set_cursor_white)
root.bind("<Key>", on_key)
root.bind("<Control-l>", set_line_spacing)
display_txt_files()  # Hiển thị danh sách file khi chạy chương trình
root.bind("<Key>", on_key)
root.mainloop()
