import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="심플 & 감성 MBTI 검사",
    page_icon="✨",
    layout="centered"
)

# 커스텀 CSS (파스텔 톤 디자인 및 폰트 설정)
st.markdown("""
    <style>
    .stApp {
        background-color: #fdf6f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        border: 1px solid #fce4ec;
        background-color: #fce4ec;
        color: #880e4f;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #f8bbd0;
        border-color: #f8bbd0;
        color: #880e4f;
    }
    .question-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        color: #333;
    }
    h1 {
        color: #ce93d8;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# MBTI 질문 데이터 (12개)
questions = [
    {"q": "주말에는 주로 어떻게 시간을 보내나요?", "options": ["사람들과 어울리며 에너지를 얻는다", "집에서 혼자 쉬는 것을 선호한다"], "type": "EI"},
    {"q": "새로운 사람을 만날 때 나는?", "options": ["먼저 말을 걸고 분위기를 주도한다", "상대방이 말을 걸어줄 때까지 기다린다"], "type": "EI"},
    {"q": "모임에서 나는 어떤 역할을 하나요?", "options": ["중심에서 대화를 이끈다", "조용히 경청하며 반응한다"], "type": "EI"},
    {"q": "미래에 대해 생각할 때 나는?", "options": ["구체적인 현실과 가능성을 본다", "다양한 상상과 추상적인 아이디어를 떠올린다"], "type": "SN"},
    {"q": "이야기를 들을 때 더 중요한 것은?", "options": ["실제 일어난 사실과 정보", "그 속에 담긴 의미와 전체적인 흐름"], "type": "SN"},
    {"q": "새로운 일을 배울 때 선호하는 방식은?", "options": ["실습을 통해 직접 해보는 것", "원리와 이론을 먼저 파악하는 것"], "type": "SN"},
    {"q": "친구의 고민 상담을 해줄 때 나는?", "options": ["현실적인 해결책을 제시한다", "충분히 공감해주고 위로를 건넨다"], "type": "TF"},
    {"q": "결정을 내릴 때 더 중요하게 생각하는 것은?", "options": ["논리적인 근거와 객관성", "주변 사람들의 기분과 가치"], "type": "TF"},
    {"q": "정직함과 친절함 중 하나를 고른다면?", "options": ["조금 아프더라도 정직한 진실", "상대방을 배려하는 따뜻한 친절"], "type": "TF"},
    {"q": "여행 계획을 세울 때 나는?", "options": ["시간 단위로 꼼꼼하게 일정을 짠다", "큰 틀만 잡고 상황에 맞춰 움직인다"], "type": "JP"},
    {"q": "과제를 수행할 때 나의 스타일은?", "options": ["미리미리 계획을 세워 일찍 끝낸다", "마감 직전 몰입해서 한 번에 처리한다"], "type": "JP"},
    {"q": "정리 정돈에 대해 어떻게 생각하나요?", "options": ["항상 제자리에 있어야 마음이 편하다", "어느 정도 어질러져 있어도 신경 쓰지 않는다"], "type": "JP"},
]

results_info = {
    "ISTJ": {"theme": "정갈한 서재", "desc": "신뢰할 수 있고 성실한 현실주의자"},
    "ISFJ": {"theme": "따뜻한 코튼향 세탁실", "desc": "소중한 사람들을 지키는 헌신적인 조력자"},
    "INFJ": {"theme": "별이 빛나는 밤의 숲", "desc": "통찰력 있는 선구자이자 이상주의자"},
    "INTJ": {"theme": "미니멀한 대리석 공간", "desc": "냉철한 전략가이자 독립적인 분석가"},
    "ISTP": {"theme": "빈티지 차고와 공구", "desc": "도구를 잘 다루는 유연한 기술자"},
    "ISFP": {"theme": "수채화 물감이 묻은 캔버스", "desc": "겸손한 예술가이자 감수성이 풍부한 사람"},
    "INFP": {"theme": "구름 위 보라색 노을", "desc": "낭만적인 이상가이자 마음이 따뜻한 열정가"},
    "INTP": {"theme": "복잡한 수식이 적힌 칠판", "desc": "끊임없이 탐구하는 철학적인 분석가"},
    "ESTP": {"theme": "활기찬 도시의 네온사인", "desc": "모험을 즐기는 수완 좋은 활동가"},
    "ESFP": {"theme": "화려한 축제와 비눗방울", "desc": "인생을 즐길 줄 아는 밝고 쾌활한 연예인"},
    "ENFP": {"theme": "알록달록한 솜사탕 동산", "desc": "상상력이 풍부하고 사람을 좋아하는 활동가"},
    "ENTP": {"theme": "아이디어가 넘치는 작업실", "desc": "도전적인 혁신가이자 똑똑한 변론가"},
    "ESTJ": {"theme": "정돈된 사무실과 다이어리", "desc": "질서를 중시하는 유능한 관리자"},
    "ESFJ": {"theme": "갓 구운 빵 냄새가 나는 카페", "desc": "주변을 잘 챙기는 친절한 협력자"},
    "ENFJ": {"theme": "햇살이 내리쬐는 온실 가든", "desc": "사람들을 이끄는 따뜻한 리더"},
    "ENTJ": {"theme": "높은 건물에서 내려다보는 야경", "desc": "비전을 제시하는 단호한 통치자"},
}

def update_score(char):
    st.session_state.scores[char] += 1
    st.session_state.step += 1

def calculate_mbti(s):
    res = ""
    res += "E" if s["E"] >= s["I"] else "I"
    res += "S" if s["S"] >= s["N"] else "N"
    res += "T" if s["T"] >= s["F"] else "F"
    res += "J" if s["J"] >= s["P"] else "P"
    return res

def main():
    st.markdown("<h1>✨ MBTI 감성 테스트 ✨</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: #9e9e9e;'>나에게 어울리는 파스텔 테마를 찾아보세요.</p>", unsafe_allow_html=True)
    
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    if st.session_state.step < len(questions):
        current_q = questions[st.session_state.step]
        
        st.markdown(f"""
        <div class="question-box">
            <p style='font-size: 14px; color: #ce93d8;'>Q{st.session_state.step + 1} / {len(questions)}</p>
            <h3 style='margin-top: 0;'>{current_q['q']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(current_q['options'][0], key=f"q{st.session_state.step}_opt1"):
                update_score(current_q['type'][0])
                st.rerun()
        with col2:
            if st.button(current_q['options'][1], key=f"q{st.session_state.step}_opt2"):
                update_score(current_q['type'][1])
                st.rerun()
                
        progress = (st.session_state.step) / len(questions)
        st.progress(progress)

    else:
        mbti = calculate_mbti(st.session_state.scores)
        result_info = results_info.get(mbti)
        
        st.balloons()
        st.markdown(f"<div class='question-box' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: #7986cb;'>당신의 유형은 {mbti} 입니다!</h2>", unsafe_allow_html=True)
        st.write(f"**{result_info['desc']}**")
        st.markdown("<hr style='border: 0.5px solid #fce4ec;'>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #9c27b0; font-weight: bold;'>추천 이미지 테마: {result_info['theme']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("다시 검사하기"):
            st.session_state.step = 0
            st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
            st.rerun()

if __name__ == "__main__":
    main()
