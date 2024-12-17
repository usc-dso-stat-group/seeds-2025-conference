import pandas as pd
from datetime import datetime
import numpy as np
import pdb

csv_file = "schedule.csv"
location_csv = "locations.csv"
session_csv = "sessions.csv"

output_file = "../schedule/index.html"  # Output HTML file

# Start building the HTML content
html_content = """
<!DOCTYPE html>
<html lang='en'>

<head>
    <base href="..">
    <link rel="shortcut icon" type="image/png" href="assets/favicon.png"/>
    <link rel="stylesheet" type="text/css" media="all" href="assets/main.css"/>
    <meta name="description" content="SEEDS Conference">
    <meta name="resource-type" content="document">
    <meta name="distribution" content="global">
    <meta name="KeyWords" content="Conference">
    <title>Schedule | SEEDS Conference</title>
    <style>
        .schedule {
            display: flex;
            margin-bottom: 20px;
        }
        .track-column {
            flex: 1;
            position: relative;
            border: 1px solid #ccc;
            background-color: #f9f9f9;
            padding: 20px;
            height: 100%; /* Ensure track column fills parent height */
        }
        .event {
            position: absolute;
            left: 10px;
            width: calc(95%);
            padding: 10px;
            border: 1px solid #ddd;
            background-color: #fff;
            box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.1);
        }
        .event-title {
            display: inline-block;
            font-weight: bold;
        }
        .event-time {
            display: inline-block;
            font-style: italic;
            margin-bottom: 5px;
        }
        .track1 {
            background-color: #e6f7ff; /* Light blue for Track 1 */
        }
        .track2 {
            background-color: #fff5e6; /* Light orange for Track 2 */
        }
    </style>
</head>

<body>

    <div class="banner">
        <img src="assets/banner.jpg" alt="SEEDS Conference">
        <div class="top-left">
            <span class="title1">SEEDS</span><span class="title2">Conference</span> <span class="year">2025</span>
        </div>
        <div class="bottom-right">
            January 8-11, 2025 <br> University of Southern California, Los Angeles (CA)
        </div>
    </div>

    <div class="navigation">
        <a title="Conference Home Page" href=".">Home</a>
        <a title="Register for the Conference" href="registration">Registration</a>
        <a title="Explore Short Courses" href="courses">Short Courses</a>
        <a title="View Conference Sessions" href="sessions">Sessions</a>
        <a class="current" title="See the Full Schedule" href="schedule">Schedule</a>
        <a title="Find Venue Details" href="venue">Venue</a>
    </div>

    <h2>Tentative Conference Schedule</h2>
"""

def shift_virtual_times(day_df, min_duration=35):
    """
    Adjust virtual times for events in day_df to enforce minimum durations
    and maintain alignment across tracks by shifting subsequent events as needed.

    Parameters:
        day_df (pd.DataFrame): DataFrame containing events for a single day.
        min_duration (int): Minimum virtual duration in minutes.

    Returns:
        pd.DataFrame: Updated day_df with shifted virtual times.
    """
    # Convert minimum duration to timedelta
    min_duration_td = pd.to_timedelta(min_duration, unit='m')

    # Sort events by virtual start time across all tracks
    day_df = day_df.sort_values('When (start, virtual)').reset_index(drop=True)

    for idx, event in day_df.iterrows():
        # Align the start time with the global end time
        start_virtual = event['When (start, virtual)']
        end_virtual = event['When (end, virtual)']
        duration = end_virtual - start_virtual

        # Extend the event to meet the minimum duration
        if duration < min_duration_td:
            new_end_virtual = start_virtual + min_duration_td
            shift = new_end_virtual - end_virtual
        else:
            shift = pd.Timedelta(0)
        
        # Update virtual times for the current event
        day_df.at[idx, 'When (end, virtual)'] += shift

        # Apply the shift to subsequent events if needed
        if shift > pd.Timedelta(0) and idx + 1 < len(day_df):
            for idx2 in range(idx+1, len(day_df)):
                if day_df.loc[idx2, 'When (start)'] >= day_df.loc[idx, 'When (end)']:
                    day_df.loc[idx2, 'When (start, virtual)'] += shift
                    day_df.loc[idx2, 'When (end, virtual)'] += shift

    # Add a Virtual Duration column
    day_df['Virtual Duration'] = (day_df['When (end, virtual)'] - day_df['When (start, virtual)']).dt.total_seconds() / 60

    return day_df




