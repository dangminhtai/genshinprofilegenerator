import os
import tkinter as tk
from tkinter import Tk, Button, Frame, Scrollbar
from PIL import Image, ImageTk, ImageDraw,ImageFont

# Hàm resize ảnh theo kích thước cố định
def resize_img_to_fit(x, target_width, target_height):
    return x.resize((target_width, target_height), Image.Resampling.LANCZOS)

def resize_img(x, scale):
    width, height = x.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    return x.resize((new_width, new_height))
# Hàm tạo góc bo tròn cho ảnh
def round_corners(image, radius):
    width, height = image.size
    mask = Image.new('L', (width, height), 255)  # Tạo mask trắng
    draw = ImageDraw.Draw(mask)
    draw.rectangle([(0, 0), (width, height)], fill=255)
    draw.pieslice([(-radius, -radius), (radius * 2, radius * 2)], 180, 270, fill=0)
    draw.pieslice([(width - radius * 2, -radius), (width, radius * 2)], 270, 360, fill=0)
    draw.pieslice([(-radius, height - radius * 2), (radius * 2, height)], 90, 180, fill=0)
    draw.pieslice([(width - radius * 2, height - radius * 2), (width, height)], 0, 90, fill=0)
    result = image.convert("RGBA")
    result.putalpha(mask)
    return result

# Tạo cửa sổ giao diện
charater=input("Nhập avatar cho nhân vật bạn muốn hiển thị: ")
nick_name=input("Nhập nick-name bạn muốn hiển thị: ")
ad_rank=input("Nhập hạng mạo hiểm muốn hiển thị: ")
world_lv=input("Nhập cấp thế giới muốn hiển thị: ")
uid=input("Nhập UID bạn muốn hiển thị: ")
exp_love=input("Nhập số nhân vật có độ ưu thích đã đầy mà bạn muốn: ")
signature=input("Nhập chữ ký bạn muốn hiển thị: ")
achivement=input("Nhập thành tựu bạn muốn hiển thị: ")
abyss=input("Nhập khiêu chiến la hoàn thâm cảnh: ")
print("Hãy chọn danh thiếp và xem kết quả.")
root = tk.Tk()
root.state("zoomed")
root.title("Profile tự tạo")
# root.iconbitmap("logo.ico")
window_width = 1000
window_height = 600
root.geometry(f"{window_width}x{window_height}")

# Tạo khung chính
main_frame = Frame(root)
main_frame.pack(fill="both", expand=True)

# Thêm canvas và thanh cuộn
canvas = tk.Canvas(main_frame)
scrollbar_y = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar_x = Scrollbar(main_frame, orient="horizontal", command=canvas.xview)

scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Frame chứa nội dung
content_frame = Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Biến toàn cục để lưu trữ các đối tượng ảnh
images_cache = {}
def on_click(image_path):
    # Xóa tất cả nội dung trong canvas, nhưng không phá hủy nó
    if canvas.winfo_exists():
        canvas.delete("all")
    else:
        print("Canvas đã bị phá hủy!")
    # root.state('zoomed')
    root.geometry("600x800")
    frame_path = "profile1.png"  # Cố định
    frame_path = "profile1.png"  # cố định
    mid_avt = f"Avatar/{charater}_Avatar.png"
    
    image_path =image_path.replace("\\", "/")
    # Mở các hình ảnh
    frame_image = Image.open(frame_path)
    frame_avt = Image.open(mid_avt)
    avt_photo = ImageTk.PhotoImage(resize_img(frame_avt, 0.34))
    frame_image = resize_img(frame_image, 0.8)  
    frame_photo = ImageTk.PhotoImage(frame_image)
    image = Image.open(image_path)
    image_photo = ImageTk.PhotoImage(resize_img(image, 0.68))
    # Hiển thị ảnh 1.png (không thay đổi kích thước)
    canvas.create_image(0, 12, anchor="nw", image=image_photo)
    # Hiển thị ảnh đã resize (profile_edited_2.png) chồng lên
    canvas.create_image(0, 0, anchor="nw", image=frame_photo)
    canvas.create_image(241, 80, anchor="nw", image=avt_photo)

    # Chèn text "Tamida" với viền xám
    text_image = Image.new("RGBA", (1000,800), (255, 255, 255, 0))  # Ảnh trong suốt
    draw = ImageDraw.Draw(text_image)

    # Tạo một hàm để căn giữa văn bản
    def create_shadow_text(text_content,size,pdx,pdy,fill_color):
        # Sử dụng textbbox để tính toán chiều rộng và chiều cao của văn bản
        def using_font(size):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(base_dir, "ja-jp.ttf")
            if not os.path.exists(font_path):
                return ImageFont.load_default()
            else:
                return ImageFont.truetype(font_path, size=size)
        font = using_font(size)  # Gọi font với kích thước 40
        bbox = draw.textbbox((0, 0), text_content, font=font)  # Sử dụng font đã tạo
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Tính tọa độ để căn giữa
        text_x = (pdx - text_width) // 2  
        text_y = (pdy - text_height) // 2 

        # Vẽ viền bóng nhỏ với màu xám
        shadow_color = (50, 50, 50, 100)  # Màu xám nhạt với alpha
        offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Các điểm lệch nhẹ tạo viền nhỏ

        for offset in offsets:
            draw.text((text_x + offset[0], text_y + offset[1]), text_content, font=font, fill=shadow_color)

        # Vẽ chữ chính với màu trắng
        draw.text((text_x, text_y), text_content, font=font, fill=fill_color)
    # Hàm tạo chữ bình thường không có shadow và không căn giữa
    def create_normal_text(text_content, size, x, y, fill_color, max_width=500):
        # Sử dụng textbbox để tính toán font
        def using_font(size):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(base_dir, "ja-jp.ttf")
            if not os.path.exists(font_path):
                return ImageFont.load_default()
            else:
                return ImageFont.truetype(font_path, size=size)
        
        font = using_font(size)  # Gọi font với kích thước
        words = text_content.split()  # Tách văn bản thành các từ
        lines = []  # Dãy chứa các dòng đã được chia
        current_line = []  # Dãy chứa các từ của dòng hiện tại
        current_line_width = 0  # Chiều dài hiện tại của dòng

        # Chia văn bản thành các dòng sao cho mỗi dòng không vượt quá max_width
        for word in words:
            word_width = font.getbbox(word)[2] - font.getbbox(word)[0]  # Tính chiều rộng từ
            # Nếu thêm từ này vào dòng hiện tại mà không vượt quá chiều rộng, thêm từ vào dòng
            if current_line_width + word_width + (len(current_line) - 1) * font.getbbox(' ')[2] <= max_width:
                current_line.append(word)
                current_line_width += word_width
            else:
                # Nếu vượt quá chiều rộng, lưu dòng hiện tại và bắt đầu dòng mới
                lines.append(" ".join(current_line))
                current_line = [word]
                current_line_width = word_width

        # Thêm dòng cuối cùng
        if current_line:
            lines.append(" ".join(current_line))

        # Vẽ từng dòng lên canvas
        for i, line in enumerate(lines):
            draw.text((x, y + i * size), line, font=font, fill=fill_color)

    def create_right_aligned_text(text_content, size, x, y, fill_color, max_width=500):
        # Sử dụng textbbox để tính toán font
        def using_font(size):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(base_dir, "ja-jp.ttf")
            if not os.path.exists(font_path):
                return ImageFont.load_default()
            else:
                return ImageFont.truetype(font_path, size=size)
        
        font = using_font(size)  # Gọi font với kích thước
        words = text_content.split()  # Tách văn bản thành các từ
        lines = []  # Dãy chứa các dòng đã được chia
        current_line = []  # Dãy chứa các từ của dòng hiện tại
        current_line_width = 0  # Chiều dài hiện tại của dòng

        # Chia văn bản thành các dòng sao cho mỗi dòng không vượt quá max_width
        for word in words:
            word_width = font.getbbox(word)[2] - font.getbbox(word)[0]  # Tính chiều rộng từ
            # Nếu thêm từ này vào dòng hiện tại mà không vượt quá chiều rộng, thêm từ vào dòng
            if current_line_width + word_width + (len(current_line) - 1) * font.getbbox(' ')[2] <= max_width:
                current_line.append(word)
                current_line_width += word_width
            else:
                # Nếu vượt quá chiều rộng, lưu dòng hiện tại và bắt đầu dòng mới
                lines.append(" ".join(current_line))
                current_line = [word]
                current_line_width = word_width
        if current_line:
            lines.append(" ".join(current_line))
        for i, line in enumerate(lines):
            line_width = font.getbbox(line)[2] - font.getbbox(line)[0]  # Tính chiều rộng của dòng
            text_x = x - line_width  # Căn phải: bắt đầu từ x - chiều rộng của dòng
            draw.text((text_x, y + i * size), line, font=font, fill=fill_color)
    #Tạo văn bản
    create_shadow_text(nick_name,40,560,450,"white")
    create_right_aligned_text(ad_rank,22,525,308,"#fdfbfc")
    create_right_aligned_text(world_lv,22,525,361,"#fdfbfc")
    create_normal_text(f"UID {uid}",20,200,40,"#f9f6fc")
    create_normal_text(signature,19,45,410,"#7d6e5f")
    create_right_aligned_text(achivement,20,530,535,"#7d6e5f")
    create_right_aligned_text(exp_love,20,530,590,"#7d6e5f")
    create_right_aligned_text(abyss,20,500,638,"#7d6e5f")
    create_right_aligned_text("Not yet attempted",19,530,689,"#dcccb7")
    # Chuyển đổi ảnh rỗng chứa chữ thành PhotoImage và hiển thị trên canvas
    text_photo = ImageTk.PhotoImage(text_image)
    canvas.create_image(0, 0, anchor="nw", image=text_photo)
    canvas.image_refs = [image_photo, frame_photo, avt_photo, text_photo]
    canvas.update()  # Cập nhật canvas nếu cần thiết


    
