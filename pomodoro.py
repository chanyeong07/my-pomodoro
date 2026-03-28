import streamlit as st
import time
import math

# 페이지 설정
st.set_page_config(page_title="Tim의 포모도로", page_icon="🍅", layout="wide")

# CSS 스타일
st.markdown("""
<style>
    .main { background-color: white; }
    .timer-container { display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .timer-number { font-size: 120px; font-weight: bold; color: #d1493c; text-align: right; width: 100%; padding-right: 50px; margin-top: -30px; font-family: monospace; }
    .status-text { font-size: 30px; font-weight: bold; color: #d1493c; width: 100%; text-align: left; padding-left: 50px; }
</style>
""", unsafe_allow_html=True)

# 팝업 메시지(다이얼로그) 함수
@st.dialog("집중 완료!")
def show_congrats():
    st.write("축하합니다! 🎉 아주 멋지게 집중하셨네요. 잠시 휴식을 취해보는 건 어떨까요?")
    if st.button("확인"):
        st.rerun()

st.title("🍅 Tim의 포모도로 타이머")

# 사이드바 설정
focus_time = st.sidebar.slider("집중 시간 선택 (분)", 1, 60, 25)

if "run" not in st.session_state:
    st.session_state.run = False

# 시작/정지 버튼
if st.sidebar.button("시작", use_container_width=True):
    st.session_state.run = True

if st.sidebar.button("정지", use_container_width=True):
    st.session_state.run = False
    st.rerun()

# 타이머 렌더링 함수
def render_timer(current_seconds, total_display_seconds=3600):
    m_val, s_val = divmod(current_seconds, 60)
    current_angle = (current_seconds / total_display_seconds) * 360
    rad = math.radians(current_angle - 90)
    x = 50 + 40 * math.cos(rad)
    y = 50 + 40 * math.sin(rad)
    large_arc = 1 if current_angle > 180 else 0
    
    svg_code = '<div class="timer-container"><svg width="500" height="500" viewBox="0 0 100 100">'
    svg_code += '<circle cx="50" cy="50" r="40" stroke="#f0f0f0" stroke-width="0.5" fill="none" />'
    for i in range(60):
        svg_code += f'<line x1="50" y1="10" x2="50" y2="12" stroke="#eee" stroke-width="0.5" transform="rotate({i*6} 50 50)" />'
    for i in range(12):
        svg_code += f'<line x1="50" y1="10" x2="50" y2="14" stroke="#ccc" stroke-width="0.8" transform="rotate({i*30} 50 50)" />'
    svg_code += '<text x="50" y="8" text-anchor="middle" font-size="4" fill="#999">0</text>'
    svg_code += '<text x="92" y="51.5" text-anchor="middle" font-size="4" fill="#999">15</text>'
    svg_code += '<text x="50" y="95" text-anchor="middle" font-size="4" fill="#999">30</text>'
    svg_code += '<text x="8" y="51.5" text-anchor="middle" font-size="4" fill="#999">45</text>'
    if current_angle > 0:
        svg_code += f'<path d="M50,50 L50,10 A40,40 0 {large_arc},1 {x},{y} Z" fill="#d1493c" opacity="0.9" />'
    svg_code += f'<circle cx="{x}" cy="{y}" r="2" fill="white" stroke="#d1493c" stroke-width="0.5" />'
    svg_code += '</svg></div>'
    return svg_code, m_val, s_val

timer_display_area = st.empty()

# 실행 로직
if not st.session_state.run:
    svg, m, s = render_timer(focus_time * 60)
    with timer_display_area.container():
        st.markdown(svg, unsafe_allow_html=True)
        st.markdown(f'<div class="timer-number">{focus_time:02d}:00</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-text">● 시간 설정 중</div>', unsafe_allow_html=True)
else:
    for t in range(focus_time * 60, -1, -1):
        if not st.session_state.run: break
        svg, m, s = render_timer(t)
        with timer_display_area.container():
            st.markdown(svg, unsafe_allow_html=True)
            st.markdown(f'<div class="timer-number">{m:02d}:{s:02d}</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-text">● 공부하기</div>', unsafe_allow_html=True)
        time.sleep(1)
        
    if st.session_state.run:
        st.session_state.run = False
        show_congrats() # 타이머 종료 시 팝업 창 띄우기
