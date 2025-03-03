import requests
import os
import re
import json

def analyze_resume_with_gemini(resume_text, job_description):
    """
    Envia currículo e descrição da vaga para análise da API Gemini
    """
    api_key = "AIzaSyBzwbCvx_LMKbGu3OiVmJzveXmW25Hfuk0"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = f"""
    Analise a compatibilidade entre o seguinte currículo e a descrição da vaga.
    Forneça uma análise detalhada e uma nota de compatibilidade de 0 a 100%.

    Currículo:
    {resume_text}

    Descrição da Vaga:
    {job_description}

    Por favor, forneça:
    1. Nota geral de compatibilidade (0-100%)
    2. Principais habilidades e qualificações correspondentes
    3. Requisitos ausentes ou lacunas
    4. Recomendações para melhoria
    """

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()

        if "candidates" in result and len(result["candidates"]) > 0:
            analysis = result["candidates"][0]["content"]["parts"][0]["text"]

            # Extrai a porcentagem usando regex
            percentage_match = re.search(r"(\d{1,3})%", analysis)
            percentage = percentage_match.group(1) if percentage_match else "N/A"

            return analysis, percentage
        else:
            raise Exception("Resposta inválida da API")

    except Exception as e:
        raise Exception(f"Erro na API: {str(e)}")