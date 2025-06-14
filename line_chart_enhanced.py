import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def line_chart():
    date_list = pd.date_range(end=pd.Timestamp.today().normalize(), periods=8).strftime("%Y-%m-%d").tolist()
    date_list2 = pd.date_range(end=date_list[0], periods=8).strftime("%Y-%m-%d").tolist()

    df = pd.read_csv('patient_info.csv')
    df['측정일'] = pd.to_datetime(df['측정일'])

    df2 = df[df['측정일'].isin(date_list)]  # 지난주 + 오늘 데이터
    df3 = df[df['측정일'].isin(date_list2)]  # 지지난주 데이터

    # 개선된 지표 요약 카드들
    cols = st.columns(len(df2.columns[1:]))
    
    for idx, column in enumerate(df2.columns[1:]):
        bb_info = round(df3[column].mean(), 1)
        b_info = round(df2[column].mean(), 1)
        change = round((b_info - bb_info) / bb_info * 100, 1) if bb_info != 0 else 0
        
        # 변화 상태 결정
        if change > 0:
            status = "증가"
            color = "#ff6b6b"
            icon = "📈"
        elif change < 0:
            status = "감소"
            color = "#51cf66"
            icon = "📉"
        else:
            status = "유지"
            color = "#339af0"
            icon = "➡️"
        
        with cols[idx]:
            st.markdown(f"""
            <div style="
                background: white;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
                border-left: 4px solid {color};
                margin-bottom: 1rem;
            ">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #333; margin: 0.5rem 0;">
                    {column}
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {color};">
                    {b_info}
                </div>
                <div style="font-size: 0.8rem; color: #666;">
                    2주 전 대비 {abs(change)}% {status}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 인터랙티브 차트 생성
    df2_reset = df2.reset_index()
    df2_reset['측정일'] = pd.to_datetime(df2_reset['측정일'])
    
    # 다중 지표 차트 생성
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=list(df2.columns[1:]),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
    
    for idx, column in enumerate(df2.columns[1:]):
        row = (idx // 2) + 1
        col = (idx % 2) + 1
        
        fig.add_trace(
            go.Scatter(
                x=df2_reset['측정일'],
                y=df2_reset[column],
                mode='lines+markers',
                name=column,
                line=dict(color=colors[idx], width=3),
                marker=dict(size=8, color=colors[idx]),
                hovertemplate=f'<b>{column}</b><br>날짜: %{{x}}<br>값: %{{y}}<extra></extra>'
            ),
            row=row, col=col
        )
    
    # 차트 레이아웃 업데이트
    fig.update_layout(
        height=600,
        showlegend=False,
        title={
            'text': '📊 주간 건강 지표 변화 추이',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#333'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Segoe UI, sans-serif")
    )
    
    # 각 서브플롯 스타일링
    for i in range(1, 5):
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            row=(i-1)//2 + 1,
            col=(i-1)%2 + 1
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            row=(i-1)//2 + 1,
            col=(i-1)%2 + 1
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 추가 인사이트 카드
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    ">
        <h4>💡 건강 인사이트</h4>
        <p>지난 주간의 건강 지표를 분석한 결과, 전반적인 건강 상태의 변화를 확인할 수 있습니다. 
        지속적인 모니터링을 통해 개인 맞춤형 건강 관리 계획을 수립하는 것이 중요합니다.</p>
    </div>
    """, unsafe_allow_html=True)

