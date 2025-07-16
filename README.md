# 🛡️ Battle Game

Battle Game é um projeto de RPG de batalha em Python, desenvolvido como trabalho da segunda unidade da disciplina de **Estrutura de Dados**. O jogo simula um combate entre um herói e um goblin, utilizando estruturas como **pilha** e **árvore de decisão** para representar a memória de ações e a inteligência artificial do inimigo.

## 👥 Integrantes

* Danilo Humberto
* Juliana Felix
* Sérgio de Castro

## ✅ Descrição do Problema Resolvido

O projeto resolve o desafio de implementar um sistema de jogo baseado em turnos, com tomada de decisões automatizada para o inimigo e registro das ações do jogador. O objetivo era aplicar estruturas de dados estudadas em sala — especialmente árvores e pilhas — em um projeto prático.

---

## 🎯 Justificativa da Escolha do Tema

Escolhemos desenvolver um jogo de RPG por turnos pois ele nos permitia explorar diversos conceitos de forma prática, assim como nos desafiar tanto na lógica, como na estrutura de código, por exemplo:

* Fluxo de ações condicionais.
* Registro e exibição de histórico.
* Simulação de uma "inteligência artificial" simples para o inimigo.
  Além disso, é um tema atrativo, didático e fácil de expandir futuramente.

---

## 🕹️ História

O reino de **Crystallum** está sendo ameaçado por um Goblin. Após anos de preparação, um guerreiro finalmente está pronto para o confronto. Assim começa a batalha final entre o **Herói** e o **Goblin**.

---
## 🖥️ Execução

Para executar o jogo:

```bash
git clone https://github.com/feliixjuliana/ProjetoED-Battle.git
```

```bash
cd ProjetoED-Battle
```

```bash
python battle_game.py
```

---

## 🧠 Desafios Enfrentados e Soluções

* **Desafio:** Construção da árvore de decisão com ramificações lógicas funcionais.
  **Solução:** Criamos a classe `NoDecisao` com atributos `condição`, `ação`, `ramo_verdadeiro` e `ramo_falso`, facilitando a montagem de decisões condicionais e reutilização da lógica.

* **Desafio:** Integrar as decisões da IA ao fluxo do jogo sem travar a jogabilidade.
  **Solução:** O método `decidir()` dentro da árvore retorna a ação a ser tomada, e o inimigo executa com base nesse retorno, mantendo o jogo fluido.

* **Desafio:** Registro eficiente de ações.
  **Solução:** Utilização da `Stack` para registrar e imprimir as últimas ações a cada turno.

---

## 📚 Aprendizados

Este projeto foi importante para colocar em prática:

* A construção de árvores de decisão com POO.
* O uso de pilhas para memória de ações.
* A criação de um loop de jogo com entrada do usuário e controle de turnos.

---

## 🏁 Resultado

O jogo termina quando um dos personagens (Herói ou Goblin) tem o HP zerado. Uma mensagem final indica o vencedor.

