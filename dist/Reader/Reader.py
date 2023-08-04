import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import re
import base64
from solver import Solver
import pygame
import threading

current_filename = ""
konami_code_sequence = []
code_reverse = []
custom_event_sequence = []
secret = ["Vol. 16","Vol. 17","Vol. End"]
secret_dict = {
    "Vol. 16": False,
    "Vol. 17": False,
    "Vol. End": False,
}
konami_code = Solver("Vm0wd2QyUXlVWGxXYTFwUFZsZG9WVll3Wkc5V1JteDBZM3BHYWxKc1NsWlZNakExVjBaYWRHVkliRmhoTVVwVVZtMXplRll5VGtsaFJscE9ZbTFvVVZadGNFZFRNazE0V2toR1UySklRazlWYWtwdlZGWmtXR1JIZEZSTlZUVkpWbTEwVjFWdFNrbFJiVGxWVm14d00xWldXbUZqTVZaeVdrWm9hVlpyV1RGV1ZFb3dWakZrU0ZOcmFHaFNlbXhXVm01d1IyUnNXWGhYYlVaWFZtczFlRlpYZUZOVWJGbDRVMnh3VjFaNlJYZFpla1poVjBaT2NtRkhhRlJTVlhCWlYxWlNSMlF5UmtkWGJrcFlZa2hDYzFacVFURlNNV1J5VjIxMFZXSlZjRWRaTUZaM1ZqRmFSbUl6WkZwaGExcFRXbFZhYTFkWFNraGhSazVwVW01Q1dWWXhaRFJpTVZWNVVtdGthbEpYVWxsWmJGWmhZMVpzY2xkdVpFNVNia0pIVmpJeE1GWlhTbFpXYWxwV1ZqTm9NMVpxU2t0VFJsWlpXa1prVjFKV2NGbFhhMVpoVkRKT2MxcElTbEJXYlZKeldXeG9iMWRzV1hoWGJYUk9VakZHTkZZeWRHdGhiRXBZWVVoT1ZrMUhVbFJXYTFwelkyeGtjbVJIZUZkaVNFSktWa1phYWs1V1dYZE5WbVJwVWtad1lWWnNXbUZOTVZweFVteHdiR0pWV2toV1J6RkhWVEZLVjJORlZsZGlSMUV3VlZSR1lWWnJNVlpXYXpWVFVrVkZOUT09").getCode().split(' ')
love_message = Solver("Vm0wd2QyUXlVWGxXYTFwT1ZsZG9WRmx0ZEhkVlJscHpXa1pPYWxKc1NsWlZNbkJUVjBaS2RHVkliRmhoTWsweFZqQmFTMlJIVmtkaVIwWlRWakZLU1ZadGRGWmxSbGw0V2toR1UySklRazlWYlhoM1pWWmFjbGt6YUZSTlZUVllWVzAxUzFsV1NuUlZiRkpWVmtWYVRGWldXbXRXTVZaeVdrWndWMDFWY0VoV1JFWmhWakZrU0ZOcmFGWmlhMHBZV1ZSR2QyRkdiSEZTYlhSWFRWWndNRlZ0ZUd0aFZscHlWMVJDVjJFeVVUQlpla1p6VmpGT2RWVnRhRlJTVlhCWVYxWmtNRkl3TlVkVmJGWlRZa2hDYzFacVFURlNNV1J5VjIxR1ZXSlZWalpWVjNCaFZqRmFkRlZVUWxkaGExcFVXWHBHVDJOc1duTlRiR1JUVFRBd01RPT0=").getCode()
next_message = Solver("Vm0wd2QyUXlWa1pOVldoVFlteEtXRmxVU205V1JsbDNXa1pPVlUxV2NEQlVWbU0xVmpGYWMySkVUbGhoTVVwVVdWWlZlRll4VG5OaVJsWlhZa2hDVVZacVNqUlpWMDE1VTJ0V1ZXSkhhRzlVVmxaM1VsWmtWMWR0ZEZSTlZUVklWbTAxVDFkSFNraFZiRkpWVmtWd2RscFdXbXRXTVZaeVdrWndWMDFWY0ZsV1Z6RTBWakZWZVZOclpHcFNiV2hvVm1wT2IyRkdXbGRYYlhSWFRWZFNlbFl5TVRCVWJVcEdWMVJDVjFaRmEzaFdWRVpTWlVaa1dWcEdhR2xTYTNCdlZtMXdUMVV4U1hoalJscFlZbGhTV0ZadGRHRmxiR1J5V2toa1ZXSkdjRlpXYlhoelZqSktWVkZZYUZkaGExcHlWV3BHYTJOc1duTlRiR1JUVFRBd01RPT0=").getCode()
reverse = Solver("YSBiIFJpZ2h0IExlZnQgUmlnaHQgTGVmdCBEb3duIERvd24gVXAgVXA=").getCode().split(" ")
final = Solver("biBnIG8gc3BhY2UgbiBoIGEgdCBzcGFjZSBuIGcgaCBp").getCode().split(" ")
final_second = Solver("TiBnIG8gc3BhY2UgTiBoIGEgdCBzcGFjZSBOIGcgaCBp").getCode().split(" ")
final_message = Solver("V2VsbCwgY+G6rXUgxJHDoyBjaGnhur9uIHRo4bqvbmcgdHJvbmcgbMOybmcgdOG7myBy4buTaS4gQ8OybiBnw6wgbuG7r2EgbcOgIGPhuq11IGNoxrBhIGJp4bq/dCB24buBIHThu5sgbuG7r2Ega2jDtG5nIG5o4buJPyDEkMOieSBsw6AgXCJWb2wuIEVuZFwiIC0gYuG7qWMgdGjGsCBjdeG7kWkgY8O5bmcgY+G7p2EgdOG7mywgaMOjeSDEkeG7jWMgbsOzIHRo4bqtdCBrxKkgbmjDqSwgdsOsIHNhdSBraGkgY+G6rXUgdOG6r3QgY2jGsMahbmcgdHLDrG5oLCB04bqldCBj4bqjIGPDoWMgdGjGsCDhu58gxJHDonkgdHJvbmcgbsOgeSBz4bq9IGLhu4sgeMOzYSBo4bq/dCDEkeG6pXkuLi4gRMO5IHNhbyB0aMOsLCDEkcOieSBsw6AgcGjhuqduIHRoxrDhu59uZyBj4bunYSBj4bqtdSwgY2jDumMgbeG7q25nIG5ow6kh").getCode()
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
        filename = os.path.splitext(txt_file)[0]  
        if (filename in secret) == False:
            files_list.insert(tk.END, filename)
        else:
            if (secret_dict[filename]):
                files_list.insert(tk.END, filename)

