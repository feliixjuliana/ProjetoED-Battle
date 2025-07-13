import random
import time

class Personagem:
    def __init__(self, nome, hp, ataque, defesa):
        self.nome = nome
        self.hp_max = hp
        self.hp = hp
        self.ataque = ataque
        self.defesa = defesa
        self.defendendo = False

    def atacar(self, alvo):
        if self.defendendo:
            print(f"{self.nome} parou de defender para atacar.")
            self.defendendo = False

        dano_bruto = random.randint(int(self.ataque * 0.8), int(self.ataque * 1.2))
        dano_real = max(1, dano_bruto - alvo.defesa)

        print(f"⚔️ {self.nome} ataca {alvo.nome}!")
        time.sleep(1)

        if alvo.defendendo:
            print(f"{alvo.nome} está defendendo e reduz o dano!")
            dano_real = max(1, int(dano_real / 2)) 
            alvo.defendendo = False 

        alvo.receber_dano(dano_real)

    def receber_dano(self, dano):
        self.hp -= dano
        print(f"💔 {self.nome} recebe {dano} de dano! HP restante: {max(0, self.hp)}")
        time.sleep(1)
        if self.hp <= 0:
            print(f"💀 {self.nome} foi derrotado!")

    def defender(self):
        print(f"🛡️ {self.nome} está se preparando para defender o próximo ataque.")
        self.defendendo = True
        time.sleep(1)

    def usar_pocao(self, cura):
        if self.defendendo:
            self.defendendo = False
        self.hp = min(self.hp_max, self.hp + cura)
        print(f"💖 {self.nome} usa uma poção e cura {cura} de HP! HP atual: {self.hp}")
        time.sleep(1)

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
        
class Inimigo(Personagem):
    def __init__(self, nome, hp, ataque, defesa):
        super().__init__(nome, hp, ataque, defesa)
        self.pocoes = 1
        self.arvore_decisao = self._construir_arvore()

    def _construir_arvore(self):
        acao_atacar = NoDecisao(acao="atacar")
        acao_defender = NoDecisao(acao="defender")
        acao_usar_pocao = NoDecisao(acao="usar_pocao")

        def condicao_hp_baixo(inimigo, jogador):
            return inimigo.hp < (inimigo.hp_max * 0.3) and inimigo.pocoes > 0

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

    def escolher_acao(self, jogador):
        acao_escolhida = self.arvore_decisao.decidir(self, jogador)
        
        print(f"\nTurno de {self.nome}...")
        time.sleep(1)

        if acao_escolhida == "atacar":
            self.atacar(jogador)
        elif acao_escolhida == "defender":
            self.defender()
        elif acao_escolhida == "usar_pocao":
            self.usar_pocao(30) 
            self.pocoes -= 1

class Jogador(Personagem):
    def __init__(self, nome, hp, ataque, defesa):
        super().__init__(nome, hp, ataque, defesa)
        self.pocoes = 2

    def escolher_acao(self, inimigo):
        print("\n--- Seu Turno ---")
        print("Escolha sua ação:")
        print("1. Atacar")
        print("2. Defender")
        print(f"3. Usar Poção ({self.pocoes} restantes)")
        
        escolha = ""
        while escolha not in ["1", "2", "3"]:
            escolha = input("Digite o número da sua escolha: ")

        if escolha == "1":
            self.atacar(inimigo)
        elif escolha == "2":
            self.defender()
        elif escolha == "3":
            if self.pocoes > 0:
                self.usar_pocao(40) 
                self.pocoes -= 1
            else:
                print("Você não tem mais poções! Ação perdida.")
                time.sleep(1)


def main():
    jogador = Jogador(nome="Herói", hp=100, ataque=20, defesa=10)
    inimigo = Inimigo(nome="Goblin", hp=80, ataque=15, defesa=8)

    print("--- INÍCIO DA BATALHA ---")
    print(f"{jogador.nome} VS {inimigo.nome}\n")

    turno = 1
    while jogador.esta_vivo() and inimigo.esta_vivo():
        print(f"--- Rodada {turno} ---")
        print(f"HP {jogador.nome}: {jogador.hp}/{jogador.hp_max} | HP {inimigo.nome}: {inimigo.hp}/{inimigo.hp_max}")
        
        jogador.escolher_acao(inimigo)

        if not inimigo.esta_vivo():
            break
            
        inimigo.escolher_acao(jogador)
        
        print("-" * 20)
        turno += 1

    print("\n--- FIM DA BATALHA ---")
    if jogador.esta_vivo():
        print(f"🎉 Parabéns, {jogador.nome}! Você venceu!")
    else:
        print(f"😞 Você foi derrotado pelo {inimigo.nome}.")

if __name__ == "__main__":
    main()