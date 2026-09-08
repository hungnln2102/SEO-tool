# Đánh giá phương pháp phân tích backlink: File phân tích thủ công vs TOSA Output

## 1. Mục tiêu đánh giá

Tài liệu này đánh giá hai file:

```text
Phân tích backlink (1).xlsx
Phân tích backlink (Output) (3).xlsx
```

theo góc nhìn **chất lượng dữ liệu và methodology phân tích backlink**, không coi file nào là benchmark tuyệt đối.

Mục tiêu:

> Xác định file nào hợp lý hơn để dùng làm nền tảng cho một hệ thống phân tích backlink lâu dài.

---

# 2. Kết luận tổng quan

Nếu chỉ xét khả năng reproduce báo cáo hiện tại:

> **TOSA Output (3) đã rất gần với file Phân tích backlink.**

Nhưng nếu bỏ tư duy benchmark và đánh giá theo logic SEO/data analysis:

> **Không nên coi bất kỳ file nào là hoàn hảo 100%.**

Phương án tốt nhất:

> **Lấy TOSA Output (3) làm nền tảng**, vì core calculation, aggregation và automation đã ổn; sau đó sửa một số logic phân tích để methodology tốt hơn file cũ.

Hai điểm quan trọng nhất cần xem lại:

1. **Referring Domains ở cấp Topic**
2. **Homepage vs Deep Page classification**

---

# 3. So sánh tổng thể

| Tiêu chí | Phân tích backlink | TOSA Output (3) | Đánh giá |
|---|---|---|---|
| Raw backlink data | Tốt | Tốt | Ngang nhau |
| Total Backlinks | Đúng | Đúng | Ngang nhau |
| Quality / Low / Unknown | Hợp lý | Hợp lý | Ngang nhau |
| URL-level backlink | Tốt | Tốt | Ngang nhau |
| URL-level Referring Domains | Tốt | Tốt | Ngang nhau |
| Topic Classification | Hợp lý | Đã gần tương đương | Ngang nhau |
| Topic Backlink Aggregation | Tốt | Tốt | Ngang nhau |
| Topic Referring Domains | Hợp lý hơn | Có dấu hiệu aggregate sai | File phân tích tốt hơn |
| Homepage / Deep Page | Có điểm đáng nghi | Có cùng vấn đề | Cả hai cần xem lại |
| Dashboard | Đầy đủ | Gần đầy đủ | File phân tích nhỉnh nhẹ |
| Khả năng automation | Thấp hơn | Cao | TOSA tốt hơn |
| Khả năng scale | Thấp hơn | Tốt hơn | TOSA tốt hơn |
| Khả năng làm nền tảng tool | Trung bình | Tốt | TOSA tốt hơn |

---

# 4. Raw Data

Cả hai file đều đang sử dụng cùng dataset chính:

```text
Total Backlinks = 26,984
Referring Domains = 1,354
Target URLs = 1,251
```

Các nhóm:

```text
Quality
Low Quality
Unknown AS
Nofollow
Sitewide
```

đã reconcile tốt.

Điều này cho thấy:

> Hai file không khác nhau ở raw input hoặc core backlink count.

Sai biệt chủ yếu nằm ở **cách aggregation và classification**.

---

# 5. Quality / Low Quality / Unknown

Cả hai file hiện cho kết quả:

```text
Quality = 1,180
Low Quality = 11,323
Unknown AS = 14,481
Total = 26,984
```

Validation:

```text
1,180
+ 11,323
+ 14,481
=
26,984
```

### Đánh giá

Logic hiện tại nhất quán.

Không cần thay đổi phần core này.

---

# 6. URL-level Analysis

Ở cấp URL, hai file hiện gần như tương đương về:

```text
Target URL
Total Backlinks
Quality Backlinks
Low Quality Backlinks
Unknown Backlinks
Referring Domains
Quality Referring Domains
Low Quality Referring Domains
Unknown Referring Domains
Nofollow
Sitewide
```

### Đánh giá

URL-level analysis hiện là phần ổn định nhất.

Có thể coi đây là foundation tốt để xây tiếp các level aggregation phía trên.

---

# 7. Vấn đề quan trọng nhất: Topic Referring Domains

Đây là điểm khác biệt methodology rõ nhất.

Ví dụ Topic:

```text
Other
```

File Phân tích backlink:

