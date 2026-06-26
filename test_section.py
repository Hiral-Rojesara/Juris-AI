
from utils.pdf_loader import load_pdf_text
from utils.section_search import find_section

bns_text = load_pdf_text("data/BNS/BNS.pdf")

section = find_section(
    bns_text,
    "103"
)

print(section)