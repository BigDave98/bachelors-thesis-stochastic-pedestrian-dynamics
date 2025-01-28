import random
from collections import Counter


class Pedestrians:
    def __init__(self):
        self.info = []
        self.positions = []
        self.prefered_next_positions = []

    def solve_conflicts(self):
        conflict = True
        while conflict:
            # Verifica o numero de ocorrencias entre as posições que os pedestres serão atribuidos para verificar se existe mais de um pedestre querendo ir para a mesma casa, caso a soma seja maior que 1 indica um conflito
            self.positions = [pedestrian.position for pedestrian in self.info]
            self.prefered_next_positions = [pedestrian.prefered_next_position for pedestrian in self.info]

            counter = Counter(self.prefered_next_positions)

            # verifica se a soma das ocorrencias dos valores é igual ao numero de posições unicas, se não for significa que existem valores repetidos logo, ha conflitos
            if sum(counter.values()) != len(set(self.prefered_next_positions)):
                # Retorna as posições onde exitem mais de um pedestre querendo ir
                conflicts = [item for item, count in counter.items() if count > 1]

                # Retorna o index de onde estão os pedestres que querem ir para a mesma posição. Verifica uma a um se a posição preferida do pedestre esta na lista de conflitos, caso esteja atribui o valor a chave.
                # Em seguida pega os indexes das posições que estão em conflito e cria uma lista
                conflicts_index = {position: [idx for idx, pos in enumerate(self.prefered_next_positions) if pos == position]
                                   for position in conflicts}  # indices

                # Baseado nas posições que estão em conflito seleciona aleatoriamente um index para cada posição onde este selecionado é o que ira para a posição enquanto os outros permanecem no mesmo local, o index
                # selecionado corresponde ao index na lista 'prefered_next_position'
                random_pedestrian = {
                    position: [random.choices(value)[0] for key, value in conflicts_index.items() if key == position]
                    for position in conflicts_index}  # w

                # Conflict position corresponde as chaves do dicionario
                for key in conflicts_index:
                    # Seleciona a lista dos index, correspondetes as chaves, nas listas de conflitos e na lista do pedestre selcionado para cada posição conflitante, para em seguida remover o pedestre que foi selecionado
                    conflicts_index[key].remove(random_pedestrian[key][0])

                    # Em seguida itera sobre cada valor que ainda está na lista de conflitos atribuido o valor inicial.
                    for conflict_index in conflicts_index[key]:
                        self.info[conflict_index].prefered_next_position = self.info[conflict_index].position

                self.prefered_next_positions = [pedestrian.prefered_next_position for pedestrian in self.info]
            # Somente retorna que não há conflitos se a condição do if for falsa
            else:
                conflict = False


    #Função deve ser definida para a classe grid e não pedestre
    def update_pedestrians_info(self, dynamic_field, exits, grid):
        # Limpa posições antigas
        grid[tuple(zip(*[p.position for p in self.info]))] = 0

        positions_update_dynamic_field = [pedestrian.position for pedestrian in self.info
                                          if pedestrian.position != pedestrian.prefered_next_position]

        dynamic_field.update_dynamic_field(positions_update_dynamic_field)

        self.info = [p for p in self.info if p.prefered_next_position not in exits]

        for p in self.info:
            p.position = p.prefered_next_position

        if not self.info:
            grid[tuple(zip(*exits))] = 2
            return grid, dynamic_field

        new_positions = [p.position for p in self.info]
        grid[tuple(zip(*new_positions))] = 1
        grid[tuple(zip(*exits))] = 2


        return grid, dynamic_field




