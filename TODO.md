# TODO: Fix 5 Problems in Streamlit App

1. **Add missing 'icon' key to insights in page_analytics** - The insights list is missing the 'icon' key, causing KeyError when accessing insight['icon'].

2. **Move Insights section inside forecast success block in page_forecaster** - The "Insights & Recommendations" section is displayed even when forecast fails, which should only show on success.

3. **Fix invalid date format in api_post call** - Change "%Y-%m-d" to "%Y-%m-%d" for proper date formatting.

4. **Fix Waste_Reduction list length mismatch in page_analytics** - Add a 4th value to match the 4 seasons.

5. **Ensure insights in page_analytics have proper icons** - Add appropriate icons to the insights list in page_analytics.
