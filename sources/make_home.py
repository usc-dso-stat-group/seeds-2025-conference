import pandas as pd

# Input and output file paths
input_keynote = "keynote_speakers.csv"
input_courses = "course_speakers.csv"
input_invited = "invited_speakers.csv"
output_html = "../index.html"

# Read the CSV files
df_keynote = pd.read_csv(input_keynote)
df_courses = pd.read_csv(input_courses)
df_invited = pd.read_csv(input_invited)

# Start the HTML content
html_content = """
<!DOCTYPE html>
<html lang='en'>


<head>
    <base href=".">
    <link rel="shortcut icon" type="image/png" href="assets/favicon.png"/>
    <link rel="stylesheet" type="text/css" media="all" href="assets/main.css"/>
    <meta name="description" content="SEEDS Conference">
    <meta name="resource-type" content="document">
    <meta name="distribution" content="global">
    <meta name="KeyWords" content="Conference">
    <title>SEEDS Conference</title>

</head>

<body>

    <div class="banner">
        <img src="assets/banner.jpg" alt="SEEDS Conference Banner">
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
    <a class="current" title="Conference Home Page" href=".">Home</a>
    <a title="Register for the Conference" href="registration">Registration</a>
    <a title="Explore Short Courses" href="courses">Short Courses</a>
    <a title="View Conference Sessions" href="sessions">Sessions</a>
    <a title="See the Full Schedule" href="schedule">Schedule</a>
    <a title="Find Venue Details" href="venue">Venue</a>
</div>

    <h2>Statistics Empowering Data Science (SEEDS)</h2>

    <p>
     The SEEDS 2025 conference will bring together researchers in statistics, data science, and business research from academia and industry in an engaging environment, aiming to start new collaborations, explore fresh research ideas, and help keep higher education offerings current and relevant in the modern age of statistics and artificial intelligence.
    </p>
    <p>
      <b>When:</b> January 8-11, 2025.
    </p>

    <p>
      <b>Where:</b> Marshall School of Business, University of Southern California, Los Angeles (CA).
    </p>

    <p>
      <b>Accommodation:</b> Los Angeles offers many convenient hotel options. The closest option to the conference venue is the <a href="https://uschotel.usc.edu/">USC Hotel</a>.
      Further, several hotels in Downtown LA offer <a href="assets/hotels-usc.pdf">USC Corporate rates</a> for guest of the University, subject to room availability.
    </p>

    <p>
      <b>Meals:</b> The registration includes breakfast, lunch, and snacks on the conference days, as well as the conference dinner.
      Additional guests can purchase a separate dinner ticket through the registration website.
    </p>

    <p>
      <b>Wi-Fi:</b> Two visitor Wi-Fi networks are available: USC Guest Wireless (no authentication required) and Eduroam (requires authentication).
    </p>

<h2>Program at a Glance</h2>
<p>
  The conference will feature:
</p>
<ul>
  <li>Three keynote presentations</li>
  <li>Invited academic sessions covering a wide range of cutting-edge topics in statistics and data science</li>
  <li>Three short courses led by experts from academia and industry</li>
  <li>A contributed poster session, open to all registered participants</li>
  <li>Poster awards for students</li>
</ul>


    <h2>Poster Session</h2>

<p>
  We welcome submissions for the Contributed Poster Session at SEEDS 2025. Student presenters will also be eligible for poster awards.
</p>
<p>
  To participate, please submit your poster title and abstract via 
  <a href="https://forms.gle/f7UQpsGwUGG687eR8" target="_blank">this form</a> 
  and notify the SEEDS organizers by email at 
  <a href="mailto:seeds.conference@marshall.usc.edu">seeds.conference@marshall.usc.edu</a> 
  no later than December 31, 2024.
</p>


"""



def write_list_of_speakers(df, title, columns_per_row=4):
    html_content = f"""
    <h2>{title}</h2>
    <p>
    </p>
    """

    # Generate HTML for a single speaker
    def generate_speaker_html(row):
        name = row["Speaker Name"]
        affiliation = row["Affiliation"]
        website = row["Website"]
        image_path = "assets/" + row["Photo"]  # Assumes a column with paths to images
        return f"""
        <td class="sponsor">
            <a href="{website}">
                <img src="{image_path}" alt="{name}" style="height: 150pt; width: auto">
                <figcaption>{name}<br>({affiliation})</figcaption>
            </a>
        </td>
        """

    # Build the HTML with rows containing up to 'columns_per_row' speakers
    for i in range(0, len(df), columns_per_row):
        html_content += """
        <table class="sponsors">
            <tr>
        """
        # Generate a row of speakers
        for _, row in df.iloc[i:i + columns_per_row].iterrows():
            html_content += generate_speaker_html(row)
        
        # Close the row and table
        html_content += """
            </tr>
        </table>
        """

    return html_content


html_content += write_list_of_speakers(df_keynote, "Keynote Speakers", columns_per_row=3)
html_content += write_list_of_speakers(df_courses, "Short Course Speakers", columns_per_row=3)
html_content += write_list_of_speakers(df_invited, "Invited Speakers", columns_per_row=3)


