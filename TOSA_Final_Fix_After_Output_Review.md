# TOSA -- Final Fix Requirements theo Benchmark Phân tích Backlink

## 1. Mục tiêu

File benchmark / nguồn cuối:

``` text
Phân tích backlink (1).xlsx
```

File output TOSA đang đánh giá:

``` text
Phân tích backlink (Output).xlsx
```

Mục tiêu duy nhất:

> **TOSA phải reproduce đúng các hạng mục, logic classification và số
> liệu của file benchmark. Không thêm và không bớt hạng mục.**

------------------------------------------------------------------------

# 2. Kết luận hiện tại

TOSA đã xử lý đúng phần **core calculation và raw aggregation**.

Phần còn sai chủ yếu nằm ở:

``` text
Topic Classification
Page Type Classification
Homepage / Deep Page Classification
Topic Analysis Distribution
Dashboard phụ thuộc classification
```

Không cần viết lại core backlink calculation.

------------------------------------------------------------------------

# 3. Trạng thái tổng thể

  Hạng mục                              Benchmark      TOSA Output Status
  ---------------------- ------------------------ ---------------- ---------
  Total Backlinks                          26,984           26,984 PASS
  Quality                                   1,180            1,180 PASS
  Low Quality                              11,323           11,323 PASS
  Unknown AS                               14,481           14,481 PASS
  Target URL Count                          1,251            1,251 PASS
  URL Analysis Total                       26,984           26,984 PASS
  Nofollow                                  9,778            9,778 PASS
  Sitewide                                      8                8 PASS
  Topic Classification         Benchmark taxonomy   Khác benchmark FAIL
  Page Type                       Benchmark logic   Khác benchmark FAIL
  Topic Analysis           Benchmark distribution   Khác benchmark FAIL
  Dashboard                             Benchmark    Khớp một phần PARTIAL

------------------------------------------------------------------------

# 4. Những phần KHÔNG cần sửa

## 4.1. Total Backlinks

Expected:

``` text
26,984
```

TOSA:

``` text
26,984
```

**Status: PASS**

------------------------------------------------------------------------

## 4.2. Quality Backlinks

Expected:

``` text
1,180
```

TOSA:

``` text
1,180
```

**Status: PASS**

------------------------------------------------------------------------

## 4.3. Low Quality Backlinks

Expected:

``` text
11,323
```

TOSA:

``` text
11,323
```

**Status: PASS**

------------------------------------------------------------------------

## 4.4. Unknown AS

Expected:

``` text
14,481
```

TOSA:

``` text
14,481
```

**Status: PASS**

------------------------------------------------------------------------

## 4.5. Reconciliation

``` text
1,180
+ 11,323
+ 14,481
=
26,984
```

**Status: PASS**

------------------------------------------------------------------------

## 4.6. URL Analysis Coverage

Expected:

``` text
1,251 Target URLs
26,984 Backlinks
```

TOSA:

``` text
1,251 Target URLs
26,984 Backlinks
```

**Status: PASS**

Core URL aggregation không cần sửa.

------------------------------------------------------------------------

## 4.7. Nofollow

Expected:

``` text
9,778
```

TOSA:

``` text
9,778
```

**Status: PASS**

------------------------------------------------------------------------

## 4.8. Sitewide

Expected:

``` text
8
```

TOSA:

``` text
8
```

**Status: PASS**

------------------------------------------------------------------------

# 5. FIX 1 -- Topic Classification

**Priority: HIGH**

Đây là lỗi lớn nhất còn lại.

Benchmark có khoảng:

``` text
34 topics
```

TOSA Output hiện chỉ còn khoảng:

``` text
21 topics
```

Điều này cho thấy taxonomy/mapping của TOSA chưa replicate benchmark.

------------------------------------------------------------------------

# 6. Ví dụ Topic sai

## Ví dụ 1

Benchmark:

``` text
Chăm sóc cá nhân > Dầu gội
= 612 backlinks
```

TOSA:

``` text
Chăm sóc cá nhân > Dầu gội
= 12 backlinks
```

Sai lệch:

``` text
-600 backlinks
```

------------------------------------------------------------------------

## Ví dụ 2

Benchmark:

``` text
Brand
= 1,561 backlinks
```

TOSA:

``` text
Brand
= 401 backlinks
```

Sai lệch:

``` text
-1,160 backlinks
```

------------------------------------------------------------------------

## TOSA đang có các nhóm không tương ứng benchmark

Ví dụ:

``` text
Chăm sóc cá nhân > Chăm sóc tóc
Other
Other - Non Product
```

Trong đó:

``` text
Other = 12,918 backlinks
Other - Non Product = 4,814 backlinks
```

Backlink đang bị gom vào các nhóm này thay vì được phân phối theo
taxonomy benchmark.

------------------------------------------------------------------------

# 7. Yêu cầu sửa Topic

Không tạo taxonomy mới.

Logic bắt buộc:

``` text
Target URL
    ↓
Áp dụng đúng logic mapping của benchmark
    ↓
Topic giống benchmark
```

Mục tiêu:

