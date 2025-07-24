import streamlit as st
import pandas as pd
import feedparser
from urllib.parse import quote
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from sentence_transformers import SentenceTransformer, util
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from newspaper import Article
import nltk
from fpdf import FPDF
from io import BytesIO

nltk.download('punkt')

@st.cache_resource
def load_models():
    summarizer = SentenceTransformer("jhgan/ko-sroberta-multitask")
    okt = Okt()
    return summarizer, okt

summarizer, okt = load_models()

# 페이지 설정
st.set_page_config(page_title="뉴스 요약 대시보드", layout="wide")
st.title("🧠🛠️🕹️ AI/로봇 뉴스 요약 대시보드")

# 사이드바
st.sidebar.header("🔍 뉴스 수집 조건")
KEYWORDS = ["AI", "로봇", "로봇감정", "로봇성격", "IT", "산업데이터", "데이터시스템"]
selected_keywords = st.sidebar.multiselect("키워드 선택", KEYWORDS, default=KEYWORDS)
extra_kw = st.sidebar.text_input("➕ 추가 키워드 (쉼표 구분)")
if extra_kw:
    selected_keywords += [kw.strip() for kw in extra_kw.split(",") if kw.strip()]
lang_option = st.sidebar.radio("🌍 뉴스 언어", ["한국어", "영어"])
max_items = st.sidebar.slider("📰 키워드별 뉴스 수", 1, 15, 5)
start_date = st.sidebar.date_input("📅 시작일", None)
end_date = st.sidebar.date_input("📅 종료일", None)

# 뉴스 본문 정제
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

# 콘텐츠 톤 분석
def analyze_tone(text):
    if len(text) > 1000 and any(word in text for word in ["우려", "논란", "환영", "논의", "과제"]):
        return "분석적"
    elif any(word in text for word in ["슬프다", "기쁘다", "충격", "감동", "분노"]):
        return "감정적"
    else:
        return "정보성"

# 태그 생성
def generate_tags(text):
    tags = []
    if "기술" in text:
        tags.append("#기술동향")
    if "시장" in text or "수요" in text:
        tags.append("#시장분석")
    if "논란" in text or "문제" in text:
        tags.append("#이슈")
    return " ".join(tags) if tags else "#일반"

# 뉴스 본문 가져오기
@st.cache_data(show_spinner=True)
def get_article_text(url, lang="ko"):
    try:
        article = Article(url, language='ko' if lang == "한국어" else 'en')
        article.download()
        article.parse()
        return article.text.strip()
    except:
        return ""

# 뉴스 크롤링
@st.cache_data(show_spinner=True)
def fetch_news(keyword, lang="ko", max_items=5):
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
            tone = analyze_tone(fulltext)
            tags = generate_tags(fulltext)
            articles.append({
                "키워드": keyword, "제목": title, "링크": link, "날짜": date,
                "본문": fulltext, "요약": summary, "키워드추출": keywords,
                "콘텐츠톤": tone, "태그": tags
            })
        except:
            continue
    return pd.DataFrame(articles)

# 수집
lang_code = "ko" if lang_option == "한국어" else "en"
df_list = [fetch_news(k, lang=lang_code, max_items=max_items) for k in selected_keywords]
if df_list:
    news_df = pd.concat(df_list).drop_duplicates(subset=["링크"])
else:
    news_df = pd.DataFrame()

# 날짜 필터
if not news_df.empty:
    news_df["날짜"] = pd.to_datetime(news_df["날짜"], errors="coerce")
    if start_date:
        news_df = news_df[news_df["날짜"] >= pd.to_datetime(start_date)]
    if end_date:
        news_df = news_df[news_df["날짜"] <= pd.to_datetime(end_date)]

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📰 뉴스 목록 보기", "📊 통계 시각화", "📁 북마크 및 PDF"])

with tab1:
    st.subheader("📰 수집된 뉴스")
    if not news_df.empty:
        if "bookmarks" not in st.session_state:
            st.session_state["bookmarks"] = []

        for i, row in news_df.iterrows():
            unique_key = f"{hash(row['링크'])}"
            st.markdown(f"### [{row['제목']}]({row['링크']})")
            st.caption(f"📅 {row['날짜'].date()} | 톤: `{row['콘텐츠톤']}` | {row['태그']}")
            st.markdown(f"🧾 요약: {row['요약']}")
            st.markdown(f"`{row['키워드추출']}`")
            if st.button("⭐ 북마크", key=f"bookmark_{unique_key}"):
                if row["링크"] not in st.session_state["bookmarks"]:
                    st.session_state["bookmarks"].append(row["링크"])

    else:
        st.info("뉴스 데이터를 찾을 수 없습니다.")

with tab2:
    st.subheader("📊 뉴스 통계 및 워드클라우드")
    if not news_df.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("#### 키워드별 뉴스 수")
            st.bar_chart(news_df["키워드"].value_counts())

            st.markdown("#### 콘텐츠 톤 분포")
            st.plotly_chart(px.histogram(news_df, x="키워드", color="콘텐츠톤", barmode="group"))

        with col2:
            st.markdown("#### ☁️ 워드클라우드")
            all_kws = ", ".join(news_df["키워드추출"].dropna())
            try:
                font_path = "C:/Windows/Fonts/malgun.ttf"
                wc = WordCloud(font_path=font_path, width=400, height=300, background_color='white').generate(all_kws)
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
            except:
                st.warning("⚠️ 워드클라우드 생성 실패. 폰트 경로 확인 필요")
    else:
        st.info("데이터가 없습니다.")

with tab3:
    st.subheader("📁 북마크 및 PDF 저장")
    if "bookmarks" in st.session_state:
        bm_df = news_df[news_df["링크"].isin(st.session_state["bookmarks"])]
        if not bm_df.empty:
            for _, row in bm_df.iterrows():
                st.markdown(f"- [{row['제목']}]({row['링크']})")
            if st.button("⬇️ PDF 다운로드"):
                pdf = FPDF()
                pdf.add_page()
                font_path = "C:/Windows/Fonts/malgun.ttf"
                pdf.add_font('Malgun', '', font_path, uni=True)
                pdf.set_font('Malgun', '', 12)
                pdf.cell(200, 10, "북마크 뉴스 요약", 0, 1, 'C')

                for _, row in bm_df.iterrows():
                    entry = (
                        f"📰 제목: {row['제목']}\n"
                        f"🧾 요약: {row['요약']}\n"
                        f"📚 본문: {row['본문'][:300]}...\n"
                        f"🏷️ 키워드: {row['키워드추출']}\n"
                        f"🌀 톤: {row['콘텐츠톤']}\n"
                        f"🔖 태그: {row['태그']}\n"
                        f"🔗 링크: {row['링크']}\n"
                        + "-"*50 + "\n"
                    )
                    pdf.multi_cell(0, 10, entry)

                temp = BytesIO()
                pdf.output(temp)
                temp.seek(0)
                st.download_button("📥 PDF 저장하기", data=temp.read(), file_name="북마크_뉴스.pdf")
        else:
            st.info("📌 북마크된 뉴스가 없습니다.")