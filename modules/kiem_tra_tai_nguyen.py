import logging
import psutil

def kiem_tra(cau_hinh):
    if not cau_hinh.get("kiem_tra_tai_nguyen", False):
        return True
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    logging.info(f"Tài nguyên hệ thống - CPU: {cpu}%, RAM: {ram}%")
    if cpu > cau_hinh.get("cpu_toi_da", 90) or ram > cau_hinh.get("ram_toi_da", 90):
        logging.warning(f"Tài nguyên hệ thống cao (CPU: {cpu}%, RAM: {ram}%)! Đang tạm dừng...")
        return False
    return True