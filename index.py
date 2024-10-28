import csv
import os
import re
import random

def csv_to_html(csv_filename, output_folder):
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')
    meet_title = ""

    try:
        with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            if len(rows) < 5:
                print("CSV file must have at least 5 rows.")
                return

            link_text = rows[0][0]
            h2_text = rows[1][0]
            link_url = rows[2][0]
            summary_text = rows[3][0]
            meet_title = link_text  # This will be used as the meet title in the index

            # Initialize HTML content with headers, navigation, and summary
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{link_text}</title>
<link rel="stylesheet" href="../css/reset.css">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<script src="https://kit.fontawesome.com/53ae34ec89.js" crossorigin="anonymous"></script>
</head>
<body>
<nav>
    <ul>
        <li><a href="index.html">Home Page</a></li>
        <li><a href="#summary">Summary</a></li>
        <li><a href="#team-results">Team Results</a></li>
        <li><a href="#individual-results">Individual Results</a></li>
        <li><a href="#gallery">Gallery</a></li>
    </ul>
</nav>
<header>
    <h1><a href="{link_url}">{link_text} <i class="fa-solid fa-arrow-up-right-from-square"></i></a></h1>
    <h2>{h2_text}</h2>
</header>
<button id="backToTopBtn" onclick="scrollToTop()">Go to Top <i class="fa-solid fa-arrow-up"></i></button>
<main class="container">
    <section id="summary">
        {summary_text}
    </section>
    """

            # Add team results section
            html_content += """<section id="team-results">
<h2>Team Results <i class="fa-solid fa-people-group"></i></h2>
<table class="table table-striped">\n"""
            
            table_start = True
            for row in rows[4:]:
                if len(row) == 3:
                    if row[0] == "Place":
                        html_content += f" <thead class='thead-dark'><tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr></thead>\n"
                    else:
                        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n"
                elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                    if table_start:
                        table_start = False
                        html_content += """</table>
</section>
<section id="individual-results">
<h2>Individual Results <i class="fa-solid fa-person-running"></i></h2>"""

                    place = row[0]
                    grade = row[1]
                    name = row[2]
                    time = row[4]
                    profile_pic = row[7]

                    html_content += f"""
<div class="athlete-div">
    <figure>
        <img src="../images/profiles/{profile_pic}" alt="Profile picture of {name}">
    </figure>
    <h4>{name}</h4>
    <dl>
        <dt>Place</dt><dd>{place}</dd>
        <dt>Time</dt><dd>{time}</dd>
        <dt>Grade</dt><dd>{grade}</dd>
    </dl>
</div>
"""

            # Add gallery section
            html_content += """</section>
<section id="gallery">
<button id="galleryButton" class="dropdown-btn up" onclick="toggleGallery()">Gallery <i class="fa-solid fa-caret-down"></i></button>
<div id="galleryContent" style="display: none;">\n"""
            url = "https://www.athletic.net/CrossCountry/meet/235827/results/943367"
            html_content += create_meet_image_gallery(url)

            # Close main content and add footer
            html_content += """
</div>
</section>
</main>
<footer>
    <p>Skyline High School</p>
    <address>
        2552 North Maple Road<br>
        Ann Arbor, MI 48103<br><br>
    </address>
    <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
    Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
</footer>
<script>
function toggleGallery() {
    const button = document.getElementById("galleryButton");
    const galleryContent = document.getElementById("galleryContent");
    if (galleryContent.style.display === "none") {
        galleryContent.style.display = "grid";
        button.classList.add("down");
        button.classList.remove("up");
    } else {
        galleryContent.style.display = "none";
        button.classList.remove("down");
        button.classList.add("up");
    }
}

window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    const backToTopBtn = document.getElementById("backToTopBtn");
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopBtn.style.display = "block";
        backToTopBtn.style.opacity = "1"; 
    } else {
        backToTopBtn.style.opacity = "0";
        setTimeout(function() {
            backToTopBtn.style.display = "none";
        }, 500);
    }
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
</body>
</html>
"""

            # Write the html content to a file
            with open(html_filename, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_content)

            print(f"HTML file '{html_filename}' created successfully.")
            return meet_title, html_filename

    except Exception as e:
        print(f"Error processing file: {e}")
        return None


def extract_meet_id(url):
    match = re.search(r"/meet/(\d+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

def select_random_photos(folder_path, num_photos=3):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if len(image_files) < num_photos:
        return ""
    return random.sample(image_files, num_photos)

def generate_image_tags(image_files, folder_path):
    img_tags = []
    for img in image_files:
        img_path = os.path.join(folder_path, img)
        img_tags.append(f'<img src="../{img_path}" width="200" alt="">')
    return "\n".join(img_tags)

def create_meet_image_gallery(url):
    meet_id = extract_meet_id(url)
    folder_path = f'images/meets/{meet_id}/'

    if not os.path.exists(folder_path):
        return ""
    
    selected_photos = select_random_photos(folder_path)
    html_image_tags = generate_image_tags(selected_photos, folder_path)
    
    return html_image_tags

def process_meet_files():
    meets_folder = os.path.join(os.getcwd(), "meets")
    if not os.path.exists(meets_folder):
        print(f"No CSV files found in folder: {meets_folder}")
        return

    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]
    meet_links = []

    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        meet_info = csv_to_html(csv_file_path, meets_folder)
        if meet_info:
            meet_links.append(meet_info)

    create_index_html(meet_links, meets_folder)

def create_index_html(meet_links, output_folder):
    index_path = os.path.join(output_folder, 'index.html')
    
    with open(index_path, 'w', encoding='utf-8') as index_file:
        index_file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Meets Index</title>
<link rel="stylesheet" href="../css/reset.css">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div class="container mt-5">
    <h1>Meet Results</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Meet Title</th>
                <th>Link</th>
            </tr>
        </thead>
        <tbody>
""")
        for title, filename in meet_links:
            relative_path = os.path.relpath(filename, output_folder)
            index_file.write(f'<tr><td>{title}</td><td><a href="{relative_path}">View Results</a></td></tr>\n')

        index_file.write("""
        </tbody>
    </table>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
</body>
</html>
""")

if __name__ == "__main__":
    process_meet_files()
