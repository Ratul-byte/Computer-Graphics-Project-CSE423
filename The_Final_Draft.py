from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import winsound
#from playsound import playsound
from math import sin, cos, pi
import random

#DRIVE UNTIL DEATH GAME(GROUP -10)
winsound.PlaySound("Running in the 90s.wav", 
                   winsound.SND_ASYNC + winsound.SND_LOOP)

#window size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

#collision variables
collision = False
get = False
collision2 = False
collision3 = False

#points
point_x = random.randint(10, 80)
point_y = 105

y_position = 105

#tree
circle1_y = 105
circle2_y = 105
circle_x = random.randint(10, 80)
circle_speed = 0.5
trunk = 96

seq = random.randint(1, 5)

dis = False  #obstacle dissappear
dis2 = False #diamond dissappear
dis3 = False
dis4 = False



speed = 0.38
diamond_speed = 0.45
obstacles_speed = 0.78

car_position = 51
car_movement_direction = 0

game_paused = False
game_reset = False
stop = True

p_speed = 0

p_cir_speed = 0

lives = 3

var = 1

p_pts_speed = 0
point_speed = 0.5

num_points = 5
points = []
score = 0

#Storing points coordinates
for i in range(num_points):
    point_x = random.uniform(23, 80)
    point_y = random.uniform(150, 110)
    points.append({'x': point_x, 'y': point_y, 'speed': point_speed})

class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)

#obstacle collision condition
def collides_with_sq_obstacle(car_pos, car_width, car_height, obstacles):
    return (car_pos - 5 < obstacles.x + obstacles.w and
                car_pos + car_width > obstacles.x and
                20 < obstacles.y + obstacles.h and
                20 + car_height > obstacles.y)

def collides_with_car(car_pos, car_width, car_height, point):
    car_aabb = AABB(car_pos - car_width / 2, 20 - car_height / 2, car_width, car_height)
    point_aabb = AABB(point['x'], point['y'], 1, 1)

    return car_aabb.collides_with(point_aabb)

def collides_with_point(car_pos, car_width, car_height, pts):
    return (car_pos - 5 == pts.x + pts.w and
            car_pos + car_width > pts.x and
            20 < pts.y + pts.h and
            20 + car_height > pts.y)

#Midpoint Line
def draw_line(x1, y1, x2, y2):
    glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if x1 < x2:
        step_x = 1
    else:
        step_x = -1

    if y1 < y2:
        step_y = 1
    else:
        step_y = -1
    x = x1
    y = y1
    cnt = 0
    if dx > dy:
        p = 2 * dy - dx
        while dx > cnt:
            glVertex2f(x, y)
            x += step_x
            if p >= 0:
                y += step_y
                p -= 2 * dx
            p += 2 * dy
            cnt += 1
    else:
        p = 2 * dx - dy
        while dy > cnt:
            glVertex2f(x, y)
            y += step_y
            if p >= 0:
                x += step_x
                p -= 2 * dy
            p += 2 * dx
            cnt += 1
    glEnd()


