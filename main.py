from shiny import App, ui
from shiny.express import render, input
from functions import umap_process, extractzip
import os

def app_ui():
    return ui.page_fluid( #user-interface
        ui.head_content(ui.tags.link(rel="stylesheet", href="styles.css")),
        ui.h1("UMAP Visualization Tool", class_ = "title"),
        ui.p("Your zip file must contain a h5ad file to create an umap."),
        ui.input_file("file_input", "Upload a zip file.", accept=".zip"),
        ui.output_text("output_message"),
        ui.output_image("output_image")
    )

def server(input, output, session): #defining server
    
    @output
    @render.text #for output text
    def output_message():
        try:
            if not input.file_input():
                return "No file uploaded yet."

            file_path = input.file_input()[0]["datapath"]
            h5ad_file = extractzip(file_path) #extract to check h5ad file

            if not h5ad_file:
                raise ValueError("No .h5ad file found in the zip.")  #raise error if no h5ad file

            return "File processed successfully! Here is the umap visualization:"
        except Exception as e:
            return f"An error occurred: {e}"
    
    @output
    @render.image #for output image
    def output_image():
        try:
            if not input.file_input():
                return None

            file_path = input.file_input()[0]["datapath"]
            h5ad_file = extractzip(file_path)  #extract to process h5ad
            if not h5ad_file:
                raise ValueError("No .h5ad file found in the zip.")  #raise error if no h5ad file

            image_path = umap_process(h5ad_file)

            return {"src": image_path, "alt": "UMAP Visualization"} #add html tags to image
        except Exception as e:
            print(f"An error occurred while processing the image: {e}")
            return None
    
    folder_path = "./data"  #to delete data that came as an input from the user
    
    @session.on_ended
    def clean_the_data():
        try:
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)  
                os.rmdir(folder_path)  
        except Exception as e:
            print(f"An error occurred while cleaning up data: {e}")
    
app = App(app_ui(), server) #define the app
app.run() #run the app