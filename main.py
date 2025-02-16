import scanpy as sc
import matplotlib.pyplot as plt
from shiny import reactive
from shiny.express import ui, render, input
import os
import zipfile
import functions as f

app_ui = ui.page_fluid(
    ui.tags.h1("UMAP Visulization Tool", class_ = "title"),
    ui.tags.label("Your zip file must contain a h5ad file to create an umap."),
    ui.input_file("file_input", "Upload a zip file.", accept=".zip"),
    ui.output_text("output_message"),
    ui.output_image("output_image")
)



