import pygame, json, main, ui

from sys import exit

pygame.init()

def edit(file):
    json_data = json.loads(file.read())
    file.close()
      
    width, height = 720, 720
    screen = pygame.display.set_mode((width + 300, height))
    pygame.display.set_caption("Verlet Object Editor")

    cellSize = 20

    points  = json_data["points"]
    sticks  = json_data["sticks"]
    paths   = json_data["forms"]
    statics = json_data["statics"]
    data = {
        "points" : points,
        "sticks" : sticks,
        "forms"  : paths,
        "statics": statics
    }

    def click_point(x, y):
        for i, p in enumerate(points):
            if round(x/cellSize) == p[0] and round(y/cellSize) == p[1]:
                return i, p

    #ui
    clear_button    = ui.Button((240, 50), "red", "Clear")
    mode_button     = ui.Button((240, 50), "white", "Stick Mode")
    save_button     = ui.Button((240, 50), "green", "Save")
    simulate_button = ui.Button((240, 50), "yellow", "Simulate")

    new_stick = []
    new_path  = []
    
    stick_mode = False
    running = True

    while running:
        m_x = pygame.mouse.get_pos()[0] # get x value of mouse position
        m_y = pygame.mouse.get_pos()[1] # get y value of mouse position

        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()     
                exit()       
            # mouse down events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    # add points at mouse position on click
                    if stick_mode == False:
                        if m_x < width:
                            point = click_point(m_x, m_y)
                            
                            if point == None:   
                                points.append((round(m_x/cellSize), round(m_y/cellSize)))
                            elif point[0] not in statics:   
                                statics.append(point[0])  
                            else:   
                                statics.remove(point[0])
                                         
                    else:
                        # start creating new stick 
                        if click_point(m_x, m_y) != None:
                            new_stick.append(click_point(m_x, m_y)[0])

                if event.button == pygame.BUTTON_RIGHT:
                    # remove point on mouse click at mouse position of point exists
                    if stick_mode == False:
                        point = click_point(m_x, m_y)
                        if point != None:
                            for i, s in sorted(enumerate(sticks), reverse=True):
                                if s[0] == point[0] or s[1] == point[0]:
                                    sticks.pop(i)
                                    continue
                                if s[0] > point[0]:
                                    s[0] -= 1
                                if s[1] > point[0]:
                                    s[1] -= 1
                            for i, p in sorted(enumerate(paths), reverse=True):
                                if p[0] == point[0] or p[1] == point[0]:
                                    paths.pop(i)
                                    continue
                                if p[0] > point[0]:
                                    p[0] -= 1
                                if p[1] > point[0]:
                                    p[1] -= 1
                            for i in sorted(range(len(statics)), reverse=True):
                                if statics[i] == point[0]:
                                    statics.pop(i)
                                    continue
                                if statics[i] > point[0]:
                                    statics[i] -= 1
                            points.pop(point[0])
                    else:
                        # start creating new path 
                        if click_point(m_x, m_y) != None:
                            new_path.append(click_point(m_x, m_y)[0])
                # gui events
                if mode_button.rect.collidepoint(m_x, m_y):
                    mode_button.color = (128, 128, 128)
                if save_button.rect.collidepoint(m_x, m_y):
                    save_button.color = (0, 128, 0)
                if clear_button.rect.collidepoint(m_x, m_y):
                    clear_button.color = (128, 0, 0)
                if simulate_button.rect.collidepoint(m_x, m_y):
                    simulate_button.color = (128, 128, 0)



            # mouse up events
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    # gui events
                    if mode_button.rect.collidepoint(m_x, m_y):
                        stick_mode = not stick_mode
                        mode_button.color = (255, 255, 255)
                        if stick_mode:   mode_button.text = "Point Mode"
                        else:           mode_button.text = "Stick Mode"
                    if save_button.rect.collidepoint(m_x, m_y):
                        save_button.color = (0, 255, 0)
                        data = {
                            "points": points,
                            "sticks": sticks,
                            "forms": paths,
                            "statics" : statics
                        }
                        file = open(file_path, "w")
                        file.write(json.dumps(data, indent=4))
                        file.close()
                    if clear_button.rect.collidepoint(m_x, m_y):
                        clear_button.color = (255, 0, 0)
                        points = []
                        sticks = []
                        paths = []
                        statics = []
                    if simulate_button.rect.collidepoint(m_x, m_y):
                        simulate_button.color = (255, 255, 0)
                        main.main(open(file.name))
                        pygame.quit()     
                        exit()      
                        
                    if stick_mode:
                        point = click_point(m_x, m_y)
                        if len(new_stick) > 0 and point != points[new_stick[0]] and point != None:
                            new_stick.append(point[0])
                            sticks.append(new_stick)
                        new_stick = []
                if event.button == pygame.BUTTON_RIGHT:
                    if stick_mode:
                        point = click_point(m_x, m_y)
                        if len(new_path) > 0 and point != points[new_path[0]] and point != None:
                            new_path.append(point[0])
                            paths.append(new_path)
                        new_path = []
                            
        screen.fill((25, 25, 25))
        # draw grid
        for y in range(0, height, cellSize):
            for x in range(0, width, cellSize):
                rect = pygame.Rect((x, y),(cellSize, cellSize))
                pygame.draw.rect(screen, (125, 125, 125), rect, 1)       
        # draw sticks
        if len(new_stick) == 1:
            pygame.draw.line(screen, (255, 255, 255), (points[new_stick[0]][0] * cellSize, points[new_stick[0]][1] * cellSize), (m_x, m_y), 1)
        for s in sticks:
            val1 = s[0]
            val2 = s[1]
            pygame.draw.line(screen, (255, 255, 255), (points[val1][0]*cellSize, points[val1][1]*cellSize), (points[val2][0]*cellSize, points[val2][1]*cellSize), 2)
        # draw paths
        if len(new_path) == 1:
            pygame.draw.line(screen, (0, 255, 0), (points[new_path[0]][0] * cellSize, points[new_path[0]][1] * cellSize), (m_x, m_y), 1)
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
        mode_button.draw(screen, 870, 600)
        save_button.draw(screen, 870, 675)
        clear_button.draw(screen, 870, 525)
        simulate_button.draw(screen, 870, 50)

        pygame.display.update()
if __name__ == "__main__":
    file_path = ui.file_prompt()
    file = open(file_path)
    edit(file)
