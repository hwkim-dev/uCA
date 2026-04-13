import os

md_path = "/home/hwkim/Desktop/github/uCA/docs/archive/experimental_v001/Drivers/ISA_Spreadsheet.md"
html_path = "/home/hwkim/Desktop/github/uCA/docs/archive/experimental_v001/Drivers/ISA_Instruction_set_architecture.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Strip meta tag to avoid conflicts
html_content = html_content.replace('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">', '')

new_md_content = """<div style="font-family: Arial, sans-serif; margin-bottom: 24px;">
    <!-- Breadcrumb area -->
    <div style="font-size: 14px; color: #0068b5; margin-bottom: 15px;">
        <a href="../../../" style="color: #0068b5; text-decoration: none;">Archive</a> / 
        <a href="../../" style="color: #0068b5; text-decoration: none;">experimental_v001</a> / 
        <a href="../" style="color: #0068b5; text-decoration: none;">Drivers</a> / 
        <b>ISA_Spreadsheet</b>
    </div>

    <!-- Blue Hero Banner -->
    <div style="background-color: #0068b5; color: white; padding: 40px; margin: 0 -20px 30px -20px;">
        <h1 style="color: white; margin-top: 0; font-size: 2.2em; font-weight: 300;">uCA ISA Spreadsheet View</h1>
        
        <div style="display: flex; flex-wrap: wrap; gap: 40px; margin-top: 30px; font-size: 14px;">
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">ID</div>
                <div style="font-size: 16px; font-weight: bold;">UCA-ISA-V1</div>
            </div>
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">Date</div>
                <div style="font-size: 16px; font-weight: bold;">04/13/2026</div>
            </div>
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">Version</div>
                <div style="font-size: 16px; font-weight: bold;">v001 (Archived)</div>
            </div>
            <div>
                <div style="opacity: 0.8; margin-bottom: 5px;">Visibility</div>
                <div style="font-size: 16px; font-weight: bold;">Public</div>
            </div>
        </div>
    </div>
</div>

This page displays the native HTML spreadsheet outline of the NPU ISA Architecture exported directly from Google Sheets. 
For a more highly detailed specification parameter definition, please navigate to the [ISA Specification](./ISA.md) page.

<div style="width: 100%; overflow-x: auto; background-color: white; padding-bottom: 50px;">
""" + html_content + "\n</div>\n"

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(new_md_content)

print("Inlined HTML successfully.")
