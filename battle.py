import random
import time

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
    
    def printStack(self):
        for e in self.items:
            print(e, end="->")
        print()

class HistoricoAcoes:
    def __init__(self):
        self.pilha = Stack()

    def registrar(self, acao):
        self.pilha.push(acao)

    def mostrar_ultimas(self, n=5):
        temp = []
        size = self.pilha.size()
        for _ in range(min(n, size)):
            temp.append(self.pilha.pop())
        print("\n📜 Últimas ações:")
        for acao in temp:
            print("•", acao)
        for acao in reversed(temp):
            self.pilha.push(acao)

class Personagem:
    def __init__(self, nome, hp, ataque, defesa, esquiva=0.2):
        self.nome = nome
        self.hp_max = hp
        self.hp = hp
        self.ataque = ataque
        self.defesa = defesa
        self.defendendo = False
        self.esquiva = esquiva

    def atacar(self, alvo, historico=None):
        if self.defendendo:
            print(f"{self.nome} parou de defender para atacar.")
            if historico:
                historico.registrar(f"{self.nome} parou de defender para atacar.")
            self.defendendo = False

        dano_bruto = random.randint(int(self.ataque * 0.8), int(self.ataque * 1.2))
        
        if random.random() < 0.2:
            print(f"⚡ {self.nome} fez um ataque CRÍTICO!")
            dano_bruto = int(dano_bruto * 1.5)

        dano_real = max(1, dano_bruto - alvo.defesa)

        print(f"⚔️ {self.nome} ataca {alvo.nome}!")
        time.sleep(1)

        if alvo.defendendo:
            print(f"{alvo.nome} está defendendo e reduz o dano!")
            dano_real = max(1, int(dano_real / 2)) 
            alvo.defendendo = False 

        if random.random() < alvo.esquiva:
            print(f"🌀 {alvo.nome} esquiva o ataque de {self.nome}!")
            if historico:
                historico.registrar(f"{alvo.nome} esquivou o ataque de {self.nome}.")
            return

        alvo.receber_dano(dano_real)
        if historico:
            historico.registrar(f"{self.nome} causou {dano_real} de dano em {alvo.nome}.")

    def receber_dano(self, dano):
        self.hp -= dano
        print(f"💔 {self.nome} recebe {dano} de dano! HP restante: {max(0, self.hp)}")
        time.sleep(1)
        if self.hp <= 0:
            print(f"💀 {self.nome} foi derrotado!")

    def defender(self, historico=None):
        print(f"🛡️ {self.nome} está se preparando para defender o próximo ataque.")
        self.defendendo = True
        time.sleep(1)
        if historico:
            historico.registrar(f"{self.nome} se defendeu.")

    def usar_pocao(self, cura, historico=None):
        if self.defendendo:
            self.defendendo = False
        self.hp = min(self.hp_max, self.hp + cura)
        print(f"💖 {self.nome} usa uma poção e cura {cura} de HP! HP atual: {self.hp}")
        time.sleep(1)
        if historico:
            historico.registrar(f"{self.nome} usou uma poção e curou {cura} de HP.")

    def esta_vivo(self):
        return self.hp > 0

class NoDecisao:
    def __init__(self, condicao=None, acao=None, ramo_verdadeiro=None, ramo_falso=None):
        self.condicao = condicao
        self.acao = acao
        self.ramo_verdadeiro = ramo_verdadeiro
        self.ramo_falso = ramo_falso

    def decidir(self, inimigo, jogador):
        if self.acao:
            return self.acao
        if self.condicao(inimigo, jogador):
            return self.ramo_verdadeiro.decidir(inimigo, jogador)
        else:
            return self.ramo_falso.decidir(inimigo, jogador)

class Inimigo:
    def __init__(self, nome, hp, ataque, defesa, esquiva=0.2):
        self.personagem = Personagem(nome, hp, ataque, defesa, esquiva)
        self.pocoes = 1
        self.arvore_decisao = self._construir_arvore()

    def _construir_arvore(self):
        acao_atacar = NoDecisao(acao="atacar")
        acao_defender = NoDecisao(acao="defender")
        acao_usar_pocao = NoDecisao(acao="usar_pocao")

        def condicao_hp_baixo(inimigo, jogador):
            return inimigo.personagem.hp < (inimigo.personagem.hp_max * 0.3) and inimigo.pocoes > 0

        def condicao_jogador_defendendo(inimigo, jogador):
            return jogador.defendendo

        no_jogador_defendendo = NoDecisao(
            condicao=condicao_jogador_defendendo,
            ramo_verdadeiro=acao_defender, 
            ramo_falso=acao_atacar        
        )

        raiz = NoDecisao(
            condicao=condicao_hp_baixo,
            ramo_verdadeiro=acao_usar_pocao, 
            ramo_falso=no_jogador_defendendo 
        )

        return raiz

    def escolher_acao(self, jogador, historico):
        acao_escolhida = self.arvore_decisao.decidir(self, jogador)

        print(f"\nTurno de {self.personagem.nome}...")
        time.sleep(1)

        if acao_escolhida == "atacar":
            self.personagem.atacar(jogador, historico)
        elif acao_escolhida == "defender":
            self.personagem.defender(historico)
        elif acao_escolhida == "usar_pocao":
            self.personagem.usar_pocao(30, historico)
            self.pocoes -= 1

