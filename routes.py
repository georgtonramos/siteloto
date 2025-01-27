from flask import Blueprint, request, jsonify, render_template
from utils import generate_combinations, format_numbers, is_even, is_odd, is_prime, is_multiple_of_3, is_fibonacci
from lotofacil import check_sequence, load_lottery_data, check_columns
import pandas as pd
import requests

main_routes = Blueprint('main_routes', __name__)

API_URL = "https://apilotofacil.georgton.tech"  # URL da API externa

def fetch_lottery_data():
    """
    Busca os dados da loteria diretamente da API.

    Returns:
        list: Lista de resultados da loteria retornados pela API, ou None em caso de erro.
    """
    try:
        response = requests.get(f"{API_URL}/resultados")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API: {e}")
        return None

def contar_pares_impares_primos_fibonacci_multiplos3(numeros):
    """Conta os números pares, ímpares, primos, Fibonacci, múltiplos de 3 e soma."""
    pares = 0
    impares = 0
    primos = 0
    fibonacci_nums = 0
    multiplos3 = 0
    soma = 0

    for numero in numeros:
        soma += numero

        if is_even(numero):
            pares += 1
        elif is_odd(numero):
            impares += 1

        if is_prime(numero):
            primos += 1

        if is_fibonacci(numero):
            fibonacci_nums += 1

        if is_multiple_of_3(numero):
            multiplos3 += 1

    return {
        "pares": pares,
        "impares": impares,
        "primos": primos,
        "fibonacci": fibonacci_nums,
        "multiplos3": multiplos3,
        "soma": soma
    }

@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/verificar')
def index():
    return render_template('index.html')

@main_routes.route('/verificar-numeros')
def verificar_numeros_page():
    return render_template('verificar_numeros.html')

@main_routes.route('/process', methods=['POST'])
def process_sequence():
    try:
        data = request.json
        if not data or 'sequence' not in data:
            return jsonify({"error": "O campo 'sequence' é obrigatório."}), 400

        sequence = data.get('sequence', [])
        if not isinstance(sequence, list) or not all(isinstance(num, (int, float)) for num in sequence):
            return jsonify({"error": "A 'sequence' deve ser uma lista de números."}), 400

        numeros = [int(num) for num in sequence]
        result = contar_pares_impares_primos_fibonacci_multiplos3(numeros)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": f"Erro de processamento: {str(e)}"}), 400

@main_routes.route('/numeros-faltantes', methods=['POST'])
def numeros_faltantes():
    data = request.get_json()
    numbers = data.get('numbers', [])

    if len(numbers) != 15:
        return jsonify({'error': 'Você deve inserir exatamente 15 números.'}), 400

    missing = []
    for i in range(1, 26):
        if i not in numbers:
            missing.append(i)

    return jsonify({'missing': missing})

@main_routes.route('/check-lotofacil', methods=['POST'])
def check_lotofacil():
    """
    Verifica se uma sequência de números foi sorteada.

    Exemplo de entrada JSON:
    {
        "sequence": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    }
    """
    data = request.get_json()
    sequence = data.get('sequence', [])

    if len(sequence) != 15:
        return jsonify({'error': 'A sequência da Lotofácil deve conter exatamente 15 números.'}), 400

    # Busca os dados da API
    lottery_data = fetch_lottery_data()
    if not lottery_data:
        return jsonify({'error': 'Erro ao buscar os dados da Lotofácil na API.'}), 500

    # Verifica se a sequência está nos dados da API
    sequence_sorted = sorted(sequence)
    for result in lottery_data:
        if sorted(result['numeros_sorteados']) == sequence_sorted:
            return jsonify({'message': f"A sequência já foi sorteada no concurso {result['numero_concurso']}."})

    return jsonify({'message': "A sequência nunca foi sorteada."})
    
@main_routes.route('/verificar-sorteio')
def verificar_sorteio_page():
    return render_template('verificar_sorteio.html')

@main_routes.route('/gerar-combinacoes', methods=['POST'])
def gerar_combinacoes_route():
    data = request.get_json()
    qtd_combinacoes = data.get('qtdCombinacoes')
    qtd_numeros = data.get('qtdNumeros')
    numeros = data.get('numeros')

    if not all([qtd_combinacoes, qtd_numeros, numeros]):
        return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400

    if not isinstance(numeros, list) or not all(isinstance(num, int) for num in numeros):
        return jsonify({'error': 'Números inválidos.'}), 400
    
    if qtd_numeros > len(numeros):
        return jsonify({'error': 'A quantidade de números por combinação não pode ser maior que a quantidade de números fornecidos.'}), 400

    combinations = generate_combinations(numeros, qtd_combinacoes, qtd_numeros)
    return jsonify({'combinations': combinations})

@main_routes.route('/gerar-combinacoes-page')
def gerar_combinacoes_page():
    return render_template('gerar_combinacoes.html')