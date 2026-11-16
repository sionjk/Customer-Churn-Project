# Working data dictionary

Source: the supplied workbook's `Data Dict` sheet. Descriptions below are
lightly paraphrased. The notes distinguish source definitions from issues
that remain unverified. One row appears to represent a customer; unique IDs
alone do not prove independent observations. Preserve source column spellings.

| Column | Source meaning | Role and interpretation notes |
|---|---|---|
| CustomerID | Unique customer ID | Identifier; preserve for tracing records, exclude from model features. |
| Churn | Churn flag | Eventual target; source dictionary does not specify 0/1 mapping, churn definition, or prediction window. |
| Tenure | Customer tenure with the organization | Numeric duration; unit is not specified. Do not label months without evidence. |
| PreferredLoginDevice | Preferred login device | Category; Phone, Mobile Phone, and Computer are observed. Investigate overlap. |
| CityTier | City tier | Coded category; definitions and ordering implications need documentation. |
| WarehouseToHome | Warehouse-to-customer-home distance | Numeric measurement; distance unit unspecified. |
| PreferredPaymentMode | Preferred payment method | Category; investigate CC/Credit Card and COD/Cash on Delivery. |
| Gender | Customer gender | Category; describe the recorded data without assuming broader representativeness. Eventual inclusion needs a purpose. |
| HourSpendOnApp | Hours spent on the app or website | Numeric duration in hours; aggregation period unspecified. |
| NumberOfDeviceRegistered | Number of registered devices | Count; numerical storage does not resolve data-quality questions. |
| PreferedOrderCat | Preferred order category in the last month | Category; investigate Mobile versus Mobile Phone. Spelling is from the source. |
| SatisfactionScore | Customer service satisfaction score | Ordered score; observed 1-5. Source does not define anchors or explicitly confirm direction. |
| MaritalStatus | Marital status | Category; eventual use needs a reason relevant to the question. |
| NumberOfAddress | Number of added addresses | Count; unusually large values require context. |
| Complain | Whether a complaint was raised in the last month | Flag; observed 0/1. Confirm coding and whether available before churn. |
| OrderAmountHikeFromlastYear | Percentage increase in orders from last year | Percentage-like measurement; wording does not fully clarify amount versus count or calculation details. |
| CouponUsed | Number of coupons used in the last month | Count; zero and missing have different meanings. |
| OrderCount | Number of orders placed in the last month | Count; missing values do not establish zero orders. |
| DaySinceLastOrder | Days since the customer's last order | Numeric recency in days; reference date unspecified. |
| CashbackAmount | Average cashback in the last month | Numeric amount; currency unspecified. Not a documented measure of revenue or total spending. |

## Definitions to resolve before interpretation

1. What exactly constitutes churn, what do its codes mean, and when was it measured?
2. Were proposed predictors measured before the recorded churn event?
3. What are the tenure and distance units and cashback currency?
4. What time window does app usage summarize?
5. Are matching profiles under different IDs independent customers or copied records?
6. What is known about the source business, collection process, and representativeness?

If a definition cannot be established, record that limitation rather than
inventing a unit, date, population, or future prediction horizon.
