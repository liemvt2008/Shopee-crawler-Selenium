# Simple crawler shopee web using Selenium

This tool helps user get product data and user rating to build up recommendation system and orthers application using machine learing or deep learning.

# Installation:

  - [Download](https://github.com/mozilla/geckodriver/releases) Firefox geckodriver, unzip, move to /usr/local/bin (macOS/Linux)
  - `pip install -r requirements.txt`

# Instruction:

Crawler need 4 parameter:

* Type Crawler - Cralwer currently support 2 type is `product` and `rating`
* Product limit - Number product want to crawl, default value is 200 product, you can increase if need more data
* Rating limit - Number user rating want to crawl, default value is 30 user/product, you can increase if need more data
* Category index - Index of category want to crawl , index can be a number or a list of number with multiple index for crawling. Default is None this mean crawler with crawl all category
* Please reference table below:


| Index | Category | Index | Category |
| ------ | ------ | ------ | ------ |
| 0 | Thoi_trang_nam | 13 |  Phu_kien_thoi_trang|
| 1 | Thoi_trang_nu | 14 |  TB_dien_gia_dung|
| 2 | Dien_thoai_Phu_kien | 15 |  Bach_hoa_online|
| 3 | Me_be | 16 |  The_thao_du_lich|
| 4 | Thiet_bi_DT | 17 |  Voucher_dich_vu|
| 5 | Nha_cua_va_doi_song | 18 |  Oto_xe_may_xe_dap|
| 6 | May_tinh_Laptop | 19 |  Nha_sach_online|
| 7 | Suc_khoe_Sac_dep | 20 |  Do_choi|
| 8 | May_anh_quay_phim | 21 |  Giat_giu_cham_soc_nha_cua|
| 9 | Giay_dep_nu | 22 |  Cham_soc_thu_cung|
| 10 | Dong_ho | 23 |  Thoi_trang_tre_em|
| 11 | Tui_vi | 24 |  San_pham_khac|
| 12 | Giay_dep_nam | - |  None|

# Execution
```bash
python crawler.py --crawl product --product_limit 20 --index [1,2,3]
```
Crawl product from shopee with 200 product/categpry and crawl from category Thoi_trang_nu, Dien_thoai_Phu_kien, Me_be

##### or
```bash
python crawler.py --crawl rating --product_limit 20 --rating_limit 30 --index 5
```
Crawl rating user from shopee with 200 product/category, 30 rating user/product and crawl from category Nha_cua_va_doi_song

# Note:
The result will appear in folder data_collected with filename is {category}_{crawl_type}.csv
Sometimes, if you need to crawl difference product page, please feel free to change to product page on the browser of selenium control, crawler will get the latest info from automation browser