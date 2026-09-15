import os
from datetime import datetime
import requests
from openai import OpenAI

def fetch_public_data():
    """
    공공 데이터 또는 실시간 트렌드 API를 호출하여 데이터를 가져오는 함수
    """
    # 추후 원하는 공공 데이터 API 엔드포인트로 교체할 수 있습니다.
    sample_data = {
        "title": "실시간 경제 및 생활 지표 리포트",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content_summary": "최근 변동성이 큰 주요 지표 분석 데이터"
    }
    return sample_data

def generate_blog_post(data):
    """
    OpenAI API를 활용해 검색엔진(SEO) 최적화 마크다운 포스트 생성
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = f"""
    다음 데이터를 바탕으로 검색엔진 상위 노출에 최적화된 블로그 포스팅 본문을 마크다운 형식으로 작성해 줘.
    
    [데이터 정보]
    - 제목 키워드: {data['title']}
    - 기준 일자: {data['date']}
    - 핵심 내용: {data['content_summary']}
    
    [작성 조건]
    1. 정보가 유익하고 가독성이 좋도록 깔끔한 마크다운(H1, H2, 테이블, 리스트)으로 작성할 것.
    2. 광고성 멘트 없이 전문적인 분석 리포트 형태로 작성할 것.
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
    filename = f"posts/{date_str}-insight.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    data = fetch_public_data()
    post_content = generate_blog_post(data)
    save_markdown_file(post_content)