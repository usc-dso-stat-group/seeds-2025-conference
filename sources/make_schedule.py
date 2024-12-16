import pandas as pd
from datetime import datetime

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

    <style>
    .navigation {
        display: flex;
        justify-content: space-around;
        padding: 10px;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .navigation a {
        text-decoration: none;
        padding: 10px 15px;
        color: #007bff;
        font-size: 24px; /* Increased font size */
        font-weight: 500; /* Medium weight for balance */
        border: 1px solid transparent;
        border-radius: 4px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .navigation a:hover {
        background-color: #007bff;
        color: white;
        border-color: #0056b3;
    }
    .navigation a.current {
        font-weight: bold;
        color: white;
        background-color: #007bff;
    }
</style>

<div class="navigation">
    <a title="Conference Home Page" href=".">Home</a>
    <a title="Register for the Conference" href="registration">Registration</a>
    <a title="Explore Short Courses" href="courses">Short Courses</a>
    <a title="View Conference Sessions" href="sessions">Sessions</a>
    <a class="current" title="See the Full Schedule" href="schedule">Schedule</a>
    <a title="Find Venue Details" href="venue">Venue</a>
</div>

    <br>

"""

def generate_schedule_html(csv_file, location_csv, session_csv, output_file):
    """
    Generate an HTML schedule, including speakers for Invited Sessions.

    Parameters:
        csv_file (str): Path to the schedule CSV file.
        location_csv (str): Path to the location CSV file.
        session_csv (str): Path to the session details CSV file with speakers.
        output_file (str): Output HTML file path.

    Returns:
        str: HTML content for the schedule.
    """
    # Read the CSV files
    df = pd.read_csv(csv_file)
    location_df = pd.read_csv(location_csv)
    session_df = pd.read_csv(session_csv, sep=',')

    # Create a dictionary for location links
    location_links = dict(zip(location_df['Location'], location_df['Location link']))
    
    # Function to format speaker links
    def format_speaker_links(speakers_str):
        """
        Convert a list of speakers separated by ';' into HTML hyperlinks.
        Joins first and middle names with underscores and appends the last name.
        """
        speakers = speakers_str.split(";")
        speaker_links = []
        for speaker in speakers:
            speaker = speaker.strip()
            if speaker:
                name_parts = speaker.split()
                last_middle = " ".join(name_parts[1:])  # Join all but the first part with spaces
                first = name_parts[0]  # First part
                link = f"sessions/index.html#{first.lower()}_{last_middle.lower()}"  # Combine for the link
                speaker_links.append(f'<a href="{link}">{speaker}</a>')
        return ", ".join(speaker_links)

    # Update session_df to include formatted speaker links
    session_df['Speakers'] = session_df['Speakers'].apply(lambda x: format_speaker_links(x) if pd.notna(x) else "")

    # Create a dictionary for session speakers with hyperlinks
    session_speakers = dict(zip(session_df['Session title'], session_df['Speakers']))

    # Initialize HTML content
    html_content = """
    <h2>Tentative Conference Schedule</h2>
    """

    # Variable to keep track of the current day and the previous event's end time
    current_day = ""
    previous_end_time = None

    # Define a function to process time strings
    def process_time(time_value):
        if isinstance(time_value, float):
            return None
        time_str = str(time_value).strip()
        if time_str in ['nan', 'NaN', '', None]:
            return None
        if '.' in time_str:
            time_str = time_str.replace('.', ':') + 'am'
        return time_str

    # Generate HTML for each row in the CSV
    for _, row in df.iterrows():
        day = row['Day'] if pd.notna(row['Day']) else ""  # Handle NaN
        start_time = process_time(row['When (start)'])
        end_time = process_time(row['When (end)'])
        event = row['What'] if pd.notna(row['What']) else ""  # Handle NaN
        event_link = row['Link'] if pd.notna(row['Link']) else ""  # Handle NaN
        location = row['Location'] if not pd.isna(row['Location']) else ""
        location_details = row['Location details'] if not pd.isna(row['Location details']) else ""

        # Add a new day header if needed
        if day and day != current_day:
            html_content += f"<h4>{day}</h4>\n"
            current_day = day
            previous_end_time = None  # Reset for the new day

        # Validate time continuity
        if start_time and previous_end_time:
            time_format = "%I:%M%p"
            start_dt = datetime.strptime(start_time, time_format)
            prev_end_dt = datetime.strptime(previous_end_time, time_format)

            if start_dt != prev_end_dt:
                print(f"Error: Event '{event}' on {day} starts at {start_time}, "
                      f"which does not match the previous event's end time ({previous_end_time}).")

        # Update the previous end time
        previous_end_time = end_time if end_time else previous_end_time

        # Add link to event if provided
        if event_link:
            event_html = f"<a title=\"{event}\" href=\"{event_link}\">{event}</a>"
        else:
            event_html = f"{event}"

        # Add speakers for "Invited Session X"
        speakers_html = ""
        if "Invited Session" in event:
            speakers = session_speakers.get(event, "")
            if speakers:
                speakers_html = f"<span style='font-size: normal;'><b>Speakers:</b> {speakers}</span><br>"

        # Format location details
        link = location_links.get(location, "")
        if location and link:
            location_html = f"<b>Location:</b> <a title=\"{location}\" href=\"{link}\">{location}</a>"
        elif location:
            location_html = f"{location}"
        else:
            location_html = ""
        location_text = f", {location_details}" if location_details else ""
        location_html += location_text

        # Format the time range
        if start_time and end_time:
            start_dt = datetime.strptime(start_time, "%I:%M%p")
            end_dt = datetime.strptime(end_time, "%I:%M%p")
            duration = end_dt - start_dt
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            formatted_duration = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            formatted_time_range = f"""<div style="width: 140px; text-align: center;">
                {start_time} - {end_time}<br>
                <span style="font-size: smaller;">Duration: {formatted_duration}</span>
            </div>"""
        else:
            formatted_time_range = ""

        # Add event HTML
        html_content += f"""
        <table>
            <tr>
                <td class=\"date\" rowspan=\"3\">
                    {formatted_time_range}
                </td>
                <td class=\"title\">
                    {event_html if event_html else event}
                </td>
            </tr>
            <tr>
                <td class=\"abstract\">
                    {speakers_html}
                    {location_html}
                </td>
            </tr>
        </table>
        """

    return html_content


html_content += generate_schedule_html(csv_file, location_csv, session_csv, output_file)


html_content += """
<footer>
    &copy; Conference Organizers
    &nbsp;|&nbsp; Design by <a href="https://github.com/mikepierce">Mike Pierce</a>
</footer>

</body>
</html>

"""

# Write to the output HTML file
with open(output_file, "w") as file:
    file.write(html_content)

print(f"HTML file '{output_file}' has been created successfully.")
