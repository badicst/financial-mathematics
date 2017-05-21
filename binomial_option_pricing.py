
# coding: utf-8

# #Pricing Option in Binomial Model
# ##Building a tree

# ##Simple case

# In[1]:

def binomial_tree_create(price, current_depth, max_depth):
    if current_depth >= max_depth:
        return {"price": price, "isleaf":True}
    up_tree = binomial_tree_create(price*1.5, current_depth + 1, max_depth)        
    down_tree = binomial_tree_create(price*0.5, current_depth + 1, max_depth)
    return {'price': price, 'up': up_tree, 'down': down_tree, 'isleaf':False}


# ###The tree:

# In[2]:

binomial_tree=binomial_tree_create(100, 0, 2)
binomial_tree


# ###A trajectory

# In[3]:

print binomial_tree["price"], binomial_tree["down"]["price"], binomial_tree["down"]["up"]["price"]


# #Adding the option payoff to the tree
# ##(modifying the tree)

# In[4]:


def add_option(tree, strike):
    if tree['isleaf']:
        tree["option"]=max(tree['price']-strike,0 )
    else:
        add_option(tree['up'], strike)
        add_option(tree['down'], strike)
        #tree["option"]=None
def add_put_option(tree, strike):
    if tree['isleaf']:
        tree["option"]=max(strike-tree['price'],0 )
    else:
        add_put_option(tree['up'], strike)
        add_put_option(tree['down'], strike)
        #tree["option"]=None

binomial_tree=binomial_tree_create(100, 0, 2)    
add_option(binomial_tree, 50)

binomial_tree
#binomial_tree


# ##Pricing the option
# ## r=0 case

# In[5]:

def option_prices(tree, q):
    if tree['isleaf']:
        return tree["option"]
    return q*option_prices(tree['up'], q)+(1-q)*option_prices(tree['down'],q)


print option_prices(binomial_tree, 0.5) 


# #r>0 case

# In[ ]:




# #Cox-Ross-Rubinstein model

# In[6]:

from math import sqrt,exp


# In[7]:

def CRR_create(price, current_depth, T, sigma, delta):
    steps=T/delta
    if current_depth >= steps:
        return {"price": price, "isleaf":True}
    up_tree = CRR_create(price*exp(sigma*sqrt(delta)), current_depth + 1, T, sigma, delta)        
    down_tree = CRR_create(price*exp(-sigma*sqrt(delta)), current_depth + 1, T, sigma, delta)
    return {'price': price, 'up': up_tree, 'down': down_tree, 'isleaf':False}


# In[8]:

def risk_neutral_prob(r,delta, sigma):
    return (exp(r*delta)-exp(-sigma*sqrt(delta)))/(exp(sigma*sqrt(delta))-exp(-sigma*sqrt(delta)))

def option_price(tree, q,r, delta):
    if tree['isleaf']:
        return tree["option"]
    return exp(-r*delta)*(q*option_price(tree['up'], q, r, delta)+(1-q)*option_price(tree['down'],q, r, delta))


# In[9]:

crr=CRR_create(50, 0, 2, 0.3, 1)


# In[10]:

print crr["price"], crr["up"]["price"], crr["up"]["up"]["price"]


# In[11]:

add_put_option(crr, 52)
q=risk_neutral_prob(0.05,1, 0.3)
q


# In[12]:

print option_price(crr, q, 0.05, 1) 


# #American option
# 

# In[13]:

def american_put_option_prices(tree, q, strike, r, delta):
    if tree['isleaf']:
        return tree["option"]
    return max(strike-tree["price"], exp(-r*delta)*(q*american_put_option_prices(tree['up'], q,
                strike, r, delta)+(1-q)*american_put_option_prices(tree['down'],q, strike, r, delta)))


# In[14]:

american_put_option_prices(crr, q, 52, 0.05,1)


# In[15]:

crr


# In[5]:

get_ipython().run_cell_magic(u'ipython', u'--config-dir', u'')


# In[ ]:




# In[ ]:



