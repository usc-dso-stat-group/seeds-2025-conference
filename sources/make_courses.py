import pandas as pd

# Input and output file paths
input_courses = "course_speakers.csv"
output_html = "../courses/index.html"

# Read the CSV files
df_courses = pd.read_csv(input_courses)

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
    <a class="current" title="Explore Short Courses" href="courses">Short Courses</a>
    <a title="View Conference Sessions" href="sessions">Sessions</a>
    <a title="See the Full Schedule" href="schedule">Schedule</a>
    <a title="Find Venue Details" href="venue">Venue</a>
</div>

    <br>

    <a name=“keynote_presentations”>
    <h3>Keynote Presentations</h4>
    </a>


"""

# Function to extract course time, title, short bio, and abstract from the file
def extract_course_time_title_bio_and_abstract(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            course_time = lines[0].strip() if len(lines) > 0 else "TBA"
            title = lines[2].strip() if len(lines) > 2 else "TBA"
            short_bio = lines[4].strip() if len(lines) > 4 else "TBA"
            abstract = lines[6].strip() if len(lines) > 6 else "TBA"
            return course_time, title, short_bio, abstract
    except FileNotFoundError:
        return "TBA", "TBA", "TBA", "TBA"


def write_list_of_courses(df, title):
    html_content = f"""
    <h3>{title}</h3>
    """

    # Generate HTML table for each speaker
    for _, row in df.iterrows():
        speaker_name = row["Speaker Name"]
        affiliation = row["Affiliation"]
        website = row["Website"]
        abstract_file = row["Abstract"]

        # Extract course time, title, bio, and abstract
        course_time, talk_title, short_bio, abstract = extract_course_time_title_bio_and_abstract("courses/" + abstract_file)

        # Append speaker information to HTML content
        html_content += f"""
        <table>
            <tr>
                <td class="title" colspan="2">
                    <div style="text-align: center; margin-top: 5px; font-size: smaller; color: gray;">
                        {course_time if course_time != 'TBA' else 'TBA'}
                    </div> <br>
                    <a href="{website}">
                        <strong>{speaker_name}</strong> ({affiliation})
                    </a>
                    <div style="text-align: center; margin-top: 10px; font-size: smaller;">
                        {talk_title if talk_title != 'TBA' else 'TBA'}
                    </div>
                </td>
            </tr>
            <tr>
                <td class="speaker" colspan="2">
                    <strong>Bio:</strong> {short_bio if short_bio != 'TBA' else 'TBA'}
                </td>
            </tr>
            <tr>
                <td class="abstract" colspan="2">
                    <strong>Abstract:</strong> {abstract if abstract != 'TBA' else 'TBA'}
                </td>
            </tr>
        </table>
        """

    return html_content


html_content += write_list_of_courses(df_courses, "Short Courses")


html_content += """
<footer>
    &copy; Conference Organizers
    &nbsp;|&nbsp; Design by <a href="https://github.com/mikepierce">Mike Pierce</a>
</footer>

</body>
</html>

"""

# Write to the output HTML file
with open(output_html, "w") as file:
    file.write(html_content)

print(f"HTML file '{output_html}' has been created successfully.")
