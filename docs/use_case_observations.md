# Use Case Observation Candidates

Generated from `employmentdata.csv` and `tourism15indicators.csv`.

Scope notes:
- Selected country set: Spain, Thailand, Morocco, Dominican Republic, Mexico, South Africa, Indonesia, Croatia, Colombia.
- Snapshot year: 2020; latest-available mode uses the most recent non-missing value at or before 2020.
- Employment-sector shares are gender-average percentages computed from the male and female WDI employment shares.
- Coverage percentages use the 20 CSV year columns (2006-2025) as the denominator.

## 1. Latest-Available Snapshot for 2020

| Country | Tourism receipts | Services | Industry | Agriculture | Poverty | Gini | GDP per capita | Urban population |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spain | n/a | 76.4 (2020) | 19.9 (2020) | 3.7 (2020) | 21.7 (2020) | 34.9 (2020) | 27,234 (2020) | 79.7 (2020) |
| Thailand | 6.0 (2020) | 46.6 (2020) | 22.3 (2020) | 31.1 (2020) | 6.8 (2020) | 35.0 (2020) | 6,986 (2020) | 57.2 (2020) |
| Morocco | 12.0 (2020) | 43.7 (2020) | 19.7 (2020) | 36.6 (2020) | 4.8 (2013) | 39.5 (2013) | 3,268 (2020) | 62.1 (2020) |
| Dominican Republic | 37.7 (2018) | 74.9 (2020) | 17.6 (2020) | 7.5 (2020) | 30.4 (2020) | 39.6 (2020) | 7,135 (2020) | 73.3 (2020) |
| Mexico | 2.6 (2020) | 65.4 (2020) | 23.1 (2020) | 11.5 (2020) | 43.9 (2020) | 44.6 (2020) | 8,841 (2020) | 78.7 (2020) |
| South Africa | 2.9 (2020) | 74.4 (2020) | 20.3 (2020) | 5.3 (2020) | 46.7 (2014) | 59.6 (2014) | 5,581 (2020) | 63.4 (2020) |
| Indonesia | 2.0 (2020) | 50.6 (2020) | 20.7 (2020) | 28.7 (2020) | 9.8 (2020) | 35.3 (2020) | 3,854 (2020) | 56.3 (2020) |
| Croatia | 23.4 (2020) | 66.9 (2020) | 27.0 (2020) | 6.1 (2020) | n/a | 29.5 (2020) | 14,808 (2020) | 56.5 (2020) |
| Colombia | 5.1 (2020) | 67.2 (2020) | 18.7 (2020) | 14.1 (2020) | 43.1 (2020) | 54.4 (2020) | 5,340 (2020) | 77.6 (2020) |

## 2. Tourism Receipts vs Services Employment

- Countries with both values in the 2020 latest-available snapshot: 8 of 9.
- Highest tourism receipts among paired countries: Dominican Republic at 37.7 (2018).
- Highest services employment among paired countries: Dominican Republic at 74.9 (2020).

| Country | Tourism receipts | Services | Services minus paired mean |
| --- | --- | --- | --- |
| Dominican Republic | 37.7 (2018) | 74.9 (2020) | 13.7 |
| Croatia | 23.4 (2020) | 66.9 (2020) | 5.7 |
| Morocco | 12.0 (2020) | 43.7 (2020) | -17.5 |
| Thailand | 6.0 (2020) | 46.6 (2020) | -14.6 |
| Colombia | 5.1 (2020) | 67.2 (2020) | 6.0 |
| South Africa | 2.9 (2020) | 74.4 (2020) | 13.2 |
| Mexico | 2.6 (2020) | 65.4 (2020) | 4.2 |
| Indonesia | 2.0 (2020) | 50.6 (2020) | -10.6 |

## 3. First and Latest Available Employment-Sector Shares

| Country | First year | First services | First industry | First agriculture | Latest year | Latest services | Latest industry | Latest agriculture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Colombia | 2006 | 63.6 | 20.2 | 16.2 | 2025 | 68.2 | 18.9 | 12.9 |
| Croatia | 2006 | 57.4 | 28.3 | 14.3 | 2025 | 70.0 | 25.8 | 4.3 |
| Dominican Republic | 2006 | 68.9 | 21.4 | 9.7 | 2025 | 76.6 | 17.3 | 6.1 |
| Indonesia | 2006 | 41.6 | 16.7 | 41.6 | 2025 | 51.6 | 21.4 | 26.9 |
| Mexico | 2006 | 64.7 | 22.7 | 12.6 | 2025 | 66.4 | 23.3 | 10.3 |
| Morocco | 2006 | 31.6 | 17.8 | 50.6 | 2025 | 47.5 | 20.9 | 31.6 |
| South Africa | 2006 | 69.6 | 24.8 | 5.7 | 2025 | 74.7 | 20.0 | 5.3 |
| Spain | 2006 | 68.9 | 26.4 | 4.7 | 2025 | 77.6 | 19.1 | 3.3 |
| Thailand | 2006 | 40.0 | 20.3 | 39.7 | 2025 | 49.8 | 22.0 | 28.3 |

