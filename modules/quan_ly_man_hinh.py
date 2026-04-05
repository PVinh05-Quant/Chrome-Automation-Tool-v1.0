import tkinter as tk
import logging
import math

def _lay_kich_thuoc_man_hinh_kha_dung():
    try:
        root = tk.Tk()
        root.withdraw()
        chieu_rong = root.winfo_screenwidth()
        chieu_cao = root.winfo_screenheight()
        root.destroy()
        return chieu_rong, chieu_cao
    except Exception as e:
        logging.warning(f"Không thể dùng tkinter để lấy kích thước màn hình, sẽ dùng cách dự phòng. Lỗi: {e}")
        return 1920, 1080

def sap_xep(trinh_dieu_khien, cau_hinh, vi_tri_slot, so_luong_slot_hien_thi_toi_da):
    try:
        thiet_lap = cau_hinh.get("sap_xep_cua_so", {})
        so_cot_mong_muon = thiet_lap.get("so_cot_mong_muon", 0)
        so_dong_mong_muon = thiet_lap.get("so_dong_mong_muon", 0)
        
        chieu_rong_mong_muon = thiet_lap.get("chieu_rong_mong_muon", 0)
        chieu_cao_mong_muon = thiet_lap.get("chieu_cao_mong_muon", 0)

        khoang_cach = thiet_lap.get("khoang_cach_giua_cac_cua_so", 5)
        bu_tru_tieu_de = thiet_lap.get("bu_tru_chieu_cao_tieu_de", 40)
        rong_kha_dung, cao_kha_dung = _lay_kich_thuoc_man_hinh_kha_dung()

        so_cot = 0
        so_hang = 0
        chieu_rong_cua_so = 0
        chieu_cao_cua_so = 0

        if chieu_rong_mong_muon > 0 and chieu_cao_mong_muon > 0:
            chieu_rong_cua_so = chieu_rong_mong_muon
            chieu_cao_cua_so = chieu_cao_mong_muon
            
            so_cot = math.floor((rong_kha_dung + khoang_cach) / (chieu_rong_cua_so + khoang_cach))
            so_hang = math.floor((cao_kha_dung + khoang_cach) / (chieu_cao_cua_so + khoang_cach))

            if so_cot_mong_muon > 0:
                so_cot = min(so_cot, so_cot_mong_muon)
            if so_dong_mong_muon > 0:
                so_hang = min(so_hang, so_dong_mong_muon)

            if so_cot == 0: so_cot = 1
            if so_hang == 0: so_hang = 1
        else:
            if so_cot_mong_muon > 0:
                so_cot = so_cot_mong_muon
                so_hang = math.ceil(so_luong_slot_hien_thi_toi_da / so_cot)
                if so_dong_mong_muon > 0:
                    so_hang = min(so_hang, so_dong_mong_muon)
            elif so_dong_mong_muon > 0: 
                so_hang = so_dong_mong_muon
                so_cot = math.ceil(so_luong_slot_hien_thi_toi_da / so_hang)
            else: 
                so_cot = math.ceil(math.sqrt(so_luong_slot_hien_thi_toi_da))
                if so_cot == 0: so_cot = 1
                so_hang = math.ceil(so_luong_slot_hien_thi_toi_da / so_cot)
            
            if so_cot == 0: so_cot = 1
            if so_hang == 0: so_hang = 1
            
            chieu_rong_cua_so = (rong_kha_dung - (khoang_cach * (so_cot + 1))) / so_cot
            chieu_cao_cua_so = (cao_kha_dung - (khoang_cach * (so_hang + 1))) / so_hang
        
        chieu_rong_cua_so = max(100, int(chieu_rong_cua_so))
        chieu_cao_cua_so = max(100, int(chieu_cao_cua_so))


        cot_hien_tai = vi_tri_slot % so_cot
        hang_hien_tai = vi_tri_slot // so_cot

        vi_tri_x = khoang_cach + cot_hien_tai * (chieu_rong_cua_so + khoang_cach)
        vi_tri_y = khoang_cach + hang_hien_tai * (chieu_cao_cua_so + khoang_cach)

        trinh_dieu_khien.set_window_position(int(vi_tri_x), int(vi_tri_y))
        trinh_dieu_khien.set_window_size(int(chieu_rong_cua_so), int(chieu_cao_cua_so + bu_tru_tieu_de))
        return so_hang, so_cot
    except Exception as e:
        logging.error(f"Lỗi khi sắp xếp cửa sổ: {e}")
        trinh_dieu_khien.set_window_position(0, 0)
        trinh_dieu_khien.set_window_size(800, 600)
        return 1, 1