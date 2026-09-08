import streamlit as st
import pandas as pd
import io
import urllib.parse
import tldextract

st.set_page_config(page_title="Topical Offsite SEO Analyzer", layout="wide")

st.title("🚀 TOSA - Topical Offsite SEO Analyzer")
st.markdown("Công cụ phân tích Backlink & Referring Domains theo **Topic (Chủ đề)** để đánh giá Topical Authority.")

st.sidebar.header("1. Upload Data")
st.sidebar.markdown("Upload 1 file Excel (chứa 4 sheet thô) HOẶC upload 4 file CSV xuất từ SEMrush.")

data_source = st.sidebar.radio("Nguồn dữ liệu:", ("File Excel tổng hợp", "Các file CSV rời"))

# Quality rules
st.sidebar.header("2. Cấu hình đánh giá")
as_threshold = st.sidebar.slider("Ngưỡng Quality Backlink (Domain AS > X)", min_value=0, max_value=100, value=20)

@st.cache_data
def process_data(pages_df, rd_df, backlink_df, anchor_df, as_thresh):
    # 1. Topic Extraction
    if 'Classification' in pages_df.columns:
        pages_df['Topic'] = pages_df['Classification'].fillna('Other')
    else:
        def get_topic(url):
            try:
                if pd.isna(url): return "Unknown"
                parsed = urllib.parse.urlparse(str(url))
                path = parsed.path.strip('/')
                if not path: return "Homepage"
                parts = path.split('/')
                if len(parts) > 0:
                    return parts[0].title().replace("-", " ")
                return "Other"
            except:
                return "Error"
        pages_df['Topic'] = pages_df['Source url'].apply(get_topic)
        
    if 'Page Type' not in pages_df.columns:
        pages_df['Page Type'] = 'Deep Page'
    
    # Create mapping dicts from Pages
    url_topic_map = dict(zip(pages_df['Source url'], pages_df['Topic']))
    url_pagetype_map = dict(zip(pages_df['Source url'], pages_df['Page Type']))

    # 2. Extract Domain for joining
    def get_domain(url):
        try:
            if pd.isna(url): return None
            url_str = str(url).strip()
            if not url_str.startswith(('http://', 'https://')):
                url_str = 'http://' + url_str
            netloc = urllib.parse.urlparse(url_str).netloc.lower()
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            return netloc
        except:
            return None

    if 'Source url' in backlink_df.columns:
        backlink_df['Source domain'] = backlink_df['Source url'].apply(get_domain)
    else:
        backlink_df['Source domain'] = None

    if 'Domain' in rd_df.columns:
        rd_df['Clean Domain'] = rd_df['Domain'].apply(get_domain)
    else:
        rd_df['Clean Domain'] = None
        
    # Merge AS score into backlinks
    if 'Domain ascore' in rd_df.columns:
        domain_as_map = dict(zip(rd_df['Clean Domain'], rd_df['Domain ascore']))
        backlink_df['Matched AS'] = backlink_df['Source domain'].map(domain_as_map)
    else:
        backlink_df['Matched AS'] = pd.NA
        
    # 3. Aggregate per URL
    url_stats = []
    grouped = backlink_df.groupby('Target url')
    
    for target_url, group in grouped:
        total_bl = len(group)
        quality_bl = len(group[group['Matched AS'] > as_thresh])
        low_quality_bl = len(group[group['Matched AS'] <= as_thresh])
        unknown_as_bl = len(group[group['Matched AS'].isna()])
        
        unique_domains = group['Source domain'].nunique()
        quality_domains = group[group['Matched AS'] > as_thresh]['Source domain'].nunique()
        low_quality_domains = group[group['Matched AS'] <= as_thresh]['Source domain'].nunique()
        unknown_domains = group[group['Matched AS'].isna()]['Source domain'].nunique()
        
        sitewide_bl = len(group[group.get('Sitewide', False) == True]) if 'Sitewide' in group.columns else 0
        nofollow_bl = len(group[group.get('Nofollow', False) == True]) if 'Nofollow' in group.columns else 0
        
        url_stats.append({
            'URL': target_url,
            'Topic': url_topic_map.get(target_url, 'Other'),
            'Page Type': url_pagetype_map.get(target_url, 'Unknown'),
            'Total Backlinks': total_bl,
            'Quality Backlinks AS > 20': quality_bl,
            'Low Quality Backlinks AS <= 20': low_quality_bl,
            'Unknown AS Backlinks': unknown_as_bl,
            'Referring Domains': unique_domains,
            'Quality Referring Domains': quality_domains,
            'Low Quality Referring Domains': low_quality_domains,
            'Unknown Referring Domains': unknown_domains,
            'Sitewide Backlinks': sitewide_bl,
            'Nofollow Backlinks': nofollow_bl,
            'Quality Rate': quality_bl / total_bl if total_bl > 0 else 0,
            'Low Quality Rate': low_quality_bl / total_bl if total_bl > 0 else 0,
            'Sitewide Rate': sitewide_bl / total_bl if total_bl > 0 else 0,
        })
        
    url_analysis_df = pd.DataFrame(url_stats)
    
    # Calculate % Total Backlinks
    if not url_analysis_df.empty:
        total_all_bl = url_analysis_df['Total Backlinks'].sum()
        url_analysis_df['% Total Backlinks'] = url_analysis_df['Total Backlinks'] / total_all_bl if total_all_bl > 0 else 0
        url_analysis_df.sort_values('Total Backlinks', ascending=False, inplace=True)

    # 4. Aggregate per Topic
    topic_stats = []
    if not url_analysis_df.empty:
        topic_group = url_analysis_df.groupby('Topic')
        for topic, group in topic_group:
            total_bl = group['Total Backlinks'].sum()
            q_bl = group['Quality Backlinks AS > 20'].sum()
            topic_stats.append({
                'Topic': topic,
                'URLs': len(group),
                'Referring Domains': group['Referring Domains'].sum(),
                'Quality Referring Domains': group['Quality Referring Domains'].sum(),
                'Total Backlinks': total_bl,
                'Quality Backlinks': q_bl,
                'Low Quality Backlinks': group['Low Quality Backlinks AS <= 20'].sum(),
                'Unknown AS': group['Unknown AS Backlinks'].sum(),
                'Sitewide Backlinks': group['Sitewide Backlinks'].sum(),
                'Quality Rate': q_bl / total_bl if total_bl > 0 else 0,
                'Low Quality Rate': group['Low Quality Backlinks AS <= 20'].sum() / total_bl if total_bl > 0 else 0
            })
            
    topic_analysis_df = pd.DataFrame(topic_stats)
    if not topic_analysis_df.empty:
        total_q_bl = topic_analysis_df['Quality Backlinks'].sum()
        topic_analysis_df['% Quality Backlinks'] = topic_analysis_df['Quality Backlinks'] / total_q_bl if total_q_bl > 0 else 0
        topic_analysis_df.sort_values('Total Backlinks', ascending=False, inplace=True)
        
    # Reorder Topic Columns
    topic_cols = ['Topic', 'URLs', 'Referring Domains', 'Quality Referring Domains', 'Total Backlinks', 'Quality Backlinks', 'Low Quality Backlinks', 'Unknown AS', 'Sitewide Backlinks', 'Quality Rate', 'Low Quality Rate', '% Quality Backlinks']
    if not topic_analysis_df.empty:
        topic_analysis_df = topic_analysis_df[topic_cols]
    
    return url_analysis_df, topic_analysis_df

