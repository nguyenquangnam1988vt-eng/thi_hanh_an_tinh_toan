import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

def tinh_toan():
    """Hàm tính toán thời gian chấp hành án"""
    try:
        # Lấy dữ liệu nhập từ session state
        ngay_bat_dau = datetime.strptime(st.session_state.ngay_bat_dau, "%d/%m/%Y")
        thoi_han = int(st.session_state.thoi_han)
        ngay_hien_tai = datetime.strptime(st.session_state.ngay_hien_tai, "%d/%m/%Y")
        rut_ngan_thang = int(st.session_state.rut_thang if st.session_state.rut_thang else 0)
        rut_ngan_ngay = int(st.session_state.rut_ngay if st.session_state.rut_ngay else 0)

        # Kiểm tra ngày hợp lệ
        if ngay_hien_tai < ngay_bat_dau:
            st.error("Lỗi: Ngày hiện tại không thể nhỏ hơn ngày bắt đầu!")
            return

        # Ngày kết thúc sau khi trừ rút ngắn
        ngay_ket_thuc = ngay_bat_dau + relativedelta(
            months=thoi_han - rut_ngan_thang,
            days=-rut_ngan_ngay
        )

        # Thời gian đã chấp hành
        da_chap_hanh = relativedelta(ngay_hien_tai, ngay_bat_dau)

        # Thời gian còn chấp hành
        con_chap_hanh = relativedelta(ngay_ket_thuc, ngay_hien_tai)

        # Lưu kết quả vào session state
        st.session_state.ket_qua = {
            'da_chap_hanh': format_thoi_gian(da_chap_hanh),
            'con_chap_hanh': format_thoi_gian(con_chap_hanh)
        }
        
    except Exception as e:
        st.error(f"Lỗi: Vui lòng nhập đúng định dạng!\nChi tiết: {e}")

# Cấu hình trang
st.set_page_config(
    page_title="Tính thời gian chấp hành án",
    page_icon="⚖️",
    layout="centered"
)

# Tiêu đề
st.title("⚖️ Phần mềm tính thời gian chấp hành án")
st.markdown("---")

# Khởi tạo session state
if 'ket_qua' not in st.session_state:
    st.session_state.ket_qua = None

# Tạo form nhập liệu - giữ nguyên layout như code gốc
st.write("### Nhập thông tin")

# Ngày bắt đầu
st.write("Ngày bắt đầu (dd/mm/yyyy):")
ngay_bat_dau = st.text_input(
    label="",
    key="ngay_bat_dau",
    placeholder="dd/mm/yyyy",
    label_visibility="collapsed"
)

# Thời hạn
st.write("Thời hạn (tháng):")
thoi_han = st.text_input(
    label="",
    key="thoi_han",
    placeholder="Số tháng",
    label_visibility="collapsed"
)

# Ngày hiện tại
st.write("Ngày hiện tại (dd/mm/yyyy):")
ngay_hien_tai = st.text_input(
    label="",
    key="ngay_hien_tai",
    placeholder="dd/mm/yyyy",
    label_visibility="collapsed",
    value=datetime.now().strftime("%d/%m/%Y")
)

# Rút ngắn tháng
st.write("Được rút ngắn (tháng):")
rut_thang = st.text_input(
    label="",
    key="rut_thang",
    placeholder="Số tháng",
    label_visibility="collapsed",
    value="0"
)

# Rút ngắn ngày
st.write("Được rút ngắn (ngày):")
rut_ngay = st.text_input(
    label="",
    key="rut_ngay",
    placeholder="Số ngày",
    label_visibility="collapsed",
    value="0"
)

# Nút tính toán
st.markdown("---")
if st.button("🔍 Tính toán", use_container_width=True):
    tinh_toan()

# Hiển thị kết quả
if st.session_state.ket_qua:
    st.markdown("---")
    st.write("### Kết quả")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📊 **Đã chấp hành**")
        st.success(st.session_state.ket_qua['da_chap_hanh'])
    
    with col2:
        st.info("📊 **Còn chấp hành**")
        st.warning(st.session_state.ket_qua['con_chap_hanh'])

# Footer
st.markdown("---")
st.caption("⚖️ Ứng dụng hỗ trợ tính thời gian chấp hành án - Phiên bản 1.0")
