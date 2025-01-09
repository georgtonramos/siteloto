from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# ... (suas funções atuais: is_fibonacci, contar_pares_impares_primos_fibonacci_multiplos3) ...
def is_fibonacci(n):
    """Verifica se um número é um número de Fibonacci."""
    if n < 0:
        return False
    if n <= 1:
        return True
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n

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

        if numero % 2 == 0:
            pares += 1
        else:
            impares += 1

        if numero > 1:
            is_primo = True
            for i in range(2, int(numero**0.5) + 1):
                if numero % i == 0:
                    is_primo = False
                    break
            if is_primo:
                primos += 1

        if is_fibonacci(numero):
            fibonacci_nums += 1

        if numero % 3 == 0:
            multiplos3 += 1

    return {
        "pares": pares,
        "impares": impares,
        "primos": primos,
        "fibonacci": fibonacci_nums,
        "multiplos3": multiplos3,
        "soma": soma
    }

def load_lottery_data(file_path, sheet_name):
    """
    Carrega os dados da loteria a partir de um arquivo Excel.

    Args:
        file_path (str): Caminho para o arquivo Excel.
        sheet_name (str): Nome da planilha com os dados.

    Returns:
        pd.DataFrame: DataFrame contendo os dados da loteria, ou None em caso de erro.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado. Verifique o caminho e o nome do arquivo.")
        return None
    except ValueError:
        print(f"Erro: A planilha '{sheet_name}' não foi encontrada no arquivo '{file_path}'. Verifique o nome da planilha.")
        return None

def check_columns(df, required_columns):
    """
    Verifica se as colunas necessárias estão presentes no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame a ser verificado.
        required_columns (list): Lista de nomes de colunas obrigatórias.

    Returns:
        bool: True se todas as colunas estiverem presentes, False caso contrário.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Erro: As seguintes colunas estão faltando no DataFrame: {', '.join(missing_columns)}")
        return False
    return True

def check_sequence(df, ball_columns, sequence):
    """
    Verifica se a sequência informada já foi sorteada.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados da loteria.
        ball_columns (list): Lista com os nomes das colunas das bolas sorteadas.
        sequence (list): Sequência de números a ser verificada.

    Returns:
        int: O número do concurso em que a sequência foi sorteada, ou -1 se não foi sorteada.
    """
    sequence_sorted = sorted(sequence)
    for index, row in df.iterrows():
        draw_numbers = sorted(row[ball_columns].tolist())
        if draw_numbers == sequence_sorted:
            return row['Concurso']
    return -1

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
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/verificar')
def index():
    return render_template('index.html')

@app.route('/verificar-numeros')
def verificar_numeros_page():
    return render_template('verificar_numeros.html')

@app.route('/process', methods=['POST'])
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

@app.route('/numeros-faltantes', methods=['POST'])
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

@app.route('/check-lotofacil', methods=['POST'])
def check_lotofacil():
    data = request.get_json()
    sequence = data.get('sequence', [])

    if df is None or not check_columns(df, bola_columns):
        return jsonify({'error': 'Erro ao carregar ou validar os dados da Lotofácil'}), 500

    if len(sequence) != 15:
        return jsonify({'error': 'A sequência da Lotofácil deve conter exatamente 15 números.'}), 400

    concurso = check_sequence(df, bola_columns, sequence)

    if concurso != -1:
        return jsonify({'message': f"A sequência {sequence} já foi sorteada no concurso {concurso}."})
    else:
        return jsonify({'message': f"A sequência {sequence} nunca foi sorteada."})
    
@app.route('/verificar-sorteio')
def verificar_sorteio_page():
    return render_template('verificar_sorteio.html')

if __name__ == '__main__':
    app.run(debug=True)