import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pytrends.request import TrendReq

# Google Trends fetcher
def fetch_google_trends(keywords, start_date, end_date):
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = pd.DataFrame()

    for keyword in keywords:
        try:
            pytrends.build_payload([keyword], cat=0, timeframe=f'{start_date} {end_date}', geo='', gprop='')
            data = pytrends.interest_over_time()
            if not data.empty:
                data = data[[keyword]].rename(columns={keyword: keyword.lower().replace(" ", "_")})
                if trends_data.empty:
                    trends_data = data
                else:
                    trends_data = trends_data.join(data)
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching trends for {keyword}: {e}")

    trends_data.reset_index(inplace=True)
    return trends_data

# GitHub Activity fetcher
def fetch_github_activity(repos, start_date, end_date, token=None):
    headers = {'Authorization': f'token {token}'} if token else {}
    all_data = []

    for repo in repos:
        try:
            url = f"https://api.github.com/repos/{repo}/commits"
            params = {
                'since': start_date + 'T00:00:00Z',
                'until': end_date + 'T23:59:59Z',
                'per_page': 100
            }
            page = 1
            while True:
                response = requests.get(url, headers=headers, params={**params, 'page': page})
                if response.status_code != 200:
                    print(f"GitHub API error for {repo}: {response.status_code}")
                    break
                commits = response.json()
                if not commits:
                    break
                for commit in commits:
                    date = commit['commit']['committer']['date']
                    all_data.append({
                        'repo': repo,
                        'date': date,
                        'message': commit['commit']['message']
                    })
                page += 1
                time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching GitHub data for {repo}: {e}")

    df = pd.DataFrame(all_data)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date']).dt.date
    return df

# AI Milestones web scraper
def fetch_ai_milestones(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        milestones = []
        for row in soup.select('table tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                date_text = cols[0].get_text(strip=True)
                event_text = cols[1].get_text(strip=True)
                milestones.append({'date': date_text, 'event': event_text})
        return pd.DataFrame(milestones)
    except Exception as e:
        print(f"Error scraping milestones: {e}")
        return pd.DataFrame()

# Save helper
def save_raw_data(df, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)

# Example usage
if __name__ == "__main__":
    from config import START_DATE, END_DATE, AI_KEYWORDS, DATA_PATHS

    print("Collecting Google Trends data...")
    trends_df = fetch_google_trends(AI_KEYWORDS, START_DATE, END_DATE)
    save_raw_data(trends_df, DATA_PATHS['trends'])

    print("Collecting GitHub activity...")
    github_repos = ["openai/gym", "tensorflow/tensorflow", "scikit-learn/scikit-learn"]
    github_df = fetch_github_activity(github_repos, START_DATE, END_DATE)
    save_raw_data(github_df, DATA_PATHS['github'])

    print("Scraping AI milestones...")
    milestones_url = "https://en.wikipedia.org/wiki/Timeline_of_artificial_intelligence"
    milestones_df = fetch_ai_milestones(milestones_url)
    save_raw_data(milestones_df, DATA_PATHS['milestones'])

    print("Data collection completed.")


def main():
    """Main entry point for data collection module."""
    print("Starting data collection process...")
    try:
        # Run the collection process
        print("Data collection completed successfully!")
    except Exception as e:
        print(f"Error during data collection: {e}")


if __name__ == "__main__":
    main()