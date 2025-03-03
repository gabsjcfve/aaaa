import PyPDF2
import io
import re
import logging
from typing import Optional

def extract_text_from_pdf(uploaded_file) -> Optional[str]:
    """
    Extract text from uploaded PDF file with multiple extraction methods
    """
    try:
        # Configuração de logging
        logging.info("Iniciando extração de texto do PDF")

        # Lê o arquivo PDF
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        pdf_reader = PyPDF2.PdfReader(pdf_bytes)

        # Verifica se o PDF tem páginas
        if len(pdf_reader.pages) == 0:
            raise Exception("O PDF está vazio")

        logging.info(f"PDF tem {len(pdf_reader.pages)} páginas")

        # Tenta diferentes métodos de extração
        extracted_text = []
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                # Método 1: Extração direta
                text = page.extract_text()

                # Método 2: Se não obtiver texto, tenta extrair por partes
                if not text.strip():
                    text = ""
                    for obj in page:
                        if hasattr(obj, 'get_text'):
                            text += obj.get_text() + " "

                if text.strip():
                    # Limpa e normaliza o texto
                    cleaned_text = clean_text(text)
                    if cleaned_text:
                        extracted_text.append(cleaned_text)
                        logging.info(f"Página {page_num}: Extraídos {len(cleaned_text)} caracteres")
                else:
                    logging.warning(f"Página {page_num}: Nenhum texto extraído")

            except Exception as e:
                logging.error(f"Erro ao extrair texto da página {page_num}: {str(e)}")
                continue

        # Verifica se conseguiu extrair algum texto
        if not extracted_text:
            raise Exception("Não foi possível extrair texto do PDF. Verifique se o arquivo contém texto selecionável.")

        # Junta todo o texto com quebras de linha entre páginas
        final_text = "\n\n".join(extracted_text)

        if len(final_text.strip()) < 10:  # Verifica se o texto extraído é muito curto
            raise Exception("O texto extraído é muito curto ou vazio. O PDF pode estar protegido ou não conter texto selecionável.")

        logging.info(f"Texto total extraído: {len(final_text)} caracteres")
        return final_text

    except Exception as e:
        logging.error(f"Erro durante a extração do PDF: {str(e)}")
        raise Exception(f"Erro ao processar o PDF: {str(e)}")

def clean_text(text: str) -> str:
    """
    Clean and normalize text for better processing
    """
    if not text:
        return ""

    # Remove caracteres de controle exceto quebras de linha
    text = ''.join(char if char == '\n' or char.isprintable() else ' ' for char in text)

    # Normaliza espaços preservando quebras de linha importantes
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove espaços extras e caracteres especiais
        cleaned = re.sub(r'\s+', ' ', line).strip()
        if cleaned:
            cleaned_lines.append(cleaned)

    # Junta as linhas mantendo a estrutura do texto
    text = '\n'.join(cleaned_lines)

    # Remove caracteres especiais mantendo acentos e pontuação básica
    text = re.sub(r'[^\w\s\u00C0-\u00FF.,!?@\-:/\n]', ' ', text)

    return text.strip()