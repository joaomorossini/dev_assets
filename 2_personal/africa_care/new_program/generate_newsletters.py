import os
import requests
import json
import time
import csv
from datetime import datetime
import re
import base64
from dotenv import load_dotenv
from urllib.parse import urlparse
import sys
import traceback

# Add parent directory to path to import openai_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai_utils import openai_generate_artwork, azure_openai_generate_artwork

# Load environment variables from .env file
load_dotenv()

# Directory paths
BASE_DIR = "/Users/morossini/Projects/1.dev_assets/2_personal/africa_care/new_program"
TEMPLATE_PATH = os.path.join(BASE_DIR, "newsletter_template.html")
LOGO_PATH = "/Users/morossini/Projects/1.dev_assets/2_personal/africa_care/assets/logo_main.png"
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Create a simple solid color image for fallback
def create_fallback_image(month, color="#F15A24"):
    """Create a simple fallback image if all other methods fail"""
    image_filename = f"{month.lower()}_image.png"
    image_path = os.path.join(IMAGES_DIR, image_filename)
    
    try:
        # Create a simple 1x1 pixel PNG with the specified color
        # We'll just write a simple red square as a fallback
        with open(image_path, 'wb') as f:
            # Very basic PNG header and data for a 200x200 orange square
            f.write(base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAAAXNSR0IArs4c6QAABClJREFUeF7t"
                "1DEBAAAIwzDAv+chx7YXWD8zZ4AACQQBD0gSRoDAOwQEYg0CtQICqcEIEBCIDUCgFhBIDUaAgEBs"
                "AAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2"
                "AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCA"
                "QGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BA"
                "IDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAg"
                "EBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQ"
                "iA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMR"
                "ICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEI"
                "EBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAE"
                "CAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbc"
                "BTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHU"
                "YAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBq"
                "MAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1"
                "GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWA"
                "QGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpA"
                "IDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0g"
                "kBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AAIEF"
                "OhCTRs3vUigAAAAASUVORK5CYII="))
        print(f"Created fallback image at {image_path}")
        return image_path
    except Exception as e:
        print(f"Error creating fallback image: {e}")
        # Return a hard-coded path as absolute last resort
        return os.path.join(BASE_DIR, "fallback.png")

# Ensure the images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