class Jogador:
    def __init__(self, nome, hp, ataque, defesa):
        self.personagem = Personagem(nome, hp, ataque, defesa)
        self.pocoes = 2

    def escolher_acao(self, inimigo, historico):
        print("\n--- Seu Turno ---")
        print("Escolha sua ação:")
        print("1. Atacar")
        print("2. Defender")
        print(f"3. Usar Poção ({self.pocoes} restantes)")

        escolha = ""
        while escolha not in ["1", "2", "3"]:
            escolha = input("Digite o número da sua escolha: ")

        if escolha == "1":
            self.personagem.atacar(inimigo.personagem, historico)
        elif escolha == "2":
            self.personagem.defender(historico)
        elif escolha == "3":
            if self.pocoes > 0:
                self.personagem.usar_pocao(40, historico)
                self.pocoes -= 1
            else:
                print("Você não tem mais poções! Ação perdida.")
                time.sleep(1)
                historico.registrar(f"{self.personagem.nome} tentou usar poção, mas não tinha mais.")

jogador = Jogador(nome="Herói", hp=100, ataque=20, defesa=10)
inimigo = Inimigo(nome="Goblin", hp=80, ataque=15, defesa=8)
historico = HistoricoAcoes()

print("✨ Era uma vez...")
time.sleep(0.5)
print("Nas terras distantes de Crystallum, um reino próspero cercado por cristais mágicos e florestas encantadas, a paz reinava há séculos.")
time.sleep(0.5)
print("Povos viviam em harmonia, guiados por reis sábios e protegidos por antigos feitiços de luz.")
time.sleep(0.5)
print("Mas toda luz gera sombra.")
time.sleep(0.5)
print("Das profundezas da Caverna Obscura, um ser emergiu: um Goblin de olhos flamejantes, alimentado por ódio antigo e magias esquecidas.")
time.sleep(0.5)
print("Com ele, vieram as trevas, os campos murcharam, e o medo se espalhou como uma praga.")
time.sleep(0.5)
print("Os anciãos previram esse dia, mas a esperança estava distante... até agora.")
time.sleep(0.5)
print("Após anos de preparação, um jovem guerreiro ergue-se entre os mortais.")
time.sleep(0.5)
print("Forjado na disciplina, treinado em honra e armado com a espada de prata ancestral, ele carrega o nome da última esperança de Crystallum: o Herói Escolhido.")
time.sleep(1)
print("As trombetas soam.")
time.sleep(1)
print("Os cristais tremem.")
time.sleep(1)
print("O destino se aproxima.")
time.sleep(1)
print("Sob o céu tempestuoso e o rugido do trovão, o Herói encara o Goblin pela primeira vez.")
time.sleep(0.5)
print("Não há palavras. Apenas o silêncio tenso antes da batalha.")
time.sleep(0.5)
print("⚔️ E assim, começa nossa jornada...")
time.sleep(0.5)
print("🎮 O RPG se inicia...")
time.sleep(0.5)
print("🔥 A batalha entre o Herói e o Goblin vai começar!\n")
time.sleep(1)
print("=" * 50)
print(">>> PREPARE-SE PARA A BATALHA <<<")
print("=" * 50)

print(f"{jogador.personagem.nome} VS {inimigo.personagem.nome}\n")

turno = 1
while jogador.personagem.esta_vivo() and inimigo.personagem.esta_vivo():
    print(f"--- Rodada {turno} ---")
    print(f"HP {jogador.personagem.nome}: {jogador.personagem.hp}/{jogador.personagem.hp_max} | HP {inimigo.personagem.nome}: {inimigo.personagem.hp}/{inimigo.personagem.hp_max}")

    jogador.escolher_acao(inimigo, historico)

    if not inimigo.personagem.esta_vivo():
        break

    inimigo.escolher_acao(jogador.personagem, historico)

    historico.mostrar_ultimas()
    print("-" * 30)
    turno += 1

print("\n--- FIM DA BATALHA ---")
if jogador.personagem.esta_vivo():
    print(f"🎉 Parabéns, {jogador.personagem.nome}! Você venceu!")
else:
    print(f"😞 Você foi derrotado pelo {inimigo.personagem.nome}.")