## 4. Structural Shifts in Employment Sectors

- Largest services increase: Morocco at 15.9 percentage points.
- Largest industry change by absolute value: Spain at -7.3 percentage points.
- Largest agriculture change by absolute value: Morocco at -18.9 percentage points.

| Country | Years | Services change | Industry change | Agriculture change |
| --- | --- | --- | --- | --- |
| Morocco | 2006-2025 | 15.9 | 3.0 | -18.9 |
| Croatia | 2006-2025 | 12.6 | -2.5 | -10.1 |
| Indonesia | 2006-2025 | 10.0 | 4.7 | -14.7 |
| Thailand | 2006-2025 | 9.7 | 1.7 | -11.4 |
| Spain | 2006-2025 | 8.7 | -7.3 | -1.4 |
| Dominican Republic | 2006-2025 | 7.7 | -4.1 | -3.6 |
| South Africa | 2006-2025 | 5.2 | -4.8 | -0.4 |
| Colombia | 2006-2025 | 4.7 | -1.3 | -3.4 |
| Mexico | 2006-2025 | 1.7 | 0.6 | -2.3 |

## 5. Data Coverage Percentages

| Indicator | Spain | Thailand | Morocco | Dominican Republic | Mexico | South Africa | Indonesia | Croatia | Colombia | Mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tourism receipts (% of exports) | 0% | 75% | 75% | 65% | 75% | 75% | 75% | 75% | 75% | 66% |
| Poverty headcount (%) | 85% | 85% | 15% | 50% | 25% | 20% | 95% | 10% | 65% | 50% |
| Gini index | 90% | 95% | 10% | 95% | 50% | 20% | 100% | 80% | 85% | 69% |
| GDP per capita (current US$) | 95% | 95% | 95% | 95% | 95% | 95% | 95% | 95% | 95% | 95% |
| Urban population (%) | 95% | 95% | 95% | 95% | 95% | 95% | 95% | 95% | 95% | 95% |
| Employment sectors, all three (%) | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

## 6. Ranked Lists

### Highest Tourism Dependence

| Rank | Country | Tourism receipts |
| --- | --- | --- |
| 1 | Dominican Republic | 37.7 (2018) |
| 2 | Croatia | 23.4 (2020) |
| 3 | Morocco | 12.0 (2020) |
| 4 | Thailand | 6.0 (2020) |
| 5 | Colombia | 5.1 (2020) |
| 6 | South Africa | 2.9 (2020) |
| 7 | Mexico | 2.6 (2020) |
| 8 | Indonesia | 2.0 (2020) |

### Highest Service Employment

| Rank | Country | Services |
| --- | --- | --- |
| 1 | Spain | 76.4 (2020) |
| 2 | Dominican Republic | 74.9 (2020) |
| 3 | South Africa | 74.4 (2020) |
| 4 | Colombia | 67.2 (2020) |
| 5 | Croatia | 66.9 (2020) |
| 6 | Mexico | 65.4 (2020) |
| 7 | Indonesia | 50.6 (2020) |
| 8 | Thailand | 46.6 (2020) |
| 9 | Morocco | 43.7 (2020) |

### Largest Increase in Services

| Rank | Country | Years | First services | Latest services | Change |
| --- | --- | --- | --- | --- | --- |
| 1 | Morocco | 2006-2025 | 31.6 | 47.5 | 15.9 |
| 2 | Croatia | 2006-2025 | 57.4 | 70.0 | 12.6 |
| 3 | Indonesia | 2006-2025 | 41.6 | 51.6 | 10.0 |
| 4 | Thailand | 2006-2025 | 40.0 | 49.8 | 9.7 |
| 5 | Spain | 2006-2025 | 68.9 | 77.6 | 8.7 |
| 6 | Dominican Republic | 2006-2025 | 68.9 | 76.6 | 7.7 |
| 7 | South Africa | 2006-2025 | 69.6 | 74.7 | 5.2 |
| 8 | Colombia | 2006-2025 | 63.6 | 68.2 | 4.7 |
| 9 | Mexico | 2006-2025 | 64.7 | 66.4 | 1.7 |

### Sparsest Poverty/Gini Coverage

| Rank | Country | Poverty coverage | Gini coverage | Average |
| --- | --- | --- | --- | --- |
| 1 | Morocco | 15% | 10% | 12% |
| 2 | South Africa | 20% | 20% | 20% |
| 3 | Mexico | 25% | 50% | 38% |
| 4 | Croatia | 10% | 80% | 45% |
| 5 | Dominican Republic | 50% | 95% | 72% |
| 6 | Colombia | 65% | 85% | 75% |
| 7 | Spain | 85% | 90% | 88% |
| 8 | Thailand | 85% | 95% | 90% |
| 9 | Indonesia | 95% | 100% | 98% |
