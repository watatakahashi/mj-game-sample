
def sort_tehai(tehai):
    # カスタムソート
    re_tehai = [hai[1] + hai[0] for hai in tehai]
    sorted_tehai = sorted(re_tehai)
    return [hai[1] + hai[0] for hai in sorted_tehai]
