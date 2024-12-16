import pandas as pd

csv_file = "schedule.csv"  # Replace with the path to your CSV file
output_file = "../schedule/schedule.html"  # Output HTML file

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
    <title>Sessions | SEEDS Conference</title>
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

import pandas as pd

def generate_schedule_html(csv_file, output_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Initialize HTML content
    html_content = """
    <h2>Tentative Conference Schedule</h2>
    """
    
    # Variable to keep track of the current day
    current_day = ""

    # Generate HTML for each row in the CSV
    for _, row in df.iterrows():
        day = row['Day'] if pd.notna(row['Day']) else ""  # Handle NaN
        start_time = row['When (start)']
        end_time = row['When (end)']
        event = row['What'] if pd.notna(row['What']) else ""  # Handle NaN
        link = row['Link'] if not pd.isna(row['Link']) else ""
        location = row['Location'] if not pd.isna(row['Location']) else ""
        location_details = row['Location details'] if not pd.isna(row['Location details']) else ""

        # Add a new day header if needed
        if day and day != current_day:
            html_content += f"<h4>{day}</h4>\n"
            current_day = day
        
        # Generate location details with link if available
        if location:
            location_html = f"<a title=\"{location}\" href=\"{link}\">{location}</a>"
        else:
            location_html = ""

        # If location details are provided
        location_text = f", {location_details}" if location_details else ""
        location_html += location_text
        
        # Ensure event is a string before checking for "Break" or "Lunch"
        if isinstance(event, str) and ("Break" in event or "Lunch" in event or "Banquet dinner" in event or "Coffee Break" in event):
            html_content += f"""
            <table>
                <tr>
                    <td class=\"date\" rowspan=\"2\">
                        {start_time} - {end_time}
                    </td>
                    <td class=\"title-special\">
                        {event}
                    </td>
                </tr>
                <tr>
                    <td class=\"abstract\">
                        {location_html}
                    </td>
                </tr>
            </table>
            """
        elif event:  # Only add the table if there's an event
            html_content += f"""
            <table>
                <tr>
                    <td class=\"date\" rowspan=\"3\">
                        {start_time} - {end_time}
                    </td>
                    <td class=\"title\">
                        {event}
                    </td>
                </tr>
                <tr>
                    <td class=\"abstract\">
                        {location_html}
                    </td>
                </tr>
            </table>
            """

    return html_content


html_content += generate_schedule_html(csv_file, output_file)


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