def create_button_img(parent, frame_path, image_path, scale=1.0, row=0, column=0):
    # Load và resize ảnh frame.png
    frame_image = Image.open(frame_path)
    frame_width, frame_height = frame_image.size
    new_frame_width = int(frame_width * scale)
    new_frame_height = int(frame_height * scale)
    frame_image = frame_image.resize((new_frame_width, new_frame_height), Image.Resampling.LANCZOS)
    frame_photo = ImageTk.PhotoImage(resize_img(frame_image, scale))

    # Lưu frame_photo vào cache
    images_cache[f"frame_photo_{row}_{column}"] = frame_photo

    # Load và resize ảnh
    image = Image.open(image_path)
    resized_image = resize_img_to_fit(image, new_frame_width - 5, new_frame_height - 5)
    rounded_image = round_corners(resize_img(resized_image, 1.07 * scale), int(2 * scale))
    resized_photo = ImageTk.PhotoImage(rounded_image)

    # Lưu resized_photo vào cache
    images_cache[f"resized_photo_{row}_{column}"] = resized_photo
    # Tạo một ảnh kết hợp giữa frame và ảnh
    combined_image = Image.new("RGBA", (new_frame_width, new_frame_height))
    # Đảm bảo ảnh có định dạng RGBA
    if resized_image.mode != 'RGBA':
        resized_image = resized_image.convert('RGBA')

    if rounded_image.mode != 'RGBA':
        rounded_image = rounded_image.convert('RGBA')

# Đảm bảo kích thước của ảnh và mặt nạ khớp nhau
    if resized_image.size != rounded_image.size:
        resized_image = resized_image.resize(rounded_image.size)

# Sử dụng mặt nạ từ rounded_image

    combined_image.paste(frame_image, (0, 0))
    combined_image.paste(resized_image, (6, 5), mask=rounded_image.convert("RGBA").split()[3])

    combined_photo = ImageTk.PhotoImage(combined_image)

    # Tạo nút Button với ảnh kết hợp
    button = Button(parent, image=combined_photo, bd=0, highlightthickness=0, command=lambda: on_click(image_path))
    button.grid(row=row, column=column, padx=10, pady=10)
    # Lưu ảnh kết hợp vào cache để tránh bị mất ảnh khi cập nhật giao diện
    images_cache[f"combined_photo_{row}_{column}"] = combined_photo

# Lấy danh sách ảnh chứa từ "Namecard" trong tất cả thư mục con
def get_image_files(folder, keyword="Namecard", extension=".png"):
    image_files = []
    for root, _, files in os.walk(folder):  # Duyệt qua tất cả các thư mục con
        for file in files:
            if keyword in file and file.endswith(extension):
                image_files.append(os.path.join(root, file))  # Thêm đường dẫn đầy đủ của file
    return image_files

# Thư mục gốc chứa ảnh
image_folder = "./"  # Thay đổi nếu thư mục khác
frame_path = "frame.png"

# Lấy danh sách tệp
image_files = get_image_files(image_folder)

# Số cột cố định và scale
fixed_columns = 8
scale = 0.9
# Bố trí ảnh vào content_frame
for i, image_file in enumerate(image_files):
    row = i // fixed_columns
    column = i % fixed_columns
    create_button_img(content_frame, frame_path, os.path.join(image_folder, image_file), scale=scale, row=row, column=column)

# Cập nhật kích thước scrollable
content_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))
# Bắt đầu vòng lặp giao diện
root.mainloop()
