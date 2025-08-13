import re
from datetime import datetime, timedelta
from xmlrpc.client import DateTime

import matplotlib.pyplot as plt
import pandas as pd

import plotly.express as px

# Example input: logs per receiver
logs = {
    'receiver1': '''Automated message sent at 2025-06-21 05:57:49
Automated message sent at 2025-06-21 05:47:49
Automated message sent at 2025-06-21 05:37:49
Automated message sent at 2025-06-21 05:17:49
Automated message sent at 2025-06-21 04:57:49
Automated message sent at 2025-06-21 04:47:49
Automated message sent at 2025-06-21 04:17:48
Automated message sent at 2025-06-21 03:47:48
Automated message sent at 2025-06-21 03:37:48
Automated message sent at 2025-06-21 02:57:47
Automated message sent at 2025-06-21 02:37:47''',
    'receiver2':'''Automated message sent at 2025-06-24 18:19:28
Automated message sent at 2025-06-24 18:09:27
Automated message sent at 2025-06-24 17:59:27
Automated message sent at 2025-06-24 17:39:27
Automated message sent at 2025-06-24 17:19:27
Automated message sent at 2025-06-24 16:59:27
Automated message sent at 2025-06-24 16:19:26
Automated message sent at 2025-06-24 15:59:26
Automated message sent at 2025-06-24 15:09:26
Automated message sent at 2025-06-24 14:59:25
Automated message sent at 2025-06-24 14:39:25
Automated message sent at 2025-06-24 14:29:25
Automated message sent at 2025-06-24 14:09:25
Automated message sent at 2025-06-24 13:59:25
Automated message sent at 2025-06-24 13:39:25
Automated message sent at 2025-06-24 13:29:24
Automated message sent at 2025-06-24 13:09:24
Automated message sent at 2025-06-24 12:59:24
Automated message sent at 2025-06-24 12:38:40
Automated message sent at 2025-06-24 12:28:40
Automated message sent at 2025-06-24 12:08:40
Automated message sent at 2025-06-24 11:18:40
Automated message sent at 2025-06-24 11:08:39
Automated message sent at 2025-06-24 10:48:39
Automated message sent at 2025-06-24 10:38:39
Automated message sent at 2025-06-24 10:28:39
Automated message sent at 2025-06-24 10:08:39
Automated message sent at 2025-06-24 09:48:39
Automated message sent at 2025-06-24 09:38:38
Automated message sent at 2025-06-24 09:28:38
Automated message sent at 2025-06-24 08:38:38
Automated message sent at 2025-06-24 08:28:38
Automated message sent at 2025-06-23 17:28:28
Automated message sent at 2025-06-23 17:18:28
Automated message sent at 2025-06-23 16:08:27
Automated message sent at 2025-06-23 15:48:27
Automated message sent at 2025-06-23 15:38:27
Automated message sent at 2025-06-23 15:28:27
Automated message sent at 2025-06-23 15:18:27
Automated message sent at 2025-06-23 14:38:26
Automated message sent at 2025-06-23 14:28:26
Automated message sent at 2025-06-23 14:18:26
Automated message sent at 2025-06-23 13:58:26
Automated message sent at 2025-06-23 13:48:26
Automated message sent at 2025-06-23 13:38:26
Automated message sent at 2025-06-23 13:08:25
Automated message sent at 2025-06-23 12:58:25
Automated message sent at 2025-06-23 12:48:25
Automated message sent at 2025-06-23 12:18:25
Automated message sent at 2025-06-23 12:08:25
Automated message sent at 2025-06-23 11:38:24
Automated message sent at 2025-06-23 10:58:24
Automated message sent at 2025-06-23 10:18:23
Automated message sent at 2025-06-23 09:08:23
Automated message sent at 2025-06-23 08:18:22
Automated message sent at 2025-06-23 08:08:22
Automated message sent at 2025-06-23 07:58:22
Automated message sent at 2025-06-23 07:38:22
Automated message sent at 2025-06-23 06:58:21
Automated message sent at 2025-06-23 06:48:21
Automated message sent at 2025-06-23 06:28:21
Automated message sent at 2025-06-23 06:18:21
Automated message sent at 2025-06-23 06:08:21
Automated message sent at 2025-06-23 05:48:20
Automated message sent at 2025-06-22 16:28:12
Automated message sent at 2025-06-22 15:38:11
Automated message sent at 2025-06-22 15:28:11
Automated message sent at 2025-06-22 13:48:10
Automated message sent at 2025-06-22 13:28:10
Automated message sent at 2025-06-22 13:18:10
Automated message sent at 2025-06-22 12:28:09
Automated message sent at 2025-06-22 12:08:09
Automated message sent at 2025-06-22 11:28:09
Automated message sent at 2025-06-22 10:58:08
Automated message sent at 2025-06-22 10:38:08
Automated message sent at 2025-06-22 10:28:08
Automated message sent at 2025-06-22 10:18:08
Automated message sent at 2025-06-22 10:08:08
Automated message sent at 2025-06-22 09:08:07
Automated message sent at 2025-06-22 08:58:07
Automated message sent at 2025-06-22 08:48:07
Automated message sent at 2025-06-22 08:38:07
Automated message sent at 2025-06-22 08:18:06
Automated message sent at 2025-06-22 07:58:06
Automated message sent at 2025-06-22 07:48:06
Automated message sent at 2025-06-22 07:38:06
Automated message sent at 2025-06-22 07:18:06
Automated message sent at 2025-06-22 06:38:05
Automated message sent at 2025-06-22 06:28:05
Automated message sent at 2025-06-22 06:18:05
Automated message sent at 2025-06-22 06:08:05
Automated message sent at 2025-06-22 05:58:05
Automated message sent at 2025-06-22 05:48:05
Automated message sent at 2025-06-22 05:28:05
Automated message sent at 2025-06-22 05:18:05
Automated message sent at 2025-06-22 05:08:04
Automated message sent at 2025-06-22 04:08:04
Automated message sent at 2025-06-22 03:48:04
Automated message sent at 2025-06-22 02:48:03
Automated message sent at 2025-06-22 02:38:03
Automated message sent at 2025-06-21 01:27:47
Automated message sent at 2025-06-21 01:07:46
Automated message sent at 2025-06-21 00:07:46
Automated message sent at 2025-06-20 23:57:46
Automated message sent at 2025-06-20 23:37:45
Automated message sent at 2025-06-20 23:27:45
Automated message sent at 2025-06-20 23:07:45
Automated message sent at 2025-06-20 22:57:45
Automated message sent at 2025-06-20 22:47:45
Automated message sent at 2025-06-20 22:27:45
Automated message sent at 2025-06-20 22:17:44
Automated message sent at 2025-06-20 22:07:44
Automated message sent at 2025-06-20 21:07:44
Automated message sent at 2025-06-20 20:57:44
Automated message sent at 2025-06-20 20:47:43
Automated message sent at 2025-06-20 20:37:43
Automated message sent at 2025-06-20 20:27:43
Automated message sent at 2025-06-20 20:07:43
Automated message sent at 2025-06-20 19:57:43
Automated message sent at 2025-06-20 19:27:43
Automated message sent at 2025-06-20 18:47:42
Automated message sent at 2025-06-20 18:37:42
Automated message sent at 2025-06-20 18:07:42
Automated message sent at 2025-06-20 17:57:42
Automated message sent at 2025-06-20 17:27:41
Automated message sent at 2025-06-20 17:17:41
Automated message sent at 2025-06-20 16:17:41''',
    "receiver3":'''Automated message sent at 2025-06-25 04:49:34
Automated message sent at 2025-06-25 05:09:35
Automated message sent at 2025-06-25 05:59:35
Automated message sent at 2025-06-25 06:39:36
Automated message sent at 2025-06-25 06:49:36
Automated message sent at 2025-06-25 02:39:33
Automated message sent at 2025-06-25 03:09:33
Automated message sent at 2025-06-25 03:29:34
Automated message sent at 2025-06-25 04:19:34
Automated message sent at 2025-06-24 11:18:40
Automated message sent at 2025-06-24 12:28:40
Automated message sent at 2025-06-24 15:29:26
Automated message sent at 2025-06-23 13:28:25
Automated message sent at 2025-06-23 14:38:26
Automated message sent at 2025-06-23 18:18:29
Automated message sent at 2025-06-25 11:29:39
Automated message sent at 2025-06-26 05:19:50
Automated message sent at 2025-06-26 03:59:49
Automated message sent at 2025-06-26 03:49:49
Automated message sent at 2025-06-26 03:39:49
Automated message sent at 2025-06-26 01:49:48
Automated message sent at 2025-06-26 01:39:48
Automated message sent at 2025-06-26 01:29:48
Automated message sent at 2025-06-26 01:19:48
Automated message sent at 2025-06-26 00:59:47
Automated message sent at 2025-06-26 00:39:47
Automated message sent at 2025-06-25 23:59:47
Automated message sent at 2025-06-25 23:49:47
Automated message sent at 2025-06-25 23:19:46
Automated message sent at 2025-06-25 21:19:45'''
}

