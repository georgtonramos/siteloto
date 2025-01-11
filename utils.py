import random

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

def generate_combinations(numbers, count, length):
    """Gera combinações evitando sequências longas."""
    combinations = []
    while len(combinations) < count:
        combination = sorted(random.sample(numbers, length))
        # Verificar se não há sequências longas (exemplo: mais de 3 números consecutivos)
        if all(combination[i] + 1 != combination[i + 1] or combination[i] + 2 != combination[i + 2] for i in range(len(combination) - 2)):
            combinations.append(combination)
    return combinations

def format_numbers(numbers):
    """Formata uma lista de números como uma string separada por vírgulas."""
    return ', '.join(map(str, numbers))

def is_even(number):
    """Verifica se um número é par."""
    return number % 2 == 0

def is_odd(number):
    """Verifica se um número é ímpar."""
    return number % 2 != 0

def is_prime(number):
    """Verifica se um número é primo."""
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_multiple_of_3(number):
    """Verifica se um número é múltiplo de 3."""
    return number % 3 == 0