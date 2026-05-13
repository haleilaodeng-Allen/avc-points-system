import streamlit as st
import pandas as pd
from datetime import timedelta

st.markdown("""
<style>

.main {
    background-color: #f5f1eb;
}

h1 {
    color: #2c2c2c;
    text-align: center;
    font-size: 48px;
}

.stButton>button {
    background-color: #b79b6c;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 20px;
    border: none;
}

.stSelectbox label,
.stDateInput label,
.stNumberInput label {
    font-size: 18px;
    color: #444;
}

</style>
""", unsafe_allow_html=True)

st.title("AVC Luxury Points System")

EXCEL_FILE = "AVC_Master_Points_Database.xlsx.xlsx"

st.title("AVC 积分查询系统")

df = pd.read_excel(EXCEL_FILE)

df.columns = [
    "Resort",
    "Room Type",
    "Start Date",
    "End Date",
    "Day Group",
    "Points"
]

df["Start Date"] = pd.to_datetime(df["Start Date"]).dt.date
df["End Date"] = pd.to_datetime(df["End Date"]).dt.date

resort = st.selectbox("选择度假村", sorted(df["Resort"].dropna().unique()))

room_df = df[df["Resort"] == resort]

room_type = st.selectbox(
    "选择房型",
    sorted(room_df["Room Type"].dropna().unique())
)

check_in = st.date_input("入住日期")

nights = st.number_input("入住晚数", min_value=1, max_value=30, value=5)

if st.button("查询积分"):
    results = []

    for i in range(nights):
        current_date = check_in + timedelta(days=i)
        weekday = current_date.strftime("%a")

        matched = df[
            (df["Resort"] == resort) &
            (df["Room Type"] == room_type) &
            (df["Start Date"] <= current_date) &
            (df["End Date"] >= current_date)
        ]

        point = None

        for _, row in matched.iterrows():
            day_group = str(row["Day Group"])

            if "Mon-Sun" in day_group or weekday in day_group:
                point = row["Points"]
                break

        results.append({
            "日期": current_date,
            "星期": weekday,
            "度假村": resort,
            "房型": room_type,
            "积分": point if point is not None else "没有找到"
        })

    result_df = pd.DataFrame(results)

    st.subheader("查询结果")
    st.dataframe(result_df, use_container_width=True)

    valid_points = pd.to_numeric(result_df["积分"], errors="coerce")
    total_points = valid_points.sum()

    st.success(f"总积分：{int(total_points)} 点")

st.divider()
st.subheader("数据库预览")
st.dataframe(df, use_container_width=True)