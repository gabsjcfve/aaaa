import streamlit as st
import time
import logging
from utils.pdf_handler import extract_text_from_pdf
from utils.api_handler import analyze_resume_with_gemini
from utils.report_generator import ReportGenerator
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Configuração da página
st.set_page_config(
    page_title="Analisador de Currículos",
    page_icon="📄",
    layout="wide"
)

# Carrega CSS personalizado
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.title("📄 Analisador de Currículos")
    st.markdown("Faça upload do seu currículo e da descrição da vaga para obter uma análise detalhada de compatibilidade")

    # Seção de upload de arquivo
    st.subheader("1. Faça Upload do Seu Currículo")
    with st.container():
        uploaded_file = st.file_uploader(
            "Faça upload do seu currículo (formato PDF)",
            type=["pdf"],
            help="⚠️ O PDF deve conter texto selecionável. PDFs digitalizados podem não funcionar corretamente."
        )

        if uploaded_file:
            st.info("ℹ️ Dicas para garantir melhor análise:\n"
                   "• Certifique-se que o texto do PDF pode ser selecionado\n"
                   "• Evite PDFs digitalizados ou protegidos\n"
                   "• O arquivo deve estar em bom estado e legível")

    # Input da descrição da vaga
    st.subheader("2. Insira a Descrição da Vaga")
    job_description = st.text_area(
        "Cole a descrição da vaga aqui",
        height=200,
        help="Copie e cole a descrição completa da vaga para uma análise mais precisa"
    )

    # Seção de análise
    if uploaded_file and job_description:
        if st.button("Analisar Currículo", type="primary"):
            try:
                with st.spinner("Processando seu currículo..."):
                    # Log do início do processo
                    logging.info("Iniciando processo de análise")

                    # Extrai texto do PDF
                    progress_text = st.empty()
                    progress_text.text("📄 Extraindo texto do currículo...")

                    resume_text = extract_text_from_pdf(uploaded_file)

                    if not resume_text:
                        st.error("Não foi possível extrair texto do PDF. Por favor, verifique se o arquivo é válido.")
                        return

                    # Análise com API Gemini
                    progress_text.text("🔍 Analisando compatibilidade...")
                    analysis_result, compatibility_score = analyze_resume_with_gemini(
                        resume_text,
                        job_description
                    )

                    # Exibe resultados
                    progress_text.empty()
                    st.success("✅ Análise concluída!")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.subheader("Resultados da Análise")
                        st.markdown(analysis_result)

                    with col2:
                        st.metric(
                            label="Nota de Compatibilidade",
                            value=f"{compatibility_score}%"
                        )

                    # Gera relatório PDF
                    progress_text.text("📊 Gerando relatório...")
                    report_gen = ReportGenerator()
                    pdf = report_gen.generate_report(
                        analysis_result,
                        compatibility_score,
                        job_description
                    )

                    # Salva e fornece link para download
                    pdf_filename = "relatorio_analise_curriculo.pdf"
                    pdf.output(pdf_filename)

                    with open(pdf_filename, "rb") as f:
                        st.download_button(
                            label="📥 Baixar Relatório da Análise",
                            data=f,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )

                    # Limpa arquivo temporário
                    os.remove(pdf_filename)

            except Exception as e:
                logging.error(f"Erro durante a análise: {str(e)}")
                st.error(f"Ocorreu um erro: {str(e)}")
                st.warning("⚠️ Dicas para resolver:\n"
                       "1. Certifique-se que o PDF não está protegido\n"
                       "2. Verifique se o texto pode ser selecionado no PDF\n"
                       "3. Se o PDF foi digitalizado, use um conversor de OCR primeiro\n"
                       "4. Tente fazer upload do arquivo novamente")
    else:
        st.info("Por favor, faça upload do seu currículo e insira a descrição da vaga para começar a análise")

if __name__ == "__main__":
    main()