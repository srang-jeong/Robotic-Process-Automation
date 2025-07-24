import streamlit as st
import pandas as pd
import feedparser
from urllib.parse import quote
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import os
from googletrans import Translator
from fpdf import FPDF
from io import BytesIO

# 1. 모델 로딩
@st.cache_resource
def load_models():
    summarizer = SentenceTransformer("jhgan/ko-sroberta-multitask")
    sentiment_ko = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment_en = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    okt = Okt()
    return summarizer, sentiment_ko, sentiment_en, okt

summarizer, sentiment_ko, sentiment_en, okt = load_models()
translator = Translator()

# 기본 설정
st.set_page_config(page_title="🧠 AI 요약 뉴스 대시보드", layout="wide")
st.title("📰 AI 뉴스 요약 대시보드")
st.caption("요약 · 감정분석 · 키워드 추출 · 감정분포 · 시계열 · PDF 저장까지 한 번에")

# 필터
KEYWORDS = ["AI", "로봇", "로봇성격", "로봇감정", "IT"]
selected_keywords = st.sidebar.multiselect("🔎 키워드 선택", KEYWORDS, default=KEYWORDS)
extra_kw = st.sidebar.text_input("➕ 추가 키워드 (쉼표로 구분)")
if extra_kw:
    selected_keywords += [kw.strip() for kw in extra_kw.split(",") if kw.strip()]
lang_option = st.sidebar.radio("🌍 언어", ["한국어", "영어"])
max_items = st.sidebar.slider("📰 키워드당 뉴스 수", 1, 10, 5)
start_date = st.sidebar.date_input("📅 시작 날짜", None)
end_date = st.sidebar.date_input("📅 종료 날짜", None)
view_type = st.sidebar.radio("🗂 보기 방식", ["카드뷰", "표"])

if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []

# 유틸 함수
def clean_text(html):
    return BeautifulSoup(html, "html.parser").get_text(separator=" ").strip()

def summarize(text, num_sent=2):
    sentences = clean_text(text).replace('!','.').split('. ')
    if len(sentences) <= num_sent: return ' '.join(sentences)
    emb = summarizer.encode(sentences)
    center = emb.mean(axis=0)
    scores = [util.pytorch_cos_sim([center],[e])[0][0] for e in emb]
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:num_sent]
    return '. '.join([sentences[i] for i in sorted(top_idx)])

def extract_keywords(text, n=5):
    nouns = [w for w in okt.nouns(clean_text(text)) if len(w) > 1]
    freq = pd.Series(nouns).value_counts() if nouns else pd.Series([])
    return ', '.join(freq[:n].index) if not freq.empty else ''

def get_sentiment(text, lang="ko"):
    try:
        if lang == "ko":
            result = sentiment_ko(text[:256])
            return result[0]["label"]
        else:
            result = sentiment_en(text)
            return {"POSITIVE":"긍정", "NEGATIVE":"부정"}.get(result[0]["label"], "중립")
    except:
        return "중립"

def fetch_news(keyword, lang="ko"):
    q = quote(keyword)
    base = f"https://news.google.com/rss/search?q={q}&hl={lang}&gl=KR&ceid=KR:{lang}"
    feed = feedparser.parse(base)
    items = []
    for entry in feed.entries[:max_items]:
        title = entry.title
        link = entry.link
        raw_summary = entry.summary if hasattr(entry, "summary") else title
        date = entry.get("published", datetime.now().strftime("%Y-%m-%d"))
        summary = clean_text(raw_summary)
        if lang == "en":
            summary = translator.translate(summary, dest="ko").text
        sumy = summarize(summary)
        keywords = extract_keywords(summary)
        senti = get_sentiment(summary, lang="ko")
        items.append({
            "키워드": keyword, "제목": title, "링크": link, "날짜": date,
            "요약": sumy, "키워드추출": keywords, "감정": senti
        })
    return pd.DataFrame(items)

df_list = [fetch_news(k, lang="ko" if lang_option=="한국어" else "en") for k in selected_keywords]
news_df = pd.concat(df_list).drop_duplicates(subset="링크")
news_df["날짜"] = pd.to_datetime(news_df["날짜"], errors="coerce")

if start_date:
    news_df = news_df[news_df["날짜"] >= pd.to_datetime(start_date)]
