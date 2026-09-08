# Đánh giá đối chiếu TOSA Report với file Phân tích Backlink

## 1. Mục tiêu đối chiếu

-   **File nguồn cuối / Benchmark:** `Phân tích backlink (1).xlsx`
-   **File output của tool cần kiểm tra:** `TOSA_Report.xlsx`

Mục tiêu là xác định mức độ TOSA tái tạo đúng dữ liệu và logic phân tích
của file nguồn cuối, đồng thời chỉ ra các lỗi cần ưu tiên sửa trong
pipeline.

------------------------------------------------------------------------

## 2. Kết luận nhanh

**TOSA đang đọc đúng phần lớn raw data đầu vào, nhưng phần xử lý,
matching, aggregation và reporting phía sau có sai lệch lớn.**

Nếu mục tiêu của TOSA là tái tạo logic của file `Phân tích backlink`,
phiên bản hiện tại **chưa đạt**.

Điểm đáng chú ý nhất:

1.  Raw data chính khớp giữa hai file.
2.  Logic Quality / Low Quality / Unknown không reconcile với Total
    Backlinks.
3.  URL Analysis của TOSA chỉ xử lý khoảng **52.1% backlink**.
4.  Khoảng **12,918 backlinks** không xuất hiện trong URL Analysis.
5.  Dashboard vẫn báo `Unknown AS = 0`, tạo ra inconsistency.
6.  Page Type và Topic Taxonomy của TOSA chưa replicate benchmark.
7.  Dashboard của TOSA thiếu nhiều metric quan trọng.

------------------------------------------------------------------------

## 3. Đối chiếu raw data

  Sheet / Dataset       File nguồn cuối               TOSA Đánh giá
  ------------------ ------------------ ------------------ ----------
  Pages                  30,000 records     30,000 records Khớp
  Referring Domain        1,354 domains      1,354 domains Khớp
  Backlink             26,984 backlinks   26,984 backlinks Khớp
  Anchor Text             6,636 records      6,636 records Khớp

### Nhận xét

Các dữ liệu đầu vào chính như:

-   Backlink
-   Source URL
-   Target URL
-   Authority Score
-   Anchor
-   Nofollow
-   Sitewide
-   Referring Domain

về cơ bản tương ứng giữa hai file.

**Kết luận:** vấn đề chính không nằm ở bước import raw data. Cần tập
trung debug pipeline xử lý sau khi ingest dữ liệu.

------------------------------------------------------------------------

## 4. Lỗi Quality / Low Quality / Unknown

Cả hai file đều sử dụng rule:

> **Quality = Domain AS \> 20**

Tuy nhiên kết quả khác nhau đáng kể.

  Metric              Nguồn cuối      TOSA     Chênh lệch
  ----------------- ------------ --------- --------------
  Total Backlinks         26,984    26,984              0
  Quality                  1,180     1,898           +718
  Low Quality             11,323    12,168           +845
  Unknown AS              14,481         0        -14,481
  Quality Rate             4.37%   \~7.03%   +2.66 điểm %

### File nguồn cuối

``` text
26,984
= 1,180 Quality
+ 11,323 Low Quality
+ 14,481 Unknown
```

Tổng dữ liệu reconcile chính xác.

### TOSA

``` text
1,898 Quality
+ 12,168 Low Quality
= 14,066 backlinks
```

Trong khi Total Backlinks vẫn là:

``` text
26,984 backlinks
```

Như vậy:

``` text
26,984 - 14,066 = 12,918 backlinks
```

đang không được giải thích trong Quality / Low Quality / Unknown.

### Đánh giá

Đây là **critical bug** vì Dashboard đang thể hiện các metric lấy từ
những population khác nhau.

Có khả năng:

-   Total Backlinks lấy trực tiếp từ raw data.
-   Quality / Low Quality lấy từ subset đã match được AS.
-   Record không match được bị drop.
-   Unknown AS lại bị set bằng 0.

Kết quả là Dashboard nhìn hợp lệ về mặt hiển thị nhưng không reconcile
về mặt dữ liệu.

------------------------------------------------------------------------

