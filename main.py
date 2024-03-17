import pygame
import os
from pygame.locals import *
import cv2
from init import init_pygame
from fonts import load_fonts
from animations import animate_elements
from text_rendering import draw_text, draw_text_with_border
from particles import ParticleSystem, RotatingRingParticleSystem
from controls import SelectionController
from ui import InitialUI, ShortcutsUI


def main():
    current_state = "main_menu"
    screen, infoObject = init_pygame()
    font_large, font_small = load_fonts()
    video_path = 'assets/vaporwave.mp4'
    img_path = 'assets/button-base.png'
    img_width, img_height = 400 * 2.5, 300 * 2.5
    pressed_img_paths = {
        "left": 'assets/button-base-left-press.png',
        "right": 'assets/button-base-right-press.png'
    }
    shortcuts_folder = {
        "student_games_shortcuts_ui": "D:/student-games",
        "normal_games_shortcuts_ui": "D:/normal-games"
    }
    

    # Example of setting up the UI based on the current state
    if current_state == "student_games_shortcuts_ui":
        shortcuts_ui = ShortcutsUI(screen, 'assets/main-ui.png', shortcuts_folder["student_games_shortcuts_ui"])
    elif current_state == "normal_games_shortcuts_ui":
        shortcuts_ui = ShortcutsUI(screen, 'assets/main-ui.png', shortcuts_folder["normal_games_shortcuts_ui"])

    # Create a Clock object
    clock = pygame.time.Clock()

    # Load and scale image
    image = pygame.image.load(img_path)
    img_width, img_height = 400*2.5, 300*2.5  # Parameterized values for scaling
    image = pygame.transform.scale(image, (img_width, img_height))

    

    # Initialize the RingParticleSystem for both buttons
    ring_particle_system_left = RotatingRingParticleSystem(screen, (infoObject.current_w // 4 + 225, infoObject.current_h // 2 - 20 ), radius=140)
    ring_particle_system_right = RotatingRingParticleSystem(screen, (3 * infoObject.current_w // 4 - 225, infoObject.current_h // 2 - 20), radius=140)

    cap = cv2.VideoCapture(video_path)
    screen_width, screen_height = pygame.display.get_surface().get_size()

    particle_system = ParticleSystem(screen, (infoObject.current_w // 2, infoObject.current_h // 2), num_particles=80) 

    selection_controller = SelectionController()


    button_position = (screen_width / 2 - img_width / 2, screen_height / 2 - img_height / 2)  # Adjust as necessary
    # This should be your button's vertical base position before any animation
    base_y_position = screen_height / 2 - img_height / 2
    # Adjust the instantiation of InitialUI
    fading_image = InitialUI(screen, img_path, pressed_img_paths, button_position, (int(img_width), int(img_height)), base_y_position)

    shortcuts_ui = None
    
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Process and display video frame
        video_height, video_width = frame.shape[:2]
        scale = screen_height / video_height
        resized_frame = cv2.resize(frame, (int(video_width * scale), screen_height))
        if resized_frame.shape[1] > screen_width:
            crop_x = (resized_frame.shape[1] - screen_width) // 2
            resized_frame = resized_frame[:, crop_x:crop_x+screen_width]
        frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame, (0, 0))

        if fading_image.fade_out:
            ring_particle_system_left.set_visibility(False)
            ring_particle_system_right.set_visibility(False)
            draw_text_visible = False
        else:
            ring_particle_system_left.set_visibility(True)
            ring_particle_system_right.set_visibility(True)
            draw_text_visible = True

        # Update and draw particles BEFORE drawing the PNG and text
        particle_system.emit()  # Generate new particles
        particle_system.update()
        particle_system.draw()

        if current_state == "main_menu":
            # Update and draw the fading image
            fading_image.update()
            fading_image.draw()

            text_y_offset = animate_elements(0)  # Animated y offset for text
            draw_text(screen, font_large, font_small, infoObject, text_y_offset, draw_text_visible)

            if selection_controller.get_selected() == 0:
                # Only activate the left particle system if the left option is selected
                ring_particle_system_left.emit()
                ring_particle_system_left.update()
                ring_particle_system_left.draw()
            else:
                # Only activate the right particle system if the right option is selected
                ring_particle_system_right.emit()
                ring_particle_system_right.update()
                ring_particle_system_right.draw()

        if (current_state in ["student_games_shortcuts_ui", "normal_games_shortcuts_ui"]) and not shortcuts_ui:
            shortcuts_ui = ShortcutsUI(screen, 'assets/main-ui.png', shortcuts_folder[current_state])

        

        if shortcuts_ui:
            shortcuts_ui.draw()
            draw_text_with_border(screen, font_large, 'DCCARCADE', 
                          (infoObject.current_w / 2 - font_large.size('DCCARCADE')[0] / 2, 220 + text_y_offset), 
                          pygame.Color('white'), pygame.Color('black'), 5)


        pygame.display.flip()
        clock.tick(120)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Inside your event loop
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if current_state == "main_menu":
                    if event.key == pygame.K_LEFT:
                        selection_controller.move_left()
                    elif event.key == pygame.K_RIGHT:
                        selection_controller.move_right()
                    elif event.key == pygame.K_SPACE:
                        direction = "left" if selection_controller.get_selected() == 0 else "right"
                        current_state = "student_games_shortcuts_ui" if selection_controller.get_selected() == 0 else "normal_games_shortcuts_ui"
                        fading_image.fade_out = True

                if current_state in ["student_games_shortcuts_ui", "normal_games_shortcuts_ui"]:
                    if event.key == pygame.K_UP:
                        shortcuts_ui.update_selection(0, -1)
                    elif event.key == pygame.K_DOWN:
                        shortcuts_ui.update_selection(0, 1)
                    elif event.key == pygame.K_LEFT:
                        shortcuts_ui.update_selection(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        shortcuts_ui.update_selection(1, 0)
                    elif event.key == pygame.K_BACKSPACE:
                        current_state = "main_menu"
                        shortcuts_ui = None
                    
                    if shortcuts_ui:
                        if event.key == pygame.K_SPACE and shortcuts_ui:
                            if shortcuts_ui.back_button_selected:
                                # Handling for back button already provided
                                current_state = "main_menu"
                                fading_image.fade_out = False
                                shortcuts_ui = None
                            else:
                                # Here, execute the selected shortcut
                                shortcuts_ui.execute_selected_shortcut()


    cap.release()  # Release the video filec
    pygame.quit()


if __name__ == "__main__":
    main()
