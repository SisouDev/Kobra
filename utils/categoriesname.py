def namecat(cat_id):
    name = {1: 'Python', 2: 'Javascript', 3: 'Framework', 4: 'Others', 5: 'Java'}
    cat_id: int
    if cat_id == 1:
        name = 'Python'
    if cat_id == 2:
        name = 'JavaScript'
    if cat_id == 3:
        name = 'FrameWork'
    if cat_id == 4:
        name = 'Others'
    if cat_id == 5:
        name = 'Java'
    if cat_id <= 0:
        name = None
    if cat_id > 5:
        name = None
    return name