## 5. URL Analysis bị mất backlink

  Metric                      Nguồn cuối      TOSA
  ------------------------- ------------ ---------
  URL được phân tích               1,251       971
  Backlink được aggregate         26,984    14,066
  Coverage                          100%   \~52.1%

### Sai lệch

TOSA đang thiếu:

-   **280 Target URLs**
-   **12,918 Backlinks**

Coverage thực tế:

``` text
14,066 / 26,984 ≈ 52.1%
```

Có nghĩa gần **47.9% backlink chưa được đưa vào URL Analysis**.

### Mức độ ưu tiên

**Critical / P0**

Nếu URL Analysis là nền tảng cho các sheet Topic Analysis và Dashboard
thì lỗi này sẽ lan truyền sang toàn bộ báo cáo phía sau.

------------------------------------------------------------------------

## 6. Khả năng lỗi nằm ở Domain Matching / AS Matching

TOSA có thêm trường:

-   `Topic` trong Pages
-   `Clean Domain` trong Referring Domain

Đây là hướng thiết kế hợp lý.

Tuy nhiên `Clean Domain` hoặc logic join có khả năng là nơi gây ra mất
dữ liệu.

Pipeline hiện tại có thể đang vận hành gần giống:

``` text
Backlink.Source URL
→ Extract Domain
→ Match Referring Domain
→ Match AS
→ Có AS: Quality / Low Quality
→ Không match: Drop record
```

Logic đúng nên là:

``` text
Backlink.Source URL
→ Normalize Domain
→ Lookup Referring Domain / AS

IF AS > 20:
    Quality
ELSE IF AS <= 20:
    Low Quality
ELSE:
    Unknown
```

### Nguyên tắc quan trọng

**Không được drop backlink chỉ vì không match được Authority Score.**

Mọi backlink phải thuộc đúng một trong ba nhóm:

``` text
Quality
Low Quality
Unknown
```

Và luôn phải đảm bảo:

``` text
Quality + Low Quality + Unknown = Total Backlinks
```

------------------------------------------------------------------------

## 7. Page Type chưa tương thích benchmark

### File nguồn cuối

  Page Type      URLs
  ----------- -------
  Deep Page     1,251

### TOSA

  Page Type        URLs
  ----------- ---------
  Product           684
  Other             172
  Brand              68
  Category           47
  **Total**     **971**

Có hai vấn đề riêng biệt.

### 7.1. Khác dimension

Benchmark đang sử dụng:

-   Homepage
-   Deep Page

TOSA sử dụng:

-   Product
-   Category
-   Brand
-   Other

Hai taxonomy này không nên thay thế nhau.

Nên tách thành hai dimension:

**Page Location**

``` text
Homepage
Deep Page
```

**Page Type**

``` text
Product
Category
Brand
Other
```

### 7.2. Thiếu URL

Ngay cả khi taxonomy khác nhau, TOSA vẫn chỉ classify **971 URLs**,
trong khi benchmark có **1,251 URLs**.

Do đó đây không chỉ là vấn đề naming mà còn liên quan đến việc URL bị
drop khỏi pipeline.

------------------------------------------------------------------------

## 8. Topic Classification chưa replicate benchmark

File nguồn cuối có taxonomy chi tiết hơn, khoảng **34 topic**, trong khi
TOSA chỉ còn khoảng **20 topic**.

Ví dụ taxonomy benchmark:

``` text
Chăm sóc cá nhân > Dầu gội
Chăm sóc cá nhân > Dầu xả
Chăm sóc cá nhân > Làm sạch cơ thể > Sữa tắm
Chăm sóc da > Chống nắng
Chăm sóc da > Tẩy trang - Làm sạch da > Tẩy trang
Chăm sóc da > Dưỡng da > Serum - Tinh chất
Mỹ phẩm > Mặt > Cushion - Phấn nước
...
```

TOSA đang aggregate ở level rộng hơn như:

``` text
Chăm sóc da
Chăm sóc cá nhân
Chăm sóc cá nhân > Chăm sóc tóc
Mỹ phẩm
Brand
Other - Non Product
Other - Product Unclassified
...
```

### Ví dụ

