# Machine Dashboard (จำลอง) - โปรเจกต์ฝึก IT/OT ตัวแรก
# รัน: streamlit run app.py
# ตอนนี้ใช้ข้อมูลจำลอง ภายหลังเปลี่ยนฟังก์ชัน read_machine() ให้อ่านจาก PLC จริง (Snap7 / OPC UA)

import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Machine Dashboard", layout="wide")
st.title("Machine Dashboard (ข้อมูลจำลอง)")

# ---------- ค่าเริ่มต้น (เหมือน memory ใน PLC) ----------
if "data" not in st.session_state:
    st.session_state.data = []          # ประวัติย้อนหลัง
    st.session_state.count = 0          # ตัวนับชิ้นงาน
    st.session_state.state = "RUN"      # สถานะเครื่อง RUN / STOP / ALARM
    st.session_state.downtime_s = 0     # เวลาหยุดสะสม (วินาที)
    st.session_state.start = time.time()


def read_machine():
    """จำลองการอ่านค่าจาก PLC ทุก 1 วินาที
    ขั้นต่อไป: แทนที่ส่วนนี้ด้วยการอ่าน tag จริง เช่น
    client.db_read(...) ของ Snap7 หรือ OPC UA
    """
    s = st.session_state
    r = random.random()
    if s.state == "RUN":
        if r < 0.03:
            s.state = "ALARM"
        elif r < 0.06:
            s.state = "STOP"
        else:
            s.count += random.randint(0, 2)
    else:
        s.downtime_s += 1
        if r < 0.2:
            s.state = "RUN"

    s.data.append({"time": datetime.now(), "count": s.count, "state": s.state})
    s.data = s.data[-600:]  # เก็บแค่ 10 นาทีล่าสุด


@st.fragment(run_every=1)  # อัปเดตทุก 1 วินาที (เหมือน scan cycle)
def live_panel():
    read_machine()
    s = st.session_state

    icon = {"RUN": "🟢", "STOP": "🟡", "ALARM": "🔴"}[s.state]
    elapsed = max(time.time() - s.start, 1)
    availability = 100 * (1 - s.downtime_s / elapsed)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("สถานะเครื่อง", f"{icon} {s.state}")
    c2.metric("จำนวนชิ้นงาน", s.count)
    c3.metric("เวลาหยุดสะสม (วินาที)", s.downtime_s)
    c4.metric("Availability", f"{availability:.1f}%")

    df = pd.DataFrame(s.data).set_index("time")
    st.subheader("จำนวนชิ้นงานสะสม")
    st.line_chart(df["count"])


live_panel()
