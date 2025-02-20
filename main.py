import scanpy as sc
import matplotlib.pyplot as plt
from shiny import reactive, App
from shiny.express import ui, render, input
import os
import zipfile
import functions as f

app_ui = ui.page(
    ui.tags.h1("UMAP Visulization Tool", class_ = "title"),
    ui.tags.label("Your zip file must contain a h5ad file to create an umap."),
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
        return "File uploaded successfully! Processing..."
    
    @output
    @render.plot
    def output_image():
        if not input.file_input():
            return None

        file_path = input.file_input()[0]["datapath"]
        
        h5ad_file = f.extractzip(file_path)       
        if not h5ad_file:
            return "No .h5ad file found in the zip."
        
        fig = f.umap_process(h5ad_file)  
        return fig 

app = App(app_ui, server)