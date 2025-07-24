import streamlit as st
import pandas as pd
import feedparser
from urllib.parse import quote
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from wordcloud import WordCloud
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
from newspaper import Article
import nltk
from fpdf import FPDF
import matplotlib.font_manager as fm

nltk.download('punkt')

# 모델 로딩
@st.cache_resource
def load_models():
    summarizer = SentenceTransformer("jhgan/ko-sroberta-multitask")
    sentiment_ko = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment_en = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    okt = Okt()
    return summarizer, sentiment_ko, sentiment_en, okt

summarizer, sentiment_ko, sentiment_en, okt = load_models()

# 초기화
st.set_page_config(page_title="AI 뉴스 대시보드", layout="wide")
st.title("🧠🛠️🕹️ AI/로봇 뉴스 요약 대시보드")

# 사이드바 입력
with st.sidebar:
    st.header("🛠️ 뉴스 수집 조건")
    KEYWORDS = ["AI", "로봇", "로봇감정", "로봇성격", "IT", "산업데이터", "데이터시스템"]
    selected_keywords = st.multiselect("🔍 관심 키워드", KEYWORDS, default=["AI", "로봇", "로봇감정", "로봇성격", "IT", "산업데이터", "데이터시스템"])
    extra_kw = st.text_input("➕ 추가 키워드 (쉼표로 구분)")
    if extra_kw:
        selected_keywords += [kw.strip() for kw in extra_kw.split(",") if kw.strip()]
    lang_option = st.radio("🌍 뉴스 언어", ["한국어", "영어"])
    max_items = st.slider("📰 키워드별 최대 뉴스 수", 1, 15, 5)
    start_date = st.date_input("📅 시작일", None)
    end_date = st.date_input("📅 종료일", None)

lang_code = "ko" if lang_option == "한국어" else "en"
senti_emoji = {"긍정": "🟢", "부정": "🔴", "중립": "🟡"}

# 감성 요약
def generate_opinion(summary, sentiment):
    base = "이 뉴스는 "
    if "긍정" in sentiment:
        return base + "긍정적인 분위기를 전달합니다."
    elif "부정" in sentiment:
        return base + "비판적 시각을 보여줍니다."
    else:
        return base + "중립적인 정보를 제공합니다."

# 본문 정제
def clean_text(html):
    return BeautifulSoup(html, "html.parser").get_text(separator=" ").strip()

# 요약
def summarize(text, num_sent=3):
    if not text or len(text.strip()) < 30:
        return "요약 불가 (본문 부족)"
    sentences = [s.strip() for s in text.replace("!", ".").split(". ") if len(s.strip()) > 10]
    if len(sentences) <= num_sent:
        return text
    emb = summarizer.encode(sentences, convert_to_tensor=True)
    center = emb.mean(dim=0)
    scores = [util.pytorch_cos_sim(center, e)[0][0].item() for e in emb]
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:num_sent]
    return ". ".join([sentences[i] for i in sorted(top_idx)])

# 키워드 추출
def extract_keywords(text, n=5):
    nouns = [w for w in okt.nouns(text) if len(w) > 1]
    freq = pd.Series(nouns).value_counts()
    return ", ".join(freq.head(n).index) if not freq.empty else "키워드 없음"

# 감성분석
def get_sentiment(text, lang="ko"):
    try:
        if lang == "ko":
            result = sentiment_ko(text[:256])
            return result[0]["label"]
        else:
            result = sentiment_en(text)
            return {"POSITIVE": "긍정", "NEGATIVE": "부정"}.get(result[0]["label"], "중립")
    except:
        return "중립"

# 본문 가져오기
@st.cache_data
def get_article_text(url, lang="ko"):
    try:
        article = Article(url, language='ko' if lang == "ko" else 'en')
        article.download()
        article.parse()
        return article.text.strip()
    except:
        return ""

