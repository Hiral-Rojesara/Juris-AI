from utils.pdf_loader import load_pdf_text

files = [
    "data/BNS/BNS.pdf",
    "data/BNSS/BNSS.pdf",
    "data/BSA/BSA.pdf",
    "data/CONSTITUTION/Constitution.pdf",
    "data/CPC/CPC.pdf",
    "data/CRPC/CrPC.pdf",
    "data/EVIDENCE/Evidence1872.pdf",
    "data/IPC/IPC.pdf"
]

for file in files:

    print("\n" + "=" * 50)
    print(file)
    print("=" * 50)

    text = load_pdf_text(file)

    print(text[:2000])