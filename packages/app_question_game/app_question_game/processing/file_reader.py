ORD_EXCEPTIONS = [
                  # 774,  # Combining Breve instead of 'й'
                  8212, 8213, 8216, 8217,
                  8218, 8219, 8220,
                  8221,
                  8222, 8223, 8224]


def has_non_extended_latin(line):
    """Check if line contains unwanted characters.

    Return True if outside of UTF-8 decimal range 0-383 for Extended Latin.
    """
    for char in line:
        ord_char = ord(char)
        if ord_char > 383 and ord_char not in ORD_EXCEPTIONS:
            err_msg = f'\nНедопустимый символ юникода: {char} {str(ord_char)}'
            raise ValueError(err_msg)


def has_non_latin_or_cyr(line):
    """Check if line contains unwanted characters.

    Return True if outside of UTF-8 decimal range 0-383 or 1024-1279
    for Extended Latin and Cyrillic, respectively.
    """
    for char in line:
        ord_char = ord(char)
        condition_1 = ord_char > 383 and ord_char < 1024
        condition_2 = ord_char > 1279
        if (condition_1 or condition_2) and ord_char not in ORD_EXCEPTIONS:
            err_msg = f'\nНедопустимый символ юникода: {char} {str(ord_char)}'
            raise ValueError(err_msg)


def has_empty_element(a_list):
    for elem in a_list:
        if not elem:
            raise ValueError


def read_file(binary_file_obj):
    """Decide which file was loaded - bitext or bitext with categories."""
    a_string = binary_file_obj.read().decode('utf-8')
    split_string = a_string.split('\n')
    first_string_elements = split_string[0].split('\t')
    for elem in first_string_elements:
        if not elem:
            err_msg = 'Вы загружаете файл с тремя элементами в первой строке. '
            err_msg += 'Элементы строки не должны быть пустыми. '
            err_msg += 'Возможно, в строке есть лишний символ табуляции.'
            raise ValueError(err_msg)
    if len(first_string_elements) == 2:
        for idx, line in enumerate(split_string):
            if len(line.strip()) > 0:  # skip empty lines
                line_elem = line.split('\t')
                if len(line_elem) != 2:
                    error_msg = 'Непоследовательное кол-во элементов в строках. '
                    error_msg += f'Недопустимая строка: {str(idx)} {str(line)}'
                    raise ValueError(error_msg)
                try:
                    has_empty_element(line_elem)
                except ValueError:
                    err_msg = 'Элементы строки не должны быть пустыми.'
                    raise ValueError(f'{err_msg} {str(idx)} {str(line)}')
        return read_bitext_file(split_string)
    elif len(first_string_elements) == 3:
        for idx, line in enumerate(split_string):
            if len(line.strip()) > 0:  # skip empty lines
                line_elem = line.split('\t')
                if len(line_elem) != 3:
                    error_msg = 'Непоследовательное кол-во элементов в строках. '
                    error_msg += f'Недопустимая строка: {str(idx)} {str(line)}'
                    raise ValueError(error_msg)
                try:
                    has_empty_element(line_elem)
                except ValueError:
                    err_msg = 'Элементы строки не должны быть пустыми.'
                    raise ValueError(f'{err_msg} {str(idx)} {str(line)}')
        return read_cat_file(split_string[1:])  # first element is headings
    else:
        msg = 'Неправильное количество элементов в строке. '
        msg += 'Должно быть 2 или 3. Получено '
        msg += str(len(split_string[0]))
        raise ValueError(msg)


def read_bitext_file(a_list) -> list:
    """Read a list of bitext strings return a list of tuples."""
    res = []
    for idx, line in enumerate(a_list):
        if len(line.strip()) > 0:  # skip empty lines
            try:
                src, trg = line.split('\t')
                src, trg = src.strip(), trg.strip()
            except ValueError as err:
                err_msg = f'Недопустимая строка: {str(idx)} {str(line)}'
                raise ValueError(str(err) + '\n' + err_msg)

            # if str == '' or trg == '':
            #     error_msg = 'Недопустимая строка: ' + str(idx) + '\n'
            #     error_msg += 'Элементы не должены быть пустыми. '
            #     error_msg += str(line)
            #     raise ValueError(error_msg)

            try:
                has_non_extended_latin(src)
                has_non_latin_or_cyr(trg)
            except ValueError as err:
                error_msg = f'Недопустимая строка: {str(idx)} \n'
                error_msg += 'Первый элемент должен быть на латиннице. '
                error_msg += 'Второй элемент - кириллица.\n'
                error_msg += str(line)
                raise ValueError(error_msg + str(err))

            res.append((src, trg))
    return res


def read_cat_file(a_list) -> list:
    """Read a list of categorized bitext strings and return a list of tuples."""
    res = []
    for idx, line in enumerate(a_list):
        if len(line.strip()) > 0:
            try:
                src, trg, cat = line.split('\t')
                src, trg, cat = src.strip(), trg.strip(), cat.strip()
            except ValueError as err:
                err_msg = f'Недопустимая строка: {str(idx)} {str(line)}'
                raise ValueError(str(err) + '\n' + err_msg)

            # if str == '' or trg == '' or cat == '':
            #     error_msg = f'Недопустимая строка: {str(idx)} \n'
            #     error_msg += 'Элементы не должены быть пустыми. '
            #     error_msg += str(line)
            #     raise ValueError(error_msg)

            try:
                has_non_extended_latin(src)
                has_non_latin_or_cyr(trg)
                has_non_latin_or_cyr(cat)
            except ValueError as err:
                error_msg = 'Недопустимая строка: ' + str(idx) + '\n'
                error_msg += 'Первый элемент должен быть на латиннице. '
                error_msg += 'Второй элемент - кириллица.\n'
                error_msg += 'Третий элемент - латиница или кирилица'
                error_msg += str(line)
                raise ValueError(error_msg + str(err))

            res.append((src, trg, cat))
    return res
