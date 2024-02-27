import random

class Game():
    
    def __init__(self):
        self.logo = """
        ███╗   ███╗██╗███╗   ██╗███████╗███████╗██╗    ██╗███████╗███████╗██████╗ ███████╗██████╗ 
        ████╗ ████║██║████╗  ██║██╔════╝██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗
        ██╔████╔██║██║██╔██╗ ██║█████╗  ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗  ██████╔╝
        ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
        ██║ ╚═╝ ██║██║██║ ╚████║███████╗███████║╚███╔███╔╝███████╗███████╗██║     ███████╗██║  ██║
        ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                
        """
        print(self.logo)
        self.height = int(input("Digite o número de linhas desejado (de 5 a 20): "))
        self.width = int(input("Digite o número de colunas desejado (de 5 a 25): "))
        self.total_bombs = int(input("Digite o número de bombas desejado (de 1 a 50): "))
        self.field = Field(self.height, self.width, self.total_bombs)
        self.won = False
        self.lost = False
        while not (self.won or self.lost):
            self.play_round()
        self.display_end()


    def play_round(self):
        self.field.show_field()
        move = input("Digite R para revelar uma casa e M para marcá-la: ").upper()
        line = int(input("Digite o número da linha da casa: "))-1
        col = ord(input("Digite a letra da coluna da casa: ").upper())-ord('A')
        
        if move == 'R':
            if self.field.field[line][col].val == 'X':
                self.lost = True
                return
            self.field.reveal_spot(line, col)

        if move == 'M':
            self.field.flag_spot(line, col)
        
        if self.field.size - self.field.amount_revealed == self.total_bombs:
            self.won = True


    def display_end(self):
        self.field.show_field(final=True)
        print("Você ganhou!" if self.won else "Você Perdeu")


class Spot():
    def __init__(self, val=' ', revealed=False, flagged=False):
        self.val = val
        self.revealed = revealed
        self.flagged = flagged


class Field():
    def __init__(self, height, width, total_bombs):
        self.height = height
        self.width = width
        self.size = self.height*self.width
        self.total_bombs = total_bombs
        self.amount_revealed = 0
        self.set_field()
        
        
    def set_field(self):
        self.field = [[Spot() for j in range(self.width)] for i in range(self.height)]
        self.bomb_locations = random.sample(range(0,self.size), self.total_bombs)

        for bomb_index in self.bomb_locations:
            line = bomb_index//self.width
            col = bomb_index%self.width
            self.field[line][col].val = 'X'
            for i in range(max(0,line-1), min(self.height,line+2)):
                for j in range(max(0,col-1), min(self.width, col+2)):
                    if self.field[i][j].val.isdigit():
                        self.field[i][j].val = str(int(self.field[i][j].val)+1)
                    elif self.field[i][j].val == ' ':
                        self.field[i][j].val = '1'

           
    def show_field(self, final=False):
        print('\nTabuleiro atual: ')
        print('\n   |', *[chr(ord('A')+i) for i in range(self.width)])
        print(' —'*(self.width+2))
        for i in range(self.height):
            if i < 9: print(' ', end='')
            print(str(i+1),'|', end=" ")
            for spot in self.field[i]:
                if spot.revealed or final == True:
                    print(spot.val, end=' ')
                elif spot.flagged:
                    print('⚑', end= ' ')
                else:
                    print('▪', end=' ')
            print('\n')


    def reveal_spot(self, line, col):
        spot = self.field[line][col]
        if spot.revealed:
            return
        spot.revealed = True
        self.amount_revealed += 1

        if spot.val == ' ':
            if line+1 < self.height and self.field[line+1][col].val != 'X':
                self.reveal_spot(line+1, col)
            if line-1 >= 0 and self.field[line-1][col].val != 'X':
                self.reveal_spot(line-1, col)
            if col+1 < self.width and self.field[line][col+1].val != 'X':
                self.reveal_spot(line, col+1)
            if col-1 >= 0 and self.field[line][col-1].val != 'X':
                self.reveal_spot(line, col-1)

    
    def flag_spot(self, line, col):
        spot = self.field[line][col]
        if spot.revealed:
            print("Esta casa já foi revelada!")
        else:
            spot.flagged = True
            

if __name__ == '__main__':
    new_game = Game()


# Redundância de nome field field
# tentar repartir em pequenas subfunções
# reler sobre getters e setters, vários acessos ficaram estranhos
# verificar se as entradas do usuário são válidas
# mudar lógica de revelar casas vazias
# longo prazo: ranking, interface gráfica
    