def check_image(filename):
    image_path = f'Vol/assets/{filename}.jpg'
    if os.path.exists(image_path):
        return image_path
    else:
        return None

def load_selected_file(event=None):
    global current_filename
    selected_index = files_list.curselection()
    if not selected_index:
        return
    filename = files_list.get(selected_index)
    try:
        with open(f"Vol/{filename}.txt", 'r', encoding='utf-8') as file:
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
    with open(f"Vol/{current_filename}.txt", 'w', encoding='utf-8') as file:  
        file.write(new_content)
    messagebox.showinfo("Thông báo", f"Nội dung của {current_filename}.txt đã được lưu.")
    display_txt_files()  

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
        threading.Thread(target=love_message).start()
        messagebox.showinfo("Thông báo", love_message)
        secret_dict["Vol. 16"] = True
        display_txt_files()
        konami_code_sequence = []  
def on_reverse(event):
    global code_reverse 
    key = event.keysym
    code_reverse.append(key)
    if code_reverse[-len(reverse):] == reverse:
        threading.Thread(target=love_message).start()
        messagebox.showinfo("Thông báo", next_message)
        secret_dict["Vol. 17"] = True
        display_txt_files()
        code_reverse = [] 
def on_final_event(event):
    global custom_event_sequence
    key = event.keysym
    custom_event_sequence.append(key)
    if custom_event_sequence[-len(final):] == final or custom_event_sequence[-len(final_second):] == final_second:
        pygame.mixer.init()
        music_file = "MzEwNwo=.mp3"  
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

        messagebox.showinfo("Thông báo", "Well, cậu đã chiến thắng trong lòng tớ rồi. Còn gì nữa mà cậu chưa biết về tớ nữa không nhỉ? Đây là \"Vol. End\" - bức thư cuối cùng của tớ, hãy đọc nó thật kĩ nhé, vì sau khi cậu tắt chương trình, tất cả các thư ở đây trong này sẽ bị xóa hết đấy... Dù sao thì, đây là phần thưởng của cậu, chúc mừng nhé!")
        secret_dict["Vol. End"] = True
        display_txt_files()

        custom_event_sequence = []
        root.protocol("WM_DELETE_WINDOW", on_closing)


