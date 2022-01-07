import pygame


class Enemy:
    def __init__(self, frame_width, frame_height, animation_row, num_frames, speed):
        self.frames = []
        sprite_sheet = pygame.image.load('skeleton_sheet.png').convert_alpha()

        for frame_number in range(0, num_frames):
            self.frames.append(sprite_sheet.subsurface(pygame.Rect(frame_number * frame_width,
                                                                   animation_row * frame_height,
                                                                   frame_width, frame_height)))

        self.current_frame_index = 0
        self.display_frame = self.frames[self.current_frame_index]
        self.speed = speed
        self.time_accumulator = 0.0

    def update(self, time_passed):  # put time passed as time_delta when calling update function
        self.time_accumulator += time_passed

        if self.time_accumulator > self.speed:
            self.time_accumulator = 0.0
            self.current_frame_index += 1

            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

            self.display_frame = self.frames[self.current_frame_index]


my_anim_2 = Enemy(64, 64, 1, 9, 0.1)



