avatar_dict = {
    0: 'anteater.svg',
    1: 'bear.svg',
    2: 'boar.svg',
    3: 'beaver.svg',
    4: 'buffalo-1.svg',
    5: 'buffalo.svg',
    6: 'cat.svg',
    7: 'chicken.svg',
    8: 'cow.svg',
    9: 'crow.svg',
    10: 'dog-1.svg',
    11: 'dog.svg',
    12: 'donkey.svg',
    13: 'elephant.svg',
    14: 'fox.svg',
    15: 'giraffe.svg',
    16: 'hedgehog.svg',
    17: 'hen.svg',
    18: 'hippopotamus.svg',
    19: 'horse.svg',
    20: 'kangaroo.svg',
    21: 'koala.svg',
    22: 'leopard.svg',
    23: 'lion.svg',
    24: 'marten.svg',
    25: 'monkey-1.svg',
    26: 'monkey.svg',
    27: 'mouse.svg',
    28: 'octopus.svg',
    29: 'ostrich.svg',
    30: 'owl.svg',
    31: 'panda.svg',
    32: 'parrot.svg',
    33: 'penguin-1.svg',
}

def get_avatar_link(digit):
    from django.contrib.staticfiles.templatetags.staticfiles import static
    name = avatar_dict[int(digit)]
    avatar = static(f'images/avatars/{name}')
    return avatar
    