#Midpoint Circle
def draw_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius

    circle_pts2(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1
        circle_pts2(x, y, cx, cy)

def mid_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius
    circle_pts(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1
        circle_pts(x, y, cx, cy)

def circle_pts(x, y, cx, cy):
    glPointSize(50)
    glBegin(GL_POINTS)
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)
    glEnd()


# def collides_with_sq_obstacle(car_pos,car_width,car_height, obstacles):
def draw_point(x, y):
    glEnable(GL_POINT_SMOOTH)
    glPointSize(18.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glDisable(GL_POINT_SMOOTH)

def circle_pts2(x, y, cx, cy):
    num_segments = 100  # Increase this value for a smoother circle
    glBegin(GL_POINTS)
    for i in range(num_segments):
        theta = 2.0 * pi * i / num_segments
        glVertex2f(x * cos(theta) + cx, y * sin(theta) + cy )
    glEnd()

def draw_car(car_position, car_width, car_height):
    car_y = 20  # Fixed y-position for the car in the middle
    # Draw wheels
    wheel_radius = car_height / 4  # Adjust the wheel size as needed
    wheel_y = car_y - car_height / 2 - wheel_radius  # Place wheels at the bottom of the car
    wheel_positions = [-car_width / 3, car_width / 3]

    glColor3f(0.0, 0.0, 0.0)  # Black color for the wheels

    glBegin(GL_POINTS)

    for wheel_position in wheel_positions:
        draw_wheel(car_position + wheel_position, wheel_y, wheel_radius)

    glEnd()

    glColor3f(1.0, 0.0, 0.0)  # Red color for the car
    glPointSize(9.0)
    
    glBegin(GL_POINTS)
    glEnd()
    # Draw car body
    for x in range(int(car_position - car_width / 2), int(car_position + car_width / 2)):
        for y in range(int(car_y - car_height / 2), int(car_y + car_height / 2)):
            glPointSize(9)
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

def draw_wheel(cx, cy, radius):
    for i in range(360):
        angle = i * 3.14159 / 180
        x = cx + radius * 0.2 * cos(angle)
        y = cy + radius * 0.7 * sin(angle)
        glVertex2f(x-0.95, y+11)
        glVertex2f(x-0.95, y+3)      
    
def draw_obstacles(obstacles):
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(10)
    glBegin(GL_POINTS)
    glEnd()
    draw_line(obstacles.x, obstacles.y, obstacles.x + obstacles.w , obstacles.y)

    draw_line(obstacles.x, obstacles.y, obstacles.x , obstacles.y+obstacles.h)

    draw_line(obstacles.x, obstacles.y+obstacles.h, obstacles.x + obstacles.w , obstacles.y+obstacles.h)

    draw_line(obstacles.x+ obstacles.w, obstacles.y+obstacles.h, obstacles.x + obstacles.w , obstacles.y)
    con = obstacles.x
    for i in range(10):
        con +=1
        draw_line(con, obstacles.y, con, obstacles.y+obstacles.h)
    
def draw_solid_diamond(diamond):
    glColor3f(0.0, 1.0, 0.0)  # Set color to green

    glBegin(GL_POINTS)
    con = diamond.x
    half_width = diamond.w // 2
    half_height = diamond.h // 2
    for i in range(half_height):
        for j in range(half_width - i, half_width + i + 1):
            # Draw two symmetrical points at a time
            glVertex2f(con + j, diamond.y + half_height + i)
            glVertex2f(con + j, diamond.y + half_height - i)
    glEnd()


#text function
def render_text(x, y, text,r,g,b):

    glColor3f(r, g, b)   # Set text color to white
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))

