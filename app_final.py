import streamlit as st
import pandas as pd
from line_chart_enhanced import line_chart
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from recommend_system_enhanced import reco1,reco2,classify_bmi,exercise,ages

# 페이지 설정
st.set_page_config(
    page_title="AI 건강상태 보고서",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    /* Streamlit 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    
    /* 전체 배경 및 기본 스타일 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 메인 컨테이너 */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        animation: fadeIn 1s ease-out;
    }
    
    /* 헤더 스타일 */
    .header-title {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: slideInDown 0.8s ease-out;
        position: relative;
        z-index: 10;
    }
    
    .header-title::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 20px;
        z-index: -1;
        backdrop-filter: blur(10px);
    }
    
    /* 환자 정보 카드 */
    .patient-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        animation: slideInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .patient-info::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    /* 메트릭 카드 스타일 */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(102, 126, 234, 0.1);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover .metric-value {
        transform: scale(1.1);
    }
    
    .metric-label {
        color: #666;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* 섹션 제목 */
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 4px solid transparent;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-clip: border-box;
        border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
        display: inline-block;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: width 0.5s ease;
    }
    
    .section-title:hover::after {
        width: 100%;
    }
    
    /* 차트 컨테이너 */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 2rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* 추천 식단 카드 */
    .recommendation-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(245, 87, 108, 0.4);
        animation: pulse 2s infinite;
    }
    
    /* 애니메이션 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* AI 추천사항 */
    .ai-guide-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        padding: 0;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        overflow: hidden;
        position: relative;
    }
    
    .ai-guide-header {
        background: rgba(255,255,255,0.1);
        padding: 2rem;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .ai-guide-content {
        padding: 2rem;
        background: rgba(255,255,255,0.05);
    }
    
    .guide-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .guide-card {
        background: rgba(255,255,255,0.15);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .guide-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .guide-card:hover::before {
        left: 100%;
    }
    
    .guide-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    .guide-card h4 {
        font-size: 1.3rem;
        margin-bottom: 1rem;
        color: white;
    }
    
    .guide-card ul {
        list-style: none;
        padding: 0;
    }
    
    .guide-card li {
        padding: 0.5rem 0;
        color: rgba(255,255,255,0.9);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .guide-card li:hover {
        color: white;
        padding-left: 10px;
    }
    
    .ai-insight {
        background: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .ai-insight h4 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: white;
    }
    
    .ai-insight p {
        font-size: 1.1rem;
        line-height: 1.6;
        color: rgba(255,255,255,0.9);
    }
    
    /* 구분선 스타일 */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 3rem 0;
        border-radius: 2px;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        .metric-card {
            padding: 1rem;
        }
        .metric-value {
            font-size: 2rem;
        }
    }
    
    /* 스크롤바 스타일링 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# 데이터 로드
df1 = pd.read_csv('food.csv')
df2 = pd.read_csv('greenbia.csv')

# 메인 컨테이너 시작
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 헤더
st.markdown('<h1 class="header-title">🏥 AI 건강상태 보고서</h1>', unsafe_allow_html=True)

# 환자 기본 정보
height, weight = 170, 85
exercise_minute = 20
bmi = weight / ((height/100) ** 2)
bmi2 = ['저체중','정상','과체중','비만 1단계','비만 2단계','고도 비만']
disease = '암'
age = 65

# 환자 정보 카드
st.markdown(f'''
<div class="patient-info">
    <h2 style="font-size: 2.5rem; margin-bottom: 1rem; position: relative; z-index: 1;">
        👤 {age}세 {disease} 환자 ({bmi2[classify_bmi(bmi)]})
    </h2>
    <p style="font-size: 1.3rem; margin-top: 1rem; position: relative; z-index: 1; opacity: 0.9;">
        🔬 AI 기반 개인 맞춤형 건강 분석 시스템으로 생성된 종합 건강 보고서입니다
    </p>
    <div style="margin-top: 1.5rem; position: relative; z-index: 1;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
            📊 데이터 분석 완료
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
            🎯 맞춤 추천 생성
        </span>
    </div>
</div>
''', unsafe_allow_html=True)

# 메트릭 카드들
st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
    <div class="metric-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🏃‍♂️</div>
        <div class="metric-value">{height}</div>
        <div class="metric-label">키 (cm)</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚖️</div>
        <div class="metric-value">{weight}</div>
        <div class="metric-label">몸무게 (kg)</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💪</div>
        <div class="metric-value">{exercise_minute}</div>
        <div class="metric-label">일일 운동시간 (분)</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="metric-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <div class="metric-value">{bmi:.1f}</div>
        <div class="metric-label">BMI 지수</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 차트 섹션
st.markdown('<h2 class="section-title">📈 건강 지표 추이 분석</h2>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
line_chart()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('---')

# 추천 식단 섹션
st.markdown('<h2 class="section-title">🍽️ AI 맞춤형 식단 추천</h2>', unsafe_allow_html=True)

# 사용자 프로필 계산
user = {'총 열량': -(df1['총 열량'].min() * (classify_bmi(bmi)*0.1)), 
        '나트륨': -(df1['나트륨'].min() * (classify_bmi(bmi)*0.1)), 
        '탄수화물': 0, 
        '당류': -(df1['당류'].min() * (classify_bmi(bmi)*0.1)), 
        '지방': -(df1['지방'].min() * (classify_bmi(bmi)*0.1)), 
        '단백질': exercise(exercise_minute)*0.1}

user2 = {'나트륨': 0,
        '탄수화물': 0,
        '당류': -(df2['당류'].min() * (classify_bmi(bmi)*0.1)) + -((df2['당류'].min() * (classify_bmi(bmi)*0.3)) if disease == '당뇨' else 0),
        '식이섬유': 0,
        '지방': -(df2['지방'].min() * (classify_bmi(bmi)*0.1)), 
        '단백질': exercise(exercise_minute)*0.1,
        'EPA+DHA': 50 if disease == '암' else 0,
        '비타민': 20 if ages(age) == 2 else 10,
        '미네랄': 20 if ages(age) == 2 else 10,
        '카테고리': ages(age)}

# 추천 시스템 실행
reco1(user)
reco2(user2)

# AI 추천사항
with st.expander("🤖 AI 종합 건강 가이드 및 추천사항"):
    guide_style = """
    <style>
    .ai-guide-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
    }
    .guide-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .guide-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    .guide-card h4 {
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    .guide-card ul {
        list-style: none;
        padding: 0;
    }
    .guide-card li {
        margin-bottom: 0.8rem;
        padding-left: 1rem;
        position: relative;
    }
    .guide-card li:before {
        content: "•";
        color: #fff;
        font-weight: bold;
        position: absolute;
        left: 0;
    }
    .ai-insight {
        background: rgba(255,255,255,0.15);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
    }
    .ai-insight h4 {
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    </style>
    """
    st.markdown(guide_style, unsafe_allow_html=True)

    guide_html = """
    <div class="ai-guide-container">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="margin: 0; font-size: 2rem;">🎯 개인 맞춤 건강 관리 전략</h2>
        </div>

        <div class="guide-grid">
            <div class="guide-card">
                <h4>🥬 식단 관리</h4>
                <ul>
                    <li><strong>탄수화물 저감</strong> - 체중 관리 효과</li>
                    <li><strong>당류 제한</strong> - 혈당 안정화</li>
                    <li><strong>열량 조절</strong> - 건강한 체중 유지</li>
                    <li><strong>균형 잡힌 영양</strong> - 필수 영양소 공급</li>
                </ul>
            </div>

            <div class="guide-card">
                <h4>💪 운동 계획</h4>
                <ul>
                    <li><strong>유산소 운동</strong> - 주 3-4회, 30분</li>
                    <li><strong>근력 운동</strong> - 주 2-3회</li>
                    <li><strong>스트레칭</strong> - 매일 10-15분</li>
                    <li><strong>활동량 증가</strong> - 일상 속 움직임</li>
                </ul>
            </div>

            <div class="guide-card">
                <h4>🏥 건강 모니터링</h4>
                <ul>
                    <li><strong>정기 검진</strong> - 월 1회 체크</li>
                    <li><strong>혈압 측정</strong> - 주 2-3회</li>
                    <li><strong>체중 관리</strong> - 매일 기록</li>
                    <li><strong>증상 관찰</strong> - 변화 모니터링</li>
                </ul>
            </div>

            <div class="guide-card">
                <h4>🧘‍♀️ 생활 습관</h4>
                <ul>
                    <li><strong>충분한 수면</strong> - 7-8시간 권장</li>
                    <li><strong>스트레스 관리</strong> - 명상, 휴식</li>
                    <li><strong>금연/금주</strong> - 건강 위험 요소 제거</li>
                    <li><strong>수분 섭취</strong> - 하루 2L 이상</li>
                </ul>
            </div>
        </div>

        <div class="ai-insight">
            <h4>💡 AI 분석 결과</h4>
            <p>
                현재 건강 상태를 종합 분석한 결과, <strong>체계적인 식단 관리</strong>와 <strong>꾸준한 운동</strong>을 통해
                건강 지표 개선이 가능할 것으로 예상됩니다. 특히 BMI 지수와 운동량을 고려할 때,
                <strong>저탄수화물 식단</strong>과 <strong>규칙적인 유산소 운동</strong>이 가장 효과적일 것으로 분석됩니다.
                지속적인 모니터링과 함께 개인 맞춤형 관리 계획을 실천해보세요!
            </p>
        </div>
    </div>
    """
    st.components.v1.html(guide_html, height=600, scrolling=True)

# 메인 컨테이너 종료
st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; 
            background: rgba(255,255,255,0.1); border-radius: 20px; backdrop-filter: blur(10px);">
    <div style="color: white; font-size: 1.1rem; margin-bottom: 1rem;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
            🏥 AI 기반 건강 관리
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
            📊 데이터 기반 분석
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
            💪 개인 맞춤 솔루션
        </span>
    </div>
    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0;">
        Powered by Advanced AI Healthcare Analytics System
    </p>
</div>
""", unsafe_allow_html=True)

