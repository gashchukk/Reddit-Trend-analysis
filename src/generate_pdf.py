from config import *

def generate_html_report(results_file: str):
    """Generate HTML report from JSON results"""

    # Load JSON
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    niche = results['niche']
    time_window = results.get('time_window_days', 'N/A')
    trends = results['trends']
    subreddits = results['subreddits']

    # Estimate total posts collected
    total_posts = sum(t['posts'] for t in trends)

    # HTML template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reddit Trend Analysis Report - {niche}</title>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height:1.6; background:#f5f5f5; color:#333; padding:20px; }}
    .container {{ max-width: 8.5in; margin: 0 auto; background:white; padding: 40px; box-shadow:0 0 20px rgba(0,0,0,0.1); }}
    .cover {{ text-align:center; padding:100px 0; }}
    .cover h1 {{ font-size:36px; color:#1a1a1a; margin-bottom:20px; }}
    .cover .niche {{ font-size:24px; color:#666; margin-bottom:30px; }}
    .meta {{ background:#f8f9fa; padding:30px; border-radius:8px; margin:40px auto; max-width:500px; border:1px solid #dee2e6; }}
    .meta-item {{ display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid #e9ecef; }}
    .meta-item:last-child {{ border-bottom:none; }}
    .meta-label {{ font-weight:600; color:#2c3e50; }}
    .meta-value {{ color:#34495e; }}
    .executive-summary {{ background:#eef2f7; border-left:4px solid #3498db; padding:20px; margin:30px 0; border-radius:4px; }}
    .executive-summary h3 {{ color:#2c3e50; margin-bottom:12px; }}
    .section {{ margin:40px 0; }}
    .section-header {{ background:#ecf0f1; padding:15px 20px; border-left:4px solid #3498db; margin-bottom:25px; font-size:20px; font-weight:600; color:#2c3e50; }}
    table {{ width:100%; border-collapse: collapse; margin:20px 0; }}
    th {{ background:#3498db; color:white; padding:12px; text-align:left; }}
    td {{ padding:12px; border:1px solid #dee2e6; }}
    tr:nth-child(even) {{ background:#f8f9fa; }}
    .trend-item {{ background:#f8f9fa; border:1px solid #dee2e6; border-radius:8px; padding:20px; margin-bottom:20px; }}
    .trend-header {{ display:flex; align-items:baseline; margin-bottom:12px; }}
    .trend-rank {{ font-size:24px; font-weight:700; margin-right:15px; min-width:50px; }}
    .rank-1 {{ color:#d4af37; }} .rank-2 {{ color:#c0c0c0; }} .rank-3 {{ color:#cd7f32; }} .rank-other {{ color:#3498db; }}
    .trend-title {{ font-size:18px; font-weight:600; color:#2980b9; flex:1; }}
    .trend-metrics {{ display:flex; gap:25px; margin:12px 0; padding:12px; background:white; border-radius:4px; flex-wrap:wrap; }}
    .metric {{ display:flex; flex-direction:column; }}
    .metric-label {{ font-size:11px; color:#7f8c8d; text-transform:uppercase; letter-spacing:0.5px; }}
    .metric-value {{ font-size:18px; font-weight:600; color:#2c3e50; }}
    .examples {{ margin-top:15px; }}
    .examples h4 {{ font-size:13px; color:#2c3e50; margin-bottom:10px; font-weight:600; }}
    .example {{ margin:8px 0; padding-left:15px; }}
    .example a {{ color:#3498db; text-decoration:none; font-weight:500; }}
    .example a:hover {{ text-decoration:underline; }}
    .example-stats {{ font-size:12px; color:#7f8c8d; margin-left:20px; }}
    .footer {{ text-align:center; margin-top:60px; padding-top:20px; border-top:2px solid #dee2e6; color:#7f8c8d; font-size:12px; }}
</style>
</head>
<body>
<div class="container">
    <div class="cover">
        <h1>Reddit Trend Analysis Report</h1>
        <div class="niche"><strong>Niche:</strong> {niche}</div>
        <div class="meta">
            <div class="meta-item"><span class="meta-label">Time Window:</span><span class="meta-value">{time_window} days</span></div>
            <div class="meta-item"><span class="meta-label">Generated:</span><span class="meta-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span></div>
        </div>
        <div class="executive-summary">
            <h3>Executive Summary</h3>
            <p>This report presents the top trending topics and discussions discovered from Reddit communities related to the "{niche}" niche. Trends are ranked by engagement score, calculated from post frequency, upvotes, and comment activity.</p>
        </div>
    </div>

    <!-- SUBREDDITS -->
    <div class="section">
        <div class="section-header">Tracked Subreddits</div>
        <table>
            <thead>
                <tr><th>Subreddit</th><th>Reason</th></tr>
            </thead>
            <tbody>
"""

    for sub in subreddits:
        html += f"<tr><td><strong>r/{sub['name']}</strong></td><td>{sub['reason']}</td></tr>\n"

    html += f"""
            </tbody>
        </table>
        <p style="margin-top:20px; color:#7f8c8d;">Total posts analyzed (estimated from trends): {total_posts:,}</p>
    </div>

    <!-- TRENDS -->
    <div class="section">
        <div class="section-header">Top Trending Topics</div>
"""

    for i, trend in enumerate(trends, 1):
        rank_class = f"rank-{i}" if i <= 3 else "rank-other"
        rank_emoji = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else ""
        html += f"""
        <div class="trend-item">
            <div class="trend-header">
                <div class="trend-rank {rank_class}">{rank_emoji} #{i}</div>
                <div class="trend-title">{trend['theme']}</div>
            </div>
            <div class="trend-metrics">
                <div class="metric"><span class="metric-label">Trend Score</span><span class="metric-value">{trend['score']:,}</span></div>
                <div class="metric"><span class="metric-label">Posts</span><span class="metric-value">{trend['posts']}</span></div>
                <div class="metric"><span class="metric-label">Upvotes</span><span class="metric-value">{trend['upvotes']:,}</span></div>
                <div class="metric"><span class="metric-label">Comments</span><span class="metric-value">{trend['comments']:,}</span></div>
            </div>
            <div class="examples"><h4>Representative Posts:</h4>
"""
        for j, post in enumerate(trend['examples'], 1):
            html += f"""
                <div class="example">{j}. <a href="{post['url']}" target="_blank">{post['title']}</a>
                    <div class="example-stats">↑ {post['score']} upvotes | 💬 {post['comments']} comments | r/{post['subreddit']}</div>
                </div>
"""

        html += "</div></div>\n"

    html += f"""
    </div>

    <div class="footer">
        <p>Report Generated by Reddit Trend Analyzer</p>
        <p>{datetime.now().strftime('%B %d, %Y')}</p>
    </div>
</div>
</body>
</html>
"""

    return html