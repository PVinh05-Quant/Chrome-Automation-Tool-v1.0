import os
import logging
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from threading import Lock

from modules.quan_ly_man_hinh import sap_xep
from modules.chrome_utils import configure_chrome_options_with_extensions


def khoi_tao(cau_hinh, nguoi_dung, khoa_thu_muc, proxy=None, vi_tri_slot=0, so_luong_slot_hien_thi_toi_da=1):
    tuy_chon_chrome = Options()

    if cau_hinh.get("su_dung_profile_rieng", False):
        thu_muc_profile = os.path.join(cau_hinh["thu_muc_profiles"], f"profile_{nguoi_dung['ma_dinh_danh']}")
        with khoa_thu_muc:
            if not os.path.exists(thu_muc_profile):
                os.makedirs(thu_muc_profile)
        tuy_chon_chrome.add_argument(f"user-data-dir={thu_muc_profile}")

    seleniumwire_options = {}

    if cau_hinh.get("su_dung_proxy", False) and proxy:
        proxy_address = f"{proxy['dia_chi_ip']}:{proxy['cong']}"
        giao_thuc = proxy.get('giao_thuc', 'http')  # Mặc định là 'http'
        
        if 'ten_dang_nhap' in proxy and 'mat_khau' in proxy:
            seleniumwire_options['proxy'] = {
                'http': f"{giao_thuc}://{proxy['ten_dang_nhap']}:{proxy['mat_khau']}@{proxy_address}",
                'https': f"{giao_thuc}://{proxy['ten_dang_nhap']}:{proxy['mat_khau']}@{proxy_address}",
                'no_proxy': 'localhost,127.0.0.1'
            }
        else:
            seleniumwire_options['proxy'] = {
                'http': f"{giao_thuc}://{proxy_address}",
                'https': f"{giao_thuc}://{proxy_address}",
                'no_proxy': 'localhost,127.0.0.1'
            }

    tuy_chon_chrome.add_argument("--disable-blink-features=AutomationControlled")
    tuy_chon_chrome.add_experimental_option("excludeSwitches", ["enable-automation"])
    tuy_chon_chrome.add_experimental_option('useAutomationExtension', False)

    su_dung_che_do_an = cau_hinh.get("su_dung_che_do_an", False)

    cac_tuy_chon_chung = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        # "--disable-extensions", # Bỏ dòng này để tiện ích mở rộng có thể hoạt động
        "--log-level=3",
        "--disable-logging"
    ]
    for tuy_chon in cac_tuy_chon_chung:
        tuy_chon_chrome.add_argument(tuy_chon)

    tuy_chon_chrome.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    thu_muc_extensions = os.path.join(current_dir, 'extensions') 
    
    ds_tien_ich_mo_rong = []
    if os.path.exists(thu_muc_extensions):
        for ten_tep in os.listdir(thu_muc_extensions):
            if ten_tep.endswith('.crx'):
                ds_tien_ich_mo_rong.append(os.path.join(thu_muc_extensions, ten_tep))
    
    logging.info("Đang cấu hình ChromeOptions với các tiện ích mở rộng...")

    tuy_chon_chrome = configure_chrome_options_with_extensions(
        existing_options=tuy_chon_chrome,
        extension_paths=ds_tien_ich_mo_rong, 
        headless=su_dung_che_do_an
    )
    logging.info("Đã cấu hình ChromeOptions thành công.")


    logging.info("Đang cài đặt ChromeDriver...")
    dich_vu = Service(ChromeDriverManager().install(), log_output=open(os.devnull, 'w')) 
    logging.info("ChromeDriver đã sẵn sàng. Đang khởi tạo trình duyệt Chrome...")

    trinh_dieu_khien = webdriver.Chrome(service=dich_vu, options=tuy_chon_chrome, seleniumwire_options=seleniumwire_options)
    logging.info("Đã khởi tạo trình duyệt Chrome thành công.")

    if not su_dung_che_do_an:
        sap_xep(trinh_dieu_khien, cau_hinh, vi_tri_slot, so_luong_slot_hien_thi_toi_da)
        logging.info(f"Đã sắp xếp vị trí cửa sổ trình duyệt tại slot {vi_tri_slot}.")

    return trinh_dieu_khien