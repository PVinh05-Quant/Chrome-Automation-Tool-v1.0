import os
import time
import math
import sys
import logging

from multiprocessing import Process, Lock, Queue
from modules.thuc_thi_kich_ban import thuc_thi
from modules.che_do_tuong_tac import chay_mot_profile
from modules.kiem_tra_tai_nguyen import kiem_tra as kiem_tra_tai_nguyen
import modules.trinh_tai_du_lieu as tai_dl

logging.getLogger('seleniumwire').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def chay_che_do_tu_dong(cau_hinh, kich_ban, danh_sach_proxy, danh_sach_nguoi_dung, khoa_thu_muc):
    logging.info("Chế độ: TỰ ĐỘNG THEO KỊCH BẢN (Chạy song song 100%)")
    
    danh_sach_cho = list(danh_sach_nguoi_dung)
    
    so_luong_song_song_toi_da = cau_hinh.get("so_luong_tien_trinh_song_song", 1)
    so_cot_mong_muon = cau_hinh.get("sap_xep_cua_so", {}).get("so_cot_mong_muon", 0)
    so_luong_slot_hien_thi_toi_da = so_luong_song_song_toi_da if so_cot_mong_muon == 0 else so_cot_mong_muon * math.ceil(so_luong_song_song_toi_da / so_cot_mong_muon)

    cac_slot_trong = Queue()
    for i in range(so_luong_song_song_toi_da):
        cac_slot_trong.put(i)

    cac_tien_trinh_dang_chay = {} 

    while danh_sach_cho or cac_tien_trinh_dang_chay:
        tien_trinh_hoan_thanh = []
        for slot_id, p in list(cac_tien_trinh_dang_chay.items()):
            if not p.is_alive():
                logging.info(f"Tiến trình {p.name} (Slot {slot_id}) đã hoàn thành. Giải phóng slot.")
                cac_slot_trong.put(slot_id)
                tien_trinh_hoan_thanh.append(slot_id)
        
        for slot_id in tien_trinh_hoan_thanh:
            del cac_tien_trinh_dang_chay[slot_id]

        while not cac_slot_trong.empty() and danh_sach_cho:
            if not kiem_tra_tai_nguyen(cau_hinh):
                logging.warning("Tài nguyên cao, tạm dừng tạo tiến trình mới trong 10 giây...")
                time.sleep(1)
                continue

            nguoi_dung = danh_sach_cho.pop(0)
            proxy = None
            if cau_hinh.get("su_dung_proxy", False) and danh_sach_proxy:
                proxy = danh_sach_proxy[int(nguoi_dung['ma_dinh_danh']) % len(danh_sach_proxy)]

            slot_de_su_dung = cac_slot_trong.get() 

            ten_tien_trinh = f"Worker-{nguoi_dung['ma_dinh_danh']}-Slot{slot_de_su_dung}"
            tien_trinh = Process(
                target=thuc_thi, 
                args=(cau_hinh, kich_ban, nguoi_dung, khoa_thu_muc, proxy, slot_de_su_dung, so_luong_slot_hien_thi_toi_da),
                name=ten_tien_trinh
            )
            cac_tien_trinh_dang_chay[slot_de_su_dung] = tien_trinh
            tien_trinh.start()
            logging.info(f"Đã khởi chạy tiến trình {ten_tien_trinh} cho người dùng {nguoi_dung['ma_dinh_danh']} vào Slot {slot_de_su_dung}.")
            
        time.sleep(1)

    for p in cac_tien_trinh_dang_chay.values():
        if p.is_alive():
            p.join()
    logging.info("Tất cả các tiến trình đã hoàn thành.")

def chay_che_do_tuong_tac(cau_hinh, danh_sach_proxy, danh_sach_nguoi_dung, khoa_thu_muc):
    logging.info("Chế độ: TƯƠNG TÁC THỦ CÔNG (Mở lần lượt)")
    cac_tien_trinh_da_mo = []
    tong_so = len(danh_sach_nguoi_dung)
    
    for i, nguoi_dung in enumerate(danh_sach_nguoi_dung):
        logging.info("\n" + "="*50)
        logging.info(f"Chuẩn bị mở Profile {i+1}/{tong_so} cho người dùng có mã: {nguoi_dung['ma_dinh_danh']}")
        try:
            input(">>> Nhấn phím Enter để tiếp tục...")
        except KeyboardInterrupt:
            logging.info("\nĐã hủy bởi người dùng.")
            break
        proxy = None
        if cau_hinh.get("su_dung_proxy", False) and danh_sach_proxy:
            proxy = danh_sach_proxy[int(nguoi_dung['ma_dinh_danh']) % len(danh_sach_proxy)]
        
        p = Process(target=chay_mot_profile, args=(cau_hinh, nguoi_dung, khoa_thu_muc, proxy, i, tong_so))
        p.start()
        cac_tien_trinh_da_mo.append(p)
        time.sleep(2)
    if not cac_tien_trinh_da_mo: 
        return
    logging.info("\n" + "="*50)
    logging.info("Đã mở tất cả các profile được yêu cầu. Bạn có thể bắt đầu làm việc.")
    logging.info("KHÔNG ĐÓNG CỬA SỔ TERMINAL NÀY NẾU BẠN VẪN ĐANG LÀM VIỆC.")
    try:
        input(">>> Sau khi hoàn thành tất cả công việc, nhấn Enter ở đây để đóng tất cả trình duyệt...")
    except KeyboardInterrupt:
        logging.info("Đã nhận tín hiệu ngắt. Đang đóng tất cả trình duyệt...")
    for p in cac_tien_trinh_da_mo:
        if p.is_alive(): 
            p.terminate()
    logging.info("Đã đóng tất cả các trình duyệt.")

def chay_chuong_trinh_chinh():
    logging.info("🚀 BẮT ĐẦU CHƯƠNG TRÌNH TỰ ĐỘNG HÓA...")
    
    cau_hinh = tai_dl.tai_cau_hinh()
    danh_sach_proxy = tai_dl.tai_danh_sach_proxy()
    danh_sach_nguoi_dung = tai_dl.tai_danh_sach_nguoi_dung()
    
    if not all([cau_hinh, danh_sach_nguoi_dung]): 
        sys.exit(1)

    cau_hinh["tong_so_nguoi_dung"] = len(danh_sach_nguoi_dung)
    os.makedirs(cau_hinh["thu_muc_profiles"], exist_ok=True)
    khoa_thu_muc = Lock()

    if cau_hinh.get("su_dung_che_do_tuong_tac", False):
        chay_che_do_tuong_tac(cau_hinh, danh_sach_proxy, danh_sach_nguoi_dung, khoa_thu_muc)
    else:
        kich_ban = tai_dl.tai_kich_ban()
        if not kich_ban:
            logging.error("Chế độ tự động yêu cầu file 'kich_ban.json'.")
            sys.exit(1)
        chay_che_do_tu_dong(cau_hinh, kich_ban, danh_sach_proxy, danh_sach_nguoi_dung, khoa_thu_muc)
    
    logging.info("✅ TẤT CẢ CÁC TÁC VỤ ĐÃ HOÀN TẤT!")

if __name__ == "__main__":
    chay_chuong_trinh_chinh()