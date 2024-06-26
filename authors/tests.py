from pdf2docx import Converter


def pdf_to_docx(input_pdf, output_docx):
    # Initialize Converter object
    cv = Converter(input_pdf)

    # Convert PDF to DOCX
    cv.convert(output_docx, start=0, end=None)

    # Close the converter
    cv.close()


if __name__ == "__main__":
    input_pdf = "/home/momin/Downloads/Lab 1-15 FT&T.pdf"  # Replace with your input PDF file path
    output_docx = "/home/momin/Downloads/Lab 1-15 FT&T.docx"  # Replace with desired output DOCX file path

    pdf_to_docx(input_pdf, output_docx)
    print(f"Conversion complete: {output_docx}")
