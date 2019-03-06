
from getproxy import GetProxy

g = GetProxy() # 1. Initialization, step 
g.init() # 2. Load input proxies list 
g .load_input_proxies() # 3. Verify the input proxies list 
g.validate_input_proxies() # 4. Load the plugin 
g.load_plugins() # 5. Grab the web proxies list 
g.grab_web_proxies() # 6. Verify the web proxies list 
x=g.validate_web_proxies( ) #7.Save all current verified proxies list 
g.save_proxies()
print(len(x))

