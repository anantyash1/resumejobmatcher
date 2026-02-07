import os
import re
from typing import Optional
import PyPDF2
import docx
from PIL import Image
import pytesseract

class ResumeParser:
    """Extract text from various resume formats"""
    
    @staticmethod
    def extract_text(file_path: str, filename: str) -> str:
        """
        Extract text from PDF, DOCX, or image files
        """
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == '.pdf':
                return ResumeParser._extract_from_pdf(file_path)
            elif ext in ['.doc', '.docx']:
                return ResumeParser._extract_from_docx(file_path)
            elif ext in ['.png', '.jpg', '.jpeg']:
                return ResumeParser._extract_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX"""
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    @staticmethod
    def _extract_from_image(file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            raise Exception(f"OCR error: {str(e)}. Ensure Tesseract is installed.")