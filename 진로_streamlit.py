import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="어휘카드 엑셀 변환기", layout="centered")

st.title("📚 단어 : 뜻 → 엑셀 변환기")
st.markdown("""
**사용 방법**  
1️⃣ 아래 텍스트창에 `단어 : 뜻` 형식으로 한 줄에 하나씩 입력  
2️⃣ '엑셀 만들기' 버튼 클릭  
3️⃣ 오른쪽에 나타난 '다운로드' 버튼으로 .xlsx 파일 저장  
""")

raw = st.text_area("단어 : 뜻 목록을 붙여넣으세요", height=200,
                   placeholder="예) 고요하다 : 아무 소리도 없이 조용하다")

if st.button("엑셀 만들기"):
    try:
        # 줄 단위로 파싱
        rows = [line.split(":", 1) for line in raw.strip().splitlines() if ":" in line]
        df = pd.DataFrame(rows, columns=["단어", "뜻"]).applymap(str.strip)

        # 엑셀을 메모리 버퍼에 저장
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="어휘카드")
        st.success(f"✅ {len(df)}개 단어가 변환되었습니다!")

        # 다운로드 버튼 제공
        st.download_button(label="엑셀 다운로드", data=buffer.getvalue(),
                           file_name="어휘카드.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.dataframe(df)  # 미리보기
    except Exception as e:
        st.error(f"⚠️ 변환 중 오류: {e}")