def set_cursor_white(event=None):
    # Đặt màu trắng cho con trỏ
    text_editor.tag_configure("white_cursor", background="white")
    text_editor.config(insertbackground="white")

def set_line_spacing(event=None):

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

def on_closing():
    # Xóa tất cả các file trong folder "Vol"
    folder_path = "Vol"  # Thay đổi đường dẫn đến folder "Vol" của bạn
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print("Đã xảy ra lỗi khi xóa file:", e)
    root.destroy()

def refresh_files_list():
    display_txt_files()

def button_hover(event):
    event.widget.config(background="#1e90ff")

def button_leave(event):
    event.widget.config(background="#272727")


root = tk.Tk()
root.title("Status Sheep")
icon_image = tk.PhotoImage(file="icon.gif")
root.wm_iconphoto(True, icon_image)
root.geometry("800x600")
# Tạo theme và font
style = ttk.Style(root)
style.theme_use("clam")  
style.configure(".", font=('Segoe UI', 12), foreground='white', background='#272727')  

frame_top = ttk.Frame(root,padding=(20, 20, 20, 20), borderwidth=0)
frame_top.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

files_list = tk.Listbox(frame_top, width=40, height=10, selectmode=tk.SINGLE, font=('Segoe UI', 12), foreground='white', background='#272727',borderwidth=0, selectborderwidth=0)
files_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


frame_buttons = ttk.Frame(frame_top)
frame_buttons.pack(side=tk.LEFT, padx=10)

btn_new = ttk.Button(frame_buttons, text="New File", command=create_new_txt_file, style='my.TButton')
btn_new.pack(pady=5)



btn_delete = ttk.Button(frame_buttons, text="Delete", command=delete_selected_file, style='my.TButton')
btn_delete.pack(pady=5)



btn_rename = ttk.Button(frame_buttons, text="Rename", command=rename_selected_file, style='my.TButton')
btn_rename.pack(pady=5)



btn_refresh = ttk.Button(frame_buttons, text="Refresh", command=refresh_files_list, style='my.TButton')
btn_refresh.pack(pady=5)



style.configure('my.TButton', font=('Segoe UI', 12), foreground='black', background='#1e90ff', padding=10)

frame_bottom = ttk.Frame(root,padding=(20, 20, 20, 20))
frame_bottom.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



frame_bottom.configure(style="Custom.TFrame")
text_editor = tk.Text(frame_bottom, wrap=tk.WORD, font=('Segoe UI', 12), foreground='white', background='#272727',borderwidth=0)
text_editor.pack(fill=tk.BOTH, expand=True)

text_editor.bind("<Control-s>", save_current_file)  # Bắt sự kiện gõ Ctrl + S để lưu

files_list.bind("<ButtonRelease-1>", load_selected_file)  # Binding sự kiện click vào item trong list để hiển thị nội dung

root.bind("<FocusIn>", set_cursor_white)

root.bind("<Control-l>", set_line_spacing)
display_txt_files()  # Hiển thị danh sách file khi chạy chương trình
root.bind("<Key>", on_key)
root.bind("<Key>", on_reverse, add="+")
root.bind("<Key>", on_final_event,add="+")


root.mainloop()
