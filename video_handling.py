
import cv2
import pygame
import os
from pygame.locals import *
from text_rendering import draw_text

def play_video(screen, video_path, img_path, font_large, font_small, infoObject, img_width=400, img_height=300):
    cap = cv2.VideoCapture(video_path)
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Load and scale image
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (img_width, img_height))

    running = True
    while running and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            video_height, video_width = frame.shape[:2]
            scale = screen_height / video_height
            resized_frame = cv2.resize(frame, (int(video_width * scale), screen_height))
            
            if resized_frame.shape[1] > screen_width:
                crop_x = (resized_frame.shape[1] - screen_width) // 2
                resized_frame = resized_frame[:, crop_x:crop_x+screen_width]
                
            frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame, (0, 0))
            
            # Draw the PNG image over the video frame
            screen.blit(image, ((screen_width - 400) / 2, (screen_height - 300) / 2))
            
            # Redraw the overlay and text to ensure they stay on top
            draw_text(screen, font_large, font_small, infoObject)
            
            pygame.display.update()
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                cap.release()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    cap.release()
                    return