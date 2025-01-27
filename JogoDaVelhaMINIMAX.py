import tkinter as tk
from tkinter import messagebox
import numpy as np

def criar_tabuleiro():
    """Cria um tabuleiro inicial para o jogo da velha."""
    return np.zeros((3, 3), dtype=int)

def movimentos_validos(tabuleiro):
    """Gera todos os movimentos válidos para o jogador."""
    return [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == 0]

def aplicar_movimento(tabuleiro, movimento, jogador):
    """Aplica um movimento no tabuleiro."""
    novo_tabuleiro = tabuleiro.copy()
    x, y = movimento
    novo_tabuleiro[x][y] = jogador
    return novo_tabuleiro

def funcao_utilidade(tabuleiro):
    """Calcula a função de utilidade com base no estado do jogo."""
    for i in range(3):
        if abs(sum(tabuleiro[i, :])) == 3:  # Linhas
            return np.sign(sum(tabuleiro[i, :]))
        if abs(sum(tabuleiro[:, i])) == 3:  # Colunas
            return np.sign(sum(tabuleiro[:, i]))

    diag1 = tabuleiro[0, 0] + tabuleiro[1, 1] + tabuleiro[2, 2]
    diag2 = tabuleiro[0, 2] + tabuleiro[1, 1] + tabuleiro[2, 0]
    if abs(diag1) == 3 or abs(diag2) == 3:  # Diagonais
        return np.sign(diag1) if abs(diag1) == 3 else np.sign(diag2)

    return 0  # Empate ou jogo não finalizado

def jogo_finalizado(tabuleiro):
    """Verifica se o jogo terminou."""
    return funcao_utilidade(tabuleiro) != 0 or not np.any(tabuleiro == 0)

def minimax(tabuleiro, profundidade, maximizando, alfa, beta):
    """Implementação do algoritmo Minimax com poda alfa-beta."""
    if profundidade == 0 or jogo_finalizado(tabuleiro):
        return funcao_utilidade(tabuleiro), None

    if maximizando:
        max_valor = float('-inf')
        melhor_movimento = None

        for movimento in movimentos_validos(tabuleiro):
            novo_tabuleiro = aplicar_movimento(tabuleiro, movimento, 1)
            valor, _ = minimax(novo_tabuleiro, profundidade - 1, False, alfa, beta)

            if valor > max_valor:
                max_valor = valor
                melhor_movimento = movimento

            alfa = max(alfa, valor)
            if beta <= alfa:
                break

        return max_valor, melhor_movimento

    else:
        min_valor = float('inf')
        melhor_movimento = None

        for movimento in movimentos_validos(tabuleiro):
            novo_tabuleiro = aplicar_movimento(tabuleiro, movimento, -1)
            valor, _ = minimax(novo_tabuleiro, profundidade - 1, True, alfa, beta)

            if valor < min_valor:
                min_valor = valor
                melhor_movimento = movimento

            beta = min(beta, valor)
            if beta <= alfa:
                break

        return min_valor, melhor_movimento

class JogoDaVelha:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Jogo da Velha")

        self.tabuleiro = criar_tabuleiro()
        self.jogador = 1  # Jogador humano sempre começa como "X"

        self.botoes = [[None for _ in range(3)] for _ in range(3)]
        self.criar_interface()

        self.janela.mainloop()



    def criar_interface(self):
        """Cria a interface gráfica do jogo."""
        for i in range(3):
            for j in range(3):
                self.botoes[i][j] = tk.Button(self.janela, text="", font=("Arial", 24), height=2, width=5,
                                              command=lambda x=i, y=j: self.jogada_humana(x, y))
                self.botoes[i][j].grid(row=i, column=j)

    def jogada_humana(self, linha, coluna):
        """Executa a jogada do jogador humano."""
        if self.tabuleiro[linha][coluna] == 0 and not jogo_finalizado(self.tabuleiro):
            self.tabuleiro[linha][coluna] = self.jogador
            self.atualizar_interface()

        if not jogo_finalizado(self.tabuleiro):
            self.jogador = -1  # Alterna para o jogador IA
            self.jogada_ia()



    def jogada_ia(self):
        """Executa a jogada da IA."""
        if not jogo_finalizado(self.tabuleiro) and self.jogador == -1:
            _, movimento = minimax(self.tabuleiro, 9, False, float('-inf'), float('inf'))
        if movimento:
            x, y = movimento
            self.tabuleiro[x][y] = self.jogador
            self.atualizar_interface()

        if not jogo_finalizado(self.tabuleiro):
            self.jogador = 1  # Alterna para o jogador humano
        else:
            self.fim_de_jogo()



    def atualizar_interface(self):
        """Atualiza a interface gráfica com o estado atual do tabuleiro."""
        simbolos = {0: "", 1: "X", -1: "O"}
        for i in range(3):
            for j in range(3):
                self.botoes[i][j].config(text=simbolos[self.tabuleiro[i][j]])

        if jogo_finalizado(self.tabuleiro):
            self.fim_de_jogo()


    def fim_de_jogo(self):
        """Exibe o resultado do jogo e pergunta se o jogador deseja reiniciar."""
        resultado = funcao_utilidade(self.tabuleiro)
        if resultado == 1:
            mensagem = "Você venceu! Parabéns!"
        elif resultado == -1:
            mensagem = "A IA venceu! Mais sorte na próxima vez."
        else:
            mensagem = "Empate!"

        # Pergunta ao jogador se deseja reiniciar
        if messagebox.askyesno("Fim de Jogo", f"{mensagem}\nDeseja jogar novamente?"):
            # Reinicia o estado do jogo
            self.tabuleiro = criar_tabuleiro()
            self.jogador = 1  # Sempre começa com o jogador humano
            self.atualizar_interface()
        else:
            self.janela.destroy()




if __name__ == "__main__":
    JogoDaVelha()