# 뉴스 수집
@st.cache_data
def fetch_news(keyword, lang="ko"):
    q = quote(keyword)
    rss_url = f"https://news.google.com/rss/search?q={q}&hl={lang}&gl=KR&ceid=KR:{lang}"
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:max_items]:
        try:
            title = entry.title
            link = entry.link
            date = entry.get("published", datetime.now().strftime("%Y-%m-%d"))
            preview = clean_text(entry.summary if hasattr(entry, "summary") else "")
            fulltext = get_article_text(link, lang)
            if not fulltext or len(fulltext.strip()) < 50:
                fulltext = preview
            summary = summarize(fulltext)
            keywords = extract_keywords(fulltext)
            senti = get_sentiment(fulltext, lang)
            opinion = generate_opinion(summary, senti)
            articles.append({
                "키워드": keyword, "제목": title, "링크": link, "날짜": date,
                "본문": fulltext, "요약": summary, "키워드추출": keywords,
                "감성": senti, "한줄평": opinion
            })
        except:
            continue
    return pd.DataFrame(articles)

# 데이터 수집 및 처리
df_list = [fetch_news(k, lang=lang_code) for k in selected_keywords]
news_df = pd.concat(df_list).drop_duplicates(subset=["링크"]) if df_list else pd.DataFrame()
news_df["날짜"] = pd.to_datetime(news_df["날짜"], errors="coerce")
news_df["감성이모지"] = news_df["감성"].map(senti_emoji)

# 북마크 초기화
if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📰 뉴스 목록 보기", "📊 통계 시각화", "📁 북마크 & PDF 저장"])

with tab1:
    st.subheader("📰 뉴스 목록")
    if news_df.empty:
        st.warning("뉴스 데이터가 없습니다.")
    else:
        for i, row in news_df.iterrows():
            row_key = str(hash(row["링크"]))
            st.markdown(f"### [{row['제목']}]({row['링크']})")
            st.caption(f"📅 {row['날짜'].date()}")
            st.markdown(f"🔎 키워드 추출: `{row['키워드추출']}`")
            st.markdown(f"📋 한줄평: {row['한줄평']}")
            st.markdown(f"{senti_emoji.get(row['감성'], '🟡')} 감성: {row['감성']}")
            if st.button("⭐ 북마크", key=f"bookmark_{row_key}"):
                if row["링크"] not in st.session_state["bookmarks"]:
                    st.session_state["bookmarks"].append(row["링크"])
            st.divider()

with tab2:
    st.subheader("📊 통계 시각화")
    if news_df.empty:
        st.warning("데이터 없음")
    else:
        st.markdown("### 키워드별 뉴스 건수")
        st.bar_chart(news_df["키워드"].value_counts())

        st.markdown("### 감성별 뉴스 분포")
        st.bar_chart(news_df["감성"].value_counts())

        st.markdown("### 워드클라우드")
        all_kws = ", ".join(news_df["키워드추출"].dropna())
        try:
            font_path = "C:/Windows/Fonts/malgun.ttf"
            wc = WordCloud(font_path=font_path, background_color='white', width=800, height=400).generate(all_kws)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        except:
            st.warning("⚠️ 워드클라우드 생성 실패")

with tab3:
    st.subheader("📁 북마크된 뉴스 PDF 저장")
    bm_df = news_df[news_df["링크"].isin(st.session_state["bookmarks"])]
    if bm_df.empty:
        st.info("북마크된 뉴스가 없습니다.")
    else:
        for _, row in bm_df.iterrows():
            st.markdown(f"- [{row['제목']}]({row['링크']})")
        if st.button("⬇️ PDF 다운로드"):
            pdf = FPDF()
            pdf.add_page()
            font_path = "C:/Windows/Fonts/malgun.ttf"
            pdf.add_font('Malgun', '', font_path, uni=True)
            pdf.set_font("Malgun", "", 12)
            pdf.cell(200, 10, "북마크 뉴스 목록", ln=1, align='C')
            for _, row in bm_df.iterrows():
                entry = f"제목: {row['제목']}\n요약: {row['요약']}\n한줄평: {row['한줄평']}\n링크: {row['링크']}\n\n"
                pdf.multi_cell(0, 10, entry)
            temp = BytesIO()
            pdf.output(temp)
            temp.seek(0)
            st.download_button("📄 PDF 저장", data=temp.read(), file_name="bookmarked_news.pdf")