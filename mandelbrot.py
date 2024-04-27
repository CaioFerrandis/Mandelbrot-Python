import pygame, math, threading

'''
Attempt of rendering Mandelbrot in pygame with the use of multithreading.
                                                           (abysmal failure, no gain of performance whatsoever)
C.F.
'''

pygame.init()

resolution = (700, 700)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Mandelbrot!")

pixels = pygame.PixelArray(screen)


def select_core(l, core):
    if core == 1:
        return l[:int((len(l))/4)]
    elif core == 2:
        return l[int((len(l))/4):int((len(l))/2)]
    elif core == 3:
        return l[int((len(l))/2):int(((len(l))*3)/4)]
    elif core == 4:
        return l[int(((len(l))*3)/4):]
    else:
        return l


def mandelbrot(grid, substeps, size, zoom, offset, core):
    new_grid = select_core(grid, core)
    for x, _ in enumerate(new_grid):
        if core is not None:
            x += len(new_grid)*(core-1)
        for y, _2 in enumerate(_):
            z = complex(0, 0)
            c = complex((((x-1)*zoom/size[0]-.5)*2)+offset[0], (((y-1)*zoom/size[0]-.5)*2)+offset[1])

            for i in range(substeps):
                color_bool = True
                z = z * z + c
                color = [(255*(i+1)/substeps), (255*(i+1)/substeps), (255*(i+1)/substeps)]
                if math.dist(list((z.real, z.imag)), (0, 0)) > 2:
                    color_bool = False
                    break
            if color_bool:
                color = [255, 255, 255]
            grid[x, y] = pygame.Color(color)
            if y % 700 == 0:
                pygame.display.update()


delta = 0.5
animate = False
running = True
substeps = 500
zoom = 2
offset = [-1, -1]

# First iteration will be rendered by dividing the mandelbrot in 4 big parts
t1 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 1))
t2 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 2))
t3 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 3))
t4 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 4))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()

    if animate:
        if zoom >= delta:
            zoom -= delta
            offset[0] += delta
            offset[1] += delta
        else:
            delta /= 2

        # Next iterations make the threads draw one line at a time sequentially,
        # which is probably the same thing, but better looking
        t1 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 1))
        t2 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 2))
        t3 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 3))
        t4 = threading.Thread(target=mandelbrot, args=(pixels, substeps, resolution, zoom, offset, 4))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    screen.fill((0, 0, 0))
    mandelbrot(pixels, substeps, resolution, zoom, offset, None)
    pygame.display.update()