# Parse timestamps
timestamp_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
recv_times = {
    recv: sorted(
        datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        for ts in re.findall(timestamp_pattern, text)
    )
    for recv, text in logs.items()
}

# Build expected timeline at 10-min intervals with fixed start
fixed_start = datetime.strptime('2025-06-19 14:47:41', '%Y-%m-%d %H:%M:%S')
end_time = max(t for times in recv_times.values() for t in times)
expected = []
cur = fixed_start
while cur <= end_time:
    expected.append(cur)
    cur += timedelta(minutes=10)

# Match each expected timestamp within ± tolerance
tolerance = timedelta(seconds=180)
records = []
for recv, times in recv_times.items():
    for ts in expected:
        records.append({
            'receiver': recv,
            'timestamp': ts,
            'received': any(abs(ts - t) <= tolerance for t in times)
        })
df = pd.DataFrame(records)

# Find continuous segments where messages are within 2 hours apart
continuous_segments = {}
max_gap = timedelta(hours=5)
for recv, group in df[df['received']].groupby('receiver'):
    times = group['timestamp'].sort_values().tolist()
    segments = []
    segment = [times[0]]
    for i in range(1, len(times)):
        if times[i] - times[i - 1] <= max_gap:
            segment.append(times[i])
        else:
            segments.append(segment)
            segment = [times[i]]
    segments.append(segment)  # last one
    continuous_segments[recv] = segments

