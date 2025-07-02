# Final Report – Exotic Option Pricing

This folder contains the high-level write-up for the **Pricing Exotic Options** project.

## Files

- **final_report.pdf**  
  The compiled PDF of the full report.

- **final_report.tex**  
  LaTeX source for the report. Edit this if you’d like to tweak formatting or add content.

- **references.bib**  
  BibTeX file holding all cited references.

## How to Rebuild

1. Install a LaTeX distribution (e.g., TeX Live, MiKTeX).  
2. From this directory, run:
   ```bash
   pdflatex final_report.tex
   bibtex final_report
   pdflatex final_report.tex
   pdflatex final_report.tex
   
3. The rebuilt PDF will appear as final_report.pdf.

### For the full computational details, see the Jupyter notebooks in the notebooks/ folder.

### For the pricing implementations, see the pricing/ package.