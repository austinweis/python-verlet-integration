import pygame
import json
import os
import main

from sys import exit

pygame.init()
fileName = "object"

font = pygame.font.Font(None, 20)

width, height = 720, 720
cellSize = 20

screen = pygame.display.set_mode((width + 300, height))
pygame.display.set_caption("Verlet Object Editor")

points  = []
sticks  = []
paths   = []
statics = []

try:
    file = open(os.path.dirname(os.path.realpath(__file__)) + "/" + fileName+".rag", "r")
    file = json.loads(file.read())

    points = file["points"]
    sticks = file["sticks"]
    paths = file["forms"]
    statics = file["statics"]
except FileNotFoundError:
    print("File not found")

data = {
    "points": points,
    "sticks": sticks,
    "forms": paths,
    "statics" : statics
}

# clear button settings
clearButton = pygame.Rect((750, 500),(240, 50))
clearButtonColor = (255, 0, 0)
clearButtonText = "Clear"

# mode button settings
modeButton = pygame.Rect((750, 575),(240, 50))
modeButtonColor = (255, 255, 255)
modeButtonText = "Stick Mode"
stickMode = False

# save button settings
saveButton = pygame.Rect((750, 650),(240, 50))
saveButtonColor = (0, 255, 0)
saveButtonText = "Save"

# simulation button settings
simulationButton = pygame.Rect((750, 50),(240, 50))
simulationButtonColor = (255, 255, 0)
simulationButtonText = "Start Simulation"

