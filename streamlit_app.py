# streamlit_app.py

import streamlit as st

# --- 앱 기본 설정 ---
st.set_page_config(
    page_title="P의 계획",
    page_icon="🎯",
)

# --- 세션 상태(Session State) 초기화 함수 ---
# 앱이 재실행되어도 데이터를 유지하기 위해 세션 상태를 사용합니다.
def initialize_state():
    """세션 상태에 필요한 변수들을 초기화합니다."""
    # 'initialized' 키가 없으면 초기화를 진행합니다.
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.level = 1
        st.session_state.j_points = 0
        st.session_state.tasks = [
            {"name": "책 10페이지 읽기 📖", "completed": False, "points": 30},
            {"name": "20분 산책 또는 운동하기 👟", "completed": False, "points": 30},
            {"name": "내일 할 일 딱 한 가지 정하기 🤔", "completed": False, "points": 30},
        ]
        # 오늘 포인트를 이미 획득했는지 추적하는 플래그
        st.session_state.points_awarded_today = False

# --- 메인 앱 로직 ---

# 세션 상태 초기화 함수 호출
initialize_state()

# --- UI 구성 ---

# 1. 제목
st.title("🎯 P의 계획")
st.write("계획이 어려운 P 유형을 위한 최소한의 계획 챌린지! J 포인트를 모아 레벨업 해보세요.")
st.divider()

# 2. 레벨 및 J 포인트 현황판
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🌟 나의 레벨", value=f"Lv. {st.session_state.level}")
with col2:
    st.metric(label="💎 J 포인트", value=f"{st.session_state.j_points} P")

# 레벨업에 필요한 J 포인트 설정
J_POINTS_FOR_LEVEL_UP = 100
progress = st.session_state.j_points / J_POINTS_FOR_LEVEL_UP
st.progress(progress, text=f"다음 레벨까지 {J_POINTS_FOR_LEVEL_UP - st.session_state.j_points}P 남음")

st.divider()

# 3. 오늘의 계획 (To-do 리스트)
st.subheader("📝 오늘의 최소 계획")
st.write("부담 갖지 말고, 딱 3가지만 해봐요!")

# 세션 상태에 저장된 task 리스트를 순회하며 체크박스 생성
all_completed = True
for i, task in enumerate(st.session_state.tasks):
    # 체크박스의 상태가 변경되면 세션 상태의 'completed' 값도 자동으로 업데이트됩니다.
    # key를 고유하게 설정하여 각 체크박스가 자신의 상태를 기억하도록 합니다.
    is_checked = st.checkbox(
        task["name"],
        value=task["completed"],
        key=f"task_{i}"
    )
    st.session_state.tasks[i]["completed"] = is_checked
    if not is_checked:
        all_completed = False

st.divider()

# 4. 계획 완료 및 포인트 지급 로직
if all_completed:
    # 모든 계획을 완료했고, 아직 오늘 포인트를 받지 않았다면
    if not st.session_state.points_awarded_today:
        st.success("🎉 모든 계획을 완료했어요! 정말 대단해요!")
        st.balloons()

        # 포인트 계산
        points_to_add = sum(task['points'] for task in st.session_state.tasks)
        st.session_state.j_points += points_to_add
        st.session_state.points_awarded_today = True # 오늘 포인트를 지급했음을 표시

        # 레벨업 체크
        if st.session_state.j_points >= J_POINTS_FOR_LEVEL_UP:
            st.session_state.level += 1
            st.session_state.j_points -= J_POINTS_FOR_LEVEL_UP # 레벨업에 사용된 포인트 차감
            st.info(f"**✨ 레벨업! Lv.{st.session_state.level}이 되었습니다!**")
        
        # 페이지를 새로고침하여 업데이트된 포인트와 레벨을 즉시 반영
        st.rerun()
    else:
        st.info("오늘의 계획을 모두 완수했습니다. 새로운 계획은 내일 다시 시작해주세요!")

# 5. 다음 날을 위한 초기화 버튼
st.subheader("🔄 새로운 하루 시작")
if st.button("새로운 계획 시작하기"):
    # 모든 task의 'completed' 상태를 False로 변경
    for task in st.session_state.tasks:
        task['completed'] = False
    # 포인트 획득 플래그 초기화
    st.session_state.points_awarded_today = False
    st.success("새로운 하루가 시작되었습니다. 오늘의 계획에 도전해보세요!")
    # 페이지 새로고침
    st.rerun()