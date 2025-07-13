# EN

# Cookie Extractor - Browser Cookie Extraction Tool cooldeep

![Cookie Extractor Banner](https://img.shields.io/badge/Project-Cookie%20Extractor-blueviolet)
![Language](https://img.shields.io/badge/Language-Python-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ⚠️ IMPORTANT NOTICE

**This tool is created for educational and research purposes only. Any unauthorized use of this code is strictly prohibited. The author takes no responsibility for any misuse of this tool.**

**This codebase is currently in a testing phase and may not be stable or bug-free. Please use it with caution and responsibility.**

## 📝 Description

Cookie Extractor is a Python tool that allows extracting (exporting) stored cookies from various popular web browsers on Windows operating systems. This tool is designed to aid in the analysis and examination of cookies for academic or development purposes, by decrypting and saving them into Netscape HTTP Cookie File (`.txt`) format.

## ✨ Features

* Supports cookie extraction from the following browsers:
    * Cốc Cốc
    * Google Chrome
    * Microsoft Edge
    * Brave
    * Opera
    * Yandex Browser
* Automatically detects and processes multiple user Profiles (e.g., `Default`, `Profile 1`, etc.).
* Decrypts cookies encrypted with DPAPI and AES-GCM (depending on the browser's cookie version).
* Saves extracted cookies into separate `.txt` files for each browser and profile, following the Netscape HTTP Cookie File format.
* Includes basic error handling for issues like locked cookie database files.
* Provides a summary of the extraction process.

## 🚀 Installation and Usage

### Requirements

* Python 3.x
* Python libraries: `pywin32`, `cryptography`, `psutil`

### Install Libraries

You can install the necessary libraries using `pip`:

```bash
pip install pywin32 cryptography psutil
````

### How to Run

1.  **Download:** Download the `cookies.py` file to your computer.

2.  **Close Browsers:** **Crucially important\!** For the tool to access the cookie database, you must **close all listed browsers** before running the script.

3.  **Run Script:** Open Command Prompt (CMD) or PowerShell, navigate to the directory containing `cookies.py`, and run the script:

    ```bash
    python cookies.py
    ```

4.  The script will prompt you to press `Enter` to start the process.

5.  Upon completion, the extracted cookies will be saved in the `cookies` directory (automatically created in the same directory as the script), organized by browser and profile.

## 📁 Output Directory Structure

```
.
├── cookies.py
└── cookies/
    ├── coc_coc/
    │   └── coc-coc_Default_cookies.txt
    ├── chrome/
    │   ├── chrome_Default_cookies.txt
    │   └── chrome_Profile_1_cookies.txt
    ├── edge/
    │   └── edge_Default_cookies.txt
    └── ...
```

## 📜 License

This codebase is released under the MIT License. See the `LICENSE` file for more details.

## 📞 Contact

If you have any questions or suggestions, please feel free to contact:

  * **Email:** danghuutruong0@gmail.com
  * **GitHub:** [danghuutruong](https://github.com/danghuutruong/cooldeep/) (Refer to the original project if applicable)

-----

Thank you for using Cookie Extractor\!

```
```

# VN

# Cookie Extractor - Công cụ Trích Xuất Cookie Trình Duyệt cooldeep

![Cookie Extractor Banner](https://img.shields.io/badge/Project-Cookie%20Extractor-blueviolet)
![Language](https://img.shields.io/badge/Language-Python-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ⚠️ CHÚ Ý QUAN TRỌNG

**Công cụ này được tạo ra với mục đích giáo dục và nghiên cứu. Việc sử dụng mã nguồn này vào bất kỳ hoạt động trái phép nào đều bị nghiêm cấm. Tác giả không chịu bất kỳ trách nhiệm nào về việc sử dụng sai mục đích của công cụ này.**

**Mã nguồn này hiện đang trong quá trình thử nghiệm (testing phase) và có thể chưa ổn định hoặc có lỗi. Vui lòng sử dụng một cách cẩn thận và có trách nhiệm.**

## 📝 Mô Tả

Cookie Extractor là một công cụ Python cho phép trích xuất (export) các cookie đã lưu trữ từ nhiều trình duyệt web phổ biến trên hệ điều hành Windows. Công cụ này được thiết kế để hỗ trợ việc phân tích và kiểm tra các cookie cho mục đích học tập hoặc phát triển, bằng cách giải mã và lưu trữ chúng vào các file định dạng Netscape HTTP Cookie File (`.txt`).

## ✨ Tính Năng

* Hỗ trợ trích xuất cookie từ các trình duyệt:
    * Cốc Cốc
    * Google Chrome
    * Microsoft Edge
    * Brave
    * Opera
    * Yandex Browser
* Tự động phát hiện và xử lý nhiều Profile người dùng (ví dụ: `Default`, `Profile 1`, v.v.).
* Giải mã cookie được mã hóa bằng DPAPI và AES-GCM (tùy thuộc vào phiên bản cookie của trình duyệt).
* Lưu trữ cookie vào các file `.txt` riêng biệt cho mỗi trình duyệt và profile, theo định dạng Netscape HTTP Cookie File.
* Xử lý lỗi cơ bản khi không thể sao chép cơ sở dữ liệu cookie do file bị khóa.
* Hiển thị tóm tắt quá trình trích xuất.

## 🚀 Cài Đặt và Sử Dụng

### Yêu cầu

* Python 3.x
* Các thư viện Python: `pywin32`, `cryptography`, `psutil`

### Cài đặt thư viện

Bạn có thể cài đặt các thư viện cần thiết bằng `pip`:

```bash
pip install pywin32 cryptography psutil
````

### Cách chạy

1.  **Tải xuống:** Tải file `cookies.py` về máy tính của bạn.

2.  **Đóng trình duyệt:** **Rất quan trọng\!** Để công cụ có thể truy cập vào cơ sở dữ liệu cookie, bạn cần **đóng tất cả các trình duyệt** được liệt kê ở trên trước khi chạy.

3.  **Chạy script:** Mở Command Prompt (CMD) hoặc PowerShell, điều hướng đến thư mục chứa file `cookies.py` và chạy script:

    ```bash
    python cookies.py
    ```

4.  Script sẽ yêu cầu bạn nhấn `Enter` để bắt đầu quá trình.

5.  Sau khi hoàn thành, các cookie đã trích xuất sẽ được lưu trong thư mục `cookies` (được tạo tự động trong cùng thư mục với script), được sắp xếp theo trình duyệt và profile.

## 📁 Cấu trúc thư mục đầu ra

```
.
├── cookies.py
└── cookies/
    ├── coc_coc/
    │   └── coc-coc_Default_cookies.txt
    ├── chrome/
    │   ├── chrome_Default_cookies.txt
    │   └── chrome_Profile_1_cookies.txt
    ├── edge/
    │   └── edge_Default_cookies.txt
    └── ...
```

## 📜 Giấy phép

Mã nguồn này được phát hành theo Giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ:

  * **Email:** danghuutruong0@gmail.com
  * **GitHub:** [danghuutruong](https://github.com/danghuutruong/cooldeep/) (Tham khảo dự án gốc nếu có)

-----

Cảm ơn bạn đã sử dụng Cookie Extractor\!

```
```
