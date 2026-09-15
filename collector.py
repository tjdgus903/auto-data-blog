import os
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq

def fetch_google_trending_topics():
    """
    구글 트렌드에서 한국(KR) 기준 실시간 급상승 검색어 수집
    """
    try:
        pytrends = TrendReq(hl='ko-KR', tz=540)
        # 한국 실시간 트렌드 데일리 핫토픽 가져오기
        trending_searches_df = pytrends.trending_searches(pn='south_korea')
        keywords = trending_searches_df[0].head(5).tolist() # 상위 5개 키워드 추출
        print(f"Collected Trending Keywords: {keywords}")
        return keywords
    except Exception as e:
        print(f"Error fetching Google Trends: {e}")
        # 에러 발생 시 예비 기본 키워드 반환
        return ["오늘의 주요 이슈", "실시간 경제 트렌드"]

def generate_blog_post(keywords):
    """
    수집된 구글 핫 키워드를 바탕으로 OpenAI API가 SEO 최적화 블로그 포스트 작성
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    keyword_str = ", ".join(keywords)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
    오늘은 {date_str}이야. 현재 구글에서 사람들이 가장 많이 검색하고 관심을 갖는 핫 키워드들은 다음과 같아: [{keyword_str}].
    
    이 키워드들을 자연스럽게 아우르면서, 검색엔진(SEO) 상위 노출에 최적화된 고품질 블로그 포스팅 본문을 마크다운 형식으로 작성해 줘.
    
    [작성 조건]
    1. 제목은 호기심을 유발하되 정보성 있는 형태로 H1(#)로 작성할 것.
    2. 각 키워드별 배경, 대중의 관심 이유, 그리고 시사점이나 유익한 정보를 깔끔한 H2(##), 표(Table), 리스트 형식으로 깊이 있게 분석할 것.
    3. 낚시성 글이 아니라 유익하고 전문적인 인사이트 리포트 톤을 유지할 것.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def save_markdown_file(content):
    """
    생성된 마크다운 파일을 posts/ 폴더 아래에 날짜별로 자동 저장
    """
    os.makedirs("posts", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"posts/{date_str}-google-trend-insight.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    keywords = fetch_google_trending_topics()
    post_content = generate_blog_post(keywords)
    save_markdown_file(post_content)