
# summaryToNotion

**summaryToNotion** is a Python-based tool designed to automate the process of summarizing content and sending it directly to Notion. Whether you're working with articles, research papers, or notes, this project allows for efficient content management by integrating summaries into Notion with ease.

## Features
- **Automatic Content Summarization**: Extract and summarize content from various sources.
- **Notion Integration**: Seamlessly send summaries and relevant details directly to a Notion page or database.
- **Customizable Settings**: Easily configure the tool to suit your needs, from choosing specific content to how the summary appears in Notion.

## Requirements
- Python 3.x
- Notion API Token and Database ID
- External libraries:
  - `openrouter api key` (for text summarization)
  - `notion` (for integrating with Notion)
  

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/lucifer-prashant/summmaryToNotion.git
   cd summmaryToNotion


2. Install the required dependencies:

  
3. Set up the Notion API credentials:

   * Obtain your Notion API token and Database ID by following [Notion API Documentation](https://developers.notion.so/).
   * Add them to your environment variables or a `.env` file.

4.  Create an api key from openrouter and place it in your `.env` file

## Usage

### Summarizing Text and Sending to Notion

Run the script to summarize content and send it to your Notion database.
Firstly run
```bash
python make_executable.py --build
```
this will create an .exe for the code and u can run it anytime without opening the code editor.
then either
```bash
python global_integration.py
```
or double click on your newly created app.

Firstly in any area select some text and hit Cltr+Q then
the script will:

1. Fetch the content.
2. Summarize the content using the configured summarization method 
3. Create a new entry in your Notion database with the summary.

### Customization

Modify the script or the config files to:

* Change the Notion database you’re working with.
* Select different summarization options or methods.
* Add or change how the data is presented in Notion.


## Acknowledgments

* **Notion API** for enabling easy database integration.
* **OpenAI API** for their advanced text summarization models.

---

Feel free to modify the sections above to reflect your project better. You can also update the sections for additional features, settings, or dependencies based on what the tool offers!
