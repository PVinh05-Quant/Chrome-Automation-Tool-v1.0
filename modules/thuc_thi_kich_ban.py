import os
import time
import random
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .khoi_tao_trinh_duyet import khoi_tao

ANH_XA_BO_CHON = {"ID": By.ID, "NAME": By.NAME, "XPATH": By.XPATH, "CSS_SELECTOR": By.CSS_SELECTOR}

def lay_gia_tri_dong(obj_gia_tri):
    if isinstance(obj_gia_tri, dict):
        loai = obj_gia_tri.get("loai")
        if loai == "so_thuc_ngau_nhien":
            return random.uniform(obj_gia_tri.get("nho_nhat", 0), obj_gia_tri.get("lon_nhat", 1))
        if loai == "so_nguyen_ngau_nhien":
            return random.randint(obj_gia_tri.get("nho_nhat", 0), obj_gia_tri.get("lon_nhat", 100))
        if loai == "tinh":
            return obj_gia_tri.get("gia_tri")
    return obj_gia_tri

def _thuc_thi_mot_buoc_con(trinh_dieu_khien, doi, buoc_con, nguoi_dung, ma_dinh_danh_nd, cau_hinh):
    return _thuc_thi_mot_buoc_con_with_bien_tam(trinh_dieu_khien, doi, buoc_con, nguoi_dung, ma_dinh_danh_nd, cau_hinh, None)

