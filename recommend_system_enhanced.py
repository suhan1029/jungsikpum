from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df1 = pd.read_csv('food.csv')
df2 = pd.read_csv('greenbia.csv')

def classify_bmi(bmi):
    if bmi < 18.5:
        return 0
    elif 18.5 <= bmi < 23.0:
        return 1
    elif 23.0 <= bmi < 25.0:
        return 2
    elif 25.0 <= bmi < 30.0:
        return 3
    elif 30.0 <= bmi < 35.0:
        return 4
    else:
        return 5

def exercise(exercise_minute):
    if exercise_minute < 30:
        return 1
    elif 30 <= exercise_minute <= 40:
        return 2
    else:
        return 3

def ages(age):
    if age >= 65:
        return 2
    elif age >= 14:
        return 1
    elif age <= 13:
        return 3

def create_nutrition_radar_chart(food_data, food_name):
    """영양소 레이더 차트 생성"""
    categories = ['총 열량', '나트륨', '탄수화물', '당류', '지방', '단백질']
    values = [food_data[cat] for cat in categories if cat in food_data.index]
    
    # 값이 없으면 빈 차트 반환
    if not values:
        return go.Figure()
    
    fig = go.Figure()
    
    # 메인 데이터
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories[:len(values)],
        fill='toself',
        name=food_name,
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.3)',
        marker=dict(size=8, color='#667eea', symbol='circle')
    ))
    
    # 배경 원형 그리드 추가
    fig.add_trace(go.Scatterpolar(
        r=[max(values) * 0.8] * len(categories[:len(values)]) if values else [0],
        theta=categories[:len(values)],
        mode='lines',
        line=dict(color='rgba(102, 126, 234, 0.1)', width=1, dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255,255,255,0.05)',
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.2] if values else [0, 100],
                gridcolor='rgba(102, 126, 234, 0.2)',
                gridwidth=1,
                tickfont=dict(size=10, color='#667eea'),
                tickcolor='rgba(102, 126, 234, 0.3)'
            ),
            angularaxis=dict(
                gridcolor='rgba(102, 126, 234, 0.2)',
                gridwidth=1,
                tickfont=dict(size=11, color='#333', family='Segoe UI'),
                linecolor='rgba(102, 126, 234, 0.3)'
            )
        ),
        showlegend=False,
        title=dict(
            text=f"🍽️ {food_name} 영양소 분석",
            x=0.5,
            font=dict(size=14, color='#333', family='Segoe UI', weight='bold')
        ),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Segoe UI, sans-serif")
    )
    
    return fig

