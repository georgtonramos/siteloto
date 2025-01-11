from flask import Blueprint, request, jsonify, render_template
from utils import generate_combinations, format_numbers, is_even, is_odd, is_prime, is_multiple_of_3, is_fibonacci
from lotofacil import check_sequence, load_lottery_data, check_columns
import pandas as pd

main_routes = Blueprint('main_routes', __name__)

# Carrega os dados da Lotofácil (fora da rota para carregar apenas uma vez)
file_path = 'LotoV7.xlsx'  # Coloque o caminho correto para o seu arquivo
sheet_name = 'LOTOFaCIL'
bola_columns = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']

df = load_lottery_data(file_path, sheet_name)

# Verifica se o DataFrame foi carregado corretamente
if df is None or not check_columns(df, bola_columns):
    print("Erro ao carregar os dados da Lotofácil. Verifique o arquivo e a planilha.")
    # Você pode decidir retornar um erro 500 aqui ou lidar de outra forma
    # return jsonify({'error': 'Erro ao carregar dados da Lotofácil'}), 500
else:
    print("Dados da Lotofácil carregados com sucesso.")

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
    data = request.get_json()
    sequence = data.get('sequence', [])

    if df is None or not check_columns(df, bola_columns):
        return jsonify({'error': 'Erro ao carregar ou validar os dados da Lotofácil'}), 500

    if len(sequence) != 15:
        return jsonify({'error': 'A sequência da Lotofácil deve conter exatamente 15 números.'}), 400

    concurso = check_sequence(df, bola_columns, sequence)

    if concurso != -1:
        # Formata a sequência para exibição
        formatted_sequence = format_numbers(sequence)
        return jsonify({'message': f"A sequência {formatted_sequence} já foi sorteada no concurso {concurso}."})
    else:
        return jsonify({'message': f"A sequência {format_numbers(sequence)} nunca foi sorteada."})
    
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