# Function to read the talk content
def read_talk_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Function to parse talk content
def parse_talk_content(content):
    """Parse the talk content to extract objectives and content details"""
    try:
        # Extract objectives
        objectives = []
        obj_match = re.search(r'## Objectivos Específicos:(.*?)##', content, re.DOTALL)
        if obj_match:
            obj_text = obj_match.group(1).strip()
            for line in obj_text.split('\n'):
                line = line.strip()
                if line and line[0].isdigit() and '. ' in line:
                    objectives.append(line[line.find('. ')+2:])
        
        # Format objectives as HTML list items
        objectives_html = ""
        for obj in objectives[:3]:  # Take only the first 3 objectives
            objectives_html += f"<li>{obj}</li>"
        
        # Extract content description
        conteudos = ""
        content_match = re.search(r'\*\*Conteúdos Programáticos\*\*(.*?)\*\*Indicações Metodológicas\*\*', content, re.DOTALL)
        if content_match:
            conteudo_text = content_match.group(1).strip()
            # Convert bullets to semicolon-separated text
            conteudos_list = []
            for line in conteudo_text.split('\n'):
                line = line.strip()
                if line and (line.startswith('•') or line.startswith('*')):
                    conteudos_list.append(line[1:].strip())
            conteudos = '; '.join(conteudos_list)
        
        # Get title
        title_match = re.search(r'## Tema: (.*?)##', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        
        return {
            'title': title,
            'objectives': objectives_html,
            'conteudos': conteudos
        }
    except Exception as e:
        print(f"Error parsing talk content: {e}")
        return {
            'title': "",
            'objectives': "",
            'conteudos': ""
        }

# Function to read calendar data
def read_calendar():
    calendar_path = os.path.join(BASE_DIR, "Novo_Calendário_Palestras_2025.csv")
    talks = []
    
    # Read the CSV file with proper handling of quoted fields (which may contain commas)
    with open(calendar_path, 'r', encoding='utf-8') as file:
        # Using csv.reader instead of DictReader to handle the file manually
        reader = csv.reader(file)
        
        # Get header row
        headers = next(reader)
        
        # Process each row
        for row in reader:
            if len(row) >= 4:  # Ensure we have enough columns
                talk = {
                    "Mês": row[0],
                    "Tema": row[1],
                    "Data": row[2],
                    "Local": row[3]
                }
                talks.append(talk)
    
    # Debug: print the first row to verify
    if talks:
        print("First talk in calendar:")
        for key, value in talks[0].items():
            print(f"  {key}: {value}")
    
    return talks

# Function to generate DALL-E prompt based on talk content
def generate_dalle_prompt(talk_data, talk_content):
    topic = talk_data["Tema"]
    month = talk_data["Mês"]
    
    # Create a specific prompt based on the talk theme
    prompts = {
        "Março": f"Create a professional, photorealistic image representing hydration at workplace in beverage industry. Show relatable workers of African/Angolan ethnicity drinking water during their shift at a modern beverage production facility, with water bottles nearby. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Abril": f"Create a professional, photorealistic image showing proper ergonomics in an industrial setting. Show relatable workers of African/Angolan ethnicity using correct posture while lifting boxes or operating machinery in a beverage factory. Include visual cues for proper body positioning. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Maio": f"Create a professional, photorealistic image representing mental health in the workplace. Show relatable diverse workers of African/Angolan ethnicity in a supportive environment, perhaps in a bright break room having a positive conversation or practicing mindfulness. Include subtle elements of stress management. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Junho": f"Create a professional, photorealistic image showing healthy eating habits for shift workers. Present nutritious meals and snacks suitable for different work schedules, perhaps in a modern industrial cafeteria setting. Include relatable workers of African/Angolan ethnicity enjoying healthy food options. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Julho": f"Create a professional, photorealistic image representing responsible alcohol consumption. Show relatable people of African/Angolan ethnicity in a social setting enjoying drinks responsibly with water present and food being served. Emphasize moderation and conscious choices. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Agosto": f"Create a professional, photorealistic image representing prevention of common infectious diseases in Angola. Show relatable people of African/Angolan ethnicity practicing handwashing, using mosquito nets, or other preventive measures relevant to malaria and other local diseases. Include a healthcare professional providing education. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Setembro": f"Create a professional, photorealistic image representing reproductive health and family planning. Show a relatable diverse family or a couple of African/Angolan ethnicity consulting with a healthcare provider, in a respectful and educational context. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Outubro": f"Create a professional, photorealistic image representing prevention and management of chronic diseases like diabetes and hypertension. Show relatable people of African/Angolan ethnicity actively managing their health through health monitoring, exercise, or healthy food choices. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Novembro": f"Create a professional, photorealistic image representing financial health and planning. Show relatable people of African/Angolan ethnicity engaged in budget planning, perhaps at a table with documents or using digital tools. Include visual elements of saving and financial security. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.",
        
        "Dezembro": f"Create a professional, photorealistic image representing work-life balance and family wellness. Show a relatable person of African/Angolan ethnicity transitioning from work to family time or enjoying quality time with family during the holiday season. Bright, positive atmosphere with orange accents. No text overlay. Clean white background."
    }
    
    return prompts.get(month, f"Create a professional, photorealistic image representing the concept of {topic}. Bright, positive atmosphere with orange accents. No text overlay. Clean white background.")

# Function to download an image from URL
def download_image_from_url(url, save_path):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully to {save_path}")
            return True
        else:
            print(f"Failed to download image: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

# Function to generate images using OpenAI utility functions
def generate_image_with_dalle(prompt, month):
    """Generate an image using OpenAI's DALL-E model via the utility functions"""
    image_filename = f"{month.lower()}_image.png"
    image_path = os.path.join(IMAGES_DIR, image_filename)
    
    # Try both Azure OpenAI and regular OpenAI for image generation
    try:
        # First try Azure OpenAI
        print(f"Generating image with Azure OpenAI DALL-E 3 for {month}...")
        try:
            image_url = azure_openai_generate_artwork(prompt, n=1, size="1792x1024")
            if download_image_from_url(image_url, image_path):
                return image_path
        except Exception as e:
            print(f"Azure OpenAI generation failed: {e}")
            print(traceback.format_exc())
        
        # Then try regular OpenAI
        print(f"Trying regular OpenAI DALL-E 3 for {month}...")
        try:
            image_url = openai_generate_artwork(prompt, n=1, size="1792x1024")
            if download_image_from_url(image_url, image_path):
                return image_path
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            print(traceback.format_exc())
        
        # If both fail, create a fallback image
        return create_fallback_image(month)
    except Exception as e:
        print(f"Error in image generation: {e}")
        print(traceback.format_exc())
        return create_fallback_image(month)

# Function to create newsletter from template
def create_newsletter(talk_data, talk_content, image_path):
    month = talk_data["Mês"]
    tema = talk_data["Tema"]  # Use the theme from the CSV
    obj_gerais = talk_content["objectives"]
    conteudos = talk_content["conteudos"]
    data = talk_data["Data"]
    local = talk_data["Local"]
    
    # Read template
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        template = file.read()
    
    # Extract short theme for better readability
    tema_curto = tema.split(":")[0] if ":" in tema else tema
    
    # Create introduction paragraph
    introducao = f"Convidamos todos os colaboradores para participar na nossa palestra mensal de saúde sobre {tema_curto}. Este tema é de extrema importância para o nosso bem-estar no ambiente de trabalho e fora dele."
    
    # Replace placeholders
    newsletter_html = template
    newsletter_html = newsletter_html.replace("[MÊS]", month)
    
    # Create a data URI for the logo to avoid path issues
    logo_data_uri = ""
    try:
        if os.path.isfile(LOGO_PATH):
            with open(LOGO_PATH, 'rb') as logo_file:
                logo_bytes = logo_file.read()
                logo_base64 = base64.b64encode(logo_bytes).decode('utf-8')
                logo_data_uri = f"data:image/png;base64,{logo_base64}"
        else:
            print(f"Logo file not found at {LOGO_PATH}")
    except Exception as e:
        print(f"Error creating data URI for logo: {e}")
    
    # Use data URI for logo if available, or keep the placeholder
    if logo_data_uri:
        newsletter_html = newsletter_html.replace("https://placeholder.com/wp-content/uploads/2018/10/placeholder.com-logo1.png", logo_data_uri)
    
    # Handle main image
    # Create data URI for the main image too for consistency
    image_data_uri = ""
    try:
        if os.path.isfile(image_path):
            with open(image_path, 'rb') as img_file:
                img_bytes = img_file.read()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                image_data_uri = f"data:image/png;base64,{img_base64}"
        else:
            print(f"Image file not found at {image_path}")
    except Exception as e:
        print(f"Error creating data URI for image: {e}")
    
    # Use data URI for main image if available
    if image_data_uri:
        newsletter_html = newsletter_html.replace("[IMAGEM_URL]", image_data_uri)
    else:
        # Create a simple blank image as last resort
        newsletter_html = newsletter_html.replace("[IMAGEM_URL]", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
    
    newsletter_html = newsletter_html.replace("[TEMA_PALESTRA]", tema)
    newsletter_html = newsletter_html.replace("[INTRODUÇÃO_PALESTRA]", introducao)
    
    # Replace objectives
    objectives_list = obj_gerais.split("<li>")
    for i, obj in enumerate(objectives_list[1:4], 1):  # Skip the first empty element
        obj_clean = obj.replace("</li>", "").strip()
        if obj_clean:
            newsletter_html = newsletter_html.replace(f"[OBJECTIVO_{i}]", obj_clean)
    
    # Replace content description - ensure proper formatting
    # Format the content description to be more readable
    formatted_conteudos = conteudos.replace(";", ".")
    newsletter_html = newsletter_html.replace("[DESCRICAO_CONTEUDOS]", formatted_conteudos)
    
    # Replace event details
    newsletter_html = newsletter_html.replace("[DATA_PALESTRA]", data)
    newsletter_html = newsletter_html.replace("[LOCAL_PALESTRA]", local)
    newsletter_html = newsletter_html.replace("[TEMA_CURTO]", tema_curto)
    
    # Save newsletter
    output_path = os.path.join(BASE_DIR, f"talk_{month.lower()}.html")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(newsletter_html)
    
    return output_path

# Function to convert HTML to PDF
def convert_html_to_pdf(html_path):
    try:
        pdf_path = html_path.replace(".html", ".pdf")
        print(f"Converting {html_path} to PDF...")
        
        # Using wkhtmltopdf command with additional options to handle local resources
        cmd = f'wkhtmltopdf --enable-local-file-access "{html_path}" "{pdf_path}"'
        os.system(cmd)
        
        if os.path.exists(pdf_path):
            print(f"PDF created: {pdf_path}")
            return True
        else:
            print(f"Failed to create PDF: {pdf_path}")
            return False
    
    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        return False

def main():
    print("Starting newsletter generation...")
    
    # Read calendar data
    calendar_data = read_calendar()
    
    generated_newsletters = []
    
    for talk in calendar_data:
        month = talk["Mês"]
        month_file = month.lower()
        
        print(f"\nProcessing: {month} - {talk['Tema']}")
        
        # Find corresponding MD file
        month_num = {
            "Março": "01_Marco",
            "Abril": "02_Abril",
            "Maio": "03_Maio",
            "Junho": "04_Junho",
            "Julho": "05_Julho",
            "Agosto": "06_Agosto",
            "Setembro": "07_Setembro",
            "Outubro": "08_Outubro",
            "Novembro": "09_Novembro",
            "Dezembro": "10_Dezembro"
        }
        
        # Get file prefix
        file_prefix = month_num.get(month, "")
        
        # Find the corresponding file
        files = os.listdir(BASE_DIR)
        talk_file = None
        
        for file in files:
            if file.startswith(file_prefix) and file.endswith(".md"):
                talk_file = file
                break
        
        if not talk_file:
            print(f"Could not find talk file for {month}")
            continue
        
        # Read and parse talk content
        talk_content = parse_talk_content(read_talk_file(os.path.join(BASE_DIR, talk_file)))
        
        # Generate DALL-E prompt
        dalle_prompt = generate_dalle_prompt(talk, talk_content)
        print(f"Generated prompt: {dalle_prompt}")
        
        # Generate image with OpenAI DALL-E 3
        image_path = generate_image_with_dalle(dalle_prompt, month)
        
        # Create and save newsletter
        newsletter_path = create_newsletter(talk, talk_content, image_path)
        print(f"Created newsletter: {newsletter_path}")
        
        generated_newsletters.append(newsletter_path)
    
    print("\nNewsletter generation completed!")
    
    # Convert all newsletters to PDF
    print("\nConverting newsletters to PDF...")
    for newsletter in generated_newsletters:
        convert_html_to_pdf(newsletter)
    
    print("\nAll done! Newsletters and PDFs are ready.")

if __name__ == "__main__":
    main() 