def _thuc_thi_mot_buoc_con_with_bien_tam(trinh_dieu_khien, doi, buoc_con, nguoi_dung, ma_dinh_danh_nd, cau_hinh, bien_tam=None):
    if bien_tam is None:
        bien_tam = {}
    hanh_dong = buoc_con.get("hanh_dong")
    buoc_so = buoc_con.get('buoc', 'N/A')
    logging.debug(f"[{ma_dinh_danh_nd}] Thực thi bước con {buoc_so}: {hanh_dong.upper()}")

    try:
        if hanh_dong == "dieu_huong":
            url = buoc_con.get("gia_tri")
            if not url:
                raise ValueError("Thiếu 'gia_tri' cho hành động 'dieu_huong'.")
            trinh_dieu_khien.get(url)

        elif hanh_dong == "cho" or hanh_dong == "tam_dung_tu_dong":
            thoi_gian = lay_gia_tri_dong(buoc_con.get("gia_tri"))
            if thoi_gian is None:
                raise ValueError("Thiếu hoặc sai định dạng 'gia_tri' cho hành động 'cho'.")
            logging.debug(f"[{ma_dinh_danh_nd}] Tạm dừng trong {thoi_gian:.2f} giây...")
            time.sleep(thoi_gian)

        elif hanh_dong == "dien_thong_tin":
            loai_bo_chon_str = buoc_con.get("loai_bo_chon")
            gia_tri_bo_chon = buoc_con.get("gia_tri_bo_chon")
            if not all([loai_bo_chon_str, gia_tri_bo_chon]):
                raise ValueError("Thiếu 'loai_bo_chon' hoặc 'gia_tri_bo_chon' cho hành động 'dien_thong_tin'.")
            
            loai_bo_chon = ANH_XA_BO_CHON.get(loai_bo_chon_str)
            if not loai_bo_chon:
                raise ValueError(f"Loại bộ chọn '{loai_bo_chon_str}' không hợp lệ.")
            
            doi_tuong_web = doi.until(EC.presence_of_element_located((loai_bo_chon, gia_tri_bo_chon)))
            doi_tuong_web.clear()
            gia_tri_nhap = buoc_con.get("gia_tri_nhap", nguoi_dung.get(buoc_con.get("khoa_gia_tri", ""), ""))
            if isinstance(gia_tri_nhap, str) and "{" in gia_tri_nhap and "}" in gia_tri_nhap:
                for k, v in (bien_tam or {}).items():
                    gia_tri_nhap = gia_tri_nhap.replace(f"{{{k}}}", str(v))
            doi_tuong_web.send_keys(gia_tri_nhap)

        elif hanh_dong == "nhan_chuot":
            loai_bo_chon_str = buoc_con.get("loai_bo_chon")
            gia_tri_bo_chon = buoc_con.get("gia_tri_bo_chon")
            if not all([loai_bo_chon_str, gia_tri_bo_chon]):
                raise ValueError("Thiếu 'loai_bo_chon' hoặc 'gia_tri_bo_chon' cho hành động 'nhan_chuot'.")
            
            loai_bo_chon = ANH_XA_BO_CHON.get(loai_bo_chon_str)
            if not loai_bo_chon:
                raise ValueError(f"Loại bộ chọn '{loai_bo_chon_str}' không hợp lệ.")
            
            doi_tuong_web = doi.until(EC.element_to_be_clickable((loai_bo_chon, gia_tri_bo_chon)))
            trinh_dieu_khien.execute_script("arguments[0].click();", doi_tuong_web)
        
        elif hanh_dong == "lay_text":
            loai_bo_chon_str = buoc_con.get("loai_bo_chon")
            gia_tri_bo_chon = buoc_con.get("gia_tri_bo_chon")
            if not all([loai_bo_chon_str, gia_tri_bo_chon]):
                raise ValueError("Thiếu 'loai_bo_chon' hoặc 'gia_tri_bo_chon' cho hành động 'lay_text'.")
            
            loai_bo_chon = ANH_XA_BO_CHON.get(loai_bo_chon_str)
            if not loai_bo_chon:
                raise ValueError(f"Loại bộ chọn '{loai_bo_chon_str}' không hợp lệ.")
            
            doi_tuong_web = doi.until(EC.presence_of_element_located((loai_bo_chon, gia_tri_bo_chon)))
            text_trich_xuat = doi_tuong_web.text
            khoa_luu = buoc_con.get("khoa_luu_text")
            if khoa_luu:
                bien_tam[khoa_luu] = text_trich_xuat
            logging.info(f"[{ma_dinh_danh_nd}] Đã lấy text từ '{buoc_con['gia_tri_bo_chon']}': '{text_trich_xuat}'")

        elif hanh_dong == "chon_dropdown":
            loai_bo_chon_str = buoc_con.get("loai_bo_chon")
            gia_tri_bo_chon = buoc_con.get("gia_tri_bo_chon")
            chon_theo = buoc_con.get("chon_theo")
            gia_tri_chon = buoc_con.get("gia_tri_chon")
            
            if not all([loai_bo_chon_str, gia_tri_bo_chon, chon_theo, gia_tri_chon is not None]):
                raise ValueError("Thiếu thông tin cần thiết cho hành động 'chon_dropdown'.")
            
            loai_bo_chon = ANH_XA_BO_CHON.get(loai_bo_chon_str)
            if not loai_bo_chon:
                raise ValueError(f"Loại bộ chọn '{loai_bo_chon_str}' không hợp lệ.")
            
            doi_tuong_web = doi.until(EC.presence_of_element_located((loai_bo_chon, gia_tri_bo_chon)))
            doi_tuong_select = Select(doi_tuong_web)

            if chon_theo == "text":
                doi_tuong_select.select_by_visible_text(gia_tri_chon)
            elif chon_theo == "value":
                doi_tuong_select.select_by_value(gia_tri_chon)
            elif chon_theo == "index":
                try:
                    doi_tuong_select.select_by_index(int(gia_tri_chon))
                except ValueError:
                    raise ValueError(f"Giá trị chọn '{gia_tri_chon}' cho 'index' phải là số nguyên.")
            else:
                raise ValueError(f"Phương thức chọn dropdown '{chon_theo}' không hợp lệ.")
            
            logging.info(f"[{ma_dinh_danh_nd}] Đã chọn '{gia_tri_chon}' từ dropdown '{buoc_con['gia_tri_bo_chon']}' theo {chon_theo}")

        elif hanh_dong == "cuon_trang":
            loai_cuon = buoc_con.get("loai_cuon", "xuong")
            
            if loai_cuon == "xuong":
                trinh_dieu_khien.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                logging.info(f"[{ma_dinh_danh_nd}] Đã cuộn xuống cuối trang.")
            elif loai_cuon == "len":
                trinh_dieu_khien.execute_script("window.scrollTo(0, 0);")
                logging.info(f"[{ma_dinh_danh_nd}] Đã cuộn lên đầu trang.")
            elif loai_cuon == "den_phan_tu":
                loai_bo_chon_str = buoc_con.get("loai_bo_chon")
                gia_tri_bo_chon = buoc_con.get("gia_tri_bo_chon")
                if not all([loai_bo_chon_str, gia_tri_bo_chon]):
                    raise ValueError("Thiếu 'loai_bo_chon' hoặc 'gia_tri_bo_chon' cho hành động 'cuon_trang' đến phần tử.")
                
                loai_bo_chon = ANH_XA_BO_CHON.get(loai_bo_chon_str)
                if not loai_bo_chon:
                    raise ValueError(f"Loại bộ chọn '{loai_bo_chon_str}' không hợp lệ.")

                doi_tuong_web = doi.until(EC.presence_of_element_located((loai_bo_chon, gia_tri_bo_chon)))
                trinh_dieu_khien.execute_script("arguments[0].scrollIntoView(true);", doi_tuong_web)
                logging.info(f"[{ma_dinh_danh_nd}] Đã cuộn đến phần tử '{buoc_con['gia_tri_bo_chon']}'.")
            elif loai_cuon == "theo_pixel":
                x_offset = buoc_con.get("x", 0)
                y_offset = buoc_con.get("y", 0)
                trinh_dieu_khien.execute_script(f"window.scrollBy({x_offset}, {y_offset});")
                logging.info(f"[{ma_dinh_danh_nd}] Đã cuộn theo pixel: ({x_offset}, {y_offset}).")
            else:
                logging.info(f"[{ma_dinh_danh_nd}] Loại cuộn '{loai_cuon}' không được hỗ trợ. Bỏ qua.")

        elif hanh_dong == "thuc_thi_js":
            ma_js = buoc_con.get("ma_js")
            if not ma_js:
                raise ValueError("Thiếu 'ma_js' cho hành động 'thuc_thi_js'.")
            ket_qua_js = trinh_dieu_khien.execute_script(ma_js)
            logging.info(f"[{ma_dinh_danh_nd}] Đã thực thi JavaScript. Kết quả: {ket_qua_js}")
        
        elif hanh_dong == "xu_ly_alert":
            hanh_dong_alert = buoc_con.get("hanh_dong_alert")
            if not hanh_dong_alert:
                raise ValueError("Thiếu 'hanh_dong_alert' cho hành động 'xu_ly_alert'.")

            try:
                alert = doi.until(EC.alert_is_present())
                if hanh_dong_alert == "chap_nhan":
                    alert.accept()
                    logging.info(f"[{ma_dinh_danh_nd}] Đã chấp nhận alert.")
                elif hanh_dong_alert == "huy_bo":
                    alert.dismiss()
                    logging.info(f"[{ma_dinh_danh_nd}] Đã hủy bỏ alert.")
                elif hanh_dong_alert == "nhap_text":
                    text_gui = buoc_con.get("text_gui")
                    if text_gui is None:
                        raise ValueError("Thiếu 'text_gui' cho hành động 'nhap_text' trong alert.")
                    alert.send_keys(text_gui)
                    alert.accept()
                    logging.info(f"[{ma_dinh_danh_nd}] Đã nhập '{text_gui}' vào alert và chấp nhận.")
                else:
                    logging.warning(f"[{ma_dinh_danh_nd}] Hành động alert '{hanh_dong_alert}' không được hỗ trợ. Bỏ qua.")
            except Exception as ex_alert:
                logging.error(f"[{ma_dinh_danh_nd}] Lỗi khi xử lý alert: {ex_alert}. Có thể không có alert hoặc loại alert không đúng.", exc_info=False)
                raise # Ném lại lỗi để bước cha có thể bắt và xử lý

        elif hanh_dong == "chuyen_cua_so":
            cua_so_dich = buoc_con.get("dich", "moi_nhat")
            
            if cua_so_dich == "moi_nhat":
                if trinh_dieu_khien.window_handles:
                    trinh_dieu_khien.switch_to.window(trinh_dieu_khien.window_handles[-1])
                    logging.info(f"[{ma_dinh_danh_nd}] Đã chuyển sang cửa sổ/tab mới nhất.")
                else:
                    logging.warning(f"[{ma_dinh_danh_nd}] Không có cửa sổ nào để chuyển đến.")
            elif cua_so_dich == "dau_tien":
                if trinh_dieu_khien.window_handles:
                    trinh_dieu_khien.switch_to.window(trinh_dieu_khien.window_handles[0])
                    logging.info(f"[{ma_dinh_danh_nd}] Đã chuyển sang cửa sổ/tab đầu tiên.")
                else:
                    logging.warning(f"[{ma_dinh_danh_nd}] Không có cửa sổ nào để chuyển đến.")
            elif cua_so_dich == "theo_tieu_de":
                tieu_de_mong_muon = buoc_con.get("tieu_de")
                if not tieu_de_mong_muon:
                    raise ValueError("Thiếu 'tieu_de' cho hành động 'chuyen_cua_so' theo tiêu đề.")
                
                tim_thay_cua_so = False
                for handle in trinh_dieu_khien.window_handles:
                    trinh_dieu_khien.switch_to.window(handle)
                    if tieu_de_mong_muon in trinh_dieu_khien.title:
                        logging.info(f"[{ma_dinh_danh_nd}] Đã chuyển sang cửa sổ/tab có tiêu đề '{tieu_de_mong_muon}'.")
                        tim_thay_cua_so = True
                        break
                if not tim_thay_cua_so:
                    logging.warning(f"[{ma_dinh_danh_nd}] Không tìm thấy cửa sổ/tab với tiêu đề '{tieu_de_mong_muon}'.")
            else:
                logging.warning(f"[{ma_dinh_danh_nd}] Loại chuyển cửa sổ '{cua_so_dich}' không được hỗ trợ. Bỏ qua.")
        
        else:
            logging.warning(f"[{ma_dinh_danh_nd}] Hành động '{hanh_dong}' không xác định hoặc không được hỗ trợ. Bỏ qua bước.")
    
    except Exception as e:
        logging.error(f"[{ma_dinh_danh_nd}] Lỗi tại bước con {buoc_so} (hành động: {hanh_dong}): {type(e).__name__} - {e}", exc_info=False)
        raise # Quan trọng: Ném lại lỗi để thoát khỏi vòng lặp/kịch bản nếu cần