``` text
Benchmark Topic
=
TOSA Topic
```

cho từng URL.

Không chỉ cần tổng backlink bằng nhau.

------------------------------------------------------------------------

# 8. Không được đánh giá Topic Analysis chỉ bằng tổng

Hiện tại:

``` text
SUM(TOSA Topic Backlinks)
=
26,984
```

Điều này chỉ chứng minh không mất backlink.

Nó **không chứng minh Topic Classification đúng**.

Acceptance phải là:

``` text
Topic A benchmark = Topic A TOSA
Topic B benchmark = Topic B TOSA
Topic C benchmark = Topic C TOSA
...
```

và:

``` text
Backlinks từng Topic benchmark
=
Backlinks từng Topic TOSA
```

------------------------------------------------------------------------

# 9. FIX 2 -- Page Type Classification

**Priority: HIGH**

TOSA đang sử dụng classification khác benchmark.

Ví dụ URL:

``` text
https://www.guardian.com.vn/
```

Benchmark:

``` text
Topic: Other
Page Type: Deep Page
```

TOSA Output:

``` text
Topic: Other - Non Product
Page Type: Other
```

=\> **FAIL**

------------------------------------------------------------------------

# 10. Ví dụ khác

URL:

``` text
https://guardian.com.vn/vn
```

Benchmark:

``` text
Topic: Other
Page Type: Deep Page
```

TOSA:

``` text
Topic: Other - Non Product
Page Type: Other
```

=\> **FAIL**

------------------------------------------------------------------------

# 11. Yêu cầu sửa Page Type

Không áp dụng framework Page Type mới.

Không tự chuyển sang:

``` text
Product
Category
Brand
Other
Content
...
```

nếu benchmark không yêu cầu như vậy.

TOSA phải reproduce:

``` text
Page Type benchmark
```

theo từng Target URL.

Acceptance:

``` text
COUNT(Page Type mismatch)
=
0
```

------------------------------------------------------------------------

# 12. FIX 3 -- Homepage / Deep Page

**Priority: HIGH**

Đây là sai lệch lớn giữa benchmark và TOSA.

Benchmark:

``` text
Homepage Backlinks = 0
Deep Page Backlinks = 26,984
```

TOSA Output:

``` text
Homepage Backlinks = 4,014
Deep Page Backlinks = 22,970
```

Sai lệch:

``` text
Homepage: +4,014
Deep Page: -4,014
```

------------------------------------------------------------------------

# 13. Không thay đổi logic benchmark

Dù logic mới có thể hợp lý hơn về mặt SEO, requirement hiện tại là:

> **Reproduce benchmark.**

Do đó TOSA phải sử dụng đúng rule khiến benchmark cho ra:

``` text
Homepage = 0
Deep Page = 26,984
```

với dataset này.

Không tự sửa logic benchmark trong scope hiện tại.

------------------------------------------------------------------------

# 14. FIX 4 -- Topic Analysis Distribution

**Priority: HIGH**

Sau khi Topic Classification được sửa, Topic Analysis phải được generate
lại.

Cần match từng dòng theo benchmark.

Kiểm tra:

``` text
Topic Name
URL Count
Total Backlinks
Quality Backlinks
Low Quality Backlinks
Unknown AS
```

với các field thực tế đang có trong benchmark.

------------------------------------------------------------------------

# 15. Acceptance cho Topic Analysis

Không chỉ:

``` text
SUM Total Backlinks = 26,984
```

Mà phải:

``` text
Benchmark Topic Count
=
TOSA Topic Count
```

Expected hiện tại:

``` text
~34 topics
```

và từng topic phải match về số liệu.

Ví dụ:

``` text
Benchmark:
Chăm sóc cá nhân > Dầu gội = 612

TOSA:
Chăm sóc cá nhân > Dầu gội = 612
```

mới được PASS.

------------------------------------------------------------------------

# 16. FIX 5 -- Dashboard Parity

**Priority: MEDIUM**

Dashboard hiện khớp phần core:

``` text
Total Backlinks
Quality
Low Quality
Unknown AS
Quality Rate
Low Quality Rate
Sitewide
Nofollow
```

Những metric phụ thuộc Page Type / Topic vẫn cần sửa sau khi
classification đúng.

------------------------------------------------------------------------

# 17. Homepage / Deep Page Dashboard

Expected benchmark:

``` text
Homepage Backlinks
Deep Page Backlinks

Homepage Share
Deep Page Share

Quality Homepage Backlinks
Quality Deep Page Backlinks
```

Tất cả phải được tính theo classification benchmark.

Không dùng classification hiện tại của TOSA.

------------------------------------------------------------------------

# 18. Largest Deep Page

Sau khi Page Type đúng, tính lại:

``` text
Largest Deep Page
Largest Deep Page Backlinks
Largest Deep Page Share
```

Kết quả phải match benchmark.

------------------------------------------------------------------------

# 19. Distribution Check

Giữ đúng logic:

``` text
Distribution Check
```

đang có trong benchmark.

Không thay bằng framework validation mới.

------------------------------------------------------------------------

# 20. Top URLs by Quality Backlinks

