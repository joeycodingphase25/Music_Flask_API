from app.blueprints.api.models import translate



keys = 'a, b, c-sharp, d, e, f-sharp, g-sharp, a'
new_keys = ''
for key in keys.replace(' ', '').split(','):
    if key in translate: 
        new_keys += translate[key]
print(new_keys)