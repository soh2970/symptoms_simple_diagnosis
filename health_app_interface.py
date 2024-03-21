import pygame

class HealthAppInterface:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Health Diagnosis App')
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        self.done = False
        self.active = False
        self.input_box = pygame.Rect(300, 300, 600, 32)
        self.button_box_next = pygame.Rect(650, 550, 100, 40)
        self.button_box_exit = pygame.Rect(350, 550, 100, 40)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color_text = pygame.Color('white')
        self.color_button = pygame.Color('grey')
        self.text = ''
        self.user_data = {"name": "", "symptoms": ""}
        self.state = "welcome"
        self.predictions = []
        self.error_message = ""


    def welcome_screen(self):
        self.screen.fill((30, 30, 30))
        self.draw_text("Welcome!", (400, 250), self.font, center=True)
        self.draw_text("We hope to give you a quick analysis based on your current symptoms.", (400, 280), self.font, center=True)
        self.draw_button("Next", self.button_box_next)

    def profile_screen(self):
        self.screen.fill((30, 30, 30))
        self.draw_text("Please enter your name below.", (400, 250), self.font, center=True)
        self.draw_input_box("Name: " + self.text, self.error_message)
        self.draw_button("Next", self.button_box_next)

    def symptom_screen(self):
        self.screen.fill((30, 30, 30))
        greeting_text = f"I hope you are having a lovely day, {self.user_data['name']}."
        self.draw_text(greeting_text, (400, 200), self.font, center=True)
        self.draw_text("What are your symptoms today?", (400, 250), self.font, center=True)
        self.draw_input_box(self.text, self.error_message)
        self.draw_button("Next", self.button_box_next)

    def result_screen(self, data_class_instance):
        self.screen.fill((30, 30, 30))
        self.draw_text("This is your result:", (400, 200), self.font, center=True)
        self.draw_text("Remember to consult a doctor before proceeding with next steps.", (400, 450), self.font, center=True)
        self.draw_text("If this is an emergency, please dial 911.", (400, 500), self.font, center=True)


        if not self.predictions:
            self.predictions = data_class_instance.predict_illness(self.user_data['symptoms'])
        for i, (illness, confidence) in enumerate(self.predictions):
            self.draw_text(f"{i+1}. {illness}: {confidence*100:.2f}%", (400, 300 + i * 40), self.font, center=True)
        self.draw_button("Exit", self.button_box_exit)

    def draw_text(self, text, position, font, center=False):
        text_surface = font.render(text, True, self.color_text)
        rect = text_surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(text_surface, rect)

    def draw_input_box(self, text, error_message=""):
        txt_surface = self.font.render(text, True, self.color_active if self.active else self.color_inactive)
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(self.screen, self.color_active if self.active else self.color_inactive, self.input_box, 2)
        if error_message:
            error_surface = self.font.render(error_message, True, (255, 0, 0))  # Red color for the error message
            self.screen.blit(error_surface, (self.input_box.x-80, self.input_box.y +50))

    def draw_button(self, text, rect, is_exit=False):
        pygame.draw.rect(self.screen, self.color_button, rect)
        self.draw_text(text, rect.center, self.font, center=True)
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                if is_exit:
                    self.done = True
                else:
                    self.next_screen()

    def next_screen(self):
        if self.state == "welcome":
            self.state = "create_profile"
        elif self.state == "create_profile":
            if self.text.strip():  # Ensure name field is not empty
                self.user_data["name"] = self.text.strip()
                self.text = ''  # Clear the text for the next input
                self.error_message = ""  # Clear any previous error messages
                self.state = "symptoms"  # Transition to the symptom input screen
            else:
                self.error_message = "Please enter your name to continue."  # Set the error message if the name field is empty
        elif self.state == "symptoms":
            if self.text.strip():  # Ensure symptoms field is not empty
                self.user_data["symptoms"] = self.text.strip()
                self.text = ''  # Clear the text for the next input
                self.error_message = ""  # Clear any previous error messages
                self.state = "show_results"  # Transition to the results screen
            else:
                self.error_message = "Please enter your symptoms to continue."  # Set the error message if the symptoms field is empty

    def run(self, data_class_instance):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            if self.state == "create_profile":
                                self.user_data["name"] = self.text
                                self.text = ''
                                self.state = "symptoms"
                            elif self.state == "symptoms":
                                self.user_data["symptoms"] = self.text
                                self.text = ''
                                self.state = "show_results"
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    elif self.button_box_next.collidepoint(event.pos) and self.state != "show_results":
                        self.next_screen()
                    elif self.button_box_exit.collidepoint(event.pos) and self.state == "show_results":
                        self.done = True

            self.screen.fill((30, 30, 30))
            if self.state == "welcome":
                self.welcome_screen()
            elif self.state == "create_profile":
                self.profile_screen()
            elif self.state == "symptoms":
                self.symptom_screen()
            elif self.state == "show_results":
                self.result_screen(data_class_instance)

            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()