if end_date:
    news_df = news_df[news_df["날짜"] <= pd.to_datetime(end_date)]

senti_emoji = {'긍정':'🟢', '부정':'🔴', '중립':'🟡'}
news_df["감정이모지"] = news_df["감정"].map(senti_emoji)

# ✅ 총 뉴스 건수 표시
st.markdown(f"### 📊 총 뉴스 건수: {len(news_df)}건")
if news_df.empty:
    st.warning("데이터가 없습니다. 키워드나 날짜 필터를 확인하세요.")
    st.stop()

# 시각화
with st.expander("📈 트렌드 분석"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👍👎 감정 분포")
        st.plotly_chart(px.pie(news_df, names="감정"))
    with col2:
        st.subheader("🔥 인기 키워드")
        all_kws = ",".join(news_df["키워드추출"].dropna().values).split(",")
        kw_freq = pd.Series([k.strip() for k in all_kws if k.strip()]).value_counts().head(10)
        st.bar_chart(kw_freq)

    st.subheader("📆 감정 시계열")
    emo_day = news_df.groupby([news_df["날짜"].dt.date, "감정"]).size().unstack().fillna(0)
    st.line_chart(emo_day)

# 키워드별 감정 비교
with st.expander("🆚 키워드 감정 비교"):
    compare_kw = st.multiselect("비교할 키워드를 선택", news_df["키워드"].unique())
    if compare_kw:
        df_comp = news_df[news_df["키워드"].isin(compare_kw)]
        fig = px.histogram(df_comp, x="감정", color="키워드", barmode="group")
        st.plotly_chart(fig)

# 뉴스 출력
st.markdown("## 🗞 뉴스 목록")
if view_type == "카드뷰":
    for _, row in news_df.iterrows():
        with st.container():
            st.markdown(f"### 📰 [{row['제목']}]({row['링크']})")
            st.caption(f"📅 {row['날짜'].date()}")
            st.markdown(f"🧾 {row['요약']}")
            senti = row["감정"]
            emoji = senti_emoji.get(senti, "")
            st.markdown(f"**감정:** {emoji} {senti}")
            st.markdown(f"`{row['키워드추출']}`")
            if row["감정"] == "부정":
                st.warning("🚨 이 뉴스는 부정적인 감정으로 분류되었습니다.")
            # ✅ 고유성 보장: 키에 row의 링크 해시 사용!
            key = f"bm_{abs(hash(row['링크']))}"
            if st.button("⭐ 북마크", key=key):
                if row["링크"] not in st.session_state["bookmarks"]:
                    st.session_state["bookmarks"].append(row["링크"])
else:
    st.dataframe(news_df[["키워드","제목","날짜","요약","감정","링크"]], use_container_width=True)

# 북마크 보기 및 PDF 저장
with st.expander("📩 북마크 뉴스 + PDF 저장"):
    bm_df = news_df[news_df["링크"].isin(st.session_state["bookmarks"])]
    if not bm_df.empty:
        st.write("⭐ 북마크 뉴스:")
        for _, row in bm_df.iterrows():
            st.markdown(f"- [{row['제목']}]({row['링크']})")
        if st.button("📄 북마크 뉴스 PDF 만들기"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_font_size(14)
            pdf.cell(200, 10, txt="북마크 뉴스 요약", ln=1, align='C')
            pdf.set_font_size(10)
            for _, row in bm_df.iterrows():
                entry = (
                    "📰 제목     : " + row['제목'] + "\n"
                    + "🧾 요약     : " + row['요약'] + "\n"
                    + "🏷️ 키워드   : " + row['키워드추출'] + "\n"
                    + "❤️ 감정     : " + row['감정'] + " " + senti_emoji.get(row['감정'], "") + "\n"
                    + "🔗 링크     : " + row['링크'] + "\n"
                    + "------------------------------------------------------------\n"
                )
                pdf.multi_cell(0, 10, entry)
            temp = BytesIO()
            pdf.output(temp)
            st.download_button("⬇️ PDF 다운로드", data=temp.getvalue(), file_name="북마크_뉴스.pdf")
    else:
        st.info("📌 북마크한 뉴스가 없습니다. 뉴스 옆 ⭐ 버튼으로 저장해보세요.")