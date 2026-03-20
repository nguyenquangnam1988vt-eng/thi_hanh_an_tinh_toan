import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def format_thoi_gian(rd: relativedelta):
    """Hàm chuyển đổi thời gian thành chuỗi năm/tháng/ngày"""
    parts = []
    if rd.years > 0:
        parts.append(f"{rd.years} năm")
    if rd.months > 0:
        parts.append(f"{rd.months} tháng")
    if rd.days > 0:
        parts.append(f"{rd.days} ngày")
    if not parts:  # nếu tất cả bằng 0
        return "0 ngày"
    return " ".join(parts)

def tinh_toan(ngay_bat_dau, thoi_han, ngay_hien_tai, rut_ngan_thang, rut_ngan_ngay):
    """Hàm tính toán thời gian chấp hành án"""
    try:
        # Ngày kết thúc sau khi trừ rút ngắn
        ngay_ket_thuc = ngay_bat_dau + relativedelta(
            months=thoi_han - rut_ngan_thang,
            days=-rut_ngan_ngay
        )

        # Thời gian đã chấp hành
        da_chap_hanh = relativedelta(ngay_hien_tai, ngay_bat_dau)

        # Thời gian còn chấp hành
        con_chap_hanh = relativedelta(ngay_ket_thuc, ngay_hien_tai)

        return {
            'da_chap_hanh': da_chap_hanh,
            'con_chap_hanh': con_chap_hanh,
            'ngay_ket_thuc': ngay_ket_thuc
        }
    except Exception as e:
        st.error(f"Lỗi tính toán: {e}")
        return None

# Cấu hình trang
st.set_page_config(
    page_title="Tính thời gian chấp hành án",
    page_icon="⚖️",
    layout="centered"
)

# Tiêu đề
st.title("⚖️ Phần mềm tính thời gian chấp hành án")
st.markdown("---")

# Tạo form nhập liệu
with st.form("form_tinh_toan"):
    col1, col2 = st.columns(2)
    
    with col1:
        ngay_bat_dau = st.date_input(
            "📅 Ngày bắt đầu",
            value=datetime.now().date(),
            format="DD/MM/YYYY"
        )
        
        thoi_han = st.number_input(
            "📆 Thời hạn (tháng)",
            min_value=1,
            value=12,
            step=1
        )
        
        rut_ngan_thang = st.number_input(
            "⬇️ Được rút ngắn (tháng)",
            min_value=0,
            value=0,
            step=1
        )
    
    with col2:
        ngay_hien_tai = st.date_input(
            "📅 Ngày hiện tại",
            value=datetime.now().date(),
            format="DD/MM/YYYY"
        )
        
        # Ô trống cho ngày hiện tại để tương thích với code cũ
        st.write("")  # Spacer
        
        rut_ngan_ngay = st.number_input(
            "⬇️ Được rút ngắn (ngày)",
            min_value=0,
            value=0,
            step=1
        )
    
    # Nút submit
    submitted = st.form_submit_button("🔍 Tính toán", use_container_width=True)

# Xử lý khi submit
if submitted:
    # Kiểm tra ngày hợp lệ
    if ngay_hien_tai < ngay_bat_dau:
        st.warning("⚠️ Ngày hiện tại không thể nhỏ hơn ngày bắt đầu!")
    else:
        # Chuyển đổi sang datetime
        ngay_bat_dau_dt = datetime.combine(ngay_bat_dau, datetime.min.time())
        ngay_hien_tai_dt = datetime.combine(ngay_hien_tai, datetime.min.time())
        
        # Tính toán
        ket_qua = tinh_toan(
            ngay_bat_dau_dt,
            thoi_han,
            ngay_hien_tai_dt,
            rut_ngan_thang,
            rut_ngan_ngay
        )
        
        if ket_qua:
            # Hiển thị kết quả
            st.markdown("---")
            st.subheader("📊 Kết quả tính toán")
            
            # Tạo layout 2 cột cho kết quả
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("**ĐÃ CHẤP HÀNH**")
                st.success(format_thoi_gian(ket_qua['da_chap_hanh']))
                
            with col2:
                st.info("**CÒN CHẤP HÀNH**") 
                st.warning(format_thoi_gian(ket_qua['con_chap_hanh']))
            
            # Hiển thị ngày kết thúc
            st.markdown("---")
            st.caption(f"📌 Ngày kết thúc dự kiến: **{ket_qua['ngay_ket_thuc'].strftime('%d/%m/%Y')}**")

# Footer
st.markdown("---")
st.caption("⚖️ Ứng dụng hỗ trợ tính thời gian chấp hành án - Dành cho mục đích tham khảo")
