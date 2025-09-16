import pygame, sys, math

# --- Init ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Simulation")
clock = pygame.time.Clock()

# --- Colors ---
BLACK = (0, 0 ,0)
RED   = (200, 50, 50)
GREEN   = (50, 200, 50)
WHITE = (255, 255, 255)
CAR_COLOR = WHITE

ground_y = 400
ampl = 30
k = 1/100
phase = 0
wave_speed = 200
points = [(x, ground_y + ampl*math.sin(k*x)) for x in range(WIDTH)]
print(points)
wheel_radius = 15
wheel_ang_front = 0
wheel_ang_rear = 0
car_w, car_h = 100, 60
car_x, car_y = WIDTH // 2, ground_y - wheel_radius*2 - car_h


vel = 0 # velocity : px/s
acc = 50000 # acceleration : px/s^2
damping = 0.99 # damping value
brake = 0.85 # braking value

def f(x): (math.sin(x/2)) * 50 + 400

def draw_curve(screen, color, f, x0, x1):
    y_prev = f(x0)
    for x in range(x0 + 1, x1):
        y = f(x)
        pygame.draw.aaline(screen, color, (x - 1, y_prev), (x, y))
        y_prev = y

x = 0
# --- Main loop ---
while True:
    x += 1
    dt = clock.tick(60) / 1000 # 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    a = 0
    is_braking = False
    # --- Keys ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: a -= acc * dt
    if keys[pygame.K_RIGHT]: a += acc * dt
    if keys[pygame.K_SPACE]: is_braking = True

    # car motion
    vel += a * dt
    if is_braking: vel *= brake 
    else: vel *= damping
    # car_x += vel * dt
    phase += vel * dt

    # screen boundaries
    # if car_x < 0: car_x = 0
    # if car_x + car_w > WIDTH: car_x = WIDTH - car_w

    # wheel pos
    wheel_front_cx = car_x+car_w/2/2
    wheel_front_cy = car_y+car_h+wheel_radius
    wheel_rear_cx = car_x+car_w/2+car_w/2/2
    wheel_rear_cy = car_y+car_h+wheel_radius

    # wheel rotation : ω = vel / rad
    wheel_ang_front += vel / wheel_radius * dt
    wheel_ang_rear += vel / wheel_radius * dt
    
    # spoke angle
    dx1 = math.cos(wheel_ang_front) * (wheel_radius - 2)
    dy1 = math.sin(wheel_ang_front) * (wheel_radius - 2)
    dx2 = math.cos(wheel_ang_front + math.pi/2) * (wheel_radius - 2)
    dy2 = math.sin(wheel_ang_front + math.pi/2) * (wheel_radius - 2)

    # front lines : A1-A2 & B1-B2
    A1 = (wheel_front_cx - dx1, wheel_front_cy - dy1) 
    A2 = (wheel_front_cx + dx1, wheel_front_cy + dy1)
    B1 = (wheel_front_cx - dx2, wheel_front_cy - dy2) 
    B2 = (wheel_front_cx + dx2, wheel_front_cy + dy2)
    # rear lines : C1-C2 & D1-D2
    C1 = (wheel_rear_cx - dx1, wheel_rear_cy - dy1) 
    C2 = (wheel_rear_cx + dx1, wheel_rear_cy + dy1)
    D1 = (wheel_rear_cx - dx2, wheel_rear_cy - dy2) 
    D2 = (wheel_rear_cx + dx2, wheel_rear_cy + dy2)

    # phase += wave_speed * dt
    points = [(x, ground_y + ampl*math.sin(k*(x + phase))) for x in range(WIDTH)]

    # --- Draw ---
    screen.fill(BLACK)
    # car
    pygame.draw.rect(screen, CAR_COLOR, (car_x, car_y, car_w, car_h), 1) # rect
    # wheel 1
    pygame.draw.circle(screen, CAR_COLOR, (wheel_front_cx, wheel_front_cy), wheel_radius, 1)
    pygame.draw.line(screen, RED, A1, A2, 1)
    pygame.draw.line(screen, RED, B1, B2, 1)
    # wheel 2
    pygame.draw.circle(screen, CAR_COLOR, (wheel_rear_cx, wheel_front_cy), wheel_radius, 1)
    pygame.draw.line(screen, RED, C1, C2, 1)
    pygame.draw.line(screen, RED, D1, D2, 1)
    # ground
    pygame.draw.aalines(screen, GREEN, False, points, 1)
    # draw_curve(screen, GREEN, f, 0, WIDTH)
    # pygame.draw.line(screen, GREEN, (0, ground_y), (WIDTH, ground_y), 1)
    # display
    pygame.display.flip()
