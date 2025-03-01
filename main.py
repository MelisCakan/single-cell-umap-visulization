from shiny import App, ui
from shiny.express import render, input
from functions import umap_process, extractzip
import os

app_ui = ui.page_fluid(
    ui.head_content(ui.tags.link(rel="stylesheet", href="styles.css")),
    ui.h1("UMAP Visulization Tool", class_ = "title"),
    ui.p("Your zip file must contain a h5ad file to create an umap."),
    ui.input_file("file_input", "Upload a zip file.", accept=".zip"),
    ui.output_text("output_message"),
    ui.output_image("output_image")
)

def server(input, output, session):
    
    @output
    @render.text
    def output_message():
        if not input.file_input():
            return "No file uploaded yet."

        file_path = input.file_input()[0]["datapath"]
        h5ad_file = extractzip(file_path)

        if not h5ad_file:
            return "No .h5ad file found in the zip."

        return "File uploaded successfully! Processing..."
    
    @output
    @render.image
    def output_image():
        if not input.file_input():
            return None

        file_path = input.file_input()[0]["datapath"]
        h5ad_file = extractzip(file_path)  
        if not h5ad_file:
            return None

        image_path = umap_process(h5ad_file)

        return {"src": image_path, "alt": "UMAP Visualization"}
    
    folder_path = "./data"  

    @session.on_ended
    def clean_the_data():
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)  
            os.rmdir(folder_path)  
    
app = App(app_ui, server)
app.run()