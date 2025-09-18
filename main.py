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
SPOKE_COLOR = RED

ground_y = 400
ampl = 30
k = 50
phase = 0
wave_speed = 200
points = [(x, ground_y + ampl*math.sin((1/k)*x)) for x in range(WIDTH)]

wheel_radius = 15
wheel_ang_front = 0
wheel_ang_rear = 0
car_w, car_h = 100, 40
car_x, car_y = WIDTH // 2, ground_y - wheel_radius*2 - car_h

vel = 0 # velocity : px/s
acc = 5000 # acceleration : px/s^2
brake = 0.85 # braking value

def f(x): (math.sin(x/2)) * 50 + 400

def draw_curve(screen, color, f, x0, x1):
    y_prev = f(x0)
    for x in range(x0 + 1, x1):
        y = f(x)
        pygame.draw.aaline(screen, color, (x - 1, y_prev), (x, y))
        y_prev = y

# text
font = pygame.font.SysFont("Arial", 25)
k_txt_surf = font.render(f"k : 1/{k}", True, WHITE)
k_txt_rect = k_txt_surf.get_rect(center=(WIDTH*0.7, 50))

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
    if keys[pygame.K_ESCAPE]: break
    if keys[pygame.K_UP]: 
        k += 1
        k_txt_surf = font.render(f"k : 1/{k}", True, (255, 255, 255))
        k_txt_rect = k_txt_surf.get_rect(center=(WIDTH*0.7, 50))
    if keys[pygame.K_DOWN]: 
        k -= 1
        if k < 1: k = 1
        k_txt_surf = font.render(f"k : 1/{k}", True, (255, 255, 255))
        k_txt_rect = k_txt_surf.get_rect(center=(WIDTH*0.7, 50))
    if keys[pygame.K_LEFT]: a -= acc * dt
    if keys[pygame.K_RIGHT]: a += acc * dt
    if keys[pygame.K_SPACE]: is_braking = True

    # car motion
    vel += a * dt
    if is_braking:
        vel *= brake
        if abs(vel) < 5: vel = 0
    vel = round(vel)
    phase += vel * dt
    
    # text
    vel_txt_surf = font.render(f"vel : {abs(vel)}", True, WHITE)
    vel_txt_rect = k_txt_surf.get_rect(center=(WIDTH*0.3, 50))

    # wheel pos
    wheel_front_cx = car_x+car_w/2/2
    wheel_front_cy = car_y+car_h+wheel_radius
    wheel_rear_cx = car_x+car_w/2+car_w/2/2
    wheel_rear_cy = car_y+car_h+wheel_radius

    # wheels on ground
    wheel_front_cy = points[int(wheel_front_cx)][1] - wheel_radius
    wheel_rear_cy = points[int(wheel_rear_cx)][1] - wheel_radius

    # wheel rotation : ω = vel / rad
    wheel_ang_front += vel / wheel_radius * dt
    wheel_ang_rear += vel / wheel_radius * dt
    
    # spoke angle
    dx1 = math.cos(wheel_ang_front) * (wheel_radius - 2)
    dy1 = math.sin(wheel_ang_front) * (wheel_radius - 2)
    dx2 = math.cos(wheel_ang_front + math.pi/3) * (wheel_radius - 2)
    dy2 = math.sin(wheel_ang_front + math.pi/3) * (wheel_radius - 2)
    dx3 = math.cos(wheel_ang_front - math.pi/3) * (wheel_radius - 2)
    dy3 = math.sin(wheel_ang_front - math.pi/3) * (wheel_radius - 2)

    # front lines
    F11 = (wheel_front_cx - dx1, wheel_front_cy - dy1) 
    F12 = (wheel_front_cx + dx1, wheel_front_cy + dy1)
    F21 = (wheel_front_cx - dx2, wheel_front_cy - dy2) 
    F22 = (wheel_front_cx + dx2, wheel_front_cy + dy2)
    F31 = (wheel_front_cx - dx3, wheel_front_cy - dy3) 
    F32 = (wheel_front_cx + dx3, wheel_front_cy + dy3)
    # rear lines
    R11 = (wheel_rear_cx - dx1, wheel_rear_cy - dy1) 
    R12 = (wheel_rear_cx + dx1, wheel_rear_cy + dy1)
    R21 = (wheel_rear_cx - dx2, wheel_rear_cy - dy2) 
    R22 = (wheel_rear_cx + dx2, wheel_rear_cy + dy2)
    R31 = (wheel_rear_cx - dx3, wheel_rear_cy - dy3) 
    R32 = (wheel_rear_cx + dx3, wheel_rear_cy + dy3)

    # phase += wave_speed * dt
    points = [(x, ground_y + ampl*math.sin((1/k)*(x + phase))) for x in range(WIDTH)]

    # --- Draw ---
    screen.fill(BLACK)
    # car
    ang = math.atan((wheel_rear_cy - wheel_front_cy) / car_w)
    x0, y0 = wheel_rear_cx+wheel_radius, wheel_rear_cy-wheel_radius
    x1, y1 = wheel_front_cx-wheel_radius, wheel_front_cy-wheel_radius
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx/L, dy/L
    nx, ny = -uy, ux
    d_offset = car_h    # blue length (px), distance from gray to red
    L_red    = L   # red length (px)
    t_along  = 0
    Sx = x0 + ux*t_along + nx*d_offset
    Sy = y0 + uy*t_along + ny*d_offset
    Ex = Sx + ux*L_red
    Ey = Sy + uy*L_red
    x2, y2 = int(Ex), int(Ey)
    x3, y3 = int(Sx), int(Sy)
    car_points = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0)]
    pygame.draw.lines(screen, WHITE, False, car_points, 1)
    # wheel 1
    pygame.draw.circle(screen, CAR_COLOR, (wheel_front_cx, wheel_front_cy), wheel_radius, 1)
    pygame.draw.line(screen, SPOKE_COLOR, F11, F12, 1)
    pygame.draw.line(screen, SPOKE_COLOR, F21, F22, 1)
    pygame.draw.line(screen, SPOKE_COLOR, F31, F32, 1)
    # wheel 2
    pygame.draw.circle(screen, CAR_COLOR, (wheel_rear_cx, wheel_rear_cy), wheel_radius, 1)
    pygame.draw.line(screen, SPOKE_COLOR, R11, R12, 1)
    pygame.draw.line(screen, SPOKE_COLOR, R21, R22, 1)
    pygame.draw.line(screen, SPOKE_COLOR, R31, R32, 1)
    # ground
    pygame.draw.aalines(screen, GREEN, False, points, 1)
    # text
    screen.blit(k_txt_surf, k_txt_rect)
    screen.blit(vel_txt_surf, vel_txt_rect)
    # display
    pygame.display.flip()
