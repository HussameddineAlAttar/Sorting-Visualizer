import pygame
import random
pygame.init()

class dispClass:
    BLACK = 0,0,0
    WHITE = 255,255,255

    RED = 255,0,0
    GREEN = 0,255,0
    BLUE = 0,0,255

    GREY_M = 160,160,160
    GREY_L = 192,192,192

    BACKGROUND_COLOR = BLACK

    GRADIENT = [WHITE,GREY_L, GREY_M]

    FONT = pygame.font.SysFont("arial", 28)
    LARGE_FONT = pygame.font.SysFont("arial", 38)

    FCOL = WHITE

    H_MARGIN = 100
    V_MARGIN = 100


    def __init__(self, width, height, A):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(A)
    
    def set_list(self, A):
        self.A = A
        self.max_val = max(A)
        self.min_val = min(A)

        self.sq_width = round((self.width - self.H_MARGIN) / len(A))
        self.sq_height = int((self.height - self.V_MARGIN) / (self.max_val - self.min_val))

        self.start_x = self.H_MARGIN // 2


def genList(nb, myMin, myMax):
    A = []
    for i in range(nb):
        A.append(random.randint(myMin, myMax))
    return A

def draw(myDisp, sorting_alg_name, ascending):
    myDisp.window.fill(myDisp.BACKGROUND_COLOR)
    
    if ascending:
        message = "{} - Ascending".format(sorting_alg_name)
        title = myDisp.FONT.render(message, 1, myDisp.GREEN)
        myDisp.window.blit(title, (myDisp.width/2 - title.get_width()/2,5))
    else:
        message = "{} - Descending".format(sorting_alg_name)
        title = myDisp.FONT.render(message, 1, myDisp.RED)
        myDisp.window.blit(title, (myDisp.width/2 - title.get_width()/2,5))

    controls = myDisp.FONT.render("R - Reset | Space - Sort | A - Ascending | D - Descending", 1, myDisp.FCOL)
    myDisp.window.blit(controls, (myDisp.width/2 - controls.get_width()/2,35))
    
    sorting = myDisp.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort", 1, myDisp.FCOL)
    myDisp.window.blit(sorting, (myDisp.width/2 - sorting.get_width()/2 , 65))

    drawList(myDisp)
    pygame.display.update()

def drawList(myDisp, color_positions = {}, clear_bg = False):
    A = myDisp.A

    if clear_bg:
        clear_rect = (myDisp.H_MARGIN//2, myDisp.V_MARGIN, myDisp.width - myDisp.H_MARGIN, myDisp.height)
        pygame.draw.rect(myDisp.window, myDisp.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(A):
        x = myDisp.start_x + i * myDisp.sq_width
        y = myDisp.height - (val - myDisp.min_val) * myDisp.sq_height

        color = myDisp.GRADIENT[i%3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(myDisp.window, color, (x, y, myDisp.sq_width, myDisp.height))

    if clear_bg:
        pygame.display.update()

def bubble_sort(myDisp, ascending = True):
    A = myDisp.A
    for i in range(len(A)):
        for j in range(len(A) - i - 1):
            drawList(myDisp, {j: myDisp.GREEN, j+1: myDisp.RED}, True)
            if (A[j] > A[j+1] and ascending) or (A[j] < A[j+1] and not ascending):
                A[j], A[j+1] = A[j+1], A[j]
                
                yield True
    return A

def insertion_sort(myDisp, ascending = True):
    A = myDisp.A
    for i in range(1,len(A)):
        key = A[i]
        while i > 0:
            cond_ascend = (A[i-1] > key) and (ascending)
            cond_descend = (A[i-1] < key) and (not ascending)

            if not (cond_ascend or cond_descend): # if neither
                break
            A[i] = A[i-1]
            i -= 1
            A[i] = key
            drawList(myDisp, {i:myDisp.GREEN, i-1 : myDisp.RED},True)
            yield True
            
    return A

def merge_sort(myDisp, ascending = True):
    A = myDisp.A
    in_merge_sort(myDisp,A, 0, len(A)-1,ascending)
    if not ascending:
        A.reverse()
    return A

def in_merge_sort(myDisp,A, start, end,ascending):
    if start < end:
        mid = (start + end)//2
        in_merge_sort(myDisp,A,start,mid,ascending)
        in_merge_sort(myDisp,A,mid+1,end,ascending)
        merge(myDisp,A,start,mid,end,ascending)
    
    
def merge(myDisp,A,start,mid,end,ascending):
    p = start
    q = mid + 1
    tempArray = []
    for i in range(start, end+1):
        drawList(myDisp, {p:myDisp.GREEN, q: myDisp.RED},True)
        if p > mid:
            tempArray.append(A[q])
            q+=1
        elif q > end:
            tempArray.append(A[p])
            p+=1
        elif A[p] < A[q]:
            tempArray.append(A[p])
            p+=1
        else:
            tempArray.append(A[q])
            q+=1
    for p in range(len(tempArray)):
        A[start] = tempArray[p]
        start += 1

def main():
    nb = 1000
    myMin = 0
    myMax = 50
    A = genList(nb, myMin, myMax)

    myDisp = dispClass(1000,600,A)

    run = True
    clock = pygame.time.Clock()

    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_name = "Bubble Sort"
    sorting_alg_gen = None


    while run:
        clock.tick(60) # frequency
        if sorting:
            try:
                next(sorting_alg_gen)
            except:
                sorting = False
        else:
            draw(myDisp, sorting_alg_name, ascending)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # end
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # end
                    run = False

                elif event.key == pygame.K_r: #randomize
                    A = genList(nb, myMin, myMax)
                    myDisp.set_list(A)
                    sorting = False
                
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_alg_gen = sorting_alg(myDisp, ascending)

                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False

                elif event.key == pygame.K_i and not sorting:
                    sorting_alg = insertion_sort
                    sorting_alg_name = "Insertion Sort"

                elif event.key == pygame.K_b and not sorting:
                    sorting_alg = bubble_sort
                    sorting_alg_name = "Bubble Sort"

                elif event.key == pygame.K_m and not sorting:
                    sorting_alg = merge_sort
                    sorting_alg_name = "Merge Sort"

    pygame.quit()

main()
print("success")