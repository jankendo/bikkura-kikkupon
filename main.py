from itertools import combinations


def display_current_array(arr):
    """配列の中身を表示"""
    return ','.join([f'{i + 1}:{val}' for i, val in enumerate(arr)])


def find_combinations(arr, target_sums, priority_label):
    """配列の中の数値から5個の合計が指定された値になる組み合わせを見つける"""
    n = len(arr)
    seen_combinations = set()
    for idxs in combinations(range(n), 5):
        idxs_sorted = tuple(sorted(idxs))
        if idxs_sorted in seen_combinations:
            continue
        combination_sum = sum(arr[i] for i in idxs)
        if combination_sum in target_sums:
            seen_combinations.add(idxs_sorted)
            yield [i + 1 for i in idxs_sorted], [arr[i] for i in idxs_sorted], combination_sum, priority_label


def get_user_input(prompt, valid_range=None):
    """ユーザー入力を処理する"""
    while True:
        try:
            user_input = int(input(prompt))
            if valid_range and user_input not in valid_range:
                print(f"入力エラー: 入力は{valid_range}の範囲内である必要があります。")
                continue
            return user_input
        except ValueError:
            print("入力エラー: 有効な数値を入力してください。")


def display_results(arr, target_sums, priority_label):
    """結果を表示し、選択されたパターンを返す"""
    results_found = False
    all_results = []
    result_id = 1

    for combination, numbers, sum_value, priority in find_combinations(arr, target_sums, priority_label):
        print(f"パターン{result_id}: インデックス: {combination}, 数値: {numbers}, 合計値: {sum_value}, {priority}")
        all_results.append((result_id, combination))
        result_id += 1
        results_found = True

    return all_results, results_found


def handle_combination_selection(arr, all_results):
    """組み合わせの選択を処理する"""
    choice = get_user_input("どの組み合わせのお皿のパターンを投入しますか (キャンセルは0)⇒ ")
    if choice != 0:
        chosen_combination = next((comb[1] for comb in all_results if comb[0] == choice), None)
        if chosen_combination:
            for idx in sorted(chosen_combination, reverse=True):
                arr.pop(idx - 1)
        else:
            print("入力エラー: 有効なパターン番号を選択してください。")


def main():
    arr = []
    primary_targets = {6, 9, 18, 37}
    secondary_targets = {13, 26, 39, 52, 65}

    while True:
        print(f"手元のお皿一覧⇒({display_current_array(arr)})")
        num = get_user_input("取ったお皿の番号を入力してください?(1～13の間、99で結果表示、88で添え字削除)⇒ ")

        if num == 99:
            if len(arr) < 5:
                print("エラー: ５皿以上食べてください")
                continue

            all_results, results_found = display_results(arr, primary_targets, '優先順位1')

            if not results_found:
                all_results, results_found = display_results(arr, secondary_targets, '優先順位2')

            if not results_found:
                print("エラー: 当選確率の高いお皿の組み合わせが見つかりません。")
            else:
                handle_combination_selection(arr, all_results)

        elif num == 88:
            delete_index = get_user_input("削除したい添え字を入力してください (キャンセルは0)⇒ ",
                                          valid_range=range(0, len(arr) + 1))
            if delete_index != 0:
                arr.pop(delete_index - 1)

        else:
            if 1 <= num <= 13:
                arr.append(num)
            else:
                print("入力エラー: 数値は1から13の間である必要があります。")


if __name__ == "__main__":
    main()