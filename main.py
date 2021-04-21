from Base import get_input
from Scripts import Scripts
from Settings import debug_data

# name, url = get_input()
data = debug_data['preferencePojo']
name, url = data['siteName'].title(), data['url_scrap']
site = Scripts()
runScript = getattr(site, name)
obj = runScript(url)
obj.run()
print('Done..')
