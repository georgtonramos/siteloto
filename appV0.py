from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/verificar')
def index():
    return render_template('index.html')

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

@app.route('/verificar-numeros')
def verificar_numeros_page():
    return render_template('verificar_numeros.html')

if __name__ == '__main__':
    app.run(debug=True)