def display_food_recommendations(df, title, emoji, color_scheme):
    """음식 추천을 카드 형태로 표시"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color_scheme[0]} 0%, {color_scheme[1]} 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        "></div>
        <h3 style="position: relative; z-index: 2; font-size: 2rem; margin: 0;">{emoji} {title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 상위 3개 음식에 대한 개선된 카드 표시
    for idx, (_, row) in enumerate(df.head(3).iterrows()):
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            border-left: 5px solid {color_scheme[0]};
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                right: 0;
                width: 100px;
                height: 100px;
                background: linear-gradient(135deg, {color_scheme[0]}, {color_scheme[1]});
                border-radius: 0 20px 0 100px;
                opacity: 0.1;
            "></div>
            <h4 style="
                color: {color_scheme[0]}; 
                margin-bottom: 1.5rem;
                font-size: 1.5rem;
                position: relative;
                z-index: 2;
            ">
                🏆 {idx + 1}위: {row['제품명']}
            </h4>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # 영양소 레이더 차트
            fig = create_nutrition_radar_chart(row, row['제품명'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 영양소 정보를 한 줄로 간결하게 표시
            nutrition_data = []
            icons = {
                '총 열량': '⚡',
                '나트륨': '🧂',
                '탄수화물': '🍞',
                '당류': '🍯',
                '지방': '🥑',
                '단백질': '🥩'
            }

            for nutrient in ['총 열량', '나트륨', '탄수화물', '당류', '지방', '단백질']:
                if nutrient in row.index:
                    nutrition_data.append(
                        (icons.get(nutrient, '📊'), nutrient, row[nutrient])
                    )

            # 레이아웃을 가로형 그리드로 구성해 공간 활용도 향상
            nutrition_html = (
                '<div style="display:grid; grid-template-columns:'
                ' repeat(auto-fit, minmax(120px,1fr)); gap:0.4rem; '
                'margin-top:1rem;">'
            )

            for icon, nutrient, value in nutrition_data:
                nutrition_html += f'''
                <div style="
                    background: linear-gradient(135deg, {color_scheme[0]}20, {color_scheme[1]}20);
                    padding: 0.4rem 0.6rem;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 600;
                    color: #333;
                    border: 1px solid {color_scheme[0]}40;
                    text-align: center;
                ">
                    {icon} {nutrient}: <strong>{value}</strong>
                </div>
                '''

            nutrition_html += '</div>'
            st.markdown(nutrition_html, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 전체 데이터 테이블 (접을 수 있는 형태) - 개선된 디자인
    with st.expander(f"📋 전체 {title} 목록 보기"):
        # 개선된 테이블 스타일 - 글자 색상 개선
        st.markdown(f"""
        <style>
        .enhanced-table {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}
        .enhanced-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .enhanced-table th {{
            background: linear-gradient(135deg, {color_scheme[0]} 0%, {color_scheme[1]} 100%);
            color: white !important;
            font-weight: 700 !important;
            text-align: center;
            padding: 1rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .enhanced-table td {{
            text-align: center;
            padding: 1rem;
            border-bottom: 1px solid #e0e0e0;
            transition: all 0.3s ease;
            color: #222 !important;
            font-weight: 500 !important;
        }}
        .enhanced-table tr:nth-child(even) td {{
            background-color: #f8f9fa;
            color: #333 !important;
        }}
        .enhanced-table tr:hover td {{
            background: linear-gradient(135deg, {color_scheme[0]}15, {color_scheme[1]}15);
            color: #222 !important;
            font-weight: 600 !important;
            transform: scale(1.01);
        }}
        .enhanced-table tr:first-child td {{
            font-weight: 700 !important;
            color: #222 !important;
            background-color: #f0f8ff;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # 데이터프레임을 HTML로 변환하여 스타일 적용
        df_html = df.to_html(classes='enhanced-table', table_id='food-table', escape=False, index=False)
        st.markdown(f'<div class="enhanced-table">{df_html}</div>', unsafe_allow_html=True)

def reco1(user):
    """일반 식단 추천"""
    target_vector = np.array(list(user.values()))
    meal_data = df1.drop('제품명', axis=1)
    
    similarities = {}
    for i in range(len(meal_data)):
        sim = cosine_similarity([target_vector], [np.array(meal_data.iloc[i])])[0][0]
        name = df1['제품명'].iloc[i]
        similarities[name] = sim
    
    sorted_meals = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    recommended_df = df1[df1['제품명'].isin([i[0] for i in sorted_meals][:7])]
    
    display_food_recommendations(
        recommended_df, 
        "맞춤형 일반 식단", 
        "🍽️", 
        ["#667eea", "#764ba2"]
    )

def reco2(user2):
    """건강 보조식품 추천"""
    target_vector = np.array(list(user2.values()))
    meal_data = df2.drop('제품명', axis=1)
    
    similarities = {}
    for i in range(len(meal_data)):
        sim = cosine_similarity([target_vector], [np.array(meal_data.iloc[i])])[0][0]
        name = df2['제품명'].iloc[i]
        similarities[name] = sim
    
    sorted_meals = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    recommended_df = df2[df2['제품명'].isin([i[0] for i in sorted_meals][:3])]
    
    # 카테고리 열 제외하고 표시
    display_columns = [col for col in recommended_df.columns if col != '카테고리']
    recommended_df_display = recommended_df[display_columns]
    
    display_food_recommendations(
        recommended_df_display, 
        "건강 보조식품", 
        "🌿", 
        ["#f093fb", "#f5576c"]
    )