```text
Referring Domains = 6,468
```

TOSA:

```text
Referring Domains = 14,640
```

Ví dụ khác:

```text
Brand
```

File Phân tích backlink:

```text
1,008 RD
```

TOSA:

```text
1,436 RD
```

Ví dụ:

```text
Chăm sóc cá nhân > Dầu gội
```

File Phân tích backlink:

```text
107 RD
```

TOSA:

```text
607 RD
```

---

# 8. Vì sao Topic RD của TOSA có khả năng sai

Nếu cùng một domain backlink tới nhiều URL trong cùng Topic:

```text
domain-a.com → URL 1
domain-a.com → URL 2
domain-a.com → URL 3
```

Ở cấp URL:

```text
URL 1 = 1 RD
URL 2 = 1 RD
URL 3 = 1 RD
```

Nếu TOSA aggregate bằng:

```text
SUM(URL Referring Domains)
```

thì kết quả Topic sẽ là:

```text
3 RD
```

Trong khi số domain thực tế chỉ là:

```text
1 unique domain
```

---

# 9. Logic đúng cho Topic Referring Domains

Phải tính từ raw backlink data:

```text
Topic
   ↓
Collect all backlinks thuộc Topic
   ↓
Extract Source Domain
   ↓
Normalize Domain
   ↓
DISTINCT Domain
   ↓
COUNT
```

Formula concept:

```text
Topic Referring Domains
=
COUNT DISTINCT(Source Domain)
```

Không phải:

```text
SUM(URL-level Referring Domains)
```

---

# 10. Đánh giá giữa hai file về Topic RD

Nếu file Phân tích backlink đang deduplicate domain ở cấp Topic, thì methodology đó đúng hơn.

Do đó:

> **Ở hạng mục Topic Referring Domains, file Phân tích backlink đáng tin hơn TOSA Output hiện tại.**

Đây là phần nên lấy logic của file Phân tích backlink để sửa TOSA.

---

# 11. Quality Referring Domains cũng cần kiểm tra tương tự

Không chỉ Total Referring Domains.

Các metric:

```text
Quality Referring Domains
Low Quality Referring Domains
Unknown Referring Domains
```

cũng phải được deduplicate ở cấp Topic.

Logic đúng:

```text
COUNT DISTINCT Domain
WHERE AS > 20
```

```text
COUNT DISTINCT Domain
WHERE AS <= 20
```

```text
COUNT DISTINCT Domain
WHERE AS IS UNKNOWN
```

Không SUM trực tiếp từ URL Analysis.

---

# 12. Homepage / Deep Page – vấn đề methodology của cả hai file

Cả hai file hiện đang cho:

```text
Homepage Backlinks = 0
Deep Page Backlinks = 26,984
```

Nhưng dataset có target URL dạng:

```text
https://guardian.com.vn/
https://www.guardian.com.vn/
```

Về bản chất SEO:

> Backlink trỏ trực tiếp vào root domain nên được coi là Homepage backlink.

Do đó:

```text
Homepage = 0
```

là một kết quả cần xem lại.

---

# 13. Logic Homepage hợp lý hơn

Các URL:

```text
https://guardian.com.vn
https://guardian.com.vn/
https://www.guardian.com.vn
https://www.guardian.com.vn/
```

sau normalization đều nên resolve thành Homepage.

Nếu có tracking parameter:

```text
https://www.guardian.com.vn/?srsltid=abc
```

thì về page location vẫn là:

```text
Homepage
```

---

# 14. TOSA phiên bản trước từng có kết quả hợp lý hơn

TOSA trước đó từng cho:

```text
Homepage Backlinks = 4,014
Deep Page Backlinks = 22,970
```

Về mặt methodology:

> Kết quả này hợp lý hơn việc coi toàn bộ 26,984 backlink là Deep Page.

Điều này cho thấy:

> Reproduce file cũ chưa chắc đồng nghĩa với phân tích đúng hơn.

---

# 15. URL Normalization nên áp dụng trước Page Location

Logic đề xuất:

```text
Target URL
    ↓
Remove tracking parameters
    ↓
Normalize protocol
    ↓
Normalize www
    ↓
Normalize trailing slash
    ↓
Parse path
```

Rule:

```text
Path = "/" hoặc empty
→ Homepage

Path khác "/"
→ Deep Page
```

---

