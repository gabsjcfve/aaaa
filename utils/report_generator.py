from fpdf import FPDF
import datetime

class ReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        # Usando fonte built-in que suporta caracteres especiais
        self.pdf.set_font('Courier')

    def generate_report(self, analysis_text, compatibility_score, job_description):
        """
        Gera relatório PDF com os resultados da análise
        """
        self.pdf.add_page()

        # Cabeçalho
        self.pdf.set_font('Courier', size=16)
        self.pdf.cell(0, 10, "Relatorio de Analise de Curriculo", ln=True, align="C")

        # Data
        self.pdf.set_font('Courier', size=10)
        self.pdf.cell(0, 10, f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)

        # Nota de Compatibilidade
        self.pdf.set_font('Courier', size=14)
        self.pdf.set_text_color(0, 102, 204)
        self.pdf.cell(0, 15, f"Nota de Compatibilidade: {compatibility_score}%", ln=True, align="C")

        # Seção da Descrição da Vaga
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font('Courier', size=12)
        self.pdf.cell(0, 10, "Descricao da Vaga:", ln=True)
        self.pdf.set_font('Courier', size=11)

        # Trata texto para evitar caracteres não suportados
        job_description = self._clean_text_for_pdf(job_description)
        self.pdf.multi_cell(0, 7, job_description)

        # Seção da Análise
        self.pdf.ln(10)
        self.pdf.set_font('Courier', size=12)
        self.pdf.cell(0, 10, "Analise:", ln=True)
        self.pdf.set_font('Courier', size=11)

        # Trata texto para evitar caracteres não suportados
        analysis_text = self._clean_text_for_pdf(analysis_text)
        self.pdf.multi_cell(0, 7, analysis_text)

        return self.pdf

    def _clean_text_for_pdf(self, text):
        """
        Limpa o texto para ser compatível com o PDF
        """
        if not text:
            return ""

        # Remove caracteres especiais mantendo apenas ASCII básico
        text = ''.join(c if ord(c) < 128 else ' ' for c in text)
        # Remove múltiplos espaços
        text = ' '.join(text.split())
        return text