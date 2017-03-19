import tensorflow as tf

def weightVariable(shape, Wname="W"):
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial, dtype=tf.float32, name=Wname)
        
def biasVariable(shape, Bname="B"):
    initial = tf.zeros(shape)
    return tf.Variable(initial, dtype=tf.float32, name=Bname)
        
def addConvLayer(inp, shape, weight_name, biases_name, act_fun=tf.nn.relu):
    with tf.name_scope("Conv_Layer"):
        with tf.name_scope("Parameters"):
            # create the weight variable:
            layer_weight = weightVariable(shape, Wname=weight_name)

            # create bias variable:
            layer_bias = biasVariable([shape[-1]], Bname=biases_name)

        return act_fun(tf.nn.conv2d(inp, layer_weight, [1, 1, 1, 1], padding="SAME") + layer_bias)
    
def addPoolLayer(inp, kernel, stride):
    return tf.nn.max_pool(inp, ksize=kernel, strides=stride, padding='SAME')
    
def addFCLayer(inp, shape, weight_name, biases_name, act_fun=tf.nn.relu):
    with tf.name_scope("Fully_Connected_Layer"):
        with tf.name_scope("Parameters"):
            layer_weight = weightVariable(shape,Wname=weight_name)
            layer_bias = biasVariable([shape[-1]], Bname=biases_name)

        if(act_fun == None): 
            return tf.matmul(inp, layer_weight) + layer_bias
        # else:
        return act_fun(tf.matmul(inp, layer_weight) + layer_bias)
