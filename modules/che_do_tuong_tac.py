import time
import logging
from selenium.common.exceptions import WebDriverException
from .khoi_tao_trinh_duyet import khoi_tao

def chay_mot_profile(cau_hinh, nguoi_dung, khoa_thu_muc, proxy=None, chi_muc=0, tong_so=1):
    """Mở một trình duyệt cho một người dùng và giữ nó ở đó cho đến khi tiến trình chính ra lệnh đóng."""
    ma_nd = nguoi_dung.get('ma_dinh_danh', 'N/A')
    print(f"Đang mở trình duyệt cho người dùng: {ma_nd}")
    trinh_dieu_khien = None
    
    try:
        url_khoi_dau = cau_hinh.get("url_khoi_dau_tuong_tac", "https://google.com")
        trinh_dieu_khien = khoi_tao(cau_hinh, nguoi_dung, khoa_thu_muc, proxy, chi_muc, tong_so)
        trinh_dieu_khien.get(url_khoi_dau)
        
        while True:
            time.sleep(3600)

    except WebDriverException as e:
        if "no such window" in str(e).lower() or "target window is closed" in str(e).lower():
            logging.info(f"Cửa sổ của người dùng {ma_nd} đã bị đóng thủ công.")
        else:
            logging.info(f"Lỗi WebDriver khi xử lý người dùng {ma_nd}: {e}")
    except Exception as e:
        logging.info(f"Lỗi không xác định với người dùng {ma_nd}: {e}")
    finally:
        logging.info(f"Tiến trình cho người dùng {ma_nd} đã kết thúc.")