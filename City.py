import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances_argmin_min
import Building


def getDistance(vec1, vec2):
    return np.linalg.norm(vec1 - vec2)


class City:

    ConcentricCircle = 0
    Sector = 1
    MultipleNucleus = 2

    CentralizedFF = 0
    DispersedFF = 1

    def __init__(self, layoutType, citySize=100):
        self.citySize = citySize
        self.layoutType = layoutType
        self.layout = []
        self.buildLayout()
        self.fireStations = []
        self.buildFireStations()

    def buildLayout(self):
        if self.layoutType == City.ConcentricCircle:
            self.buildConcentricCircleLayout()
        elif self.layoutType == City.Sector:
            self.buildSectorLayout()
        elif self.layoutType == City.MultipleNucleus:
            self.buildMultiNucleusLayout()
        else:
            self.buildConcentricCircleLayout()

    def buildConcentricCircleLayout(self):
        halfSize = self.citySize / 2
        center = np.asarray([self.citySize / 2, self.citySize / 2])
        for i in range(self.citySize):
            self.layout.append([])
            for j in range(self.citySize):
                point = np.asarray([i, j])
                dis = getDistance(point, center)
                if dis < halfSize / 3:
                    self.layout[i].append(Building.CommercialBuilding(i, j))
                elif halfSize / 3 <= dis < halfSize * 2 / 3:
                    self.layout[i].append(Building.ResidentialBuilding(i, j))
                else:
                    self.layout[i].append(Building.IndustrialBuilding(i, j))

    def buildSectorLayout(self):
        halfSize = self.citySize / 2
        axisX = np.asarray([1, 0])
        for i in range(self.citySize):
            self.layout.append([])
            for j in range(self.citySize):
                vec = np.asarray([i, j]) - np.asarray([halfSize, halfSize])
                cos = vec.dot(axisX) / max(np.linalg.norm(vec), 0.1)
                angle = np.arccos(cos)*180/np.pi
                if (0 <= angle < 60 and j < halfSize) or (120 <= angle <= 180 and j >= halfSize):
                    self.layout[i].append(Building.ResidentialBuilding(i, j))
                elif 60 <= angle < 120:
                    self.layout[i].append(Building.CommercialBuilding(i, j))
                elif (0 <= angle < 60 and j >= halfSize) or (120 <= angle <= 180 and j < halfSize):
                    self.layout[i].append(Building.IndustrialBuilding(i, j))
                else:
                    self.layout[i].append(Building.Building(i, j))

    def buildMultiNucleusLayout(self):
        halfSize = self.citySize / 2
        commercialCenter = np.asarray([[halfSize/2, halfSize/2],
                                       [halfSize, halfSize],
                                       [self.citySize - halfSize / 2, self.citySize - halfSize / 5]])
        industrialCenter = np.asarray([[self.citySize - halfSize / 2, halfSize / 2],
                                       [halfSize / 3, self.citySize - halfSize / 3],
                                       [self.citySize - halfSize / 3, self.citySize - halfSize / 3]])
        for i in range(self.citySize):
            self.layout.append([])
            for j in range(self.citySize):
                point = np.asarray([i, j])
                if getDistance(point, commercialCenter[0]) < 10 \
                        or getDistance(point, commercialCenter[1]) < 20 \
                        or getDistance(point, commercialCenter[2]) < 10:
                    self.layout[i].append(Building.CommercialBuilding(i, j))
                elif getDistance(point, industrialCenter[0]) < 10 \
                        or getDistance(point, industrialCenter[1]) < 35 \
                        or getDistance(point, industrialCenter[2]) < 15:
                    self.layout[i].append(Building.IndustrialBuilding(i, j))
                else:
                    self.layout[i].append(Building.ResidentialBuilding(i, j))

    def getW(self):
        wShot = np.zeros([self.citySize, self.citySize])
        for i in range(self.citySize):
            for j in range(self.citySize):
                wShot[i][j] = self.layout[i][j].w
        return wShot

    def getD(self):
        dShot = np.zeros([self.citySize, self.citySize])
        for i in range(self.citySize):
            for j in range(self.citySize):
                dShot[i][j] = self.layout[i][j].d
        return dShot

    def getT(self):
        tShot = np.zeros([self.citySize, self.citySize])
        for i in range(self.citySize):
            for j in range(self.citySize):
                tShot[i][j] = self.layout[i][j].t
        return tShot

    def show(self):
        plt.figure()
        plt.subplot(2, 2, 1)
        self.drawT()
        plt.subplot(2, 2, 2)
        self.drawW()
        plt.subplot(2, 2, 3)
        self.drawD()
        plt.show()

    def drawW(self):
        wShot = self.getW()
        plt.imshow(wShot, cmap='turbo', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.colorbar()
        plt.title('Risk(wij) Distribution')

    def drawD(self):
        dShot = self.getD()
        plt.imshow(dShot, cmap='coolwarm', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.colorbar()
        plt.title('Distance(dij) Distribution')

    def drawT(self):
        tShot = self.getT()
        plt.imshow(tShot, cmap='rainbow', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        # plt.colorbar()
        plt.title('Layout Distribution')

    def buildFireStations(self):
        self.fireStations.append([self.citySize/2, self.citySize/2])
        self.update()

    def update(self):
        buildings = []
        for row in self.layout:
            for building in row:
                buildings.append([building.x, building.y])

        nearestIndexList, nearestDisList = pairwise_distances_argmin_min(buildings, self.fireStations)
        for i in range(len(nearestIndexList)):
            x = buildings[i][0]
            y = buildings[i][1]
            self.layout[x][y].setDistance(nearestDisList[i])


if __name__ == "__main__":
    # city1 = City(City.Sector)
    # city1.show()

    # city2 = City(City.ConcentricCircle)
    # city2.show()

    # w = city1.getW()  # np.array
    # d = city1.getD()  # np.array
    city3 = City(City.MultipleNucleus)
    city3.show()