# 16. Topic Classification

TOSA Output (3) hiện đã gần như đồng bộ Topic với file Phân tích backlink.

Ví dụ các topic:

```text
Brand
Chăm sóc cá nhân > Dầu gội
Chăm sóc da > Chống nắng
Other
...
```

đã về đúng distribution.

### Đánh giá

Không còn lý do lớn để thay đổi taxonomy hiện tại nếu mục tiêu là dùng chung taxonomy business đã xác định.

Tuy nhiên:

> Topic taxonomy nên được đánh giá theo giá trị phân tích SEO, không chỉ vì nó giống file cũ.

Nếu taxonomy hiện tại phản ánh đúng category/business structure thì nên giữ.

---

# 17. Topic Backlink Aggregation

Các metric:

```text
Total Backlinks
Quality
Low Quality
Unknown
```

ở Topic level hiện đã tương đối tốt.

Vấn đề chính không còn ở backlink volume mà ở:

```text
Referring Domain aggregation
```

Do đó không nên rewrite toàn bộ Topic Analysis.

Chỉ cần sửa phần RD logic.

---

# 18. Dashboard

File Phân tích backlink hiện có dashboard đầy đủ hơn về layout và một số bảng summary.

TOSA đã gần tương đương.

Nếu đánh giá không theo benchmark thì Dashboard không nhất thiết phải giống 100%.

Điều quan trọng là metric phải:

1. Đúng
2. Không double-count
3. Có giá trị ra quyết định SEO

---

# 19. Metric nào nên giữ

Nên giữ:

```text
Total Backlinks
Quality Backlinks
Low Quality Backlinks
Unknown AS
Quality Rate
Low Quality Rate
Nofollow
Nofollow Rate
Sitewide
Sitewide Rate
Homepage
Deep Page
Homepage Share
Deep Page Share
Quality Homepage
Quality Deep Page
Largest Deep Page
Top URLs by Quality Backlinks
Top Topics by Quality Backlinks
```

Đây đều là các metric có giá trị thực tế cho backlink analysis.

---

# 20. Referring Domain quan trọng hơn Backlink Volume trong nhiều trường hợp

Ví dụ:

```text
1 domain
→ 1,000 backlinks
```

không có cùng giá trị với:

```text
1,000 domains
→ mỗi domain 1 backlink
```

Do đó Topic Analysis phải ưu tiên phân biệt:

```text
Backlink Volume
vs
Unique Referring Domains
```

Nếu RD bị cộng trùng thì report có thể tạo perception sai về độ rộng backlink profile.

---

# 21. Sitewide Backlink

Sitewide metric hiện được tính nhất quán.

Tuy nhiên khi đánh giá SEO:

```text
Backlink Count
```

không nên được dùng thay thế:

```text
Referring Domain diversity
```

Một sitewide domain có thể tạo rất nhiều backlink nhưng chỉ tăng:

```text
1 Referring Domain
```

Do đó fix RD aggregation càng quan trọng.

---

# 22. Unknown AS

Unknown hiện chiếm:

```text
14,481 / 26,984
≈ 53.67%
```

Đây là tỷ lệ rất lớn.

Điều này không có nghĩa 53.67% backlink là xấu.

Nó chỉ có nghĩa:

> Không có Authority Score đủ để classify theo rule hiện tại.

Vì vậy nên giữ Unknown tách biệt, không ép vào Low Quality.

Cả hai file hiện đang làm đúng điểm này.

---

# 23. File nào tốt hơn về data integrity?

### Core Calculation

Ngang nhau.

### URL Analysis

Ngang nhau.

### Topic Backlink Count

Ngang nhau.

### Topic Referring Domains

File Phân tích backlink tốt hơn.

### Homepage / Deep Page

Cả hai hiện có logic cần xem lại.

### Automation

TOSA tốt hơn.

---

# 24. File nào tốt hơn về methodology?

Không nên chọn một file nguyên trạng.

Phương án tốt nhất:

```text
TOSA Output (3)
```

làm base.

Sau đó:

```text
+ Topic RD logic của file Phân tích backlink
+ Homepage normalization hợp lý hơn
```

---

# 25. Kiến trúc dữ liệu đề xuất cho TOSA

