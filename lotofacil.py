import pandas as pd
from utils import is_fibonacci

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