import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *

# Musica
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("audio/sw.mp3")

pygame.mixer.music.play(-1)

width = 1000
height = 1000

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

model_files = ["modelos/UFO.obj", "modelos/nave.obj", "modelos/nave1.obj", "modelos/rocket.obj"]
current_model_index = 0

rend.setShader(vertexShader=general_vertex_shader, fragmentShader=rainbow_fragment_shader)

models = [Model(file) for file in model_files]

for model in models:
    model.loadTexture("texturas/lavita.jpg")
    model.position.z = -5.5
    model.scale = glm.vec3(2, 2, 2)
    model.rotation.x = 45

rend.scene.append(models[current_model_index])

isRunning = True
mouse_dragging = False
last_mouse_position = (0, 0)

while isRunning:
    deltaTime = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False


            # Cambia el modelo y shader al presionar teclas z, x, c, v
            if event.key == pygame.K_z:
                current_model_index = 0
            elif event.key == pygame.K_x:
                current_model_index = 1
            elif event.key == pygame.K_c:
                current_model_index = 2
            elif event.key == pygame.K_v:
                current_model_index = 3

            rend.scene = [models[current_model_index]]  

            if event.key == pygame.K_1:
                rend.setShader(vertexShader=general_vertex_shader, fragmentShader=rainbow_fragment_shader)
            elif event.key == pygame.K_2:
                rend.setShader(vertexShader=general_vertex_shader, fragmentShader=dalmata_fragment_shader)
            elif event.key == pygame.K_3:
                rend.setShader(vertexShader=general_vertex_shader, fragmentShader=waves_fragment_shader)
            elif event.key == pygame.K_4:
                rend.setShader(vertexShader=general_vertex_shader, fragmentShader=discoBall_fragment_shader)

        # Inicio de la rotación del modelo con el mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_dragging = True
                last_mouse_position = pygame.mouse.get_pos()

        # Fin de la rotación del modelo con el mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                mouse_dragging = False

        # Movimiento del mouse para rotar todos los modelos
        elif event.type == pygame.MOUSEMOTION:
            if mouse_dragging:
                mouse_position = pygame.mouse.get_pos()
                dx = mouse_position[0] - last_mouse_position[0]
                dy = mouse_position[1] - last_mouse_position[1]

                for model in models:
                    model.rotation.y += dx * 0.2
                    model.rotation.x += dy * 0.2

                last_mouse_position = mouse_position


    # Movimientos de la cámara
    if keys[K_d]:
        rend.camPosition.x = max(rend.camPosition.x - 5 * deltaTime, -width/2 + 50)

    if keys[K_a]:
        rend.camPosition.x = min(rend.camPosition.x + 5 * deltaTime, width/2 - 50)

    if keys[K_w]:
        rend.camPosition.y = max(rend.camPosition.y - 5 * deltaTime, -height/2 + 50)

    if keys[K_s]:
        rend.camPosition.y = min(rend.camPosition.y + 5 * deltaTime, height/2 - 50)

    if keys[K_q]:
        rend.camPosition.z -= 5 * deltaTime

    if keys[K_e]:
        rend.camPosition.z += 5 * deltaTime

    # Limitar movimiento de objetos
    for model in rend.scene:
        model.position.x = max(min(model.position.x, width/2 - 50), -width/2 + 50)
        model.position.y = max(min(model.position.y, height/2 - 50), -height/2 + 50)

    rend.elapsedTime += deltaTime
    rend.render()

    pygame.display.flip()

pygame.quit()