newStick = []
newPath  = []
running = True
while running:
    # get mouse position
    mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

    # get user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()     
            exit()       
        # mouse down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # add points at mouse position on click, if mouse position is on grid
                if stickMode == False:
                    if mouseX < width:
                        _newPoint = True
                        for i in range(len(points)): 
                            if round(mouseX/cellSize) == points[i][0] and round(mouseY/cellSize) == points[i][1]:
                                _static = False
                                for j in statics:
                                    if j == i:
                                        _static = True
                                if _static:
                                    statics.remove(i)
                                else:
                                    statics.append(i)
                                _newPoint = False
                        if _newPoint == True:   points.append((round(mouseX/cellSize), round(mouseY/cellSize)))
                else:
                    # start creating new stick 
                    for i in range(len(points)):
                        if round(mouseX/cellSize) == points[i][0] and round(mouseY/cellSize) == points[i][1]:
                            newStick.append(i)

            if event.button == pygame.BUTTON_RIGHT:
                # remove point on mouse click at mouse position of point exists
                if stickMode == False:
                    for i in range(len(points)): 
                        if round(mouseX/cellSize) == points[i][0] and round(mouseY/cellSize) == points[i][1]:
                            s = len(sticks)
                            while s > 0:
                                s-=1
                                if sticks[s][0] == i or sticks[s][1] == i:
                                    sticks.remove(sticks[s])
                                    continue
                                if sticks[s][0] > i:
                                    sticks[s][0] -= 1
                                if sticks[s][1] > i:
                                    sticks[s][1] -= 1
                            s = len(paths)
                            while s > 0:
                                s-=1
                                if paths[s][0] == i or paths[s][1] == i:
                                    paths.remove(paths[s])
                                    continue
                                if paths[s][0] > i:
                                    paths[s][0] -= 1
                                if paths[s][1] > i:
                                    paths[s][1] -= 1
                            points.remove(points[i])
                            p = len(statics)
                            while p > 0:
                                p-=1
                                if statics[p] == i:  
                                    statics.remove(i)
                                    continue
                                if statics[p] > i: 
                                    statics[p] -= 1      
                            break
    
                else:
                    # start creating new path 
                    for i in range(len(points)):
                        if round(mouseX/cellSize) == points[i][0] and round(mouseY/cellSize) == points[i][1]:
                            newPath.append(i)
            # gui events
            if modeButton.collidepoint(mouseX, mouseY):
                modeButtonColor = (128, 128, 128)
            if saveButton.collidepoint(mouseX, mouseY):
                saveButtonColor = (0, 128, 0)
            if clearButton.collidepoint(mouseX, mouseY):
                clearButtonColor = (128, 0, 0)
            if simulationButton.collidepoint(mouseX, mouseY):
                simulationButtonColor = (128, 128, 0)



        # mouse up events
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                # gui events
                if modeButton.collidepoint(mouseX, mouseY):
                    stickMode = not stickMode
                    modeButtonColor = (255, 255, 255)
                    if stickMode:   modeButtonText = "Point Mode"
                    else:   modeButtonText = "Stick Mode"
                if saveButton.collidepoint(mouseX, mouseY):
                    saveButtonColor = (0, 255, 0)
                    data = {
                        "points": points,
                        "sticks": sticks,
                        "forms": paths,
                        "statics" : statics
                    }

                    file = open(os.path.dirname(os.path.realpath(__file__))+ "/" + fileName + ".rag", "w")
                    file.write(json.dumps(data, indent=4))
                    file.close()
                if clearButton.collidepoint(mouseX, mouseY):
                    clearButtonColor = (255, 0, 0)
                    points = []
                    sticks = []
                    paths = []
                    statics = []
                if simulationButton.collidepoint(mouseX, mouseY):
                    simulationButtonColor = (255, 255, 0)
                    main.main()
                    pygame.quit()     
                    exit()      
                    
                if stickMode == False:
                    pass
                else:
                    for i in range(len(points)): 
                        if round(mouseX/cellSize) == points[i][0] and round(mouseY/cellSize) == points[i][1]:
                            if len(newStick) > 0:
                                if points[i] != points[newStick[0]]:
                                    newStick.append(i)
                                    sticks.append(newStick)
                    newStick = []
            if event.button == pygame.BUTTON_RIGHT:
                if stickMode == False:
                    pass
                else:
                    for i in range(len(points)): 
                        if round(mouseX/cellSize) == points[i][0] and round(mouseY/cellSize) == points[i][1]:
                            if len(newPath) > 0:
                                if points[i] != points[newPath[0]]:
                                    newPath.append(i)
                                    paths.append(newPath)
                    newPath = []
                        



    screen.fill((25, 25, 25))
    # draw grid
    for y in range(0, height, cellSize):
        for x in range(0, width, cellSize):
            rect = pygame.Rect((x, y),(cellSize, cellSize))
            pygame.draw.rect(screen, (125, 125, 125), rect, 1)
    
    # draw sticks
    if len(newStick) == 1:
        pygame.draw.line(screen, (255, 255, 255), (points[newStick[0]][0] * cellSize, points[newStick[0]][1] * cellSize), (mouseX, mouseY), 1)
    for s in sticks:
        val1 = s[0]
        val2 = s[1]
        pygame.draw.line(screen, (255, 255, 255), (points[val1][0]*cellSize, points[val1][1]*cellSize), (points[val2][0]*cellSize, points[val2][1]*cellSize), 2)
    # draw paths
    if len(newPath) == 1:
        pygame.draw.line(screen, (0, 255, 0), (points[newPath[0]][0] * cellSize, points[newPath[0]][1] * cellSize), (mouseX, mouseY), 1)
    for s in paths:
        val1 = s[0]
        val2 = s[1]
        pygame.draw.line(screen, (0, 255, 0), (points[val1][0]*cellSize, points[val1][1]*cellSize), (points[val2][0]*cellSize, points[val2][1]*cellSize), 1)
    # draw points
    for i in range(len(points)):
        _color = (255, 255, 255)
        for p in statics:
            if p == i:
                _color = (255, 0, 0)
        pygame.draw.circle(screen, _color, (points[i][0] * cellSize, points[i][1] * cellSize), 5)

    # draw gui
    textSurface = font.render(modeButtonText, True, (0, 0, 0))
    pygame.draw.rect(screen, modeButtonColor, modeButton)
    screen.blit(textSurface, (modeButton.centerx - textSurface.get_width()/2, modeButton.centery - textSurface.get_height()/2))

    textSurface = font.render(saveButtonText, True, (0, 0, 0))
    pygame.draw.rect(screen, saveButtonColor, saveButton)
    screen.blit(textSurface, (saveButton.centerx - textSurface.get_width()/2, saveButton.centery - textSurface.get_height()/2))

    textSurface = font.render(clearButtonText, True, (0, 0, 0))
    pygame.draw.rect(screen, clearButtonColor, clearButton)
    screen.blit(textSurface, (clearButton.centerx - textSurface.get_width()/2, clearButton.centery - textSurface.get_height()/2))

    textSurface = font.render(simulationButtonText, True, (0, 0, 0))
    pygame.draw.rect(screen, simulationButtonColor, simulationButton)
    screen.blit(textSurface, (simulationButton.centerx - textSurface.get_width()/2, simulationButton.centery - textSurface.get_height()/2))

    pygame.display.update()