# Calculate % received per segment
segment_stats = []
for recv, segments in continuous_segments.items():
    for i, segment in enumerate(segments, 1):
        seg_start = segment[0]
        seg_end = segment[-1]
        seg_expected = [ts for ts in expected if seg_start <= ts <= seg_end]
        seg_received = sum(any(abs(ts - t) <= tolerance for t in recv_times[recv]) for ts in seg_expected)
        percent = (seg_received / len(seg_expected)) * 100 if seg_expected else 0
        segment_stats.append({
            'receiver': recv,
            'segment': i,
            'start': seg_start,
            'end': seg_end,
            'received': seg_received,
            'expected': len(seg_expected),
            'percent': round(percent, 2)
        })

print("\n% Received in each continuous span (gaps \u2264 5h):")
print(pd.DataFrame(segment_stats).to_string(index=False))

# Prepare data for heatmap
heatmap_df = df.pivot(index='receiver', columns='timestamp', values='received').fillna(0)

# Create interactive heatmap with Plotly Express
fig = px.imshow(
    heatmap_df,
    labels=dict(x='Time', y='Receiver'),
    x=heatmap_df.columns,
    y=heatmap_df.index,
    aspect='auto',
    zmin=0, zmax=1,
    color_continuous_scale='Blues',
)

# Configure x-axis ticks every 4 hours and gridlines every hour
four_hours_ms = 4 * 60 * 60 * 1000
one_hour_ms = 1 * 60 * 60 * 1000
fig.update_xaxes(
    type='date',
    dtick=one_hour_ms,
    showgrid=True,
    gridwidth=0.5,
    gridcolor='lightgrey',
    tickmode='array',
    tickvals=[ts for ts in heatmap_df.columns if (ts - heatmap_df.columns[0]).total_seconds() % (4*60*60) == 0],
    tickformat='%H:%M',
    tickangle=45
)

fig.update_layout(
    title='Interactive Heatmap of Received (1) vs Missed (0)',
    xaxis_title='Time',
    yaxis_title='Receiver',
    coloraxis_showscale=False
)

fig.show()
