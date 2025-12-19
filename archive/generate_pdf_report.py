"""
Dynamic PDF Report Generator for CyberSentinel AI
Parses Project_Report.md and renders a professional PDF (Thesis Style)
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import os
import re

class MarkdownPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(25, 25, 25)
        self.content_width = self.w - 2 * self.l_margin
        self.chapter_count = 0
        
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'CyberSentinel AI - Final Project Report | Page {self.page_no()}', align='R')
            self.ln(15)
            
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', align='C')

    def add_title_page(self):
        self.add_page()
        self.ln(60)
        
        # Title
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(22, 33, 62) # Dark Blue
        self.multi_cell(0, 12, 'CYBERSENTINEL\nAI-BASED MEMORY FORENSICS ANALYZER', align='C')
        self.ln(20)
        
        # Separator
        self.set_draw_color(0, 242, 96) # Neon Green
        self.set_line_width(2)
        self.line(40, self.get_y(), 170, self.get_y())
        self.ln(20)
        
        # Subtitle
        self.set_font('Helvetica', '', 16)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, 'FINAL PROJECT REPORT (THESIS EDITION)', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(40)
        
        # Metadata
        self.set_font('Helvetica', '', 12)
        metadata = [
            ("Version", "4.0 (Ultimate Edition)"),
            ("Date", datetime.now().strftime("%B %d, %Y")),
            ("Author", "Development Team"),
            ("Institution", "Department of Computer Science & Cybersecurity")
        ]
        
        for label, value in metadata:
            self.set_font('Helvetica', 'B', 12)
            self.cell(40, 8, label + ":", align='R')
            self.set_font('Helvetica', '', 12)
            self.cell(0, 8, f"  {value}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def render_markdown_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        in_code_block = False
        code_buffer = []
        
        in_table = False
        table_buffer = []
        
        for line in lines:
            line = line.strip()
            
            # --- Code Blocks ---
            if line.startswith('```'):
                if in_code_block:
                    self.render_code_block(code_buffer)
                    code_buffer = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue
            
            if in_code_block:
                code_buffer.append(line)
                continue
                
            # --- Tables (Basic parsing) ---
            if line.startswith('|'):
                if not in_table:
                    in_table = True
                    table_buffer = []
                table_buffer.append(line)
                continue
            elif in_table:
                # Table ended
                self.render_table(table_buffer)
                table_buffer = []
                in_table = False
                # Fall through to process current line
                
            if not line:
                self.ln(5)
                continue
                
            # --- Headers ---
            if line.startswith('# '):
                self.render_chapter_title(line[2:])
            elif line.startswith('## '):
                self.render_section_title(line[3:])
            elif line.startswith('### '):
                self.render_subsection_title(line[4:])
                
            # --- Placeholders ---
            elif line.startswith('[PLACEHOLDER:'):
                desc = line.replace('[PLACEHOLDER:', '').replace(']', '').strip()
                self.render_placeholder(desc)
                
            # --- Bullet Points ---
            elif line.startswith('* ') or line.startswith('- '):
                self.render_bullet(line[2:])
                
            # --- Math/Latex (Simplified) ---
            elif line.startswith('$$'):
                self.render_math(line.replace('$$', ''))
                
            # --- Body Text ---
            else:
                self.render_body_text(line)
                
        # Flush any remaining buffers
        if table_buffer:
            self.render_table(table_buffer)

    def render_chapter_title(self, text):
        self.add_page()
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(22, 33, 62)
        # Green accent bar
        self.set_fill_color(0, 242, 96)
        self.rect(20, self.get_y(), 2, 12, 'F')
        
        self.set_x(25)
        self.multi_cell(0, 10, text.upper())
        self.ln(10)

    def render_section_title(self, text):
        self.ln(5)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(40, 40, 60)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def render_subsection_title(self, text):
        self.ln(2)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(60, 60, 80)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def render_body_text(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        text = text.replace('**', '') 
        text = self.normalize_text(text)
        self.multi_cell(self.content_width, 6, text)

    def render_bullet(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        text = text.replace('**', '')
        text = self.normalize_text(text)
        self.set_x(30) # Indent
        self.cell(5, 6, '-', align='C')
        
        # Calculate remaining width
        # Page width - Right Margin - Current X
        curr_x = self.get_x()
        width = self.w - self.r_margin - curr_x
        self.multi_cell(width, 6, text)

    def render_code_block(self, lines):
        self.ln(4)
        self.set_font('Courier', '', 9)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(0, 0, 0)
        
        # Calculate max width needed or use page width
        # Simple rendering
        for line in lines:
            line = self.normalize_text(line)
            # Indent code
            self.set_x(30)
            self.multi_cell(0, 5, line, fill=True)
        self.ln(4)

    def render_placeholder(self, desc):
        self.ln(5)
        self.set_fill_color(240, 240, 250)
        self.set_draw_color(200, 200, 200)
        self.set_dash_pattern(dash=3, gap=2)
        x, y = self.get_x(), self.get_y()
        self.rect(x, y, self.content_width, 50, 'DF')
        self.set_dash_pattern(dash=0, gap=0)
        
        self.set_xy(x, y + 20)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 100, 150)
        self.cell(self.content_width, 10, f'[FIGURE: {desc}]', align='C')
        self.set_xy(x, y + 55)

    def render_math(self, formula):
        self.ln(5)
        self.set_font('Helvetica', 'I', 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, f"Formula: {formula}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def render_table(self, table_lines):
        # A very basic pipe table parser
        # Expectation: 
        # | Header | Header |
        # | --- | --- |
        # | Data | Data |
        
        rows = []
        for line in table_lines:
            # simple split by pipe
            cells = [c.strip() for c in line.split('|') if c.strip() != '']
            if not cells: continue
            rows.append(cells)
            
        if len(rows) < 2: return # Invalid table
        
        headers = rows[0]
        # Skip separator line (row 1 usually '---')
        data_rows = rows[2:] if len(rows) > 1 and set(rows[1][0]) <= {'-', ':'} else rows[1:]
        
        col_count = len(headers)
        if col_count == 0: return
        col_width = self.content_width / col_count
        
        self.ln(5)
        # Render Header
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(22, 33, 62)
        self.set_text_color(255, 255, 255)
        for h in headers:
            self.cell(col_width, 8, self.normalize_text(h), border=1, align='C', fill=True)
        self.ln()
        
        # Render Data
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        fill = False
        for row in data_rows:
            if fill:
                self.set_fill_color(248, 249, 252)
            else:
                self.set_fill_color(255, 255, 255)
            
            # Ensure row has enough cells
            padded_row = row + [''] * (col_count - len(row))
            
            # Find max height for this row
            max_h = 7
            
            # Print cells
            # Note: multi_cell in a table row is complex in FPDF. 
            # We will use simple cell and truncate if too long for this basic logic.
            for cell in padded_row[:col_count]:
                txt = self.normalize_text(cell)
                self.cell(col_width, 7, txt, border=1, align='C', fill=True)
            self.ln()
            fill = not fill
        self.ln(5)

    def normalize_text(self, text):
        """Fix unicode characters for latin-1"""
        replacements = {
            '\u2013': '-', '\u2014': '-',
            '\u2018': "'", '\u2019': "'",
            '\u201c': '"', '\u201d': '"',
            '\u2022': '-',
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        
        # Strip other non-latin-1 chars
        return text.encode('latin-1', 'ignore').decode('latin-1')

def generate():
    pdf = MarkdownPDF()
    pdf.add_title_page()
    
    if os.path.exists('Project_Report.md'):
        pdf.render_markdown_file('Project_Report.md')
    else:
        print("Project_Report.md not found!")
        return

    outfile = 'CyberSentinel_AI_Ultimate_Report.pdf'
    pdf.output(outfile)
    print(f"Success! Report generated: {os.path.abspath(outfile)}")

if __name__ == '__main__':
    generate()
