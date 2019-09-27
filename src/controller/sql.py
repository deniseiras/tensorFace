if __name__ == '__main__':
    with open('/media/denis/dados/downloads/sql2.txt', 'w') as s:
        with open('/media/denis/dados/downloads/faces2.txt') as f:
            for line in f:
                line = line.rstrip()
                split = line.split('/')
                filename = split[len(split)-1]
                sql = "update face_record set filename = '{}' where filename = '{}';\n ".format(filename, line)
                print(sql)
                s.write(sql)


