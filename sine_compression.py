
import numpy as np
from sklearn.metrics import mean_squared_error

'''
It's not very well optimized, too big arrays will take too much time or will use your entire RAM. And I'm not sure if it's working fully correct.
'''

np.random.seed(5557)

array1 = np.random.randn(1000,1)
#array1 = np.arange(np.prod((10,10) )).reshape(10,10)

np.random.seed(588857)

array2 = np.random.randn(1000,1)
#array2 = np.arange(np.prod((10,10) )).reshape(10,10)



# High Frequency Sin
def high_sin(x, max_abs_value):
  return  (np.sin(x*1000000)*max_abs_value) # max_abs_value is the maximum absolute value it can compress | max(abs())


def dist(point1, point2, point3, point4):
    return (np.sqrt((point3 - point1)**2 + (point4 - point2)**2))


def cal_distance(x, array1, array2, max_abs_value):
   return np.apply_along_axis(lambda x: dist((x), high_sin(x, max_abs_value), array1, array2), 0, x)


def points(stack, samples, near, max_abs_value):
  linear = np.array([])
  for i, val in enumerate(stack):
  	linear = np.hstack((linear,np.linspace(val*(1-near),val*(1+near),(samples//stack.shape[0]))))
  return linear[np.argmin((cal_distance(linear,stack[:(stack.shape[0]//2)].reshape(-1,1),stack[(stack.shape[0]//2):].reshape(-1,1), max_abs_value)),axis= 1)]
  




def compress(array1,array2, samples, near, max_abs_value):
	return (np.apply_along_axis(points, 1, (np.hstack((array1, array2))), samples, near, max_abs_value))
	
def recover(compressed, max_abs_value):
	return ((compressed),high_sin(compressed, max_abs_value))




result = compress(array1,array2,100000, 0.03, 15)



#print("result", result.reshape(-1))

recovered = recover(result, 15)
recovered_array1 = (recovered[0])
recovered_array2 = (recovered[1])


#print(array1.reshape(-1),'\nCoordenadas X:',recovered_array1.reshape(-1),'\n\n',array2.reshape(-1))


#print(recovered_array1.shape,array1.shape)

#print("\nCoordenadas Y:", recovered_array2.reshape(-1))


mse = mean_squared_error(array1, (recovered_array1))
print("Mean Squared Error:", mse)

mse = mean_squared_error(array2, (recovered_array2))
print("Mean Squared Error:", mse)

