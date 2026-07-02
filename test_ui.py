# test_ui.py
import pygame
import sys
from ui.ui_manager import UIManager

def test_ui():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("UI Manager Test")
    clock = pygame.time.Clock()
    
    ui_manager = UIManager(800, 600)
    ui_manager.set_tool("line")
    ui_manager.select_color_by_name("Red")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    ui_manager.toggle_help()
                elif event.key == pygame.K_c:
                    ui_manager.clear_canvas()
                elif event.key == pygame.K_1:
                    ui_manager.select_color_by_name("Red")
                elif event.key == pygame.K_2:
                    ui_manager.select_color_by_name("Green")
                elif event.key == pygame.K_3:
                    ui_manager.select_color_by_name("Blue")
                elif event.key == pygame.K_l:
                    ui_manager.set_tool("line")
                elif event.key == pygame.K_p:
                    ui_manager.set_tool("polyline")
                elif event.key == pygame.K_g:
                    ui_manager.set_tool("polygon")
                elif event.key == pygame.K_s:
                    ui_manager.set_tool("selection")
        
        screen.fill((50, 50, 50))
        ui_manager.update(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_ui()