uploaded_excel = None
pages_file = None
rd_file = None
bl_file = None
anchor_file = None

if data_source == "File Excel tổng hợp":
    uploaded_excel = st.sidebar.file_uploader("Upload Phân tích backlink.xlsx", type=["xlsx", "xls"])
else:
    pages_file = st.sidebar.file_uploader("Upload Pages CSV", type=["csv", "xlsx"])
    rd_file = st.sidebar.file_uploader("Upload Referring Domains CSV", type=["csv", "xlsx"])
    bl_file = st.sidebar.file_uploader("Upload Backlinks CSV", type=["csv", "xlsx"])
    anchor_file = st.sidebar.file_uploader("Upload Anchor Text CSV", type=["csv", "xlsx"])

if st.sidebar.button("Phân tích dữ liệu"):
    with st.spinner("Đang đọc dữ liệu..."):
        try:
            if data_source == "File Excel tổng hợp" and uploaded_excel is not None:
                xl = pd.ExcelFile(uploaded_excel)
                pages_df = pd.read_excel(uploaded_excel, sheet_name='Pages')
                rd_df = pd.read_excel(uploaded_excel, sheet_name='Referring domain')
                backlink_df = pd.read_excel(uploaded_excel, sheet_name='Backlink')
                anchor_df = pd.read_excel(uploaded_excel, sheet_name='Anchor text')
            elif data_source == "Các file CSV rời" and pages_file and rd_file and bl_file:
                def read_file(f):
                    if f.name.endswith(".csv"): return pd.read_csv(f)
                    return pd.read_excel(f)
                
                pages_df = read_file(pages_file)
                rd_df = read_file(rd_file)
                backlink_df = read_file(bl_file)
                anchor_df = read_file(anchor_file) if anchor_file else pd.DataFrame()
            else:
                st.warning("Vui lòng upload đủ file thô!")
                st.stop()
                
            st.success("Load file thành công! Đang xử lý data...")
            
            url_df, topic_df = process_data(pages_df, rd_df, backlink_df, anchor_df, as_threshold)
            
            url_fmt = {col: "{:.2%}" for col in ['Quality Rate', 'Low Quality Rate', 'Sitewide Rate', '% Total Backlinks'] if col in url_df.columns}
            topic_fmt = {col: "{:.2%}" for col in ['Quality Rate', 'Low Quality Rate', '% Quality Backlinks'] if col in topic_df.columns}
            
            st.subheader("📊 1. Topic Analysis (Sức mạnh Offsite theo Topic)")
            st.dataframe(topic_df.style.format(topic_fmt), use_container_width=True)
            
            st.subheader("🔗 2. URL Analysis (Chi tiết từng trang)")
            st.dataframe(url_df.style.format(url_fmt), use_container_width=True)
            
            # Create Excel for download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                pages_df.to_excel(writer, sheet_name='Pages', index=False)
                rd_df.to_excel(writer, sheet_name='Referring domain', index=False)
                backlink_df.to_excel(writer, sheet_name='Backlink', index=False)
                if not anchor_df.empty:
                    anchor_df.to_excel(writer, sheet_name='Anchor text', index=False)
                url_df.to_excel(writer, sheet_name='URL Analysis', index=False)
                topic_df.to_excel(writer, sheet_name='Topic Analysis', index=False)
                
                # Full Dashboard Sheet Match
                dash_data = [
                    {"BACKLINK ANALYSIS DASHBOARD": "Quality rule", "Unnamed: 1": f"Domain ascore > {as_threshold}", "Unnamed: 2": None, "Unnamed: 3": None, "Unnamed: 4": None},
                    {"BACKLINK ANALYSIS DASHBOARD": "Total Backlinks", "Unnamed: 1": len(backlink_df), "Unnamed: 2": None, "Unnamed: 3": None, "Unnamed: 4": None},
                    {"BACKLINK ANALYSIS DASHBOARD": "Quality Backlinks", "Unnamed: 1": url_df['Quality Backlinks AS > 20'].sum() if not url_df.empty else 0, "Unnamed: 2": None, "Unnamed: 3": None, "Unnamed: 4": None},
                    {"BACKLINK ANALYSIS DASHBOARD": "Low Quality Backlinks", "Unnamed: 1": url_df['Low Quality Backlinks AS <= 20'].sum() if not url_df.empty else 0, "Unnamed: 2": None, "Unnamed: 3": None, "Unnamed: 4": None},
                    {"BACKLINK ANALYSIS DASHBOARD": "Unknown AS Backlinks", "Unnamed: 1": url_df['Unknown AS Backlinks'].sum() if not url_df.empty else 0, "Unnamed: 2": None, "Unnamed: 3": None, "Unnamed: 4": None},
                ]
                pd.DataFrame(dash_data).to_excel(writer, sheet_name='Backlink Dashboard', index=False)

                # Format Percentages in Excel
                workbook = writer.book
                pct_format = workbook.add_format({'num_format': '0.00%'})

                ws_url = writer.sheets['URL Analysis']
                for col_name in ['Quality Rate', 'Low Quality Rate', 'Sitewide Rate', '% Total Backlinks']:
                    if col_name in url_df.columns:
                        col_idx = url_df.columns.get_loc(col_name)
                        ws_url.set_column(col_idx, col_idx, 15, pct_format)

                ws_topic = writer.sheets['Topic Analysis']
                for col_name in ['Quality Rate', 'Low Quality Rate', '% Quality Backlinks']:
                    if col_name in topic_df.columns:
                        col_idx = topic_df.columns.get_loc(col_name)
                        ws_topic.set_column(col_idx, col_idx, 15, pct_format)

            st.download_button(
                label="📥 Tải xuống File Excel Báo cáo",
                data=output.getvalue(),
                file_name="TOSA_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        except Exception as e:
            st.error(f"Lỗi khi xử lý dữ liệu: {e}")

