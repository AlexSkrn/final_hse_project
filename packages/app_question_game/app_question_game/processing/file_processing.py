ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    """Check if the file extension is okey."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def read_file(a_string):
#     """Read bitext and return a list of tuples."""
#     res = []
#     for idx, line in enumerate(a_string.split('\n')):
#         if len(line.strip()) > 0:
#             try:
#                 src, trg = line.split('\t')
#             except ValueError:
#                 raise ValueError('Wrong line: ' + str(idx) + ' ' + str(line))
#             else:
#                 res.append(
#                        (src.strip(), trg.strip())
#                        )
#     return res
