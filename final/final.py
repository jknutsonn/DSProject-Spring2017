#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import sys, pygame, os, math, time, random, bisect

pygame.init()
pygame.display.list_modes()
myfont = pygame.font.SysFont("monospace", 15)

screen = pygame.display.set_mode((1200, 600))
arrow_angle = math.radians(90)
clock = pygame.time.Clock()
done = False

size = width, height = 1200, 600
running = 1
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0
gameplay = 0
hits = 0

p_color = (255, 0, 0)
p_xcord = 30
arrow_x = 30
arrow_y = 100
arrow_r = 20

ball_r = 3
ball_c = white
ball_t = 0
ball_x = 25
ball_y = height/2
vel_x = 30
vel_y = 0

flag_topx = width-33
flag_topy = height/2-4
flag_w = 16
flag_h = 8
score = []

# Power bar
def progress(direction, p_xcord):
	if direction > 1 and p_xcord < 100:
		p_xcord = p_xcord+8
	elif direction < 1 and p_xcord > 0:
		p_xcord = p_xcord-8
	pygame.draw.rect(screen, p_color, pygame.Rect(30, 550, 30+p_xcord, 30))
	return p_xcord

def rotatearrow(direction):
	global arrow_x,arrow_y,arrow_angle
	if direction > 0:
		arrow_angle = arrow_angle + math.radians(-10)
	elif direction < 0:
		arrow_angle = arrow_angle + math.radians(10)
	x = arrow_x + arrow_r*math.cos(arrow_angle)
	y = arrow_y - arrow_r*math.sin(arrow_angle)
	pygame.draw.aaline(screen, (250, 250, 15),(arrow_x,arrow_y), (x,y))

def midpt_disp(start, end, roughness, v_d = None, num_i = 16):
	if v_d is None:
		v_d = (start[1]+end[1])/2
	points = [start, end]
	iteration = 1
	while iteration <= num_i:
		points_tup = tuple(points)
		for i in range(len(points_tup)-1):
			midpt = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2, [0, 1]))
			midpt[1] = midpt[1] + random.choice([-v_d, v_d])
			bisect.insort(points, midpt)
		v_d *= 2 ** (-roughness)
		iteration = iteration + 1
	return points

line = midpt_disp([0+50, height/2], [width-50, height/2], 1.8, 200, 12)
#line2 = midpt_disp([0+50, height/2], [width-50, height/2], 2.0, 250, 12)
#for i in range(len(line)):
#	print((line[i-1][0],line[i-1][1]),(line[i][0], line[i][1]))	

def line_data():
	global line
	data = []
	data.append(height/2)
	for i in range(50):
		data.append(height/2)
	x = 0
	for i in range(width-100):
		while (i+50) != int(line[x][0]):
			x = x + 1
		data.append(int(line[x][1]))
	for i in range(50):
		data.append(height/2)
	return data


#Ball movement
def moveball(color, new_x, new_y):
	time.sleep(.01)
	pygame.display.update(pygame.draw.circle(screen, color, (int(new_x), int(new_y)), ball_r, ball_t))

def hitball(angle, velocity):
	vel_y = velocity * math.sin(angle)
	print (vel_y)
	vel_x = velocity * math.cos(angle)
	t = (vel_y / 9.8)* 2
	global ball_x, ball_y, data
	pos_x = ball_x
	pos_y = ball_y
	dt = t / 100
	dt_total = dt
	vel_y = vel_y * -1
	# Ball is moving fast enough to move
	while vel_y < -4:
		# Run until the ball hits the ground
		#while pos_y <= data[int(pos_x)]+2 and pos_y>=data[int(pos_x)]-2 or pos_y >= data[int(pos_x)]:
		#while pos_y >= data[int(pos_x)]-6 and pos_y <= data[int(pos_x)]+6 or pos_y <= data[int(pos_x)]:
		while pos_y <= data[int(pos_x)]:
			vel_y = vel_y + (4.9)*dt
			moveball(black, pos_x, pos_y)
			pos_x = pos_x + vel_x*dt
			pos_y = pos_y + vel_y*dt

			# Hit a wall
			if pos_x > width:
				vel_x = -vel_x
				pos_x = width - 1
			#if pos_y <= 0:
			#	vel_y = -vel_y
			#	pos_y = 1
			if pos_x < 1:
				vel_x = -vel_x
				pos_x = 1	

			#print(pos_x)

			dt_total += dt
			if pos_y > data[int(pos_x)]:
				break
			moveball(ball_c, pos_x, pos_y)	

			#ball hits flag
			if pos_x > flag_topx and pos_x < flag_topx + flag_w:
				if pos_y > flag_topy and pos_y < flag_topy + flag_h:
					return 1;
					break

		# Bouncing
		dt_total = dt_total - 2*dt
		if pos_x >= 1 and pos_x <= width:
			pos_x = pos_x - (vel_x*dt)
		pos_y = data[int(pos_x)] #data is ground data

		# Calculate the bounce angle
		inco_x1 = pos_x - (vel_x*dt)
		inco_y1 = pos_y - (vel_y*dt)
		inco_x2 = pos_x
		inco_y2 = pos_y
		gd_x1 = pos_x - 2
		gd_y1 = data[int(gd_x1)]
		gd_x2 = pos_x + 2
		gd_y2 = data[int(gd_x2)]
		gd_slope = (gd_y2-gd_y1)/gd_x2-gd_x1
		gd_norm = -1 / gd_slope
		#angle_incomingball = 
	
		velocity = velocity * 0.3
		vel_y = velocity * math.sin(angle)
		t = (vel_y / 9.8) * 2
		#dt = dt
		dt_total = dt
		vel_y = vel_y * -1
		ball_x = pos_x
		ball_y = pos_y
