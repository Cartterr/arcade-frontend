
import pygame
import os
import glob
from pygame.locals import *
from animations import animate_elements
from utils import ico_to_surface, extract_icon, get_target_exe_path_lnk, get_target_exe_path_url, extract_icon_from_exe
import subprocess
import webbrowser

class InitialUI:
    def __init__(self, screen, original_img_path, pressed_img_paths, position, size, base_y):
        self.screen = screen
        self.original_image = pygame.image.load(original_img_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)
        self.pressed_images = {
            "left": pygame.image.load(pressed_img_paths["left"]).convert_alpha(),
            "right": pygame.image.load(pressed_img_paths["right"]).convert_alpha()
        }
        self.base_position = position
        self.position = position
        self.base_y = base_y
        self.size = size
        self.current_image = self.original_image
        self.alpha = 255
        self.fade_out = False
        self.keep_faded = False

    def switch_to_pressed(self, direction):
        self.current_image = pygame.transform.scale(self.pressed_images[direction], self.size)
        self.fade_out = True
        self.keep_faded = True

    def update(self):
        # Vertical animation
        y_offset = animate_elements(0)  # Assuming 0 as starting point for simplicity
        self.position = (self.base_position[0], self.base_y + y_offset)

        if self.fade_out and self.alpha > 0:
            self.alpha -= 5  # Adjust fading speed as necessary
            if self.alpha <= 0:
                # Once faded, do not automatically reset to original image
                self.alpha = 0

    def draw(self):
        temp_image = self.current_image.copy()
        temp_image.set_alpha(self.alpha)
        self.screen.blit(temp_image, self.position)

    def reset(self):
        # Resets the image to its original state and stops the fade out
        self.current_image = self.original_image
        self.alpha = 255
        self.fade_out = False
        self.keep_faded = False