```text
RAW BACKLINKS
    ↓
DOMAIN NORMALIZATION
    ↓
TARGET URL NORMALIZATION
    ↓
QUALITY CLASSIFICATION
    ↓
URL ANALYSIS
    ↓
TOPIC MAPPING
    ↓
TOPIC BACKLINK AGGREGATION
    ↓
TOPIC DISTINCT RD AGGREGATION
    ↓
HOMEPAGE / DEEP PAGE
    ↓
DASHBOARD
```

---

# 26. Fix cụ thể cho TOSA

## FIX 1 – Topic Referring Domains

Priority:

```text
HIGH
```

Thay:

```text
SUM(URL.Referring Domains)
```

bằng:

```text
COUNT DISTINCT normalized Source Domain
GROUP BY Topic
```

---

## FIX 2 – Topic Quality Referring Domains

Priority:

```text
HIGH
```

Logic:

```text
COUNT DISTINCT Domain
WHERE Domain AS > 20
GROUP BY Topic
```

---

## FIX 3 – Topic Low Quality RD

Priority:

```text
HIGH
```

Logic:

```text
COUNT DISTINCT Domain
WHERE Domain AS <= 20
GROUP BY Topic
```

---

## FIX 4 – Topic Unknown RD

Priority:

```text
HIGH
```

Logic:

```text
COUNT DISTINCT Domain
WHERE AS missing
GROUP BY Topic
```

---

## FIX 5 – Homepage / Deep Page

Priority:

```text
MEDIUM
```

Không ép logic theo file cũ.

Dùng normalized target URL.

Rule:

```text
normalized path = "/"
→ Homepage

otherwise
→ Deep Page
```

---

# 27. Những phần không cần sửa

Không cần sửa:

```text
Total Backlinks
Quality Backlinks
Low Quality Backlinks
Unknown Backlinks
URL-level backlink aggregation
Nofollow
Sitewide
Topic Backlink totals
Topic taxonomy hiện tại
```

---

# 28. Recommendation cuối cùng

Nếu mục tiêu là:

> **Copy đúng báo cáo manual**

thì tiếp tục dùng file Phân tích backlink làm benchmark.

Nhưng nếu mục tiêu là:

> **Xây TOSA thành tool phân tích backlink đúng methodology và dùng lâu dài**

thì không nên ép tất cả logic theo file manual.

Phương án nên dùng:

```text
TOSA Output (3)
        ↓
Fix Topic Unique RD
        ↓
Fix Homepage / Deep Page normalization
        ↓
Final Methodology
```

---

# 29. Đánh giá điểm

## File Phân tích backlink

### Ưu điểm

- Topic-level RD có logic đáng tin hơn.
- Dashboard hoàn thiện.
- Có thể dùng làm reference cho nhiều metric.

### Nhược điểm

- Homepage / Deep Page có dấu hiệu chưa hợp lý.
- Khó scale nếu phụ thuộc xử lý manual.
- Không nên được coi là chuẩn tuyệt đối chỉ vì được tạo trước.

### Đánh giá

```text
8.5 / 10
```

---

## TOSA Output (3)

### Ưu điểm

- Core calculation tốt.
- URL analysis tốt.
- Topic classification hiện đã ổn.
- Automation và khả năng scale tốt.
- Có thể trở thành single pipeline phân tích backlink.

### Nhược điểm

- Topic Referring Domains có khả năng double-count.
- Homepage / Deep Page hiện đang follow logic chưa hợp lý.
- Một số Dashboard output còn phụ thuộc các lỗi aggregation trên.

### Đánh giá hiện tại

```text
8.5–9 / 10
```

Sau khi fix RD aggregation và Homepage:

```text
9.5 / 10
```

---

# 30. Kết luận cuối

Không nên chọn:

```text
File Phân tích backlink
```

làm chuẩn tuyệt đối về methodology.

Cũng không nên giữ nguyên:

```text
TOSA Output (3)
```

mà không sửa.

Phương án tốt nhất:

> **Lấy TOSA Output (3) làm nền tảng chính, giữ các core calculation hiện tại, sửa Referring Domain aggregation ở cấp Topic theo nguyên tắc COUNT DISTINCT, và xác định Homepage/Deep Page dựa trên normalized Target URL.**

Sau các thay đổi này:

> **TOSA sẽ không chỉ reproduce được báo cáo cũ mà còn có methodology dữ liệu hợp lý hơn để sử dụng lâu dài cho backlink analysis.**