def thuc_thi(cau_hinh, kich_ban, nguoi_dung, khoa_thu_muc, proxy=None, chi_muc_nguoi_dung=0, tong_so_nguoi_dung=1):
    trinh_dieu_khien = None
    ma_dinh_danh_nd = nguoi_dung.get('ma_dinh_danh', 'KHONG_XAC_DINH')
    logging.info(f"Bắt đầu xử lý người dùng có mã: {ma_dinh_danh_nd}")
    
    try:
        trinh_dieu_khien = khoi_tao(cau_hinh, nguoi_dung, khoa_thu_muc, proxy, chi_muc_nguoi_dung, tong_so_nguoi_dung)
        thoi_gian_cho_toi_da = cau_hinh.get("thoi_gian_cho_toi_da", 30)
        doi = WebDriverWait(trinh_dieu_khien, thoi_gian_cho_toi_da)

        for buoc_hien_tai in kich_ban:
            hanh_dong = buoc_hien_tai.get("hanh_dong")
            buoc_so = buoc_hien_tai.get('buoc', 'N/A')
            logging.info(f"[{ma_dinh_danh_nd}] Bước {buoc_so}: {hanh_dong.upper()}...")
            
            try:
                if hanh_dong == "vong_lap":
                    so_lan_lap_toi_da = buoc_hien_tai.get("lap_toi_da", -1) # -1 nghĩa là lặp vô hạn nếu không có điều kiện dừng
                    dieu_kien_dung = buoc_hien_tai.get("dieu_kien_dung")
                    buoc_con_list = buoc_hien_tai.get("buoc_con", [])

                    if not buoc_con_list:
                        logging.warning(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so} không có bước con nào. Bỏ qua.")
                        continue # Bỏ qua vòng lặp nếu không có bước con

                    lan_lap_hien_tai = 0
                    while True:
                        if so_lan_lap_toi_da != -1 and lan_lap_hien_tai >= so_lan_lap_toi_da:
                            logging.info(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Đã đạt số lần lặp tối đa ({so_lan_lap_toi_da}). Thoát vòng lặp.")
                            break

                        if dieu_kien_dung:
                            try:
                                loai_bo_chon_dk_str = dieu_kien_dung.get("loai_bo_chon")
                                gia_tri_bo_chon_dk = dieu_kien_dung.get("gia_tri_bo_chon")
                                loai_kiem_tra_dk = dieu_kien_dung.get("loai_kiem_tra", "ton_tai")

                                if not all([loai_bo_chon_dk_str, gia_tri_bo_chon_dk]):
                                    logging.error(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Thiếu thông tin bộ chọn cho điều kiện dừng.")
                                    break # Thoát vòng lặp do cấu hình điều kiện dừng lỗi

                                loai_bo_chon_dk = ANH_XA_BO_CHON.get(loai_bo_chon_dk_str)
                                if not loai_bo_chon_dk:
                                    logging.error(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Loại bộ chọn điều kiện dừng '{loai_bo_chon_dk_str}' không hợp lệ.")
                                    break # Thoát vòng lặp

                                # Kiểm tra điều kiện dừng
                                if loai_kiem_tra_dk == "ton_tai":
                                    doi.until(EC.presence_of_element_located((loai_bo_chon_dk, gia_tri_bo_chon_dk)))
                                    logging.info(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Đã tìm thấy phần tử điều kiện dừng. Thoát vòng lặp.")
                                    break # Dừng vòng lặp nếu phần tử tồn tại
                                elif loai_kiem_tra_dk == "khong_ton_tai":
                                    # Chờ cho phần tử biến mất
                                    doi.until(EC.invisibility_of_element_located((loai_bo_chon_dk, gia_tri_bo_chon_dk)))
                                    logging.info(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Phần tử điều kiện dừng đã biến mất. Thoát vòng lặp.")
                                    break
                                # Có thể thêm các loại kiểm tra khác như "hien_thi", "khong_hien_thi", "co_text", v.v.
                                else:
                                    logging.warning(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Loại kiểm tra điều kiện dừng '{loai_kiem_tra_dk}' không được hỗ trợ. Tiếp tục lặp.")
                            except Exception as e_dk:
                                logging.debug(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Điều kiện dừng chưa thỏa mãn hoặc lỗi kiểm tra: {e_dk}")
                                pass # Tiếp tục lặp nếu điều kiện chưa thỏa mãn

                        logging.info(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Bắt đầu lần lặp thứ {lan_lap_hien_tai + 1}...")
                        
                        thanh_cong_trong_lan_lap = True
                        bien_tam = {}
                        for buoc_con_item in buoc_con_list:
                            try:
                                # Gọi hàm trợ giúp để thực thi từng bước con, truyền bien_tam
                                _thuc_thi_mot_buoc_con_with_bien_tam(trinh_dieu_khien, doi, buoc_con_item, nguoi_dung, ma_dinh_danh_nd, cau_hinh, bien_tam)
                            except Exception as e_con:
                                logging.error(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Lỗi tại bước con. Dừng lần lặp hiện tại. Lỗi: {e_con}")
                                thanh_cong_trong_lan_lap = False
                                break # Thoát khỏi các bước con của lần lặp hiện tại
                        
                        if not thanh_cong_trong_lan_lap:
                            logging.error(f"[{ma_dinh_danh_nd}] Vòng lặp ở bước {buoc_so}: Lần lặp hiện tại thất bại. Thoát vòng lặp chính.")
                            break # Thoát khỏi vòng lặp chính nếu có lỗi trong bước con

                        lan_lap_hien_tai += 1
                        # Tạm dừng giữa các lần lặp chính
                        thoi_gian_cho_giua_cac_lap = cau_hinh.get("thoi_gian_cho_giua_cac_lap", 1)
                        if thoi_gian_cho_giua_cac_lap > 0:
                            logging.debug(f"[{ma_dinh_danh_nd}] Tạm dừng giữa các lần lặp trong {thoi_gian_cho_giua_cac_lap:.2f} giây.")
                            time.sleep(thoi_gian_cho_giua_cac_lap)

                else:
                    # Các hành động không phải vòng lặp sẽ được xử lý ở đây
                    _thuc_thi_mot_buoc_con(trinh_dieu_khien, doi, buoc_hien_tai, nguoi_dung, ma_dinh_danh_nd, cau_hinh)

            except Exception as e:
                # Ghi log chi tiết hơn về lỗi của từng bước (cả vòng lặp và các bước khác)
                logging.error(f"[{ma_dinh_danh_nd}] Lỗi nghiêm trọng tại bước {buoc_so} (hành động: {hanh_dong}): {type(e).__name__} - {e}", exc_info=False)
                break # Dừng kịch bản nếu một bước gặp lỗi

    except Exception as e_tong:
        # Xử lý các lỗi nghiêm trọng hơn (ví dụ: lỗi khởi tạo trình duyệt)
        logging.error(f"Lỗi nghiêm trọng khi xử lý người dùng {ma_dinh_danh_nd}: {type(e_tong).__name__} - {e_tong}", exc_info=True)
    finally:
        if trinh_dieu_khien:
            try:
                trinh_dieu_khien.quit()
                logging.info(f"[{ma_dinh_danh_nd}] Đã đóng trình duyệt.")
            except Exception as e_quit:
                logging.error(f"[{ma_dinh_danh_nd}] Lỗi khi đóng trình duyệt: {e_quit}", exc_info=False)
        logging.info(f"Hoàn tất xử lý người dùng có mã: {ma_dinh_danh_nd}")