So sánh trực tiếp:

``` text
Benchmark Top URLs
vs
TOSA Top URLs
```

Phải match:

``` text
URL
Quality Backlinks
Ranking
```

và các field khác nếu benchmark có.

------------------------------------------------------------------------

# 21. Top Topics by Quality Backlinks

Phần này phải generate lại sau khi Topic Classification được sửa.

Nếu Topic sai:

``` text
Top Topics
```

dù calculation đúng vẫn không được coi là PASS.

Acceptance:

``` text
Benchmark Top Topics
=
TOSA Top Topics
```

------------------------------------------------------------------------

# 22. Không thêm hạng mục mới

Trong lần sửa tiếp theo **không triển khai thêm**:

``` text
Classification Confidence
Classification Trace
Data Quality Score
AI Classification Score
Authority Score Distribution mới
New Page Type framework
New Topic framework
New Dashboard KPI
Warning Engine mở rộng
SEO Recommendation Engine
Client Config UI
```

Các phần trên nằm ngoài scope benchmark.

------------------------------------------------------------------------

# 23. Không dùng URL slug để tạo taxonomy mới

Nếu TOSA đang có logic:

``` text
Không match Topic
→ Parse URL slug
→ Tạo Topic mới
```

thì phải bỏ khỏi final output nếu benchmark không làm như vậy.

Topic chỉ cần:

``` text
giống benchmark.
```

------------------------------------------------------------------------

# 24. Những việc Developer cần làm tiếp

Thứ tự:

``` text
1. Không sửa core backlink calculation

2. Compare URL-by-URL:
   Benchmark Topic
   vs
   TOSA Topic

3. Fix Topic mapping

4. Compare URL-by-URL:
   Benchmark Page Type
   vs
   TOSA Page Type

5. Fix Page Type mapping

6. Rebuild Topic Analysis

7. Rebuild Dashboard

8. Compare Top URL

9. Compare Top Topic

10. Remove output ngoài benchmark

11. Final comparison
```

------------------------------------------------------------------------

# 25. Recommended Debug Method

Tạo bảng internal để debug:

  ------------------------------------------------------------------------------
  Target URL Benchmark   TOSA Topic Topic      Benchmark   TOSA Page  Page Match
             Topic                  Match      Page Type   Type       
  ---------- ----------- ---------- ---------- ----------- ---------- ----------

  ------------------------------------------------------------------------------

Sau đó filter:

``` text
Topic Match = FALSE
```

và:

``` text
Page Match = FALSE
```

Developer chỉ cần xử lý các mismatch.

Không cần thay đổi phần đã PASS.

------------------------------------------------------------------------

# 26. Final Acceptance Checklist

## Core

-   [x] Total Backlinks = 26,984
-   [x] Quality = 1,180
-   [x] Low Quality = 11,323
-   [x] Unknown = 14,481
-   [x] URL Count = 1,251
-   [x] URL Analysis Total = 26,984
-   [x] Nofollow = 9,778
-   [x] Sitewide = 8

## Classification

-   [ ] Topic từng URL match benchmark
-   [ ] Page Type từng URL match benchmark
-   [ ] Homepage / Deep Page match benchmark

## Topic Analysis

-   [ ] Topic list match benchmark
-   [ ] Topic count match benchmark
-   [ ] URL Count từng topic match
-   [ ] Backlinks từng topic match
-   [ ] Quality từng topic match
-   [ ] Low Quality từng topic match
-   [ ] Unknown từng topic match

## Dashboard

-   [ ] Homepage Backlinks match
-   [ ] Deep Page Backlinks match
-   [ ] Homepage Share match
-   [ ] Deep Page Share match
-   [ ] Quality Homepage match
-   [ ] Quality Deep Page match
-   [ ] Largest Deep Page match
-   [ ] Distribution Check match
-   [ ] Top URLs match
-   [ ] Top Topics match

## Scope

-   [ ] Không thiếu hạng mục benchmark
-   [ ] Không thêm hạng mục ngoài benchmark

------------------------------------------------------------------------

# 27. Definition of Done

TOSA được coi là DONE khi:

``` text
Phân tích backlink (Output).xlsx
```

với cùng input tạo ra:

``` text
Các hạng mục
+
Classification
+
Aggregation
+
Dashboard
```

tương đương:

``` text
Phân tích backlink (1).xlsx
```

------------------------------------------------------------------------

# 28. Chốt

## Không sửa nữa

``` text
Raw Data
Backlink Count
AS Matching
Quality
Low Quality
Unknown
URL Aggregation
Nofollow
Sitewide
```

Các phần này đã PASS.

## Tập trung sửa

``` text
Topic Classification
        ↓
Page Type Classification
        ↓
Homepage / Deep Page
        ↓
Topic Analysis Distribution
        ↓
Dashboard dependent metrics
        ↓
Top Topics
```

### Final Goal

> **Không làm TOSA nhiều tính năng hơn. Chỉ làm TOSA reproduce chính xác
> file `Phân tích backlink (1).xlsx`, không thêm và không bớt hạng
> mục.**