Benchmark:

``` text
Chăm sóc cá nhân > Dầu gội
→ 612 backlinks
```

TOSA có xu hướng đưa dữ liệu vào parent topic rộng hơn như:

``` text
Chăm sóc cá nhân > Chăm sóc tóc
```

### Đánh giá

Nếu requirement của TOSA là replicate báo cáo nguồn cuối thì **Topic
Taxonomy hiện tại chưa đủ độ chi tiết và chưa đồng nhất với benchmark**.

Cần đưa taxonomy benchmark thành một cấu hình/reference cố định thay vì
để tool tự suy diễn topic ở level khác.

------------------------------------------------------------------------

## 9. Dashboard chưa đầy đủ

Benchmark có khoảng **57 dòng metric**, trong khi TOSA hiện chỉ có
khoảng **6 dòng summary chính**.

Các metric benchmark có nhưng TOSA còn thiếu gồm:

-   Quality Rate
-   Low Quality Rate
-   Sitewide Backlinks
-   Sitewide Rate
-   Nofollow Backlinks
-   Nofollow Rate
-   Homepage Backlinks
-   Deep Page Backlinks
-   Homepage Share
-   Deep Page Share
-   Quality Homepage Backlinks
-   Quality Deep Page Backlinks
-   Largest Deep Page
-   Largest Deep Page Backlinks
-   Largest Deep Page Share
-   Distribution Check
-   Top URLs by Quality Backlinks
-   Top Topics by Quality Backlinks

### Đánh giá

TOSA hiện mới đáp ứng phần **basic backlink summary**, chưa đạt mức
reporting completeness của file benchmark.

------------------------------------------------------------------------

## 10. Đánh giá tổng thể

  Hạng mục                    Đánh giá                  Priority
  --------------------------- ------------------------- ----------
  Import raw data             Tốt -- gần như khớp       P3
  Giữ raw backlink records    Tốt                       P3
  Referring Domain data       Tốt                       P3
  Anchor data                 Tốt                       P3
  Domain normalization        Cần kiểm tra              P0
  AS matching                 Có vấn đề lớn             P0
  Quality classification      Sai                       P0
  Unknown classification      Sai nghiêm trọng          P0
  URL aggregation             Mất \~47.9% backlink      P0
  Page Location / Page Type   Logic chưa đồng nhất      P1
  Topic classification        Chưa replicate taxonomy   P1
  Dashboard                   Thiếu nhiều metric        P2
  Data reconciliation         Chưa đạt                  P0

------------------------------------------------------------------------

## 11. Thứ tự ưu tiên sửa TOSA

### P0 --- Data Integrity

#### 1. Fix Domain Normalization

Chuẩn hóa domain trước khi join:

-   lowercase
-   remove protocol
-   remove `www.`
-   remove trailing slash
-   xử lý subdomain theo rule rõ ràng
-   xử lý query string
-   xử lý port nếu có
-   xử lý domain malformed

#### 2. Fix AS Matching

Mọi backlink phải được lookup Referring Domain.

Nếu không tìm thấy AS:

``` text
AS Status = Unknown
```

Không được loại record.

#### 3. Fix Quality Classification

Rule:

``` text
AS > 20     → Quality
AS <= 20    → Low Quality
AS missing  → Unknown
```

#### 4. Fix URL Aggregation

Mọi Target URL trong backlink dataset phải được aggregate.

Expected:

``` text
SUM(URL Analysis.Total Backlinks)
=
Raw Backlink Count
```

Với dataset hiện tại:

``` text
Expected = 26,984
```

------------------------------------------------------------------------

### P1 --- Classification

#### 5. Tách Page Location và Page Type

Không sử dụng `Product / Category / Brand` thay cho
`Homepage / Deep Page`.

Nên có:

``` text
Page Location:
- Homepage
- Deep Page

Page Type:
- Product
- Category
- Brand
- Other
```

#### 6. Replicate Topic Taxonomy

Dùng taxonomy của benchmark làm reference.

Ưu tiên mapping theo:

``` text
URL
→ Page metadata
→ Topic taxonomy
```

