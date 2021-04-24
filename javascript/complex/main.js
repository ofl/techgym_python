const hands = ['グー', 'チョキ', 'パー'];

function start_message(){
    print('start_message', 'じゃんけんスタート');
}

function get_you_hand() {
    return Math.floor(Math.random() * 3);
}

function view_result(hand_diff) {
    if (hand_diff == 0) {
        print('result', 'あいこ');
    } else if (hand_diff == -1 || hand_diff == 2 ) {
        print('result', '勝ち');
    } else {
        print('result', '負け');
    }
}

function get_hand_name(hand_number) {
    return hands[hand_number];
}

function view_hand(my_hand, you_hand) {
    print('my_hand', '自分の手は' + get_hand_name(my_hand));
    print('you_hand', '相手の手は' + get_hand_name(you_hand));
}

function play(button){
    const my_hand = button.value;
    const you_hand = get_you_hand();
    view_hand(my_hand, you_hand)

    const hand_diff = my_hand -you_hand;
    view_result(hand_diff);
}

function print(place, str) {
    const element = document.getElementById(place);
    element.innerHTML = str;
}

// グーチョキパーのボタンを押した時にplay関数を実行するための設定
const buttons = document.querySelectorAll('.hands');
buttons.forEach(button => { 
    button.addEventListener('click', () => {
        play(button);
    })
});

start_message();
