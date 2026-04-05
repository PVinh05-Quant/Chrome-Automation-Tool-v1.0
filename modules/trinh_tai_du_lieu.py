import json
import csv
import os
import logging

def tai_cau_hinh():
    try:
        with open('data/cau_hinh.json', 'r', encoding='utf-8') as f:
            cau_hinh = json.load(f)
        cau_hinh['thu_muc_profiles'] = os.path.join(os.getcwd(), cau_hinh.get('thu_muc_profiles', 'profiles'))
        return cau_hinh
    except Exception as e:
        logging.error(f"Lỗi khi tải file cau_hinh.json: {e}")
        return None


def tai_danh_sach_proxy():
    danh_sach = []
    try:
        with open('data/danh_sach_proxy.csv', 'r', encoding='utf-8') as f:
            trinh_doc_csv = csv.DictReader(f)
            for hang in trinh_doc_csv:
                danh_sach.append(hang)
        return danh_sach
    except FileNotFoundError:
        logging.error("Lỗi: Không tìm thấy file 'data/danh_sach_proxy.csv'.")
        return []


def tai_danh_sach_nguoi_dung():
    danh_sach = []
    try:
        with open('data/danh_sach_nguoi_dung.csv', 'r', encoding='utf-8') as f:
            trinh_doc_csv = csv.DictReader(f)
            for hang in trinh_doc_csv:
                danh_sach.append(hang)
        return danh_sach
    except FileNotFoundError:
        logging.error("Lỗi: Không tìm thấy file 'data/danh_sach_nguoi_dung.csv'.")
        return []

def tai_kich_ban():
    try:
        with open('data/kich_ban.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []