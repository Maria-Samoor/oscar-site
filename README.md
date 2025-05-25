# Oscar Winners Website

A web application that displays Oscar winners data organized by year and name, served through an Apache web server in a Docker container.

## Technologies Used

- **Shell Scripting**: For downloading and processing JSON data
- **Python**: For downloading and processing CSV data
- **Docker**: For containerization and deployment
- **Apache HTTP Server**: For hosting the generated HTML files
- **jq**: For JSON processing in shell scripts
- **Pandas**: For CSV processing in Python

## Features

1. Data Processing:
   - Downloads and merges Oscar winner data from multiple sources
   - Processes both JSON and CSV formats
   - Adds gender information to each entry
   - Maintains proper sorting by year

2. HTML Generation:
   - Creates individual pages for each year
   - Creates individual pages for each actor/actress
   - Generates index pages with links to all entries
   - Handles special characters in names

3. Docker Deployment:
   - Lightweight Alpine-based container
   - Apache web server configuration
   - Security hardening
   - Port 8090 exposure

## Installation and Usage

### Option 1: Build and Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Maria-Samoor/oscar-site.git
   cd oscar-site
2. Build the Docker image:
   ```bash
   docker build -t oscar-site .
3. Run the container:
   ```bash
   docker run -d -p 8090:8090 oscar-site
### Option 2:  Pull Pre-built Docker Image 
1. Pull Docker Image:
   ```bash
   docker pull mariaahs/oscar-site
2. Run the container:
   ```bash
   docker run -d -p 8090:8090 mariaahs/oscar-site


### Access the application:
  ```bash
  http://localhost:8090/Years
  http://localhost:8090/Names
