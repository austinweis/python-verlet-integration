import json, pygame
import rag, editor, ui

pygame.init()

def main(file):
    # window properties
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Verlet Physics Simulation")
    screen_color = (25, 25, 25)
    screen.fill(screen_color)

    clock = pygame.time.Clock()
    scale = 20

    # gui objects
    menu_bar       = ui.Button((width, 20), (120, 120, 120))
    edit_button    = ui.Button((100, 20), (200, 200, 200), "Editor")

    friction_label = ui.Title((200, 200, 200), "friction")
    friction_input = ui.InputBox((100, 20), (200, 200, 200), str(rag.friction), True)
    gravity_label  = ui.Title((200, 200, 200), "gravity")
    gravity_input  = ui.InputBox((100, 20), (200, 200, 200), str(rag.gravity), True)
    bounce_label   = ui.Title((200, 200, 200), "bounce")
    bounce_input   = ui.InputBox((100, 20), (200, 200, 200), str(rag.bounce), True)
    rigidity_label = ui.Title((200, 200, 200), "rigidity")
    rigidity_input = ui.InputBox((100, 20), (200, 200, 200), str(rag.rigidity), True)

    # load ragdoll from json 
    json_data = json.loads(file.read())
    ragdoll = rag.Rag(json_data)
    file.close()

    mouse_point = None # point following mouse

    point_radius, stick_width = 5, 3

    def update_rag(rag, rigidity):
        rag.move_dynamic_points()
        for _ in range(rigidity):
            rag.update_sticks()
            rag.constrain_points((width/scale, height/scale))

    def draw_rag(rag):
        color = (255, 255, 255)
        for s in rag.sticks:
            p0 = rag.points[s[0]]
            p1 = rag.points[s[1]]
            pygame.draw.line(screen, color, (p0[0] * scale, p0[1] * scale), (p1[0] * scale, p1[1] * scale), stick_width)
        for i, p in enumerate(rag.points):
            if i in rag.statics:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.circle(screen, color, (p[0] * scale, p[1] * scale), point_radius)


    running = True
    while running:
        m_x = pygame.mouse.get_pos()[0] # get x value of mouse position
        m_y = pygame.mouse.get_pos()[1] # get y value of mouse position

        #gui
        screen.fill(screen_color)
        update_rag(ragdoll, int(rag.rigidity))
        draw_rag(ragdoll)
        menu_bar.draw(screen, width/2, menu_bar.rect.height/2)
        edit_button.draw(screen, edit_button.rect.width/2, edit_button.rect.height/2)

        friction_input.draw(screen, 200, gravity_input.rect.height/2)
        friction_label.draw(screen, 125, 10)
        gravity_input.draw(screen, 350, gravity_input.rect.height/2)
        gravity_label.draw(screen, 275, 10)
        bounce_input.draw(screen, 500, gravity_input.rect.height/2)
        bounce_label.draw(screen, 425, 10)
        rigidity_input.draw(screen, 650, gravity_input.rect.height/2)
        rigidity_label.draw(screen, 575, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, p in enumerate(ragdoll.points):
                    if round(p[0]) == round(m_x/scale) and round(p[1]) == round(m_y/scale):
                        mouse_point = i
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_point = None
                if event.button == pygame.BUTTON_LEFT:
                    if edit_button.rect.collidepoint(m_x, m_y):     
                        editor.edit(open(file.name))
                        pygame.quit()
                        exit()
            friction_input.handle_event(event)
            gravity_input.handle_event(event)
            bounce_input.handle_event(event)
            rigidity_input.handle_event(event)

            rag.friction = 0 if friction_input.text == '' else float(friction_input.text)
            rag.gravity  = 0 if gravity_input.text  == '' else float(gravity_input.text)
            rag.bounce   = 0 if bounce_input.text   == '' else float(bounce_input.text)
            rag.rigidity = 0 if rigidity_input.text == '' else int(rigidity_input.text)

        if mouse_point in ragdoll.statics:
            ragdoll.move_static_point(mouse_point, (m_x/scale, m_y/scale))
        elif mouse_point != None:
            ragdoll.points[mouse_point] = [m_x/scale, m_y/scale] * 2
            
        pygame.display.update()
        clock.tick(60)
        
if __name__ == '__main__':
    file = open(ui.file_prompt())
    main(file)