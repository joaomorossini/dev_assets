<context>
After developing a new program for the company, it is time to create the images for each talk. These images will be used to produce engaging internal communications materials for each of the health talks in the program.
</context>

<aesthetics>
- Color palette:
    - White Background: #FFFFFF – A clean and minimalistic white dominating the background.
    - Orange Accent: #F15A24 – A warm and vibrant orange used in the lower border and logos.
    - Black Text: #000000 – Used for textual elements such as "LUANDA, MÊS, ANO."
- A personalized cover image for each talk
</aesthetics>

<goal>
Prepare the improved communication materials for each talk of the new program
</goal>

<instructions>
- Use html to create a template . Think of this material as a newletter that is sent via email to the employees
- Make sure to use the color palette and aesthetics described above
- Based on the content of each talk located in /Users/morossini/Projects/1.dev_assets/2_personal/africa_care/new_program, create a prompt to generate an image for each talk
- Use AzureOpenAI with Dall-E 3 to generate one image for each talk
    - Aspect ratio: Widescreen
    - Model: dall-e-3
    - Deployment name: dall-e-3
- Use error handling to make sure all the images are generated correctly. Azure sometimes fails to generate the image, so you need to retry, probably with a different prompt because we may have triggered the moderation filter by mistake.
- Use the template to create the communication materials for each talk, including text and image
- Save each newsletter in the folder /Users/morossini/Projects/1.dev_assets/2_personal/africa_care/new_program/talk_[talk_month].html
</instructions>
