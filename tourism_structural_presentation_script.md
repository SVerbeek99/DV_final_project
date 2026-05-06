# 5-Minute Presentation Script
## Tourism and Structural Transformation

### Slide 1 — Title and motivation (0:00–0:40)
Our project is called **Tourism and Structural Transformation**. The motivation is that tourism is often presented as a positive development strategy because it brings international receipts, supports services, and can increase GDP. However, tourism-led development may also create a more specialized economic structure. Instead of strengthening a broad productive base, some countries may shift employment away from agriculture or industry and become increasingly service-oriented.

The question we want to explore is not whether tourism is good or bad in general. Instead, we ask whether countries that depend more on tourism show a different pattern of structural transformation than less tourism-dependent countries.

### Slide 2 — Research question and hypothesis (0:40–1:20)
Our main research question is:

**How does tourism dependence relate to changes in employment structure, and do these changes correspond to broader development outcomes?**

Our central hypothesis is:

**Countries with stronger tourism dependence tend to shift their employment structure toward services, while agriculture and industry lose relative weight. This shift may coincide with GDP growth, but not always with lower poverty or inequality.**

This is an exploratory hypothesis. We are not claiming that tourism directly causes the decline of agriculture or industry. Instead, the dashboard is designed to reveal structural patterns and exceptions across countries and over time.

### Slide 3 — Data and variables: What (1:20–2:00)
We use World Development Indicators data for 15 countries between 2006 and 2025. The most complete part of the dataset is employment by sector, which is available for agriculture, industry, and services, separately for male and female employment.

The main indicators are:
- international tourism receipts as a percentage of total exports,
- employment in agriculture, industry, and services,
- GDP per capita,
- urban population,
- poverty headcount,
- and GINI index where available.

From Munzner’s “What” perspective, this is tabular, temporal, multivariate data. Countries are the main items, year is the temporal dimension, and the indicators are mostly quantitative attributes.

### Slide 4 — User tasks: Why (2:00–2:45)
The dashboard is designed for exploratory analysis. Users should be able to perform several tasks:

First, they can compare countries by tourism dependence and sectoral employment. Second, they can inspect whether highly tourism-dependent countries are more service-oriented. Third, they can follow the employment structure of one country over time. Fourth, they can compare whether the service shift coincides with GDP, poverty, or inequality outcomes.

In abstract visualization terms, the tasks are to compare, correlate, filter, inspect temporal trends, detect outliers, and connect patterns across multiple coordinated views. These tasks are difficult to solve with a single chart or a table, which is why an interactive dashboard is appropriate.

### Slide 5 — Dashboard design: How (2:45–4:10)
The first view is a scatter plot where the x-axis shows tourism receipts and the y-axis shows a selected sectoral employment variable, for example services employment or industry employment. Position is used because it is one of the strongest visual channels for quantitative comparison. Color encodes region, and size represents GDP per capita.

The second view shows tourism receipts against a social or development outcome, such as poverty headcount, GINI, GDP per capita, or urban population. This view helps us examine whether tourism-oriented structural transformation is associated with broader development outcomes.

The third view is a time-series chart for a selected country. It shows employment in agriculture, industry, and services over time, with tourism receipts shown as an additional trend. This supports temporal inspection and helps users understand whether a country is becoming more service-oriented.

The fourth view compares sector composition across selected countries using grouped bars. This helps users directly compare employment structures.

Finally, we include a data coverage heatmap. This is important because tourism, poverty, and GINI are not available for all country-years. Instead of hiding missing data, we make it visible as part of the analytical design.

The interaction strategy is based on filtering and linked views. Users can select countries, change the year, switch between exact-year and latest-available data, and click a country in the scatter plot to update the time-series panel.

### Slide 6 — Expected insights and limitations (4:10–5:00)
We expect to find that several tourism-dependent countries show a strong service-oriented employment profile. In some cases, this may happen alongside declining agriculture or stagnant industry. However, the dashboard also allows us to identify exceptions: countries with high tourism but still significant industry, or countries with service growth but limited improvement in poverty or inequality.

A key limitation is that the dashboard does not establish causality. Tourism may be one factor among many, and employment shifts can also be driven by urbanization, education, trade, or broader economic development. Another limitation is missing data for tourism, poverty, and GINI. This is why our main structural analysis relies on the complete employment series, while social outcomes are used as contextual evidence.

Overall, the contribution of the project is an interactive tool that helps users explore how tourism-led development relates to structural transformation and uneven development outcomes.
