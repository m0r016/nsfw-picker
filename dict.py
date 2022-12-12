dict = {
  'sample/hardwood-timber.jpg': {
    'drawings': 0.01506318524479866, 
    'hentai': 0.023085521534085274, 
    'neutral': 0.9159455895423889, 
    'porn': 0.021340474486351013, 
    'sexy': 0.024565137922763824
    }
  }

dict_drawings = [dict.get('drawings') for dict in dict.values()]
dict_hentai = [dict.get('hentai') for dict in dict.values()]
dict_neutral = [dict.get('neutral') for dict in dict.values()]
dict_porn = [dict.get('porn') for dict in dict.values()]
dict_sexy = [dict.get('sexy') for dict in dict.values()]

if dict_neutral[0] > 0.5:
  print('neutral')