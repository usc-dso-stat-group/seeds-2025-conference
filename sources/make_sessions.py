import pandas as pd

# Input and output file paths
input_keynote = "keynote_speakers.csv"
input_invited = "invited_speakers.csv"
output_html = "../sessions/index.html"

# Read the CSV files
df_keynote = pd.read_csv(input_keynote)
df_invited = pd.read_csv(input_invited)

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
    <a class="current" title="View Conference Sessions" href="sessions">Sessions</a>
    <a title="See the Full Schedule" href="schedule">Schedule</a>
    <a title="Find Venue Details" href="venue">Venue</a>
</div>

    <br>

"""

# Function to extract title and abstract from the file
def extract_title_and_abstract(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            title = lines[0].strip() if len(lines) > 0 else "TBA"
            abstract = lines[2].strip() if len(lines) > 2 else "TBA"
            return title, abstract
    except FileNotFoundError:
        return "TBA", "TBA"

def write_list_of_talks(df, title):

    html_content = f"""
    <h2>{title}</h2>
    <p>
    """

    # Generate HTML table for each speaker
    for _, row in df.iterrows():
        speaker_name = row["Speaker Name"]
        affiliation = row["Affiliation"]
        website = row["Website"]
        abstract_file = row["Abstract"]

        # Extract title and abstract
        title, abstract = extract_title_and_abstract("abstracts/"+abstract_file)

        # Append speaker information to HTML content
        html_content += f"""
        <table>
            <tr>
                <td class="date" rowspan="2">
                </td>
                <td class="title">
                    <a href="{website}">{speaker_name} ({affiliation})</a>
                </td>
            </tr>
            <tr>
                <td class="speaker">
                 {title}
                </td>
            </tr>
            <tr>
                <td class="date" rowspan="2">
                </td>
                <td class="abstract">
                  Abstract: {abstract}
                </td>
            </tr>
        </table>
        """

    # Close the HTML structure
    html_content += """
    </p>
    """

    return html_content


html_content += write_list_of_talks(df_keynote, "Keynote Talks")
html_content += write_list_of_talks(df_invited, "Invited Talks")


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