def generate_schedule_html(df, location_df, session_df):
    """
    Generate HTML for the schedule dynamically based on day and track.

    Parameters:
        df (pd.DataFrame): Schedule data.
        location_df (pd.DataFrame): Location data.
        session_df (pd.DataFrame): Session details.

    Returns:
        str: Generated HTML content.
    """
    def preprocess_time_column(column):
        """Normalize time strings."""
        column = column.str.replace(r'([apAP][mM])$', r' \1', regex=True)
        return pd.to_datetime(column, format='%I:%M %p', errors='coerce')

    # Preprocess time columns
    df['When (start)'] = preprocess_time_column(df['When (start)'])
    df['When (end)'] = preprocess_time_column(df['When (end)'])

    # Add virtual times (for alignment)
    df['When (start, virtual)'] = df['When (start)']
    df['When (end, virtual)'] = df['When (end)']

    # Add a default Track column if missing
    if 'Track' not in df.columns:
        df['Track'] = 'Single Track'

    # Create a dictionary for location links
    location_links = dict(zip(location_df['Location'], location_df['Location link']))

    # Format speaker links
    def format_speaker_links(speakers_str):
        speakers = speakers_str.split(";")
        return ", ".join(
            f'<a href="sessions/index.html#{s.strip().replace(" ", "_").lower()}">{s.strip()}</a>'
            for s in speakers if s.strip()
        )

    # Add speaker links to session_df
    session_df['Speakers'] = session_df['Speakers'].apply(lambda x: format_speaker_links(x) if pd.notna(x) else "")
    session_speakers = dict(zip(session_df['Session title'], session_df['Speakers']))

    # Initialize HTML
    day_html_content = ""

    # Process each day
    grouped_days = df.groupby('Day', sort=False)
    for day, day_df in grouped_days:
        day_html_content += f"<h3>{day}</h3>\n"

        # Shift virtual times
        day_df = shift_virtual_times(day_df)

        earliest_time = day_df['When (start, virtual)'].min()
        latest_time = day_df['When (end, virtual)'].max()
        pixels_per_minute = 2
        min_schedule_height = 200  # Minimum height for each day's schedule
        title_offset = 50

        def calculate_offset(time):
            return int((time - earliest_time).total_seconds() / 60) * pixels_per_minute

        def calculate_height(start, end):
            duration = (end - start).total_seconds() / 60
            return max(50, int(duration * pixels_per_minute))  # Minimum height of 50px

        # Create tracks
        track_columns_html = ""
        max_track_height = 0
        for track, track_events in day_df.groupby('Track'):
            track_content = ""
            track_start_time = track_events['When (start, virtual)'].min()
            track_end_time = track_events['When (end, virtual)'].max()
            track_minutes = (track_end_time - track_start_time).total_seconds() / 60
            max_track_height = max(max_track_height, int(track_minutes * pixels_per_minute))

            for _, row in track_events.iterrows():
                top_offset = calculate_offset(row['When (start, virtual)']) + title_offset
                height = calculate_height(row['When (start, virtual)'], row['When (end, virtual)'])
                event_time = f"{row['When (start)'].strftime('%I:%M %p')} - {row['When (end)'].strftime('%I:%M %p')}"
                event_duration = (row['When (end)'] - row['When (start)']).total_seconds() / 60
                hours = int(event_duration // 60)  # Whole hours
                minutes = int(event_duration % 60)  # Remaining minutes

                if hours > 0:  # Format as "Xh Ym" for events over 1 hour
                    duration_str = f"({hours}h {minutes}m)" if minutes > 0 else f"({hours}h)"
                else:  # Format as "Xm" for shorter events
                    duration_str = f"({minutes}m)"
                event_html = f"<a href='{row['Link']}'>{row['What']}</a>" if pd.notna(row['Link']) else row['What']
                location_html = f"<b>Location:</b> {row['Location']}" if pd.notna(row['Location']) else ""
                speakers_html = session_speakers.get(row['What'], "")

                event = row['What']
                spacing = "&nbsp;&nbsp;"
                spacing_2 = "&nbsp;&nbsp;|&nbsp;&nbsp;"

                if pd.notna(event) and event.lower().startswith("invited"):
                    track_content += f"""
                    <div class="event" style="top: {top_offset}px; height: {height}px;">
                    <div class="event-time">{event_time}{spacing}{duration_str}</div>
                    <div class="event-title">{spacing_2}{event_html}</div>
                    <div class="event-details">{speakers_html}<br>{location_html}</div>
                    </div>
                    """
                elif pd.notna(event) and event.lower().startswith("short"):
                    track_content += f"""
                    <div class="event" style="top: {top_offset}px; height: {height}px;">
                    <div class="event-time">{event_time}{spacing}{duration_str}</div>
                    <div class="event-title">{spacing_2}{event_html}</div>
                    <div class="event-details">{location_html}</div>
                    </div>
                    """
                else:
                    track_content += f"""
                    <div class="event" style="top: {top_offset}px; height: {height}px;">
                    <div class="event-time">{event_time}{spacing}{duration_str}</div>
                    <div class="event-title">{spacing_2}{event_html}</div>
                    <div class="event-details">{location_html}</div>
                    </div>
                    """


            # Assign CSS classes based on track name
            track_class = "track1" if "Main Track" in track else "track2"  # Example condition
            track_columns_html += f"""
            <div class="track-column {track_class}">
                <h5>{track}</h5>
                {track_content}
            </div>
            """

        # Use the maximum track height for the schedule
        total_day_height = max(max_track_height, min_schedule_height) + title_offset

        # Set height in the schedule div
        day_html_content += f"""
        <div class="schedule" style="height: {total_day_height}px;">
            {track_columns_html}
        </div> <br><br>
        """

    return day_html_content

# Read data
df = pd.read_csv(csv_file)
location_df = pd.read_csv(location_csv)
session_df = pd.read_csv(session_csv, sep=',')

df['Day'] = df['Day'].fillna(method='ffill')

html_content += generate_schedule_html(df, location_df, session_df)

html_content += """
<footer>&copy; Conference Organizers</footer>
</body>
</html>
"""

# Write to file
with open(output_file, "w") as file:
    file.write(html_content)

print(f"HTML file '{output_file}' has been created successfully.")
