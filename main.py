import ipywidgets as widgets
from IPython.display import display, clear_output, Javascript
import pandas as pd
import zipfile
import os
import json

def pointBreak():
    output = widgets.Output()
    paths_output = widgets.Output()
    with open('snippets.json', 'r') as file:
       with output:
           data = json.load(file)
           paths_df=pd.DataFrame(data[1])
    with paths_output:
        display(paths_df)
    
    title = widgets.HTML(value="<h2>Tools</h2>")
    
    file_to_zip = widgets.Text(description="File Path:")
    extract_to = widgets.Text(description="Extract Path:", disabled=True)
    create_folder = widgets.Checkbox(value=False, description="specify extract path")
    unzip = widgets.Button(description="unzip", button_style="success")
    clear_btn = widgets.Button(description="clear", button_style="danger")
    btns=widgets.HBox([unzip, clear_btn])
    
    tab1=widgets.VBox([file_to_zip, extract_to, create_folder, btns])
    
    code_snippets = widgets.Dropdown(
        options=['Select','Spark Session Creation', 'Pandas to Spark DF', 'Pandas DF to Workbook']
    )
    snippet=widgets.Textarea(layout=widgets.Layout(width="80%", height="100px"))
    copy_button = widgets.Button(
        button_style="info",
        icon="copy",
        layout=widgets.Layout(width="100px", height="auto")
    )
    
    coderow1=widgets.HBox([code_snippets, copy_button])
    coderow2=widgets.VBox([coderow1, snippet])
    
    tab2acc1 = widgets.Accordion(children=[coderow2, paths_output])
    tab2acc1.set_title(0, 'Code')
    tab2acc1.set_title(1, 'Paths')
    
    tab2=widgets.VBox([tab2acc1])
    
    tabs = widgets.Tab()
    tabs.children = [tab1, tab2]
    tabs.set_title(0, 'Unzip')
    tabs.set_title(1, 'Snippets')
    
    def copy_to_clipboard(b):
        with output:
            clear_output()
            print('copied!')
            text_value = snippet.value.replace("\n", "\\n").replace("'", "\\'")
            display(Javascript(f"""
            navigator.clipboard.writeText("{text_value}");
            """))
    
    def switchContent(change):
        with output:
            clear_output()
            if(change['new']!='Select'):
                snippet.value=data[0]['code'][change['new']]['code']
            else:
                snippet.value=''
            return
    
    def unzip_file(b):
        with output:
            clear_output()
            dirs=file_to_zip.value.split('/')
            folder=dirs[len(dirs)-1].split('.')[0]
            if(not create_folder.value):
                extract_path=folder
            else:
                extract_path=extract_to.value
                if not os.path.exists(extract_path):
                    print(f"{extract_path} path does not exists!")
                    return
            if file_to_zip.value=='' or  (not os.path.exists(file_to_zip.value)):
                print('Please check zip file name')
                return
            with zipfile.ZipFile(file_to_zip.value, 'r') as zipf:
                zipf.extractall(extract_path)
            print(f"Files extracted successfully to {extract_path}")
    
    def execute_cmd(cmd):
        try:
            print(subprocess.run(cmd, check=True))
            print("success!")
        except Exception as e:
            print("An error occurred:", e)
    
    def switchOption(change):
        with output:
            clear_output()
            extract_to.disabled=not extract_to.disabled
            print('toggled!')
    
    def clear(b):
        with output:
            clear_output()
            return
    
    
    unzip.on_click(unzip_file)
    clear_btn.on_click(clear)
    copy_button.on_click(copy_to_clipboard)
    create_folder.observe(switchOption, names='value')
    code_snippets.observe(switchContent, names='value')
    display(title, tabs, output)

def start():
    pointBreak()