def display():
    global y_position, score, speed, circle1_y, circle2_y, point_speed, circle_speed, diamond, circle_x, seq, car_position, game_paused, obstacles_speed, collision, var, dis, lives, point_y, point_x, trunk, points
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw road
    glColor3f(0.41, 0.41, 0.41)
    draw_line(80, 10, 80, 100)
    draw_line(80, 10, 80, 90)
    draw_line(80, -5, 80, 80)

    draw_line(20, 10, 20, 100)
    draw_line(20, 10, 20, 90)
    draw_line(20, -5, 20, 80)

    glColor3f(0.41, 0.41, 0.41)
    glPointSize(10)
    glBegin(GL_POINTS)
    for x in range(0, 110):
        for y in range(20, 81):
            glVertex2f(y, x)
    glEnd()
    

    # Draw circles with updated y-coordinates
    glColor3f(0.0, 1.0, 0.0)  # Green color for the circles
    #glEnable(GL_POINT_SMOOTH)
    m = 0
    n = 0
    for i in range(seq):
        glColor3f(0.0, 1.0, 0.0)
        mid_circle(10, circle1_y+m, 4)

        glColor3f(0.545, 0.271, 0.075)
        glPointSize(20)
        draw_line(10, trunk+n, 10, trunk+7+n)

        glColor3f(0.0, 1.0, 0.0)
        mid_circle(90, circle1_y+m, 4)
        
        glColor3f(0.545, 0.271, 0.075)
        glPointSize(20)
        draw_line(90, trunk+n, 90, trunk+7+n)
        m+=20
        n+=20
    #draw_circle(circle_x, circle2_y, 2)

    # Draw moving line
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(7.5)
    #draw_line(y_position, 50, y_position + 11, 50)
    draw_line(50, y_position, 50, y_position + 30)
    
    #draw obstacles        
    draw_obstacles(obstacles)

    draw_obstacles(obstacles2)
    draw_obstacles(obstacles3)
    
    # Draw moving points
    glColor3f(1.0, 0.843, 0.0) #golden color
    
    for point in points:
        draw_point(point['x'], point['y'])

        # Check for collision with car
        if collides_with_car(car_position, 5, 10, point):
            print("Point collected!")
            speed+=0.025
            circle_speed+=0.005
            point_speed+=0.005
            score+=1
            point['y'] = 105
            point['x'] = random.uniform(23, 80)

    #draw diamond
    if game_paused == False and lives != 0:
        draw_solid_diamond(diamond) 

    # Draw car
    glPointSize(12)
    draw_car(car_position, 5, 10)

    # Draw "Lives" information text
    glColor3f(1.0, 1.0, 1.0)
    render_text(5, 10, f"Lives: {lives}",0.0, 0.0, 0.0)
    render_text(5, 90, f"Score: {score}",0.0, 0.0, 0.0)

    # Check if the game is over and display "Game Over" continuously
    if lives == 0:
        glColor3f(1.0, 0.0, 0.0)  # Set text color to white
        render_text(43, 50, "Game Over",0.0, 1.0, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        render_text(43, 45, f"Your Final Score: {score}!",1.0, 1.0, 1.0)
    glutSwapBuffers()   

def animation():
    global y_position,stop, speed, point_speed,diamond_speed, circle1_y, circle2_y, circle_speed, circle_x, seq, car_position, dis3, dis4, game_paused, obstacles_speed, dis2, collision, collision2, collision3, var, dis, lives, point_y, point_x, trunk
    if stop:
        if game_paused == False:  # Check if the game is not paused
            circle1_y -= circle_speed
            circle2_y -= circle_speed
            trunk -= circle_speed

            # Reset circles to the top if they reach the bottom
            if trunk < -100:
                trunk = 105

            if circle1_y < -100:
                circle1_y = 105
                seq = random.randint(1, 5)
            if circle2_y < -300:
                circle2_y = 105
                circle_x = random.randint(30, 70)

        # Update the y-coordinate for each moving point
        if game_paused == False and lives != 0:
            for point in points:
                point['y'] -= point['speed']
                if point['y'] < -13:
                    point['y'] = 105
                    point['x'] = random.uniform(23, 80)
                    #point_y = random.uniform(20, 80)

        # Update the y-coordinate for the animation
        if game_paused == False:
            y_position -= speed
            if y_position < -25:
                y_position = 105

        #OBSTACLES animation
        obstacles.y -= speed
        obstacles2.y -= speed
        obstacles3.y -= speed

        if obstacles.y < 0 or dis == True:
            # once_neg = True
            # felled = True
            # obstacles_speed += .01
                
            obstacles.x = random.randint(20, 70)
            obstacles.y = 105
            dis = False
        if obstacles2.y < 0 or dis3 == True:
            # once_neg = True
            # felled = True
            # obstacles_speed += .01
                
            obstacles2.x = random.randint(20, 70)
            obstacles2.y = 105
            dis3 = False

        if obstacles3.y < 0 or dis4 == True:
            # once_neg = True
            # felled = True
            # obstacles_speed += .01
                
            obstacles3.x = random.randint(20, 70)
            obstacles3.y = 105
            dis4 = False


        #diamond_animation
        diamond.y-= diamond_speed
        diamon_dis = -2000
        if diamond.y < diamon_dis or dis2 == True:
            # once_neg = True
            # felled = True
            # obstacles_speed += .01
                
            diamond.x = random.randint(20, 70)
            diamond.y = 1000
            dis2 = False

        get = collides_with_sq_obstacle(car_position, 4, 8, diamond)
        if get:
            lives +=1
            diamon_dis = diamon_dis*2
            print("gotchaaaa!")
            get = False
            dis2 = True

        collision = collides_with_sq_obstacle(car_position, 4, 8, obstacles)
        collision2 = collides_with_sq_obstacle(car_position, 4, 8, obstacles2)
        collision3 = collides_with_sq_obstacle(car_position, 4, 8, obstacles3)
        if collision == True:
            #print(var)
            #var +=1
            collision = False
            dis = True
            lives-=1
            print("Ughhh!!")
            if lives == 0:
                print("Game Over")
                winsound.PlaySound(None, 0)
                # speed = 0
                # circle_speed = 0
                # point_speed = 0
                # diamond_speed = 0
                stop = False
            else:
                print(f"Lives remaining {lives}")

        if collision2 == True:
            #render_text(50, 50, f"It's your lucky day mate ('-')")
            collision2 = False
            dis3 = True
            print("It's your lucky day mate ('-')")

        if collision3 == True:
            #render_text(50, 50, f"It's your lucky day mate ('-')")
            collision3 = False
            dis4 = True
            print("It's your lucky day mate ('-')")

        glutPostRedisplay()


def key_action(key, x, y):
    global car_position, game_paused, lives,stop

    # Adjust the car position based on the arrow keys
    if game_paused == False and lives!=0:
        if key == GLUT_KEY_LEFT and car_position > 24:
            car_position -= 1.5
            #print('l', car_position)
        elif key == GLUT_KEY_RIGHT and car_position < 78:
            car_position += 1.5
            #print('r', car_position)

    glutPostRedisplay()

def mouse_action(button, state, x, y):
    global game_paused, speed, circle_speed, point_speed, p_speed, p_cir_speed, p_pts_speed, game_reset, score, diamond_speed
    global point_x, point_y, y_position, circle1_y, circle2_y, circle_x, trunk, lives, obstacles, obstacles2, obstacles3, stop

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and lives!=0: #pause the game
        game_paused = not game_paused
        if game_paused == True:
        # if stop == True:    
            # p_speed = speed
            # p_cir_speed = circle_speed
            # p_pts_speed = point_speed
            # speed = 0
            # circle_speed = 0
            # point_speed = 0
            # diamond_speed = 0
            stop = False
        else:
            stop = True
            # speed = p_speed
            # circle_speed = p_cir_speed
            # point_speed = p_pts_speed
            # p_speed = 0
            # p_cir_speed = 0
            # p_pts_speed = 0
            # diamond_speed = 0.45
            
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN: #restart the game
        winsound.PlaySound("Running in the 90's.wav", 
                   winsound.SND_ASYNC + winsound.SND_LOOP)
        stop = True
        speed = 0.4
        circle_speed = 0.5 
        point_speed = 0.5
        point_x = random.randint(10, 80)
        point_y = 105

        y_position = 105

        circle1_y = 105
        circle2_y = 105
        circle_x = random.randint(10, 80)

        diamond.y = 1000
        lives = 3
        trunk = 96
        score = 0
        obstacles = AABB(random.randint(20, 70), 100-10, 10, 10)
        obstacles2 = AABB(random.randint(20, 70), 100-10, 10, 10)
        obstacles3 = AABB(random.randint(20, 70), 100-10, 10, 10)

obstacles = AABB(random.randint(20, 70), 100-10, 10, 10)
obstacles2 = AABB(random.randint(20, 70), 100-10, 10, 10)
obstacles3 = AABB(random.randint(20, 70), 100-10, 10, 10)

#obstacles_speed = 1

diamond = AABB(x=40, y=1000, w=8, h=8)

def init():
    glClearColor(1, 0.76, 0.5, 1.75)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 100, 0, 100)  # Adjust the coordinates as needed

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"DRIVE UNTIL DEATH")

    init()
    glutDisplayFunc(display)
    glutSpecialFunc(key_action)
    glutMouseFunc(mouse_action) 
    glutIdleFunc(animation)
    glutMainLoop()

if __name__ == "__main__":
    main()