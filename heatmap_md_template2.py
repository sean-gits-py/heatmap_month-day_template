#heatmap_md_template2.py

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Generate a date range from 1/1/2024 to 12/31/2024
start_date = pd.to_datetime('2024-01-01')
end_date = pd.to_datetime('2024-12-31')
dates = pd.date_range(start=start_date, end=end_date)

# 2. Load activity data from a CSV file
# Ensure your CSV has 'date' and 'activity' columns
# Adjust the file path as needed
activity_df = pd.read_csv('activity_data.csv')

# 3. Convert 'date' column to datetime if it's not already
activity_df['date'] = pd.to_datetime(activity_df['date'])

# 4. Filter activity data to include only dates within the specified range
activity_df = activity_df[(activity_df['date'] >= start_date) & (activity_df['date'] <= end_date)]

# 5. Merge the activity data with the full date range to ensure all dates are represented
# This ensures that dates with zero activity are included
df = pd.DataFrame({'date': dates})
df = df.merge(activity_df, on='date', how='left')
df['activity'] = df['activity'].fillna(0)

# 6. Add 'day_of_week' and 'week' columns to the DataFrame
df['day_of_week'] = df['date'].dt.dayofweek  # Monday=0, Sunday=6
df['day_of_week'] = (df['day_of_week'] + 1) % 7  # Shift so Sunday=0, Saturday=6

# Create a unique 'week' index starting from 0
df['week'] = ((df['date'] - start_date).dt.days) // 7

# 7. Pivot the DataFrame to create a matrix suitable for a heatmap
heatmap_data = df.pivot_table(index='day_of_week', columns='week', values='activity', aggfunc='sum')

# 8. Reorder the days of the week to start from Sunday
day_order = [0, 1, 2, 3, 4, 5, 6]
heatmap_data = heatmap_data.reindex(day_order)

# 9. Prepare month labels for the x-axis
week_starts = df.groupby('week')['date'].min()
week_months = week_starts.dt.strftime('%b')
month_changes = week_months[week_months != week_months.shift(1)].index

# 10. Create the heatmap using Plotly
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    colorscale='Greens',
    xgap=1,  # Gap between cells
    ygap=1,
    hoverongaps=False,
    colorbar=dict(title='Activity')
))

# 11. Update layout for better appearance
fig.update_layout(
    title='Activity Heatmap for 2024',
    xaxis_nticks=53,
    yaxis_nticks=7,
    yaxis=dict(autorange='reversed'),  # To have Sunday at the top
    template='plotly_white',
    xaxis_title='Month',
    yaxis_title='Day of Week',
    margin=dict(l=40, r=40, t=40, b=40)
)

# 12. Update x-axis ticks to show month names at the correct positions
fig.update_xaxes(
    tickmode='array',
    tickvals=month_changes,
    ticktext=week_months[month_changes],
    tickangle=0
)

# 13. Display the heatmap
fig.show()