#	moveball(black, pos_x, pos_y)
#	pos_x = ball_x + vel_x*t
#	pos_y = ball_y + vel_y*t + 4.9*t*t
#	moveball(ball_c, pos_x, pos_y)
	ball_x = pos_x
	ball_y = data[int(pos_x)]
#	moveball(ball_c, ball_x, ball_y)
	print(ball_x, ball_y)

	# ball has not made it into the hole
	return 0;

# Main loop
it = 0
playing = True
data = line_data()
for holenumber in range(9):
	while(playing == True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				playing = false
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					p_xcord = progress(2, p_xcord)
				if event.key == pygame.K_DOWN:
					p_xcord = progress(0, p_xcord)
				if event.key == pygame.K_SPACE:
					gameplay = hitball(arrow_angle, p_xcord) 
					hits += 1
				if event.key == pygame.K_RIGHT:
					rotatearrow(1)
				if event.key == pygame.K_LEFT:
					rotatearrow(-1)

		#screen.fill(black)

		pygame.draw.line(screen, green, (0, height/2), (50, height/2))
		pygame.draw.line(screen, green, (width-50, height/2), (width, height/2))

		# Flag
		pygame.draw.ellipse(screen, (20,70,15), [flag_topx, flag_topy, flag_w, flag_h])
		pygame.draw.line(screen, (200,200,200), (width-25, height/2), (width-25, height/2-20))
		pygame.draw.polygon(screen, red, [[width-25, height/2-20],[width-25, height/2-15],[width-35, height/2-18+(it%3)]])
	
		i = 1
		while i < (len(line)):
			pygame.draw.aaline(screen, green, (line[i-1][0],line[i-1][1]),(line[i][0], line[i][1]))
#			print((line[i-1][0],line[i-1][1]),(line[i][0],line[i][1]))	
#			pygame.draw.aaline(screen, blue, (line2[i-1][0],line2[i-1][1]),(line2[i][0], line2[i][1]))	
			i = i + 1
			
		moveball(ball_c, ball_x, ball_y)
	
		arrow_x = ball_x 
		arrow_y = ball_y
		x = arrow_x + arrow_r*math.cos(arrow_angle)
		y = arrow_y - arrow_r*math.sin(arrow_angle)
		pygame.draw.aaline(screen, (250,250,15),(arrow_x,arrow_y), (x,y))
		
		#Draw scoreboard
		pygame.draw.rect(screen, white, pygame.Rect(0, height-65, 320, 65));
		label = myfont.render("Some text!" ,1, (255,255,255))
		screen.blit(label, (100,100))
		
		#Draw power bar
		pygame.draw.rect(screen, black, pygame.Rect(28,548,136,34))
		pygame.draw.rect(screen, blue, pygame.Rect(30,550,132,30))
		pygame.draw.rect(screen, p_color, pygame.Rect(30,550,30+p_xcord,30))
		
		it = it + 1
		pygame.display.flip()
		
		# Ball in hole
		if gameplay != 0:
			score.append(hits)
			print ("YOU WIN " + str(hits))
			playing = False

	screen.fill(black)
	line = midpt_disp([0+50, height/2], [width-50, height/2], 1.8, 200, 12)
	data = line_data()
	playing = True
	gameplay = 0
	hits = 0
	ball_x = 25
	ball_y = height/2

