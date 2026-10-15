import pymupdf
import re
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "The Islamabad Capital Territory Child Marriage Restraint Act, 2025 (Act No. XI of 2025) (1).pdf"
)


# --------------------------------------------------
# 1. Extract text from PDF
# --------------------------------------------------

def extract_text(pdf_path):
    """
    Extract selectable text from every page of the PDF.

    Args:
        pdf_path: Path to the law PDF.

    Returns:
        Complete extracted text as a single string.
    """

    try:
        document = pymupdf.open(pdf_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        text = "\n".join(pages)

        if not text.strip():
            raise ValueError("No text could be extracted from the PDF.")

        return text

    except Exception as error:
        raise RuntimeError(
            f"PDF extraction failed: {error}"
        ) from error


# --------------------------------------------------
# 2. Clean extracted text
# --------------------------------------------------

def clean_text(text):
    """
    Clean common PDF extraction artifacts while preserving
    the legal text and section structure.
    """

    # Remove repeated Gazette page header/footer
    text = re.sub(
        r"(?im)^\s*THE GAZETTE OF PAKISTAN.*$",
        "",
        text
    )

    text = re.sub(
        r"(?im)^\s*PART\s+I\s*$",
        "",
        text
    )

    # Remove standalone page numbers
    text = re.sub(
        r"(?m)^\s*\d+\s*$",
        "",
        text
    )

    # Fix common OCR/PDF extraction errors
    replacements = {
        "eightecn": "eighteen",
        "eighleen": "eighteen",
        "femalc": "female",
        "malc": "male",
        "u''ho": "who",
        "chrld": "child",
        "punishcd": "punished",
        "pcrsuadcs": "persuades",
        "cohcrccs": "coerces",
        "imprisonmcnt": "imprisonment",
        "cxtend": "extend",
        "finc": "fine",
        "maniage": "marriage",
        "marriagc": "marriage",
        "contractitrg": "contracting",
        "regstrar": "registrar",
        "M&ai": "Nikah",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Strip each line
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    text = "\n".join(lines)

    return text.strip()


# --------------------------------------------------
# 3. Create legal section-based chunks
# --------------------------------------------------

def create_chunks(text, size=1500, overlap=150):
    """
    Split the law into chunks using numbered legal sections.

    Legal sections are preferred over arbitrary character splitting
    because keeping a section together improves retrieval quality.

    Args:
        text: Cleaned legal document.
        size: Maximum chunk size in characters.
        overlap: Character overlap for long sections.

    Returns:
        List of dictionaries containing chunk text and section metadata.
    """

    # Match sections such as:
    # 1. Short title...
    # 2. Definitions...
    # 3. Registration...
    section_pattern = r"(?m)(?=^\s*\d+\.\s+)"

    sections = re.split(section_pattern, text)

    chunks = []

    for section in sections:

        section = section.strip()

        if len(section) < 100:
            continue

        # Extract section number
        match = re.match(r"^(\d+)\.\s+", section)

        if match:
            section_number = int(match.group(1))
        else:
            section_number = 0

        # --------------------------------------------------
        # Section fits inside one chunk
        # --------------------------------------------------

        if len(section) <= size:

            chunks.append(
                {
                    "text": section,
                    "section": section_number
                }
            )

        # --------------------------------------------------
        # Long section
        # --------------------------------------------------

        else:

            start = 0
            chunk_number = 0

            while start < len(section):

                chunk = section[
                    start:start + size
                ].strip()

                if chunk:

                    chunks.append(
                        {
                            "text": chunk,
                            "section": section_number,
                            "part": chunk_number
                        }
                    )

                start += size - overlap
                chunk_number += 1

    return chunks


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("PAKISTANI LAW RAG - PREPROCESSING")
    print("=" * 60)

    # --------------------------------------------------
    # Read PDF
    # --------------------------------------------------

    print("\nReading PDF...")

    raw_text = extract_text(PDF_PATH)

    print("PDF extraction successful!")

    # --------------------------------------------------
    # Document statistics
    # --------------------------------------------------

    print("\nDOCUMENT STATISTICS")
    print("-" * 60)

    print("Characters:", len(raw_text))
    print("Words:", len(raw_text.split()))

    print("\nFIRST 500 CHARACTERS")
    print("-" * 60)

    print(raw_text[:500])

    # --------------------------------------------------
    # Cleaning
    # --------------------------------------------------

    cleaned_text = clean_text(raw_text)

    print("\nAFTER CLEANING")
    print("-" * 60)

    print("Characters:", len(cleaned_text))
    print("Words:", len(cleaned_text.split()))

    # --------------------------------------------------
    # Chunking
    # --------------------------------------------------

    chunks = create_chunks(
        cleaned_text,
        size=1500,
        overlap=150
    )

    print("\nCHUNKING")
    print("-" * 60)

    print("Method: Legal section based")
    print("Chunk size:", 1500)
    print("Overlap:", 150)
    print("Total chunks:", len(chunks))

    # --------------------------------------------------
    # Show examples
    # --------------------------------------------------

    print("\nEXAMPLE CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(chunks[:3], 1):

        print(f"\n--- CHUNK {i} ---")
        print("Section:", chunk["section"])
        print(chunk["text"])

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETED")
    print("=" * 60)