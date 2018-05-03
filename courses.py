def course_create(db, data):
    print("CREATE > ", data)
    course_num = data['courseNum']
    course_name = data['name'] if 'name' in data else ''
    course_desc =  data['description'] if 'description' in data else ''

    store_original_data(db, course_num, data)

    db.sadd('courseNums', course_num)

    # add courseNum to dept and courseNum lists
    splitNum = split_course_num(course_num)
    db.sadd('dept:' + splitNum[0], course_num)
    db.sadd('courseNum:' + splitNum[1], course_num)

    # tokenize indexes
    tokenize_string_to_indexes(db, course_name, 'ind', course_num)
    tokenize_string_to_indexes(db, course_desc, 'ind', course_num)

def course_delete(db, data):
    print("DELETE > ", data)
    # TODO: remove the possibility of this not existing
    course_num = data['courseNum'] if 'courseNum' in data else None
    if course_num is None:
        return

    # fetch the original data
    orig_data = db.hgetall('courseOrig:' + course_num)
    course_name = orig_data['name'] if 'name' in orig_data else ''
    course_desc =  orig_data['description'] if 'description' in orig_data else ''

    # remove courseNum to dept and courseNum lists
    db.srem('courseNums', course_num)
    
    splitNum = split_course_num(course_num)
    db.srem('dept:' + splitNum[0], course_num)
    db.srem('courseNum:' + splitNum[1], course_num)

    # delete tokenized string from indexes
    tokenize_string_to_indexes(db, course_name, 'ind', course_num, True)
    tokenize_string_to_indexes(db, course_desc, 'ind', course_num, True)

    db.delete('courseOrig:' + course_num)

def store_original_data(db, key, data):
    key = 'courseOrig:' + key
    db.delete(key)
    for key_name in data:
        db.hset(key, key_name, data[key_name])

def split_course_num(course_num):
    index = 0
    for i, c in enumerate(course_num):
        if c.isdigit():
            index = i
            break
    return (course_num[0:index], course_num[index:])

def tokenize_string_to_indexes(db, string, set_prefix, value, is_delete = False):
    words = tokenize_string(string)
    for word in words:
        set_name = set_prefix + ':' + word
        if not is_delete:
            db.sadd(set_name, value)
        else:
            db.srem(set_name, value)

def tokenize_string(string):
    return list(word for word in string.lower().split(" ") if len(word) > 3)