Hạn chế tự gom category lên parent level nếu benchmark đang yêu cầu
taxonomy chi tiết.

------------------------------------------------------------------------

### P2 --- Reporting

#### 7. Hoàn thiện Dashboard

Sau khi data integrity đã đúng mới bổ sung:

-   Rates
-   Homepage / Deep Page distribution
-   Sitewide
-   Nofollow
-   Quality distribution
-   Top URL
-   Top Topic
-   Concentration
-   Distribution checks

Không nên ưu tiên làm đẹp Dashboard trước khi P0 được giải quyết.

------------------------------------------------------------------------

## 12. Validation Gate nên bổ sung vào tool

TOSA nên có bước validation tự động trước khi xuất report.

### Check 1 --- Quality Reconciliation

``` text
Quality
+ Low Quality
+ Unknown
=
Total Backlinks
```

Nếu FALSE:

``` text
REPORT STATUS = FAILED
```

### Check 2 --- URL Aggregation

``` text
SUM(URL Analysis.Total Backlinks)
=
Total Backlinks
```

Nếu FALSE:

``` text
REPORT STATUS = FAILED
```

### Check 3 --- Topic Aggregation

Nếu mỗi URL chỉ thuộc một topic:

``` text
SUM(Topic Analysis.Total Backlinks)
=
Total Backlinks
```

### Check 4 --- URL Coverage

``` text
Distinct Target URLs in Backlink
=
URLs in URL Analysis
```

### Check 5 --- Quality Breakdown

``` text
SUM(URL Analysis.Quality)
=
Dashboard.Quality
```

Tương tự với:

``` text
Low Quality
Unknown
```

### Check 6 --- Không cho phép silent drop

Nên có metric:

``` text
Unmatched Domain Count
Unmatched Backlink Count
Unclassified URL Count
Unclassified Topic Count
```

Tool phải hiển thị các record không classify được thay vì bỏ qua.

------------------------------------------------------------------------

## 13. Expected Result sau khi sửa

Sau khi sửa pipeline, TOSA cần đạt tối thiểu:

``` text
Raw Backlinks
        ↓
     26,984
        ↓
 ┌──────┼─────────┐
 ↓      ↓         ↓
Quality Low     Unknown
1,180  11,323   14,481
 └──────┼─────────┘
        ↓
     26,984
```

Đồng thời:

``` text
URL Analysis
SUM Total Backlinks
= 26,984
```

và:

``` text
Topic Analysis
SUM Total Backlinks
= 26,984
```

Các Dashboard metric phải được tính từ cùng một processed dataset thay
vì lấy từng metric từ các population khác nhau.

------------------------------------------------------------------------

## 14. Kết luận

TOSA đã làm tốt phần **ingestion raw data**, vì các dataset chính giữa
hai file gần như khớp hoàn toàn.

Vấn đề hiện tại tập trung ở tầng:

``` text
Domain Matching
        ↓
AS Matching
        ↓
Quality Classification
        ↓
URL Aggregation
        ↓
Topic Classification
        ↓
Dashboard
```

Bug quan trọng nhất là TOSA chỉ aggregate **14,066 / 26,984 backlinks
(\~52.1%)**, khiến khoảng **12,918 backlink (\~47.9%)** không được phản
ánh trong URL Analysis, trong khi Dashboard vẫn báo `Unknown AS = 0`.

Do đó, ưu tiên hiện tại **không nên là bổ sung thêm tính năng hoặc làm
đẹp report**. Cần sửa **data integrity và reconciliation trước**.

Sau khi các validation sau đều PASS:

``` text
Quality + Low + Unknown = Total
URL Analysis Total = Raw Total
Topic Analysis Total = Raw Total
Distinct Target URL Coverage = 100%
```

mới nên tiếp tục hoàn thiện taxonomy và Dashboard.

**Kết luận cuối:** TOSA có nền tảng raw-data tốt nhưng pipeline phân
tích hiện chưa đủ tin cậy để sử dụng output làm báo cáo backlink cuối
cùng. Trọng tâm sprint tiếp theo nên là **P0 Data Integrity → P1
Classification → P2 Reporting**.