class ShortcutsUI:
    def __init__(self, screen, ui_background_path, shortcuts_folder):
        self.screen = screen
        self.background = pygame.image.load(ui_background_path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (screen.get_width() / 1.5, screen.get_height() / 1.5))
        self.shortcuts_folder = shortcuts_folder
        self.shortcuts = []
        self.scroll_offset = 0
        self.load_shortcuts()

        self.selection_row = 0
        self.selection_col = 0
        self.max_rows = 0  # Will be calculated
        self.max_cols = 7  # Fixed number of columns

        self.max_visible_rows = 3
        self.back_button_selected = False

    
    
    def update_selection(self, dx, dy):
        # Handling the selection when moving left to the "go back" icon
        if dx < 0 and self.selection_col == 0 and not self.back_button_selected:
            self.back_button_selected = True
        # Handling the selection when moving right from the "go back" icon to the grid
        elif dx > 0 and self.back_button_selected:
            self.back_button_selected = False
            self.selection_col = 0  # Reset to the first column in the grid
        # Regular grid navigation
        elif not self.back_button_selected:
            if dx != 0:  # Left/right navigation
                self.selection_col = max(0, min(self.selection_col + dx, self.max_cols - 1))
            if dy != 0:  # Up/down navigation
                # Ensure up/down navigation is confined to the grid
                self.selection_row = max(0, min(self.selection_row + dy, (len(self.shortcuts) - 1) // self.max_cols))



    def draw_selection(self):
        if not self.shortcuts or self.back_button_selected:
            return
        # Now directly use the stored attributes
        x = self.start_x + self.selection_col * (self.icon_size + self.x_padding)
        y = self.start_y + self.selection_row * (self.icon_size + self.y_padding) - self.scroll_offset
        # Draw the selection ring
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x + self.icon_size / 2), int(y + self.icon_size / 2)), int(self.icon_size / 2) + 5, 2)

    def load_shortcuts(self):
        """Load shortcuts from the specified folder, handling .lnk and .url files."""
        for shortcut_path in glob.glob(os.path.join(self.shortcuts_folder, '*')):
            print(f"Loading shortcut: {shortcut_path}")
            shortcut_name = os.path.splitext(os.path.basename(shortcut_path))[0]  # Get the name without extension

            icon_surface = None  # Initialize icon_surface to None for each shortcut

            if shortcut_path.endswith('.lnk'):
                print("Shortcut is a .lnk file")
                # target_path = get_target_exe_path_lnk(shortcut_path)
                # # Assuming the icon can be directly extracted from the target .exe
                # if os.path.exists(target_path):
                #     print(f"Extracting icon from {target_path}")    
                #     icon_surface = extract_icon_from_exe(target_path)
                icon_surface = pygame.image.load('assets/gamepad.png').convert_alpha()
                    
            if shortcut_path.endswith('.url'):
                # If the shortcut is a .url file, use the default "gamepad.png" icon
                print(f"Using default icon for: {shortcut_name}")
                icon_surface = pygame.image.load('assets/gamepad.png').convert_alpha()

            if icon_surface:
                self.shortcuts.append((icon_surface, shortcut_name, shortcut_path))  # Append a tuple of icon_surface and shortcut_name



    def update_scroll(self, scroll_amount):
        """Updates the scroll offset based on user input or another mechanism."""
        self.scroll_offset += scroll_amount

    def format_name(self, name, max_length=15):
        """Formats the name to include line breaks for better display."""
        # Split the name into words
        words = name.split()
        formatted_name = ""
        current_line = ""
        for word in words:
            # Check if adding the next word exceeds the max length
            if len(current_line + word) > max_length:
                # Add a line break if the current line + word exceeds max length
                formatted_name += (current_line + "\n").lstrip()
                current_line = word + " "
            else:
                current_line += word + " "
        # Add the last line
        formatted_name += current_line.strip()
        return formatted_name

    def execute_selected_shortcut(self):
        if not self.shortcuts or self.back_button_selected:
            return

        # Get the path of the selected shortcut
        idx = self.selection_row * self.max_cols + self.selection_col
        if idx < len(self.shortcuts):
            _, _, shortcut_path = self.shortcuts[idx]
            
            if shortcut_path.endswith('.url'):
                # For .url files, open the default web browser
                webbrowser.open(shortcut_path)
            else:
                # For other shortcuts, attempt to run them directly
                subprocess.Popen(['cmd', '/c', shortcut_path], shell=True)

    def draw(self):
        # Calculate and store positions and sizes as instance attributes
        self.bg_x = (self.screen.get_width() - self.background.get_width()) // 2
        self.bg_y = (self.screen.get_height() - self.background.get_height()) // 2
        self.start_x = self.bg_x + 85
        self.start_y = self.bg_y + 180
        self.icon_size = 64 * 1.25
        self.x_padding = 90
        self.y_padding = 100

        # Calculate the top left position to center the background
        bg_x = (self.screen.get_width() - self.background.get_width()) // 2
        bg_y = (self.screen.get_height() - self.background.get_height()) // 2

        # Draw the UI background centered
        self.screen.blit(self.background, (self.bg_x, self.bg_y))

        font = pygame.font.Font(None, 24)  # Adjust font size as needed.

        # Define the visible area for icons.
        visible_area_start_y = self.start_y
        visible_area_end_y = self.start_y + self.max_visible_rows * (self.icon_size + self.y_padding) - self.y_padding

        # Update the scroll offset based on the selection to ensure the selected icon is visible.
        if self.selection_row >= self.max_visible_rows:
            self.scroll_offset = (self.selection_row - self.max_visible_rows + 1) * (self.icon_size + self.y_padding)
        elif self.selection_row < (self.scroll_offset // (self.icon_size + self.y_padding)):
            self.scroll_offset = max(0, self.selection_row * (self.icon_size + self.y_padding))

        # Ensure the scroll offset does not exceed the content height.
        total_content_height = (len(self.shortcuts) // self.max_cols + 1) * (self.icon_size + self.y_padding)
        self.scroll_offset = min(self.scroll_offset, total_content_height - visible_area_end_y + visible_area_start_y)

        # Load and scale the back icon
        back_icon = pygame.image.load('assets/go-back.png').convert_alpha()
        back_icon_scaled = pygame.transform.scale(back_icon, (110, 110))  # Adjust size as needed
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        middle_x = screen_width // 2
        back_icon_position_x = middle_x - back_icon_scaled.get_width() // 2 - 680  # Adjust the 100 pixels to position it further to the left as needed
        back_icon_position_y = screen_height // 2 - back_icon_scaled.get_height() // 2 - 280
        self.screen.blit(back_icon_scaled, (back_icon_position_x, back_icon_position_y))


        if self.back_button_selected:
            pygame.draw.circle(self.screen, (255, 255, 255), (back_icon_position_x + 55, back_icon_position_y + 55), 60, 2)

        for idx, (icon_surface, name, path) in enumerate(self.shortcuts):
            column = idx % self.max_cols
            row = idx // self.max_cols

            x = self.start_x + column * (self.icon_size + self.x_padding)
            y = self.start_y + row * (self.icon_size + self.y_padding) - self.scroll_offset

            # Draw the icon if it's within the visible area.
            if visible_area_start_y <= y < visible_area_end_y:
                self.screen.blit(pygame.transform.scale(icon_surface, (self.icon_size, self.icon_size)), (x, y))

                formatted_name = self.format_name(name)
                name_y = y + self.icon_size + 5  # Offset for name below the icon.
                for line in formatted_name.split('\n'):
                    line_surface = font.render(line, True, (255, 255, 255))
                    line_x = x + (self.icon_size - line_surface.get_width()) / 2
                    self.screen.blit(line_surface, (line_x, name_y))
                    name_y += line_surface.get_height()

        self.draw_selection()