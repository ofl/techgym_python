const hands = ['グー', 'チョキ', 'パー'];
const results = document.getElementById('results');
const line_break = document.getElementById('line_break');

function start_message(){
    print('じゃんけんスタート');
}

function get_you_hand() {
    return Math.floor(Math.random() * 3);
}

function view_result(hand_diff) {
    if (hand_diff == 0) {
        print('あいこ');
    } else if (hand_diff == -1 || hand_diff == 2 ) {
        print('勝ち');
    } else {
        print('負け');
    }
}

function get_hand_name(hand_number) {
    return hands[hand_number];
}

function view_hand(my_hand, you_hand) {
    print('自分の手は' + get_hand_name(my_hand));
    print('相手の手は' + get_hand_name(you_hand));
}

function play(button){
    const my_hand = button.value;
    const you_hand = get_you_hand();
    view_hand(my_hand, you_hand)

    const hand_diff = my_hand -you_hand;
    view_result(hand_diff);
    add_line_break();
}

function print(str) {
    const node = document.createElement('P')
    node.innerHTML = str
    results.appendChild(node);
}

function add_line_break() {
    const node = line_break.cloneNode()
    results.appendChild(node);
}

// グーチョキパーのボタンを押した時にplay関数を実行するための設定
const buttons = document.querySelectorAll('.hands');
buttons.forEach(button => { 
    button.addEventListener('click', () => {
        play(button);
    })
});

start_message();
