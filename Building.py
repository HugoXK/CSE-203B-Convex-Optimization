import numpy as np


class Building:
    BUILDING = -1
    RESIDENTIAL_BUILDING = 0
    COMMERCIAL_BUILDING = 1
    INDUSTRIAL_BUILDING = 2

    dijMax = 10000

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 0.0
        self.d = Building.dijMax
        self.t = Building.BUILDING

    def getDistance(self, building):
        return np.linalg.norm(np.asarray([self.x, self.y]) - np.asarray([building.x, building.y]))

    def setDistance(self, distance):
        self.d = distance


class ResidentialBuilding(Building):
    wMean = 0.25
    wVar = 0.25
    wMax = 0.5
    wMin = 0.0

    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.t = Building.RESIDENTIAL_BUILDING
        self.w = max(min(np.random.normal(ResidentialBuilding.wMean, ResidentialBuilding.wVar),
                         ResidentialBuilding.wMax),
                     ResidentialBuilding.wMin)


class CommercialBuilding(Building):
    wMean = 0.5
    wVar = 0.25
    wMax = 0.75
    wMin = 0.25

    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.t = Building.COMMERCIAL_BUILDING
        self.w = max(min(np.random.normal(CommercialBuilding.wMean, CommercialBuilding.wVar),
                         CommercialBuilding.wMax),
                     CommercialBuilding.wMin)


class IndustrialBuilding(Building):
    wMean = 0.75
    wVar = 0.25
    wMax = 1.0
    wMin = 0.5

    def __init__(self, x, y):
        Building.__init__(self, x, y)
        self.t = Building.INDUSTRIAL_BUILDING
        self.w = max(min(np.random.normal(IndustrialBuilding.wMean, IndustrialBuilding.wVar),
                         IndustrialBuilding.wMax),
                     IndustrialBuilding.wMin)
