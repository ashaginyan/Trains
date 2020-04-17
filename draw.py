import cv2
import cmath
   
# path  
path = '8_723.jpg'
   
# Reading an image in default mode 
image = cv2.imread(path) 
image = cv2.resize(image, (1200, 700))
   
# Window name in which image is displayed 
window_name = 'Image'

A = [(0, 206), (0, 340), (0, 495), (55, 699), (245, 699), (435, 699), (697, 699), 
     (867, 699), (1039, 699), (1199, 653), (1199, 455), (1199, 310)]
B = [(121, 91), (181, 140), (222, 170), (315, 204), (406, 211), (511, 216), 
     (653, 216), (766, 216), (853, 211), (942, 204), (951, 182), (1051, 93)]
C = [(218, 3), (296, 0), (351, 0), (420, 0), (478, 0), (544, 0), (633, 0), 
     (691, 0), (751, 0), (813, 0), (866, 0), (919, 0)]

# Длины между началом и концом видимого участка в метрах
L = [70, 80, 98, 114, 114, 114, 114, 114, 114, 98, 86, 76]

def get_k_b(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    k = (y1 - y2) / (x1 - x2)
    b = y1 - k * x1
    return round(k, 2), round(b)

def get_dist(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  r = ((x2-x1)**2+(y2-y1)**2)**0.5
  return round(r)

def y(x, k, b):
    return k*x + b

# Расстояния от А до середины видимого отрезка пути в пикселях (АВ)
M = []
for i in range(len(A)):
  M.append(get_dist(A[i], B[i]))

# Расстояния АС в пикселях
W = []
for i in range(len(A)):
  W.append(get_dist(A[i], C[i]))

k = []
b = []

# Рассчитываем угловой коэффициент и b для каждой прямой
for i in range(len(A)):
    k_, b_ = get_k_b(A[i], C[i])
    k.append(k_)
    b.append(b_)

#print(k)
print(b)

# N - номер пути, x - расстояние от А до текущей точки в пикселях
# D - расстояние от конца горки до текущей точки в метрах
def D(x, N, M=M, L=L, W=W):
  assert len(L) == len(W) == len(M)
  K = (W[N] - M[N]) / M[N]
  D = L[N] * K / ((W[N] / x) - 1 + K)
  return round(D)

def x(D, N, M=M, L=L, W=W):
    assert len(L) == len(W) == len(M)
    K = (W[N] - M[N]) / M[N]
    x = W[N] / (L[N]*K/(D) + 1 -K)
    return round(x)

for i in range(3, 9):
    print('Way #', i)
    start_point = A[i]

    end_point = C[i]
  
    # Green color in BGR 
    color = (0, 255, 0) 
  
    # Line thickness of 9 px 
    thickness = 4
    
    image = cv2.line(image, start_point, end_point, color, thickness)
    r = 0
    for j in range(L[i]):
        if j % 20 == 2:
            r = x(j, i)
            y = round(W[i] - r)
            x1 = round((y - b[i]) / k[i])
            y = round(k[i] * x1 + b[i])
            #print('D:', j, 'r:', r, 'x:', x1, 'y:', y, 'L:', L[i], 'b:', b[i], 'k:', k[i])
            h_start = x1 - 20, y
            h_end = x1 + 20, y

            font = cv2.FONT_HERSHEY_SIMPLEX 
            org = (x1+10, y+10) 
            fontScale = 1
            image = cv2.line(image, h_start, h_end, color, thickness)
            image = cv2.putText(image, str(78+j), org, font,fontScale, color, thickness, cv2.LINE_AA) 

  
# Displaying the image  
cv2.imshow(window_name, image)  
cv2.waitKey(0)