html_content += """
    <h2>Organizers</h2>
    <p>
      The SEEDS 2025 conference is organized by the <a href="https://usc-dso-stat-group.github.io/">Statistics Group</a> within the Data Sciences and Operations (DSO) Department of the University of Southern California, Marshall School of Business.
      For further information, please <a href="mailto:seeds.conference@marshall.usc.edu">contact the SEEDS organizers</a>.

      <br>
      <br>
    </p>
    
    <table class="sponsors">
        <tr>
            <td class="sponsor">
                <a href="https://sites.google.com/site/xintonghomepage/">
                    <img src="assets/Tong.jpg" alt="Xing Tong" style="height: 150pt; width: auto">
                    <figcaption>Xin Tong</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="https://gmukherjee.github.io/">
                    <img src="assets/Mukherjee.jpg" alt="Gourab Mukherjee" style="height: 150pt; width: auto">
                    <figcaption>Gourab Mukherjee</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="https://mkolar.coffeejunkies.org/">
                    <img src="assets/Kolar.jpg" alt="Mladen Kolar" style="height: 150pt; width: auto">
                    <figcaption>Mladen Kolar</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="http://faculty.marshall.usc.edu/jinchi-lv/">
                    <img src="assets/Lv.jpg" alt="Jinchi Lv" style="height: 150pt; width: auto">
                    <figcaption>Jinchi Lv</figcaption>
                </a>
            </td>
        </tr>
    </table>
    <table class="sponsors">
        <tr>
            <td class="sponsor">
                <a href="https://www.paromitadubey.com/">
                    <img src="assets/Dubey.jpg" alt="Paromita Dubey" style="height: 150pt; width: auto">
                    <figcaption>Paromita Dubey</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="http://faculty.marshall.usc.edu/Adel-Javanmard/">
                    <img src="assets/Javanmard.jpg" alt="Adel Javanmard" style="height: 150pt; width: auto">
                    <figcaption>Adel Javanmard</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="https://msesia.github.io/">
                    <img src="assets/Sesia.jpg" alt="Matteo Sesia" style="height: 150pt; width: auto">
                    <figcaption>Matteo Sesia</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="http://faculty.marshall.usc.edu/yingying-fan/">
                    <img src="assets/Fan.jpg" alt="Yingying Fan" style="height: 150pt; width: auto">
                    <figcaption>Yingying Fan</figcaption>
                </a>
            </td>
        </tr>
    </table>
    <table class="sponsors">
        <tr>
            <td class="sponsor">
                <a href="http://faculty.marshall.usc.edu/jacob-bien/">
                    <img src="assets/Bien.jpg" alt="Jacob Bien" style="height: 150pt; width: auto">
                    <figcaption>Jacob Bien</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="https://zijungao.github.io/">
                    <img src="assets/Gao.jpg" alt="Zijun Gao" style="height: 150pt; width: auto">
                    <figcaption>Zijun Gao</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="https://deshen24.github.io/">
                    <img src="assets/Shen.jpg" alt="Dennis Shen" style="height: 150pt; width: auto">
                    <figcaption>Dennis Shen</figcaption>
                </a>
            </td>
            <td class="sponsor">
                <a href="https://sites.google.com/berkeley.edu/waverlywei/home">
                    <img src="assets/Wei.jpg" alt="Waverly Wei" style="height: 150pt; width: auto">
                    <figcaption>Waverly Wei</figcaption>
                </a>
            </td>
        </tr>
    </table>



    <h2>Accessibility</h2>
    
    Individuals with disabilities who need accommodations to attend this event should <a href="mailto:seeds.conference@marshall.usc.edu">contact the SEEDS organizers</a>. 
    It is kindly requested that individuals requiring accommodations or auxiliary aids such as sign language interpreters and alternative format materials, notify the conference organizers at least 7 days prior to the beginning of the event. Every reasonable effort will be made to provide reasonable accommodations in an effective and timely manner.



    <h2>Code of Conduct</h2>
     The SEEDS Conference is a forum for community-building and scholarly exchange, and we hope to foster a welcoming and positive environment for everyone.    
     Any form of harassment, discrimination, or abuse will not be tolerated. As a general code of conduct, we will adopt the ACM Policy Against Harassment. Since the event will be held on the grounds of the University of Southern California (USC), participants should also be aware of all applicable USC policies. To report an incident or discuss any concerns, please <a href="mailto:seeds.conference@marshall.usc.edu">contact the SEEDS organizers</a>. 
     You may also use the USC reporting options, including reaching out to the Title IX coordinator. 

    <p>

    <footer>
        &copy; Conference Organizers
        &nbsp;|&nbsp; Design by <a href="https://github.com/mikepierce">Mike Pierce</a>
    </footer>

</body>
</html>
"""

# Write the final HTML content to file
with open(output_html, "w") as file:
    file.write(html_content)

print(f"HTML file '{output_html}' has been created successfully.")
