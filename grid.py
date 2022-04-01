import cell

class Grid():
    HEIGHT = 40
    WIDTH = 40
    grid = []
    

    def __init__(self):
        row = []
        for i in range(self.WIDTH):
            row.append(cell.Cell())
        for j in range(self.HEIGHT):
            self.grid.append(row)